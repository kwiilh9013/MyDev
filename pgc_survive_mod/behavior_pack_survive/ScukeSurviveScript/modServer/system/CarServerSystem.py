# -*- encoding: utf-8 -*-
import random
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.car.carConfig import CarEngineTypeStr, BrokenCarEngineTypeStr, \
	GetRescueConfig, GetRepairNeedItems, IsNotRescueRayBlock
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import RemoldUIRange
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.car.baseCarLogic import BaseCarLogic
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class CarServerSystem(BaseServerSystem):
	"""载具 服务端"""
	def __init__(self, namespace, systemName):
		super(CarServerSystem, self).__init__(namespace, systemName)

		# 玩家使用方块的cd记录
		self._blockUseCDDict = {}

		# 载具对象
		self._carObjDict = {}
		# 任务模块
		self._taskSys = None

		pass

	def Destroy(self):
		super(CarServerSystem, self).Destroy()
		for obj in self._carObjDict.values():
			obj.Destroy()
		self._carObjDict.clear()
		pass

	# region 事件
	@EngineEvent()
	def AddEntityServerEvent(self, args):
		"""实体添加事件"""
		engineTypeStr = args.get("engineTypeStr")
		if engineTypeStr == CarEngineTypeStr:
			entityId = args.get("id")
			# 创建实体对象
			self.GetOrCreateCarLogicObj(entityId, engineTypeStr)
		pass

	@EngineEvent()
	def MobDieEvent(self, args):
		"""实体死亡事件"""
		entityId = args.get("id")
		cause = args.get("cause")
		# 清除实体对象（如果是kill，则不会重新生成）
		self.PopCarLogicObj(entityId, isRemove= cause == minecraftEnum.ActorDamageCause.Suicide)
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体被移除事件"""
		entityId = args.get("id")
		# 清除实体对象
		self.PopCarLogicObj(entityId, isRemove=True)
		pass

	@EngineEvent()
	def StartRidingServerEvent(self, args):
		"""即将开始骑乘事件"""
		rideId = args.get("victimId")
		engineTypeStr = self.GetEngineTypeStr(rideId)
		if engineTypeStr == CarEngineTypeStr:
			# 只有玩家上骑才进行判断，其他生物上骑，不做拦截
			if args.get("actorId") in serverApi.GetPlayerList():
				car = self.GetOrCreateCarLogicObj(rideId, engineTypeStr)
				if car:
					if car.IsCanRide() is False:
						args["cancel"] = True
		pass

	@EngineEvent()
	def EntityStartRidingEvent(self, args):
		"""开始骑乘事件"""
		rideId = args.get("rideId")
		engineTypeStr = self.GetEngineTypeStr(rideId)
		if engineTypeStr == CarEngineTypeStr:
			playerId = args.get("id")
			# 上骑
			car = self.GetOrCreateCarLogicObj(rideId, engineTypeStr)
			if car:
				car.StartRiding(playerId)
		pass

	@EngineEvent()
	def EntityStopRidingEvent(self, args):
		"""停止骑乘事件"""
		playerId = args.get("id")
		rideId = args.get("rideId")
		cancel = args.get("cancel")
		if cancel is False:
			# 下骑
			car = self.GetCarLogicObj(rideId)
			if car:
				car.StopRiding(playerId)
		pass

	@EngineEvent()
	def ServerBlockUseEvent(self, args):
		"""点击方块事件"""
		playerId = args.get("playerId")
		blockName = args.get("blockName")
		dimensionId = args.get("dimensionId")
		pos = (args.get("x"), args.get("y"), args.get("z"))
		if blockName == BlockEnum.CarRemold:
			t = time.time()
			if t - self._blockUseCDDict.get(playerId, 0) > 0.5:
				self._blockUseCDDict[playerId] = t
				self.TryOpenRemoldUI(playerId, dimensionId, pos)
		pass

	@EngineEvent()
	def ServerItemUseOnEvent(self, args):
		"""对方块使用物品事件"""
		blockName = args.get("blockName")
		if blockName == BlockEnum.CarRemold:
			args["ret"] = True
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ItemsClientSystem)
	def ItemUsedEvent(self, args):
		"""使用道具物品事件"""
		stage = args.get("stage")
		if stage == "start_rescue":
			# 开启救援
			self.TryStartRescue(args)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.CarClientSystem)
	def CarCtrlEvent(self, args):
		"""载具事件"""
		stage = args.get("stage")
		if stage == "repair_broken":
			# 修复损坏载具
			self.RepairBrokenCar(args)
		pass
	# endregion

	# region 救援
	def TryStartRescue(self, args):
		"""尝试开启救援功能"""
		playerId = args.get("__id__")
		info = {"stage": "start_rescue",}
		# 判断玩家附近，是否有载具，如果有，则允许救援，并开启timer，延迟后tp
		posComp = compFactory.CreatePos(playerId)
		pos = posComp.GetPos()
		dimension = engineApiGas.GetEntityDimensionId(playerId)
		if pos:
			cfg = GetRescueConfig()
			maxDistance2 = cfg.get("maxDistance", 16) ** 2
			# 获取附近的一个载具
			hasCar = False
			for carEntityId in self._carObjDict.keys():
				carPosComp = compFactory.CreatePos(carEntityId)
				carPos = carPosComp.GetPos()
				carDimension = engineApiGas.GetEntityDimensionId(carEntityId)
				if carDimension == dimension and commonApiMgr.GetDistanceXZSqrt(pos, carPos) <= maxDistance2:
					hasCar = True
					# 判断位置是否可救援
					canRescue, rayPos = self.CheckPosBlocksByRescue(pos, dimension)
					if canRescue:
						# 开启救援
						checkCount = 10
						# 延迟执行逻辑
						engineApiGas.AddTimer(cfg.get("delayTPTime", 1), self.DelayRescueCarTimer, playerId, carEntityId, checkCount)
					else:
						info["tips"] = 13
					break
			if not hasCar:
				info["tips"] = 12
		# 客户端开始效果逻辑
		self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass

	def DelayRescueCarTimer(self, playerId, entityId, checkCount):
		"""延迟救援某个载具，配合效果表现"""
		# 先检测玩家位置，是否符合条件
		# 如果不符合，则在玩家位置附近随机位置进行检测，上限10次
		posComp = compFactory.CreatePos(playerId)
		pos = posComp.GetPos()
		checkPos = None
		if pos:
			checkPos = (int(pos[0]), pos[1], int(pos[2]))
		dimension = engineApiGas.GetEntityDimensionId(playerId)
		if checkPos and checkCount > 0:
			# 判断坐标是否符合条件：在水面上、或者在方块平台上（小平台）
			canRescue, rayPos = self.CheckPosBlocksByRescue(checkPos, dimension)
			if canRescue:
				# 符合条件
				# tp载具
				eposComp = compFactory.CreatePos(entityId)
				eposComp.SetPos(rayPos)
				# 设置玩家直接驾驶载具
				carObj = self.GetCarLogicObj(entityId)
				if carObj:
					carObj.CarCtrlEvent({"__id__": playerId, "stage": "geton", "entityId": entityId,})
				# 扣道具耐久
				cfg = GetRescueConfig()
				serverApiMgr.UpdateCarriedItemDurability(playerId, cfg.get("durability", 100), itemsConfig.ItemsNameEnum.CarRescue)
				# 更新任务进度
				taskSys = self.GetTaskSystem()
				if taskSys:
					taskSys.IncreaseAccumulationByFullKey(playerId, "Car.rescued", 1)
			else:
				# 该点不符合条件，则重新选点
				radius = 16
				posX = random.randint(checkPos[0] - radius, checkPos[0] + radius)
				posZ = random.randint(checkPos[2] - radius, checkPos[2] + radius)
				posY = engineApiGas.GetTopBlockHeight((posX, posZ), dimension)
				checkPos = (posX, posY, posZ)
				# 启动新的timer，避免一帧执行太多逻辑
				checkCount -= 1
				engineApiGas.AddTimer(0.05, self.DelayRescueCarTimer, playerId, entityId, checkCount)
		pass

	def CheckPosBlocksByRescue(self, pos, dimension):
		"""检查pos是否符合救援条件
		:param pos: 玩家头部位置
		"""
		# 射线相关参数
		rayCfg = [
			{"rot": (1, 0, 0), "offset": (-1, 0, 0), "distance": 3},
			{"rot": (0, 0, 1), "offset": (0, 0, -1), "distance": 3},
			{"rot": (0, -1, 0), "offset": (0, 0, 0), "distance": 2, "ground": True},
		]
		canRescue = True
		rayPos = None
		for ray in rayCfg:
			rayPos = (pos[0] + ray["offset"][0], pos[1] + ray["offset"][1], pos[2] + ray["offset"][2])
			blockList = serverApi.getEntitiesOrBlockFromRay(dimension, rayPos, ray["rot"], ray["distance"], False, minecraftEnum.RayFilterType.OnlyBlocks)
			if blockList:
				for block in blockList:
					if block.get("type") == "Block":
						if ray.get("ground"):
							if IsNotRescueRayBlock(block.get("identifier")):
								# 检测脚底时，如果脚底是岩浆等，则不符合条件
								canRescue = False
								break
						else:
							# 横向的两次检测，只要有方块就不符合条件
							canRescue = False
							break
			if canRescue is False:
				break
		return canRescue, rayPos
	# endregion

	# region 修复
	def RepairBrokenCar(self, args):
		"""修复损坏载具"""
		playerId = args.get("__id__")
		entityId = args.get("entityId")
		engineComp = compFactory.CreateEngineType(entityId)
		if engineComp.GetEngineTypeStr() == BrokenCarEngineTypeStr:
			# 扣除物品
			repairItems = GetRepairNeedItems()
			res = serverApiMgr.DeductMultiItemsCount(playerId, repairItems)
			if res:
				# 将实体替换为载具实体
				serverApiMgr.SpawnEntityById(self, entityId, CarEngineTypeStr)
				self.DestroyEntity(entityId)
		pass
	# endregion

	# region 功能
	def GetOrCreateCarLogicObj(self, entityId, engineTypeStr):
		"""获取/创建载具对象"""
		obj = self._carObjDict.get(entityId)
		if obj is None:
			if engineTypeStr == CarEngineTypeStr:
				obj = BaseCarLogic(self, entityId, engineTypeStr)
				self._carObjDict[entityId] = obj
		return obj
	
	def GetCarLogicObj(self, entityId):
		"""获取载具对象"""
		return self._carObjDict.get(entityId)
	
	def GetAllCarLogicObj(self):
		"""获取所有载具对象list"""
		return self._carObjDict.values()
	
	def PopCarLogicObj(self, entityId, isRemove=False):
		"""删除载具对象"""
		obj = self._carObjDict.pop(entityId, None)
		if obj:
			# 重新生成新的载具
			if not isRemove:
				obj.RespawnCar()
				self.DestroyEntity(entityId)
			obj.Destroy()
		pass

	def TryOpenRemoldUI(self, playerId, dim, pos):
		"""尝试打开改造界面"""
		# 获取附近的载具，看是否有在范围内的
		minDist = RemoldUIRange
		minCarObj = None
		for entityId, obj in self._carObjDict.iteritems():
			if obj.GetDimension() == dim:
				# 判断范围
				cpos = engineApiGas.GetEntityPos(entityId)
				dist = commonApiMgr.GetDistanceSqrt(pos, cpos)
				if dist < minDist:
					minCarObj = obj
					minDist = dist
		if minCarObj:
			# 打开改造界面
			minCarObj.OpenRemoldUI(playerId)
		else:
			# 提示附近没车辆
			info = {
				"stage": "open_remold",
			}
			self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass
	
	def GetEngineTypeStr(self, entityId):
		"""获取实体engineTypeStr"""
		engineComp = compFactory.CreateEngineType(entityId)
		return engineComp.GetEngineTypeStr()
	
	def GetTaskSystem(self):
		"""获取任务系统"""
		if self._taskSys is None:
			self._taskSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TaskServerSystem)
		return self._taskSys
	# endregion

