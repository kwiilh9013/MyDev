# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon.cfg.struct import buildStructConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BuildStructLogic(CommonEventRegister):
	"""生成建筑逻辑 服务端"""
	def __init__(self, severHandler, playerId, structData):
		"""
		:param structData={structId, dimension, pos, rot, rebuilding/续建模式, index/当前建造进度}: 建筑数据
		"""
	# def __init__(self, severHandler, playerId, structId, centerPos, rot, dimension=None, index=None, rangeEntityId=None):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		self._playerId = playerId
		
		self._structId = structData.get("structId")
		# 所在维度
		self._dimension = structData.get("dimension")
		if self._dimension is None:
			self._dimension = engineApiGas.GetEntityDimensionId(self._playerId)
			
		# 获取config
		structCfg = buildStructConfig.GetStructPaletteDict(self._structId)
		# 建筑大小
		self._structSize = structCfg.get("volume", (1, 1, 1))
		# 体积总数，用于判断遍历完
		self._totalBlockCount = self._structSize[0] * self._structSize[1] * self._structSize[2]
		# 底面（长*宽）总数，用于计算坐标
		self._buttomBlockCount = self._structSize[0] * self._structSize[1]

		if structData.get("rebuilding") is not True:
			# 初建模式

			# 建筑旋转，限制在-90、0、90、180的值
			rot = structData.get("rot")
			self._rot = commonApiMgr.Get90Rot(rot)
			# 建筑左下角位置：注意xz的对应关系
			x, z = self.GetXZByRotate((self._structSize[1] // 2), (self._structSize[0] // 2), self._rot)
			centerPos = structData.get("pos")
			self._startPos = (
				centerPos[0] - x,
				centerPos[1],
				centerPos[2] - z
			)
			
			# 当前生成到的方块索引
			self._currentBuildIndex = 0

			# 扣除材料，如果材料足够，才扣除
			hasEnough = self.DelectMaterials()
			if hasEnough is False:
				# 材料不足
				self.Destroy()
				return
		else:
			# 续建模式，即退出重进后，继续建造
			# 角度
			self._rot = structData.get("rot")
			# 左下角坐标
			self._startPos = structData.get("pos")
			# 当前生成到的方块索引
			self._currentBuildIndex = structData.get("index")
		
		# 转换方块数据，变成按顺序排列，方便一个个生成方块
		# 优化：依附方块才能摆放的方块类型，单独一个字典，到最后再生成这部分。如按钮、旗帜、画等
		self._blockList = []	# 用于存储方块数据，减小字典占用
		self._posDict = {}		# 用于存储方块位置索引，用于遍历生成
		blockIndex = 0 
		for block, indexList in structCfg.get("common", {}).iteritems():
			self._blockList.append(block)
			# 按照方块索引顺序，将数据填入字典中
			for index in indexList:
				self._posDict[index] = blockIndex
			# 方块id索引
			blockIndex += 1
		
		# 建造特效实体
		self._buildingEntityId = None

		self._blockComp = compFactory.CreateBlockInfo(self._levelId)
		self._chunkComp = compFactory.CreateChunkSource(self._levelId)

		# 区块不加载的等待时间，秒
		self._waitingChunkTime = 0

		# 记录建造数据
		self._server.SetBuildData(self._playerId, self._structId, self._startPos, self._rot)
		
		# 启动timer，开始生成建筑
		self._buildTimer = engineApiGas.AddRepeatTimer(buildStructConfig.BuildStructTimerCD, self.BuildStructTimer)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		# 清除范围实体
		if self._buildingEntityId:
			self._server.DestroyEntity(self._buildingEntityId)
		# 清除对象记录
		self._server._buildObjDict.pop(self, None)
		self._server = None
		if self._buildTimer:
			engineApiGas.CancelTimer(self._buildTimer)
			self._buildTimer = None
		del self._blockList
		self._posDict.clear()
		# 清除对象自己
		del self
		pass


	def BuildStructTimer(self):
		"""tick生成建筑"""
		# 如果处于区块不加载的等待时间，则仅更新时间，不执行以下逻辑
		if self._waitingChunkTime > 0:
			self._waitingChunkTime -= buildStructConfig.BuildStructTimerCD
			return
		
		# 取出一个方块数据
		# TEST
		# buildCount = buildStructConfig.OnceBuildBlockCount * 10
		buildCount = buildStructConfig.OnceBuildBlockCount
		while self._currentBuildIndex < self._totalBlockCount and buildCount > 0:
			# 获取方块数据
			blockIndex = self._posDict.get(self._currentBuildIndex)
			if blockIndex is None:
				# 获取不到blockIndex，有可能是该位置没有方块
				# 迭代到下一个索引
				self._currentBuildIndex += 1
				continue
			
			# 有拿到方块索引
			# 生成方块
			block = self._blockList[blockIndex]
			setPos = self.GetBlockPosByIndex(self._currentBuildIndex)
			# 判断该位置是否加载
			if self._chunkComp.CheckChunkState(self._dimension, setPos):
				# # 获取旋转后的aux
				aux = buildStructConfig.GetBlockRotateAux(block[0], block[1], self._rot)
				# 设置方块
				self._blockComp.SetBlockNew(setPos, {"name": block[0], "aux": aux}, buildStructConfig.OldBlockHandling, self._dimension, updateNeighbors=False)
				# 迭代到下一个索引
				self._currentBuildIndex += 1
				# 更新设置方块的数量（遍历不更新）
				buildCount -= 1

				# 客户端播放特效、音效
				if self._currentBuildIndex % 5 == 0:
					# 仅发送给同维度的客户端
					nearbyPlayers = serverApiMgr.GetNearbyPlayerList(self._dimension, self._startPos, 72)
					info = {"stage": "build_effects", "build_pos": setPos}
					self.SendMsgToMultiClient(nearbyPlayers, eventConfig.BuildStructEvent, info)

					# 设置建造特效实体位置
					# 如果没生成，则先进行生成
					buildingEntityPos = (setPos[0], setPos[1] + 5, setPos[2])
					if not self._buildingEntityId:
						self._buildingEntityId = serverApiMgr.SpawnEntity(self._server, buildStructConfig.BuildingEffectEngineTypeStr, pos=buildingEntityPos, dimension=self._dimension)
						self._server.AddNeedRemoveEntity(self._buildingEntityId)
					else:
						posComp = compFactory.CreatePos(self._buildingEntityId)
						if posComp:
							posComp.SetPos(buildingEntityPos)
			else:
				# 区块不加载，跳过，并进入等待时间
				self._waitingChunkTime = buildStructConfig.WaitingChunkTime
				break

		if self._currentBuildIndex >= self._totalBlockCount:
			# 结束循环
			self.Destroy()
		pass

	def DelectMaterials(self):
		"""扣除材料"""
		itemDictList = serverApiMgr.GetPlayerInventoryItemList(self._playerId)
		cfg = buildStructConfig.StructIdCfg.get(self._structId)
		materials = cfg.get("materials", [])
		slotItemDict = {}
		# 先校验数量是否足够
		hasEnough = True
		for item in materials:
			itemName = item[0]
			needCount = item[1]
			slotItemDict[itemName] = {}
			for slot, invItem in enumerate(itemDictList):
				if invItem and invItem.get("newItemName") == itemName:
					needCount -= invItem.get("count", 0)
					slotItemDict[itemName][slot] = invItem.get("count", 0)
					if needCount <= 0:
						# 数量足够
						break
			if needCount > 0:
				# 数量不足
				hasEnough = False
				break
		if hasEnough:
			# 扣除物品
			itemComp = compFactory.CreateItem(self._playerId)
			for item in materials:
				itemName = item[0]
				needCount = item[1]
				for slot, count in slotItemDict[itemName].iteritems():
					# 扣除指定数量
					if needCount >= count:
						itemComp.SetInvItemNum(slot, 0)
						needCount -= count
					else:
						itemComp.SetInvItemNum(slot, count - needCount)
						needCount = 0
					if needCount <= 0:
						# 扣完
						break
		return hasEnough
 
	def GetBlockPosByIndex(self, index):
		"""根据索引获取方块位置"""
		offset = [
			(index % self._buttomBlockCount) // self._structSize[0],
			index // self._buttomBlockCount,
			index % self._structSize[0],
		]
		# 对偏移进行旋转
		offset[0], offset[2] = self.GetXZByRotate(offset[0], offset[2], self._rot)
		setPos = (
			self._startPos[0] + offset[0],
			self._startPos[1] + offset[1],
			self._startPos[2] + offset[2]
		)
		return setPos
	
	def GetXZByRotate(self, x, z, rot):
		"""根据旋转角度，获取新的位置，角度需是-90、0、90、180"""
		if rot == 90:
			# 交换位置、z取反
			x, z = -z, x
		elif rot == 180:
			# 取反
			x, z = -x, -z
		elif rot == -90:
			# 交换位置、x取反
			x, z = z, -x
		return x, z
	
	def IsOnceBuilding(self, structId, startPos, rot):
		"""判断是否是同一建筑，同一建筑的坐标相同，旋转角度相同"""
		if structId != self._structId:
			return False
		if startPos != self._startPos:
			return False
		if rot != self._rot:
			return False
		return True
	
	def GetBuidHeight(self):
		"""获取已经建造到的高度，用于撤销操作"""
		return self._currentBuildIndex // self._buttomBlockCount

	def SaveBuildingData(self):
		"""保存建筑数据"""
		structData = {
			"playerId": self._playerId,
			"structId": self._structId,
			"dimension": self._dimension,
			"pos": self._startPos,
			"rot": self._rot,
			"index": self._currentBuildIndex,
		}
		self._server.SaveBuildingProgressData(structData)

	