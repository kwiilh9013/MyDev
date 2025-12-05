# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.struct import buildStructConfig
from ScukeSurviveScript.modServer.struct.buildStructLogic import BuildStructLogic
from ScukeSurviveScript.modServer.struct.revokeStructLogic import RevokeStructLogic
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BuildStructServerSystem(BaseServerSystem):
	"""一键建造 服务端"""
	def __init__(self, namespace, systemName):
		super(BuildStructServerSystem, self).__init__(namespace, systemName)

		# 记录需删除的实体id
		self._needRemoveEntityDict = {}

		# 记录玩家建造的建筑数据，用于撤销操作: {playerId: (structId, startPos, rotate)}
		self._playerBuildStructDict = {}

		# 记录建造对象: { obj: playerId }
		self._buildObjDict = {}

		self._eventFunctions = {
			# 创建建筑模型
			"build_range": self.ShowBuildRange,
			# 更改建筑模型位置
			"build_pos": self.ChangeBuildPos,
			# 旋转
			"rotate": self.SetRotateBuild,
			# 取消建造
			"cancel_build": self.SetCancelBuild,
			# 开始建造
			"start_build": self.StartBuildStruct,
			# 撤销上一次建造
			"revoke": self.SetRevokeBuild,
		}

		pass

	def Destroy(self):
		super(BuildStructServerSystem, self).Destroy()
		# 删除实体
		for entityId in self._needRemoveEntityDict.keys():
			self.DestroyEntity(entityId)
		self._needRemoveEntityDict.clear()
		for obj in self._buildObjDict.keys():
			obj.SaveBuildingData()
			obj.Destroy()
		self._buildObjDict.clear()
		pass

	# region 事件
	@EngineEvent()
	def LoadServerAddonScriptsAfter(self, args=None):
		"""加载服务端脚本后事件"""
		# 读取未生成完的建造，重新生成
		buildingDataList = self.LoadBuildingProgressData()
		# 创建建造对象
		for buildingData in buildingDataList:
			# 创建生成建筑对象，由对象来处理整个生成逻辑
			playerId = buildingData.get("playerId")
			buildingData["rebuilding"] = True
			obj = BuildStructLogic(self, playerId, buildingData)
			self._buildObjDict[obj] = playerId
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体删除事件"""
		entityId = args.get("id")
		# 如果是建造实体，则删除
		val = self._needRemoveEntityDict.pop(entityId, None)
		if val is not None:
			self.DestroyEntity(entityId)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.BuildStructClientSystem)
	def BuildStructEvent(self, args):
		"""一键建造事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	
	# region 建造逻辑
	def ShowBuildRange(self, args):
		"""显示建造范围"""
		playerId = args.get("__id__")
		structId = args.get("structId")
		# 生成实体，位置需限制在方块中间
		dim = engineApiGas.GetEntityDimensionId(playerId)
		plyPos = engineApiGas.GetEntityPos(playerId)
		rot = engineApiGas.GetEntityRot(playerId)
		# 获取朝向发射的射线命中位置，如果获取不到，则在玩家当前位置生成
		pos = serverApiMgr.GetRayBlockPos(dim, plyPos, serverApi.GetDirFromRot(rot), buildStructConfig.GetCrossMaxDistance)
		if pos is None:
			pos = (plyPos[0], plyPos[1] - 2.62, plyPos[2])
		if pos:
			# 对坐标偏移到方块上面中间
			pos = (int(pos[0]) + 0.5, int(pos[1] + 1), int(pos[2]) + 0.5)
			# 生成实体
			entityId = serverApiMgr.SpawnEntity(self, buildStructConfig.BuildRangeEngineTypeStr, pos=pos, dimension=dim)
			# 同步到客户端，客户端显示模型
			info = {"stage": "build_range", "structId": structId, "entityId": entityId, "playerId": playerId}
			self.SendMsgToAllClient(eventConfig.BuildStructEvent, info)
			self.AddNeedRemoveEntity(entityId)
		pass

	def ChangeBuildPos(self, args):
		"""改变建筑模型位置"""
		entityId = args.get("entityId")
		pos = args.get("pos")
		posComp = compFactory.CreatePos(entityId)
		posComp.SetFootPos(pos)
		pass

	def SetRotateBuild(self, args):
		"""旋转建筑模型"""
		entityId = args.get("entityId")
		# 固定顺时针转90度
		rotComp = compFactory.CreateRot(entityId)
		rot = rotComp.GetRot()
		rotComp.SetRot((0, rot[1] + 90))
		pass

	def SetCancelBuild(self, args):
		"""取消建造"""
		# 删除实体
		entityId = args.get("entityId")
		self.DestroyEntity(entityId)
		pass

	def StartBuildStruct(self, args):
		"""
		开始生成建筑
		:param buildEntityId: 显示范围的实体id，用于定位
		"""
		playerId = args.get("__id__")
		structId = args.get("structId")
		buildEntityId = args.get("entityId")
		posComp = compFactory.CreatePos(buildEntityId)
		pos = posComp.GetFootPos()
		if pos:
			# 判断当前正在建造的数量，如果达到上限，就无法再建造
			if len(self._buildObjDict) >= buildStructConfig.BuildingLogicMaxCount:
				engineApiGas.NotifyOneMessage(playerId, buildStructConfig.GetTips(51), "§c")
			else:
				pos = commonApiMgr.GetBlockPosByEntityPos(pos)
				rotComp = compFactory.CreateRot(buildEntityId)
				rot = rotComp.GetRot()
				# 创建生成建筑对象，由对象来处理整个生成逻辑
				structData = {
					"structId": structId,
					"pos": pos,
					"rot": rot[1],
				}
				obj = BuildStructLogic(self, playerId, structData)
				self._buildObjDict[obj] = playerId
			# 清除实体
			self.DestroyEntity(buildEntityId)
		pass

	def SetRevokeBuild(self, args):
		"""撤销上一次建造"""
		playerId = args.get("__id__")
		val = self._playerBuildStructDict.pop(playerId, None)
		if val:
			# 如果该建筑还在建造中，则先停止
			height = None
			for obj, plyId in self._buildObjDict.iteritems():
				if plyId == playerId:
					if obj.IsOnceBuilding(val[0], val[1], val[2]):
						height = obj.GetBuidHeight()
						obj.Destroy()
						break
			# 执行清除方块逻辑
			RevokeStructLogic(self, playerId, val[0], val[1], val[2], height=height)
		pass

	def SetBuildData(self, playerId, structId, startPos, rotate):
		"""记录玩家最后一次建造的建筑数据"""
		self._playerBuildStructDict[playerId] = (structId, startPos, rotate)
		pass

	def LoadBuildingProgressData(self):
		"""初始化时，读取建筑进度"""
		# playerId, structId, startPos, rotate, dimension, index
		key = self.GetBuildingExtraKey()
		extraComp = compFactory.CreateExtraData(self.mLevelId)
		buildingDataList = extraComp.GetExtraData(key)
		if not buildingDataList:
			buildingDataList = []
		else:
			# 读取后即删除数据
			extraComp.SetExtraData(key, None)
		return buildingDataList

	def SaveBuildingProgressData(self, buildingData):
		"""存储建筑进度"""
		# playerId, structId, startPos, rotate, dimension, index
		key = self.GetBuildingExtraKey()
		extraComp = compFactory.CreateExtraData(self.mLevelId)
		buildingDataList = extraComp.GetExtraData(key)
		if not buildingDataList:
			buildingDataList = []
		if buildingData not in buildingDataList:
			buildingDataList.append(buildingData)
			extraComp.SetExtraData(key, buildingDataList)
			extraComp.SaveExtraData()
		pass

	def GetBuildingExtraKey(self):
		"""获取存储建造进度数据的key"""
		return "{}_struct_building_data".format(modConfig.ModNameSpace)

	# endregion

	def AddNeedRemoveEntity(self, entityId):
		"""添加需要删除的实体id"""
		self._needRemoveEntityDict[entityId] = True
		pass
