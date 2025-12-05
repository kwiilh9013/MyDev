# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.cfg.ladarConfig import EngineArriveDistSqrt, GetEngineCfg, GetEngineKeyList, IsEngineEnum, TargetTypeEnum
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class LadarServerSystem(BaseServerSystem):
	"""雷达 服务端"""
	def __init__(self, namespace, systemName):
		super(LadarServerSystem, self).__init__(namespace, systemName)

		# 雷达目标点数据: [(dim, pos, type)...]
		self._globalTargetPosList = []
		# 玩家已经到达过的点: {player: [(dim, pos, type)...]}
		self._playerArrivePosDict = {}

		# 判断到达位置的timer
		self._arrivePosTimer = None
		# 玩家位置缓存，用于判断玩家是否移动
		self._playerPosCache = {}

		self._eventFunctions = {
			# 添加雷达目标点
			"add_target_pos": self.AddTargetPos,
			"remove_target_pos": self.RemoveTargetPos,
			# 到达某个点
			"arrive_pos": self.SetPlayerArrivePos,
		}

		pass

	def Destroy(self):
		super(LadarServerSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.LadarEvent, self.LadarEvent)
		if self._arrivePosTimer:
			engineApiGas.CancelTimer(self._arrivePosTimer)
			self._arrivePosTimer = None
		pass

	# region 事件
	@EngineEvent()
	def LoadServerAddonScriptsAfter(self, args=None):
		"""加载服务端脚本后事件"""
		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.LadarEvent, self.LadarEvent)
		self.LoadGlobalTargetPosList()

		# 启动timer，负责判断玩家是否到达某个点
		self._arrivePosTimer = engineApiGas.AddRepeatTimer(1, self.CheckPlayerArrivePosTimer)

		# 初始添加第一个发动机位置
		engineType = TargetTypeEnum.Engine1
		engineCfg = GetEngineCfg(engineType)
		if engineCfg:
			self.AddTargetPos({"pos": engineCfg["pos"], "type": engineType,})
		else:
			print("_____ ERROR 发动机没有雷达相关的配置。发动机engineEnum=", engineType)
		pass

	@EngineEvent()
	def ClientLoadAddonsFinishServerEvent(self, args):
		"""玩家客户端加载完成事件"""
		playerId = args.get("playerId")
		self.SetPlayerLogin(playerId)
		pass

	@EngineEvent()
	def PlayerIntendLeaveServerEvent(self, args):
		"""玩家离开事件"""
		playerId = args.get("playerId")
		# 保存玩家数据
		self.SavePlayerArrivePosDict(playerId)
		# 如果是最后一名玩家，则保存全局数据
		playerList = serverApi.GetPlayerList()
		if playerId in playerList:
			playerList.remove(playerId)
		if len(playerList) <= 0:
			self.SaveGlobalTargetPosList()
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.LadarClientSystem)
	def LadarEvent(self, args):
		"""雷达事件 & 雷达订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass

	# endregion
	
	# region 雷达目标点逻辑
	def SetPlayerLogin(self, playerId):
		"""玩家登录逻辑"""
		# 获取玩家到达过的点数据
		self.LoadPlayerArrivePosDict(playerId)

		# 将玩家未到达过的点 or 发动机点，同步给该玩家
		# 封装发动机发现状态数据
		arrivePosList = self._playerArrivePosDict.get(playerId, [])
		posList = []
		engineList = []
		for key in self._globalTargetPosList:
			if IsEngineEnum(key[2]):
				posList.append(key)
				if key in arrivePosList:
					engineList.append(key[2])
			else:
				if key not in arrivePosList:
					posList.append(key)

		# 同步给该玩家
		if posList:
			info = {
				"stage": "add_multiple",
				"posList": posList,
				"engineList": engineList,
			}
			self.SendMsgToClient(playerId, eventConfig.LadarEvent, info)
		pass
	
	def CheckPlayerArrivePosTimer(self):
		"""判断玩家是否到达某个点"""
		# 遍历玩家的目标点数据
		for playerId in serverApi.GetPlayerList():
			plyPos = engineApiGas.GetEntityPos(playerId)
			if plyPos != self._playerPosCache.get(playerId):
				self._playerPosCache[playerId] = plyPos
				dim = engineApiGas.GetEntityDimensionId(playerId)
				# TODO: 当前只判断发动机
				# 判断该玩家是否有没解锁的发动机
				nextKey = None
				for key in GetEngineKeyList():
					if key not in self._playerArrivePosDict.get(playerId, []):
						nextKey = key
						break
				if nextKey is None:
					continue
				# 判断和目标点的距离
				for val in self._globalTargetPosList:
					if val[0] != dim:
						continue
					if val[2] >= TargetTypeEnum.Engine1:
						dist = commonApiMgr.GetDistanceXZSqrt(plyPos, val[1])
						if dist <= EngineArriveDistSqrt:
							# 到达目标点
							self.SetPlayerArrivePos({"__id__": playerId, "pos": val[1], "type": val[2], "dimension": val[0],})
							# 解锁下一个发动机位置（如果该位置还没添加）
							if nextKey not in self._globalTargetPosList:
								self.AddTargetPos({"pos": nextKey[1], "type": nextKey[2],})
							break
		pass

	def AddTargetPos(self, args):
		"""添加雷达目标点"""
		pos = args.get("pos")
		targetType = args.get("type")
		dimension = args.get("dimension", 0)
		pos = (int(pos[0]), int(pos[1]), int(pos[2]))
		key = (dimension, pos, targetType)
		if key not in self._globalTargetPosList:
			self._globalTargetPosList.append(key)
			# 同步给未到达过该点的玩家
			playerList = serverApi.GetPlayerList()
			for player in playerList:
				if key not in self._playerArrivePosDict.get(player, []):
					# 同步给该玩家
					info = {
						"stage": "add",
						"pos": pos,
						"type": targetType,
						"dimension": dimension,
					}
					self.SendMsgToClient(player, eventConfig.LadarEvent, info)
		pass

	def RemoveTargetPos(self, args):
		"""删除雷达目标点"""
		pos = args.get("pos")
		targetType = args.get("type")
		dimension = args.get("dimension", 0)
		isRemove = False
		if targetType:
			# 有传递类型
			key = (dimension, pos, targetType)
			if key in self._globalTargetPosList:
				self._globalTargetPosList.remove(key)
				isRemove = True
		else:
			# 没有传递类型
			for key in self._globalTargetPosList:
				if key[0] == dimension and key[1] == pos:
					self._globalTargetPosList.remove(key)
					targetType = key[2]
					isRemove = True
					break
		if isRemove:
			# 同步给未到达过该点的玩家，删除该点
			key = (dimension, pos, targetType)
			playerList = serverApi.GetPlayerList()
			for player in playerList:
				if key not in self._playerArrivePosDict.get(player, []):
					# 同步给该玩家
					info = {
						"stage": "remove",
						"pos": pos,
						"dimension": dimension,
					}
					self.SendMsgToClient(player, eventConfig.LadarEvent, info)
		pass

	def SetPlayerArrivePos(self, args):
		"""玩家到达某个点"""
		playerId = args.get("__id__")
		pos = args.get("pos")
		dimension = args.get("dimension", 0)
		targetType = args.get("type")
		# 记录数据
		key = (dimension, pos, targetType)
		posList = self._playerArrivePosDict.get(playerId, [])
		if key not in posList:
			posList.append(key)
			self._playerArrivePosDict[playerId] = posList
			
			# 如果是发动机，则同步到达状态到客户端
			if IsEngineEnum(targetType):
				info = {
					"stage": "engine_state",
					"type": targetType,
					"state": 1,
				}
				self.SendMsgToClient(playerId, eventConfig.LadarEvent, info)
		pass
	# endregion

	# region 数据存取
	def LoadGlobalTargetPosList(self):
		"""加载全局雷达目标点列表"""
		key = "{}_global_target_pos_list".format(modConfig.ModNameSpace)
		extraComp = compFactory.CreateExtraData(self.mLevelId)
		data = extraComp.GetExtraData(key)
		if data is None:
			data = []
		self._globalTargetPosList = data
		pass

	def SaveGlobalTargetPosList(self):
		"""保存全局雷达目标点列表"""
		key = "{}_global_target_pos_list".format(modConfig.ModNameSpace)
		extraComp = compFactory.CreateExtraData(self.mLevelId)
		extraComp.SetExtraData(key, self._globalTargetPosList)
		extraComp.SaveExtraData()
		pass

	def LoadPlayerArrivePosDict(self, playerId):
		"""加载玩家到达过的点数据"""
		key = "{}_player_arrive_pos_dict".format(modConfig.ModNameSpace)
		extraComp = compFactory.CreateExtraData(playerId)
		data = extraComp.GetExtraData(key)
		if data is None:
			data = []
		self._playerArrivePosDict[playerId] = data
		pass

	def SavePlayerArrivePosDict(self, playerId):
		"""保存玩家到达过的点数据"""
		if self._playerArrivePosDict.get(playerId):
			key = "{}_player_arrive_pos_dict".format(modConfig.ModNameSpace)
			extraComp = compFactory.CreateExtraData(playerId)
			extraComp.SetExtraData(key, self._playerArrivePosDict[playerId])
			extraComp.SaveExtraData()
			# 清除缓存
			self._playerArrivePosDict.pop(playerId, None)
		pass
	
	# endregion
