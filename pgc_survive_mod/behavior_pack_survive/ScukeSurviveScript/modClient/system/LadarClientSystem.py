# -*- coding: utf-8 -*-
import random
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon.cfg import ladarConfig, molangConfig
from ScukeSurviveScript.modCommon import modConfig
compFactory = clientApi.GetEngineCompFactory()


class LadarClientSystem(BaseClientSystem):
	"""雷达 客户端"""
	def __init__(self, namespace, systemName):
		super(LadarClientSystem, self).__init__(namespace, systemName)
		
		# 手持物品id
		self._carriedItemName = None

		# 雷达更新timer
		self._ladarModelUpdateTimer = None
		# 雷达更新时间
		self._ladarUpdateTime = 0

		# 玩家当前角度值
		self._playerLastRot = 0
		self._playerAddedRot = 0

		# 玩家坐标
		self._playerLastPos = None

		# 目标点数据: { dim: [(pos, type)...] }
		self._targetPosDict = {}
		# 目标实体数据：{entityId: type}
		self._targetEntityDict = {}
		# 当前显示的目标点最后的索引
		self._currentTargetIndex = 0
		# 发动机状态数据: {enum: state/0/1/2}
		self._engineStateDict = {}

		# 雷达音效播放的计时
		self._soundPlayTime = 0
		# 上次播放的音效规则
		self._lastSoundPlayRule = None

		# 死机的冷却计时
		self._outOfOrderStartTime = 0
		# 死机状态
		self._outOfOrderState = False

		self._rotComp = compFactory.CreateRot(self.mPlayerId)
		self._posComp = compFactory.CreatePos(self.mPlayerId)

		self._eventFunctions = {
			"add": self.AddTargetPos,
			"add_multiple": self.AddMultipleTargetPos,
			"engine_state": self.UpdateEngineTargetState,
			"remove": self.RemoveTargetPos,
		}
		pass

	def Destroy(self):
		super(LadarClientSystem, self).Destroy()
		self._targetPosDict.clear()
		pass
	
	# region 事件
	@EngineEvent()
	def UiInitFinished(self, args=None):
		# 延迟执行，此时可能还在初始化UI中
		def initUI():
			# 获取手持的物品
			self._carriedItemName = None
			item = clientApiMgr.GetPlayerCarriedItem(self.mPlayerId)
			self.OnCarriedNewItemChangedClientEvent({"itemDict": item})
		engineApiGac.AddTimer(0.1, initUI)

		pass
	
	@EngineEvent()
	def OnCarriedNewItemChangedClientEvent(self, args):
		"""主手持物品改变事件"""
		itemDict = args.get("itemDict")
		itemName = None
		if itemDict:
			itemName = itemDict.get("newItemName")
		# 如果手持的是指定道具，且之前不是手持，才执行逻辑
		if itemName != self._carriedItemName:
			if itemName == ladarConfig.LadarItemName:
				self.SetLadarUpdateState(True)
			elif self._carriedItemName == ladarConfig.LadarItemName:
				self.SetLadarUpdateState(False)
		
		self._carriedItemName = itemName
		pass

	# TODO: 2024.09.20 去掉显示生物的功能，改成仅显示发动机
	# @EngineEvent()
	# def AddEntityClientEvent(self, args):
	# 	"""实体添加事件"""
	# 	entityId = args.get("id")
	# 	engineTypeStr = args.get("engineTypeStr")
	# 	targetType = ladarConfig.GetTargetType(engineTypeStr)
	# 	if targetType is not None:
	# 		if targetType == ladarConfig.TargetTypeEnum.GoldCreeper:
	# 			# 如果是黄金苦力怕，则判断是否驯服了
	# 			if not engineApiGac.IsTamed(entityId):
	# 				self.AddTargetPos({"entityId": entityId, "type": targetType})
	# 		else:
	# 			self.AddTargetPos({"entityId": entityId, "type": targetType})
	# 	pass

	# @EngineEvent()
	# def RemoveEntityClientEvent(self, args):
	# 	"""实体删除事件"""
	# 	entityId = args.get("id")
	# 	self.RemoveTargetPos({"entityId": entityId})
	# 	pass

	@EngineEvent()
	def LeftClickReleaseClientEvent(self, args=None):
		"""鼠标左键释放事件"""
		self.TapBeforeClientEvent(args)
		pass

	@EngineEvent()
	def TapBeforeClientEvent(self, args):
		"""点击屏幕事件"""
		if self._carriedItemName == ladarConfig.LadarItemName:
			if self._outOfOrderState:
				# 播放攻击动画
				plyComp = compFactory.CreatePlayer(self.mLevelId)
				plyComp.Swing()
				# 概率从死机中恢复
				rdm = random.random()
				if rdm < ladarConfig.OutOfOrderRecoverProb:
					self.SetOutOfOrder(False)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.LadarServerSystem)
	def LadarEvent(self, args):
		"""雷达事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def EffectPlayEvent(self, args):
		"""从建筑系统来的播放特效事件"""
		stage = args.get("stage")
		if stage == "engine":
			# 发动机特效
			# 记录该发动机点燃的状态，用于更新雷达状态
			pos = args.get("pos")
			if pos:
				# 根据pos计算属于哪个发动机
				for key in ladarConfig.GetEngineKeyList():
					if commonApiMgr.GetDistanceXZSqrt(pos, key[1]) <= 90000:
						self.SetEngineTargetState(key[2], 2)
						break
		pass
	# endregion

	# region 雷达模型效果展示
	def SetLadarUpdateState(self, state):
		"""设置雷达更新状态，启动、关闭timer"""
		if state:
			if not self._ladarModelUpdateTimer:
				self._ladarModelUpdateTimer = engineApiGac.AddRepeatedTimer(ladarConfig.LadarRefreshTime, self.LadarRefreshTimer)
		else:
			if self._ladarModelUpdateTimer:
				engineApiGac.CancelTimer(self._ladarModelUpdateTimer)
				self._ladarModelUpdateTimer = None
			self._playerLastRot = 0
			self._playerAddedRot = 0
			self._ladarUpdateTime = 0
			self._soundPlayTime = 0
			self._outOfOrderStartTime = 0
		pass

	def LadarRefreshTimer(self):
		"""刷新雷达模型效果"""
		if self._ladarModelUpdateTimer is None:
			return

		self._ladarUpdateTime += ladarConfig.LadarRefreshTime

		# 死机逻辑
		if not self._outOfOrderState:
			# 死机概率触发
			if self._ladarUpdateTime - self._outOfOrderStartTime > ladarConfig.OutOfOrderCD:
				prob = random.random()
				if prob < ladarConfig.OutOfOrderProb:
					# 设置死机
					self.SetOutOfOrder(True)
		# 如果死机了，则不再往下执行
		if self._outOfOrderState:
			return

		# 玩家自己的朝向
		rot = self._rotComp.GetRot()
		rot1 = commonApiMgr.GetRotBy360(rot[1])
		if rot1 != self._playerLastRot:
			# 计算角度，对从-170到170的情况做处理，否则做插值计算时，动画会倒转：累加角度值，使角度值从0一直往上加或减，不会跳转数值，从而不出现倒转的情况
			# 计算角度前后值的差值
			addRot = rot1 - self._playerLastRot
			if addRot > 180:
				addRot -= 360
			elif addRot < -180:
				addRot += 360
			self._playerAddedRot += addRot
			self._playerLastRot = rot1
			# 修改molang
			info = {
				"stage": "set_molang", "entityId": self.mPlayerId, 
				"molang": molangConfig.QueryEnum.PlayerRotYaw, "value": self._playerAddedRot, 
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)

		# 目标位置的距离
		hideIndex = None
		if len(self._targetPosDict) > 0 or len(self._targetEntityDict) > 0:
			pos = self._posComp.GetPos()
			if pos != self._playerLastPos:
				self._playerLastPos = pos
				hideIndex = 0
				# 判断维度
				dim = clientApiMgr.GetCurrentDimension()
				dimPosList = self._targetPosDict.get(dim)
				if dimPosList is None:
					dimPosList = []
				
				# TODO: 2024.09.20 去掉显示生物的功能，改成仅显示发动机
				# # 将实体的数据转换为坐标
				# entityPosList = []
				# for entityId, ttype in self._targetEntityDict.iteritems():
				# 	# 如果是黄金苦力怕，则判断是否驯服了
				# 	if ttype == ladarConfig.TargetTypeEnum.GoldCreeper:
				# 		if engineApiGac.IsTamed(entityId):
				# 			self._targetEntityDict.pop(entityId, None)
				# 			continue
				# 	epos = engineApiGac.GetEntityPos(entityId)
				# 	if epos:
				# 		entityPosList.append((epos, ttype))
				
				# topPosList = entityPosList
				# topPosList.extend(dimPosList)
				# if len(entityPosList) + len(dimPosList) > ladarConfig.TargetMaxCount:
				# 	# 计算曼哈顿距离（仅用于判断远近）
				# 	distPosList = []
				# 	for val in topPosList:
				# 		# 排除发动机
				# 		if ladarConfig.IsEngineEnum(val[1]):
				# 			continue
				# 		# 计算距离
				# 		dist = commonApiMgr.GetManhattanDistanceXZ(pos, val[0])
				# 		distPosList.append((dist, val))
				# 	# 排序，取前N个（N和列表长度接近，则用sort排序；N远小于列表长度，才用heapq.nsmallest）
				# 	# 筛选出最近的N个点
				# 	distPosList.sort(key=lambda x:x[0])
				# 	topPosList = [t[1] for t in distPosList[:ladarConfig.TargetMaxCount]]

				# # 挨个计算xz值，并设置molang
				# minDist = None
				# minType = None
				# for index, tposVal in enumerate(topPosList):
				# 	# 排除发动机
				# 	if ladarConfig.IsEngineEnum(tposVal[1]):
				# 		continue
				# 	# 再次筛选，超过一定距离后的坐标，同样不显示
				# 	dist = commonApiMgr.GetDistanceXZSqrt(pos, tposVal[0])
				# 	if dist <= ladarConfig.ScanRangeSqrt:
				# 		distX = tposVal[0][0] - pos[0]
				# 		distZ = tposVal[0][2] - pos[2]
				# 		self.SetTargetMolang(index, distX, distZ)
				# 		# 最小距离
				# 		if minDist is None or dist < minDist:
				# 			minDist = dist
				# 			minType = tposVal[1]
				# 		hideIndex = index + 1

				# 显示发动机
				minDist = None
				minType = None
				for val in dimPosList:
					if ladarConfig.IsEngineEnum(val[1]):
						dist = commonApiMgr.GetDistanceXZSqrt(pos, val[0])
						distX = val[0][0] - pos[0]
						distZ = val[0][2] - pos[2]
						self.SetEngineTargetMolang(val[1], distX, distZ)
						# 最小距离
						if minDist is None or dist < minDist:
							minDist = dist
							minType = val[1]
				
				# 根据距离计算音效播放规则
				targetType = minType
				self._lastSoundPlayRule = ladarConfig.GetTargetSoundPlayRule(minDist, targetType)
				print("___________ ", self._lastSoundPlayRule)

			# 播放音效（手持时才播放）
			if self._lastSoundPlayRule:
				rule = self._lastSoundPlayRule
				if self._ladarUpdateTime - self._soundPlayTime >= rule["cd"]:
					self._soundPlayTime = self._ladarUpdateTime
					sound = rule.get("sound")
					if sound:
						clientApiMgr.PlayCustomMusic(sound["sound"], pos, pitch=sound.get("pitch", 1))
		else:
			# 没有目标点
			hideIndex = 0

		# 隐藏剩余的（如果有剩余）
		if hideIndex is not None and hideIndex != self._currentTargetIndex:
			for i in xrange(hideIndex, ladarConfig.TargetMaxCount):
				self.SetTargetMolang(i, 0, 0)
			self._currentTargetIndex = hideIndex
		pass

	def AddTargetPos(self, args):
		"""添加目标点"""
		entityId = args.get("entityId")
		targetType = args.get("type", ladarConfig.TargetTypeEnum.Default)
		if entityId:
			# 添加实体
			val = self._targetEntityDict.get(entityId)
			if val is None:
				self._targetEntityDict[entityId] = targetType
				# 强制刷新一次显示
				self._playerLastPos = None
		else:
			# 添加坐标点
			pos = args.get("pos")
			dimension = args.get("dimension", 0)
			dimVal = self._targetPosDict.get(dimension)
			if dimVal is None:
				dimVal = []
			key = (pos, targetType)
			if key not in dimVal:
				dimVal.append(key)
				self._targetPosDict[dimension] = dimVal
				# 强制刷新一次显示
				self._playerLastPos = None
		pass

	def AddMultipleTargetPos(self, args):
		"""添加多个目标点，用于登录初始化"""
		posList = args.get("posList")
		# 添加坐标点
		for val in posList:
			dimVal = self._targetPosDict.get(val[0])
			if dimVal is None:
				dimVal = []
			key = (val[1], val[2])
			if key not in dimVal:
				dimVal.append(key)
				self._targetPosDict[val[0]] = dimVal
		# 记录发动机到达状态
		engineList = args.get("engineList")
		for keyType in engineList:
			self.SetEngineTargetState(keyType, 1)
		# 强制刷新一次显示
		self._playerLastPos = None
		pass

	def UpdateEngineTargetState(self, args):
		"""更新发动机状态"""
		indexEnum = args.get("type")
		state = args.get("state")
		self.SetEngineTargetState(indexEnum, state)
		pass

	def RemoveTargetPos(self, args):
		"""移除目标点"""
		isRemove = False
		entityId = args.get("entityId")
		if entityId:
			# 移除实体
			val = self._targetEntityDict.pop(entityId, None)
			if val:
				isRemove = True
		else:
			pos = args.get("pos")
			dimension = args.get("dimension", 0)
			dimVal = self._targetPosDict.get(dimension)
			if dimVal:
				for val in dimVal:
					if val[0] == pos:
						dimVal.remove(val)
						isRemove = True
						break
		# 强制立即刷新一次显示
		if isRemove:
			self._playerLastPos = None
			self.LadarRefreshTimer()
		pass

	def SetOutOfOrder(self, state):
		"""设置损坏状态"""
		self._outOfOrderState = state
		info = {
			"stage": "set_molang", "entityId": self.mPlayerId,
			"molang": molangConfig.QueryEnum.LadarOutOfOrder, "value": 1 if state else 0,
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		self._outOfOrderStartTime = self._ladarUpdateTime
		pass

	def SetTargetMolang(self, molangIndex, distX, distZ):
		"""设置目标点molang值"""
		molangList = molangConfig.QueryEnum.LadarTargetDistList[molangIndex]
		self.SetTargetMolangValues(molangList, distX, distZ)
		pass

	def SetEngineTargetMolang(self, indexEnum, distX, distZ):
		"""设置发动机molang值"""
		index = indexEnum - ladarConfig.TargetTypeEnum.Engine1
		molangList = molangConfig.QueryEnum.LadarEngineDistList[index]
		self.SetTargetMolangValues(molangList, distX, distZ)
		pass

	def SetTargetMolangValues(self, molangList, distX, distZ):
		"""设置目标点molang值"""
		molangValues = {
			molangList[0]: commonApiMgr.Clamp(distX * ladarConfig.MapScales, -ladarConfig.MapMaxX, ladarConfig.MapMaxX),
			molangList[1]: commonApiMgr.Clamp(distZ * ladarConfig.MapScales, -ladarConfig.MapMaxY, ladarConfig.MapMaxY),
		}
		# 计算icon缩放
		maxDist = max(abs(distX), abs(distZ))
		if maxDist <= ladarConfig.MapActualLength:
			molangValues[molangList[2]] = 1
		else:
			molangValues[molangList[2]] = commonApiMgr.Clamp( 1 - (maxDist - ladarConfig.MapActualLength) * ladarConfig.MapScaleDecisionLenghtRate, ladarConfig.MapIconScaleRange[0], ladarConfig.MapIconScaleRange[1])
		# 修改molang
		info = {
			"stage": "set_molangs", "entityId": self.mPlayerId,
			"molangValue": molangValues,
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass
	
	def SetEngineTargetState(self, indexEnum, state):
		"""设置发动机状态, 0-2"""
		# 如果之前的记录是已点燃，则不更新状态（点燃状态最优先）
		oldState = self._engineStateDict.get(indexEnum)
		if oldState == state or oldState == 2:
			return
		self._engineStateDict[indexEnum] = state
		index = indexEnum - ladarConfig.TargetTypeEnum.Engine1
		molangList = molangConfig.QueryEnum.LadarEngineDistList[index]
		# 修改molang
		info = {
			"stage": "set_molangs", "entityId": self.mPlayerId,
			"molangValue": {
				molangList[3]: self._engineStateDict.get(indexEnum, 0),
			},
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass

	# endregion
	
