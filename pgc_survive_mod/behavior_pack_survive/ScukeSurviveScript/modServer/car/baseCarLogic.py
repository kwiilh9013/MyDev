# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modServer.car.baseCarDrive import BaseCarDrive
from ScukeSurviveScript.modServer.car.baseCarRemold import BaseCarRemold
from ScukeSurviveScript.modServer.car.baseCarAttr import BaseCarAttr
from ScukeSurviveScript.modServer.car.baseCarSkill import BaseCarSkill
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BaseCarLogic(CommonEventRegister):
	"""基地车 主逻辑 服务端"""
	def __init__(self, severHandler, entityId, engineTypeStr):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		self._entityId = entityId
		self._engineTypeStr = engineTypeStr
		# 实体所在维度，当上骑时更新
		self._dimension = engineApiGas.GetEntityDimensionId(self._entityId)
		
		# 操作对象
		self.mDriveObj = BaseCarDrive(severHandler, entityId, self)
		# 属性对象
		self.mAttrObj = BaseCarAttr(severHandler, entityId, self)
		# 改造对象
		self.mRemoldObj = BaseCarRemold(severHandler, entityId, self)
		# 技能对象
		self.mSkillObj = BaseCarSkill(severHandler, entityId, self)

		# config
		self._attrConfig = carConfig.BaseCarAttrConfig

		# 骑乘的操作时间，用于判断是否是通过自定义UI骑乘
		# 设置初始值，这样在启动游戏时本来乘骑的玩家也不至于被踢下
		self._rideCtrlTime = time.time()

		# 乘客列表（包括玩家和其他生物）
		self._riderList = []
		# 设置复活点的timer
		self._respawnPosTimer = None

		# 撞飞实体的数据缓存，用于避免频繁触发
		self._knockEntityDict = {}
		
		# 瘫痪状态
		self._isInhibit = False
		self._inhibitTimer = None

		# 组件
		self._rideComp = compFactory.CreateRide(self._entityId)
		self._posComp = compFactory.CreatePos(self._entityId)
		self._rotComp = compFactory.CreateRot(self._entityId)
		self._blockComp = compFactory.CreateBlockInfo(self._levelId)

		# 监听事件
		Instance.mEventMgr.RegisterEvent(eventConfig.ElectromagnetismSubscribeEvent, self.ElectromagnetismSubscribeEvent)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectromagnetismSubscribeEvent, self.ElectromagnetismSubscribeEvent)
		self._server = None
		self.mDriveObj and self.mDriveObj.Destroy()
		self.mDriveObj = None
		self.mAttrObj and self.mAttrObj.Destroy()
		self.mAttrObj = None
		self.mRemoldObj and self.mRemoldObj.Destroy()
		self.mRemoldObj = None
		self.mSkillObj and self.mSkillObj.Destroy()
		self.mSkillObj = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def OnMobHitMobServerEvent(self, args):
		"""生物撞击事件"""
		mobId = args.get("mobId")
		if mobId == self._entityId:
			hittedMobList = args.get("hittedMobList")
			self.SetKnockHitEntity(hittedMobList)
		pass

	@EngineEvent()
	def MobDieEvent(self, args):
		"""实体死亡事件"""
		attacker = args.get("attacker")
		if attacker == self._entityId:
			cause = args.get("cause")
			if cause == minecraftEnum.ActorDamageCause.EntityAttack:
				taskSys = self.GetTaskSystem()
				if taskSys:
					# 驾驶员
					playerId = self.GetRider()
					if playerId:
						taskSys.IncreaseAccumulationByFullKey(playerId, "Car.killed", 1)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.CarClientSystem)
	def CarCtrlEvent(self, args):
		"""载具控制事件"""
		playerId = args.get("__id__")
		stage = args.get("stage")
		entityId = args.get("entityId")
		if entityId == self._entityId:
			if stage == "geton":
				# 上骑
				self._rideCtrlTime = time.time()
				rideComp = compFactory.CreateRide(entityId)
				rideComp.SetPlayerRideEntity(playerId, entityId)
		elif playerId in self.GetRiderList():
			if stage == "getoff_mercenary":
				# 雇佣兵下车
				self.SetMercenaryStopRide(playerId)
		pass

	def ElectromagnetismSubscribeEvent(self, args):
		"""订阅 电磁瘫痪事件"""
		stage = args.get("stage")
		if stage == "inhibit":
			# 瘫痪
			# 判断是否是在本载具附近
			if self.GetDimension() == args["dimension"]:
				radius = args["radius"] * 2
				if commonApiMgr.GetDistanceSqrt(self._posComp.GetPos(), args["pos"]) <= radius ** 2:
					# 瘫痪
					self.SetInhibit(args["duration"])
		pass
	# endregion

	# region 乘骑
	def StartRiding(self, playerId):
		"""设置乘骑"""
		# 只有玩家上骑才执行逻辑
		if playerId in serverApi.GetPlayerList():
			self.mDriveObj.StartRiding(playerId)
			self._rideCtrlTime = None
			# 更新维度
			self._dimension = engineApiGas.GetEntityDimensionId(self._entityId)
			# 开启碰撞生物的监听
			plyComp = compFactory.CreatePlayer(self._entityId)
			plyComp.OpenPlayerHitMobDetection()
			# 设置复活点
			self.StartSetRespawn(True, playerId)
			# 生物上骑（需延迟，玩家刚登录时，可能是玩家先触发，再是其他生物触发）
			engineApiGas.AddTimer(0.1, self.SetMercenaryStarRide, playerId)
		# 更新乘客列表
		self._riderList.append(playerId)
		
		# 同步乘骑数据到客户端
		isRider = playerId == self.GetRider()
		info = {
			"stage": "startRiding",
			"rideId": self._entityId,
			"isRider": isRider,
		}
		# 如果是驾驶员，则再同步能源数据、改造数据
		if isRider:
			info["energy"] = self.GetCurrentEnergy()
			info["maxEnergy"] = self.GetMaxEnergy()
			info["usePartData"] = self.GetUsePartData()
			# 配件技能CD
			cds = {}
			for partId in info["usePartData"].values():
				cd = self.mSkillObj.GetSkillCD(partId)
				if cd:
					cds[partId] = cd
			if cds:
				info["cds"] = cds
		self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass

	def IsCanRide(self):
		"""是否可以骑乘"""
		# 判断是否是通过自定义UI上骑，如果不是，则不允许上骑
		if self._rideCtrlTime:
			if time.time() - self._rideCtrlTime < 1.0:
				return True
		return False

	def StopRiding(self, playerId):
		"""停止乘骑/下骑"""
		# 只有玩家才执行逻辑
		if playerId in serverApi.GetPlayerList():
			self.mDriveObj.StopRiding(playerId)
			# 存储一次能源
			self.mAttrObj.SaveAttrData()
			# 设置复活点
			self.StartSetRespawn(False, playerId)
			# 关闭飞行（如果此时没有驾驶员了）
			if self.GetRider() is None and self.GetFlyState() is True:
				self.mSkillObj.SetStartFlyState({"__id__": playerId, "state": False})

		# 更新乘客列表
		if playerId in self._riderList:
			self._riderList.remove(playerId)

		if len(self._riderList) <= 0:
			# 如果没有玩家了，才关闭碰撞生物的监听
			plyComp = compFactory.CreatePlayer(self._entityId)
			plyComp.ClosePlayerHitMobDetection()
		pass

	def GetRider(self):
		"""获取驾驶员id"""
		return self.mDriveObj and self.mDriveObj.GetRider()
	# endregion
	
	# region 重新生成载具
	def RespawnCar(self):
		"""原地重新生成载具，在载具死亡时调用"""
		# 生成载具
		entityId = serverApiMgr.SpawnEntityById(self._server, self._entityId, carConfig.CarEngineTypeStr)
		# 转存强化数据
		self.ExportAttrDataToEntity(entityId)
		# 血量重置为1点血，玩家需要维修
		attrComp = compFactory.CreateAttr(entityId)
		attrComp.SetAttrValue(minecraftEnum.AttrType.HEALTH, 1)
		pass
	
	def ExportAttrDataToEntity(self, entityId):
		"""导出属性到指定实体"""
		# 导出属性到新载具
		self.mAttrObj.ExportDataToEntity(entityId)
		# 导出改造属性到新载具
		self.mRemoldObj.ExportDataToEntity(entityId)
		pass
	# endregion

	# region 碰撞
	def SetKnockHitEntity(self, hitEntityList):
		"""撞到实体的逻辑"""
		realSpeed = self.mDriveObj.GetCurrentRealSpeed()
		hurtParam = self._attrConfig["crashHurtParam"]
		# 如果载具速度达到某个值，才可以撞飞生物
		if realSpeed >= hurtParam["knockSpeed"]:
			hurtSpeedLimit = hurtParam["hurtSpeed"]
			startPos = self._posComp.GetPos()
			# 如果撞到实体，则进行击退
			currentT = time.time()
			for entityId in hitEntityList:
				# 排除乘客
				if entityId not in self.GetRiderList():
					# 判断CD
					t = self._knockEntityDict.get(entityId, 0)
					if currentT - t >= 1.0:
						# 撞飞
						posComp = compFactory.CreatePos(entityId)
						endPos = posComp.GetPos()
						vector = (endPos[0] - startPos[0], endPos[1] - startPos[1], endPos[2] - startPos[2])
						actionComp = compFactory.CreateAction(entityId)
						knockbackPower = hurtParam["knockbackPower"]
						# 获取前杠的撞击加成数据
						attrCfg = self.GetFrontBumperPartAttrCfg()
						if attrCfg and attrCfg.get("knockback"):
							knockbackPower += attrCfg["knockback"]
						actionComp.SetMobKnockback(vector[0], vector[2], realSpeed * hurtParam["knockbackPower"], 0.8, 0.8)
						# 造成伤害
						if realSpeed >= hurtSpeedLimit:
							attrComp = compFactory.CreateAttr(entityId)
							maxHealth = attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
							if maxHealth:
								damage = maxHealth * hurtParam["damageRatio"]
								damageLimit = hurtParam["maxDamage"]
								# 前杠的伤害加成
								if attrCfg and attrCfg.get("hit_max_damage"):
									damageLimit = attrCfg["hit_max_damage"]
								damage = min(damage, damageLimit)
								hurtComp = compFactory.CreateHurt(entityId)
								hurtComp.Hurt(int(damage), minecraftEnum.ActorDamageCause.EntityAttack, self._entityId)
						self._knockEntityDict[entityId] = currentT
						# 降低移速
						self.mDriveObj.SetCutSpeedByKnock()
			# print("___________ SetHitEntityTrigger", hitEntityList)
		pass
	# endregion
	
	# region 复活点
	def StartSetRespawn(self, state, playerId=None):
		"""启动设置复活点，每10秒设置一次"""
		if state:
			if not self._respawnPosTimer:
				self._respawnPosTimer = engineApiGas.AddRepeatTimer(10, self.SetRespawnTimer)
		else:
			if self._respawnPosTimer:
				engineApiGas.CancelTimer(self._respawnPosTimer)
				self._respawnPosTimer = None
		if playerId:
			self.SetRespawnPos(playerId)
		pass
	
	def SetRespawnTimer(self):
		"""循环设置复活点timer"""
		for playerId in self._riderList:
			self.SetRespawnPos(playerId)
		pass

	def SetRespawnPos(self, playerId, pos=None):
		"""设置复活点"""
		# 设置复活点为载具当前位置
		if pos is None:
			pos = self._posComp.GetFootPos()
		plyComp = compFactory.CreatePlayer(playerId)
		plyComp.SetPlayerRespawnPos(pos, self._dimension)
		pass
	# endregion

	# region npc上车逻辑
	def SetMercenaryStarRide(self, playerId):
		"""设置雇佣兵，上车"""
		# 将该玩家驯服的NPC，都设置上骑，主要是针对黄金苦力怕和雇佣兵
		filters = {
			"all_of": [
				{"test": "is_family", "subject": "other", "value": "mercenary"},
				{"test": "is_riding", "subject": "other", "value": False}
			]
		}
		entityList = engineApiGas.GetEntitiesAround(playerId, 16, filters)
		hasNPC = False
		if entityList:
			for entityId in entityList:
				# 判断驯服
				owner = engineApiGas.GetOwnerId(entityId)
				if owner == playerId:
					hasNPC = True
					# 设置上骑
					rideComp = compFactory.CreateRide(entityId)
					rideComp.SetRiderRideEntity(entityId, self._entityId)
		if hasNPC is False:
			# 获取乘骑生物，如果有该玩家的NPC，则显示UI
			riderList = self.GetRiderList()
			for entityId in riderList:
				owner = engineApiGas.GetOwnerId(entityId)
				if owner == playerId:
					hasNPC = True
					break
		if hasNPC:
			# 客户端显示UI
			info = {
				"stage": "mercenary",
				"state": True,
			}
			self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass

	def SetMercenaryStopRide(self, playerId):
		"""设置雇佣兵，下车"""
		# 获取乘骑生物，如果有该玩家的NPC，则显示UI
		riderList = self.GetRiderList()
		for i in xrange(len(riderList) - 1, -1, -1):
			entityId = riderList[i]
			owner = engineApiGas.GetOwnerId(entityId)
			if owner == playerId:
				# 下骑
				rideComp = compFactory.CreateRide(entityId)
				rideComp.StopEntityRiding()
		# 客户端关闭UI
		info = {
			"stage": "mercenary",
			"state": False,
		}
		self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass
	# endregion

	# region 瘫痪
	def SetInhibit(self, duration):
		"""设置瘫痪状态"""
		# 如果之前没瘫痪
		if not self._isInhibit:
			# 更新瘫痪状态
			self._isInhibit = True
			# 发送消息到客户端显示瘫痪特效
			info = {
				"stage": "inhibit",
				"state": True,
				"entityId": self._entityId,
			}
			self.SendMsgToAllClient(eventConfig.CarCtrlEvent, info)
			# 停止行驶
			self.StopSteer()

		# 更新瘫痪时间
		# 启动timer，延迟恢复
		if self._inhibitTimer:
			engineApiGas.CancelTimer(self._inhibitTimer)
		self._inhibitTimer = engineApiGas.AddTimer(duration, self.DelayRecoverInhibitTimer)
		pass

	def DelayRecoverInhibitTimer(self):
		"""延迟恢复瘫痪状态"""
		if self._inhibitTimer:
			engineApiGas.CancelTimer(self._inhibitTimer)
			self._inhibitTimer = None
		self._isInhibit = False
		# 发送消息到客户端取消瘫痪特效
		info = {
			"stage": "inhibit",
			"state": False,
			"entityId": self._entityId,
		}
		self.SendMsgToAllClient(eventConfig.CarCtrlEvent, info)

	def IsInhibit(self):
		"""是否瘫痪"""
		return self._isInhibit
	# endregion

	# region 耐久
	def UpdateMaxDurability(self, durability):
		"""更新耐久上限"""
		return self.mAttrObj.SetAddMaxDurability(durability)

	def SetUpdateDurability(self, durability):
		"""更新耐久数据"""
		return self.mAttrObj.SetUpdateDurability(durability)
	
	def GetCurrentDurability(self):
		"""获取当前耐久"""
		return self.mAttrObj.GetCurrentDurability()

	def GetMaxDurability(self):
		"""获取最大耐久"""
		return self.mAttrObj.GetMaxDurability()
	# endregion

	# region 能源
	def UpdateMaxEnergy(self, energy):
		"""更新能源上限"""
		return self.mAttrObj.SetAddMaxEnergy(energy)

	def SetRunConsumeEnergy(self, runDistance):
		"""行驶消耗能源"""
		return self.mAttrObj.SetRunConsumeEnergy(runDistance)

	def SetConsumeEnergy(self, energy):
		"""消耗能源, energy>0"""
		return self.mAttrObj.SetUpdateEnergy(-energy)

	def GetCurrentEnergy(self):
		"""获取当前能源"""
		return self.mAttrObj.GetCurrentEnergy()

	def GetMaxEnergy(self):
		"""获取最大能源"""
		return self.mAttrObj.GetMaxEnergy()
	# endregion

	# region 改造
	def OpenRemoldUI(self, playerId):
		"""打开改造UI请求"""
		self.mRemoldObj.OpenRemoldUI(playerId)
		pass

	def IsCanRunInWater(self):
		"""是否可在水面行驶"""
		return self.mRemoldObj.IsCanRunInWater()
	
	def GetUsePartData(self):
		"""获取使用中的改造配件数据"""
		return self.mRemoldObj.GetUsePartData()
	
	def GetFrontBumperPartAttrCfg(self):
		"""获取前杠的attr加成数据"""
		return self.mRemoldObj.GetFrontBumperPartAttrCfg()
	
	# endregion

	# region 功能方法
	def IsCanSteer(self):
		"""载具是否可行驶"""
		# 能源
		if self.GetCurrentEnergy() <= 0:
			return False
		# 耐久
		if self.GetCurrentDurability() <= 0:
			return False
		# 瘫痪状态
		if self.IsInhibit():
			return False
		return True
	
	def StopSteer(self):
		"""因耐久、能源耗尽、瘫痪，停止行驶"""
		# 停止飞行状态
		self.mSkillObj.SetStartFlyState({"__id__": self.GetRider(), "state": False})
		pass
	
	def GetRiderList(self):
		"""获取乘客列表(包括玩家和非玩家)"""
		return self._riderList
	
	def GetPlayerList(self):
		"""获取玩家乘客列表"""
		return self.mDriveObj.GetPlayerList()
	
	def GetRider(self):
		"""获取驾驶员"""
		return self.mDriveObj.GetRider()
	
	def GetDimension(self):
		"""获取实体所在维度"""
		return self._dimension
	
	def GetEntityId(self):
		"""获取实体所在维度"""
		return self._entityId
	
	def GetTaskSystem(self):
		"""获取任务系统"""
		return self._server.GetTaskSystem()
	
	def GetFlyState(self):
		"""获取飞行状态"""
		return self.mSkillObj.GetFlyState()
	# endregion
