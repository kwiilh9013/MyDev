# -*- encoding: utf-8 -*-
import random
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.randomEvent.randomEventConfig import GetRandomPhaseEventCfg, GetRandomEventClass, \
	TriggerEventCD, TriggerEventMinDistance, EventDimensions
compFactory = serverApi.GetEngineCompFactory()


class RandomEventServerSystem(BaseServerSystem):
	"""随机事件 system"""
	def __init__(self, namespace, systemName):
		super(RandomEventServerSystem, self).__init__(namespace, systemName)
		self._tick = 0

		# config
		# 检测事件触发频率
		self._triggerEventCD = TriggerEventCD
		# # TEST 测试数据
		# self._triggerEventCD = 10 * 30
		# 事件能触发的维度
		self._dimensionList = EventDimensions

		# 事件触发数据的统计
		# 玩家移动距离: {player: (pos, dist), ...}
		self._playerMoveDistDict = {}
		# 载具移动距离
		self._carMoveDistDict = {}
		# 主世界玩家列表
		self._overworldPlayerList = []

		# 事件对象: {entityId: obj, ...}
		self._eventObjDict = {}

		# 组件

		# phaseEvent sys
		self._phaseEventSys = None
		self._carSys = None
		pass

	def Destroy(self):
		super(RandomEventServerSystem, self).Destroy()
		self._overworldPlayerList = None
		for event in list(self._eventObjDict.itervalues()):
			event.Destroy()
		self._eventObjDict = None
		pass

	# region 事件
	def Update(self):
		"""tick事件"""
		self._tick += 1
		tick = self._tick

		# 尝试触发事件
		self.TryTriggerAllEvents(tick)
		pass

	@EngineEvent()
	def AddServerPlayerEvent(self, args):
		"""玩家登录事件"""
		playerId = args["id"]
		# 判断玩家维度
		dim = engineApiGas.GetEntityDimensionId(playerId)
		if dim == 0:  # 主世界
			if playerId not in self._overworldPlayerList:
				self._overworldPlayerList.append(playerId)
		pass

	@EngineEvent()
	def DimensionChangeFinishServerEvent(self, args):
		"""玩家维度改变事件"""
		playerId = args["playerId"]
		toDimensionId = args["toDimensionId"]
		if toDimensionId == 0:  # 主世界
			if playerId not in self._overworldPlayerList:
				self._overworldPlayerList.append(playerId)
		else:
			if playerId in self._overworldPlayerList:
				self._overworldPlayerList.remove(playerId)
		pass

	@EngineEvent()
	def DelServerPlayerEvent(self, args):
		"""玩家退出事件"""
		playerId = args["id"]
		if playerId in self._overworldPlayerList:
			self._overworldPlayerList.remove(playerId)
		self._playerMoveDistDict.pop(playerId, None)
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体被销毁事件"""
		entityId = args["id"]
		self._carMoveDistDict.pop(entityId, None)
		pass
	# endregion

	# region 随机事件逻辑
	def TryTriggerAllEvents(self, tick):
		"""尝试触发 所有类随机事件"""
		
		"""
		按触发类型，划分事件大类
			不同的触发类型，执行不同的事件逻辑
		行驶距离类：
			....
		如果此时没有触发事件，才往下执行其他大类的事件
		操作类事件：
			挑选出可触发的目标：操作次数达到要求、按位置来算目标点 or 按范围内所有玩家算一个目标点
		"""

		# 限制执行频率
		if tick % self._triggerEventCD != 0:
			return False

		# 距离类事件
		if self.TryTriggerDistEvents(tick):
			return
		
		# 操作类事件
		pass

	def TryTriggerDistEvents(self, tick):
		"""尝试触发 距离类随机事件"""
		
		"""
		事件分为唯一事件和非唯一事件；唯一事件是同时只能存在一个，如刷npc类；非唯一事件是可同时出现多个，如反叛降临类
		每个实体，同时只能触发一个事件；多个实体，可都触发同一种事件
		
		挑选出可触发的目标，行驶距离达标、载具有驾驶员且没损坏、乘骑载具的玩家
		轮询目标，挨个判断事件触发概率
			如果触发的事件是唯一事件，则return
			如果不是唯一事件，则继续轮询
		"""
		
		# 获取当前天数对应的事件配置
		day = self.GetCurrentDay()
		cfg = GetRandomPhaseEventCfg(day)
		if not cfg:
			# log.logerror("RandomEventServerSystem.TryTriggerDistEvents cfg is None, day: %d", day)
			return False
		eventProbRatio = cfg.get("eventProbRatio")
		if not eventProbRatio:
			# 没有配置，则该天无事件
			# # TEST
			# print("__________ RandomEventServerSystem.TryTriggerDistEvents none cfg eventProbRatio", day)
			return False
		
		# 收集数据 + 维护目标列表
		targetDict = {}	# {id: prob}
		# 获取有效的玩家
		playerList = self.GetOverworldPlayers()
		distDict = self._playerMoveDistDict
		for player in playerList:
			if self._eventObjDict.get(player):
				continue
			# 计算玩家移动距离
			if not self.IsMoveDistance(player, distDict, eventProbRatio.get("human", 0)):
				continue
			# 记录id
			targetDict[player] = distDict[player][1]
		# 获取有效的车辆
		carObjList = self.GetCarSys().GetAllCarLogicObj()
		distCarDict = self._carMoveDistDict
		if carObjList:
			for car in carObjList:
				if not car.GetRider():
					continue
				if car.GetDimension() not in self._dimensionList:
					continue
				# 将乘骑的玩家剔除（需要先剔除，否则会将车辆上的玩家也判断一次）
				riderList = car.GetPlayerList()
				for rider in riderList:
					targetDict.pop(rider, None)
				entityId = car.GetEntityId()
				if self._eventObjDict.get(entityId):
					continue
				if not car.IsCanSteer():
					continue
				# 计算车辆移动距离
				if not self.IsMoveDistance(entityId, distCarDict, eventProbRatio.get("car", 0)):
					continue
				# 记录id
				targetDict[entityId] = distCarDict[entityId][1]
				
		# # TEST
		# print("___________ targetDict", targetDict)

		# 轮询
		hasEvent = False
		for target, prob in targetDict.iteritems():
			# 随机概率
			rdm = random.random()
			if rdm > prob:
				# # TEST
				# print("__________ RandomEventServerSystem.TryTriggerDistEvents failure prob=", prob)
				continue

			# 获取事件池
			pool = cfg["distEvents"]
			poolWeights = cfg.get("distEventsWitghts")
			if poolWeights is None:
				poolWeights = commonApiMgr.GetTotalWeight(pool)
				cfg["distEventsWitghts"] = poolWeights
			# 根据权重随机事件
			eventCfg = commonApiMgr.GetValueFromWeightPool(pool, poolWeights)
			# # TEST
			# print("__________ RandomEventServerSystem.TryTriggerDistEvents event=", eventCfg, ", prob=", prob)
			if eventCfg and eventCfg["event"]:
				# 事件触发成功，清除距离概率数据
				self.ClearMoveDist(target)
				# 创建事件
				eventObj = self.TriggerEvent(eventCfg["event"], target)
				if eventObj:
					hasEvent = True
					# 如果事件是全局唯一，则结束轮询
					if eventObj.IsUniqueness():
						break
				pass
		return hasEvent
	
	def IsMoveDistance(self, entityId, distDict, probRatio):
		"""判断是否移动距离达标, 距离不达标返回False"""
		# 计算移动距离
		pos = engineApiGas.GetEntityPos(entityId)
		if not pos:
			return False
		distVal = distDict.get(entityId)
		if not distVal:
			distDict[entityId] = (pos, 0)
			return False
		dist = commonApiMgr.GetDistanceXZ(pos, distVal[0])
		if dist < TriggerEventMinDistance:
			return False
		# 计算触发概率
		if probRatio:
			prob = dist * probRatio
		else:
			prob = 1.0
		# 更新缓存数据
		distDict[entityId] = (pos, prob + distVal[1])
		return True
	
	def ClearMoveDist(self, entityId):
		"""清除移动距离的数据"""
		self._playerMoveDistDict.pop(entityId, None)
		self._carMoveDistDict.pop(entityId, None)
		pass

	def TriggerEvent(self, eventType, target):
		"""触发指定类型的事件"""
		eventClass = GetRandomEventClass(eventType)
		if eventClass and self.CheckEventMutex(eventClass):
			eventObj = eventClass(self, eventType, target)
			self._eventObjDict[target] = eventObj
			# 启动事件
			eventObj.Start()
			return eventObj
		return None

	def CheckEventMutex(self, eventClass):
		"""检查事件互斥, True=不互斥"""
		mutexEvents = eventClass.GetMutexEvents()
		for mutexEvent in mutexEvents:
			if mutexEvent in self._eventObjDict:
				return False
		return True
	
	# endregion
	
	# region api
	def GetOverworldPlayers(self):
		"""获取主世界玩家列表"""
		return self._overworldPlayerList
	
	def CancelEvent(self, targetId):
		"""取消事件"""
		event = self._eventObjDict.pop(targetId, None)
		if event:
			event.Destroy()
		pass

	def GetCurrentDay(self):
		"""获取当前天数"""
		phaseSys = self.GetPhaseSys()
		if phaseSys:
			return phaseSys.Days
		return 0
	
	def GetPhaseSys(self):
		"""获取阶段服务端系统"""
		if self._phaseEventSys is None:
			self._phaseEventSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PhaseServerSystem)
		return self._phaseEventSys
	
	def GetCarSys(self):
		"""获取阶段服务端系统"""
		if self._carSys is None:
			self._carSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.CarServerSystem)
		return self._carSys
	# endregion
