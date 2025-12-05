# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetPartSkillConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import PartEnum
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


_FireCauses = (
	minecraftEnum.ActorDamageCause.Fire,
	minecraftEnum.ActorDamageCause.FireTick,
	minecraftEnum.ActorDamageCause.Lava,
)
"""火焰伤害"""
_ImmuneDamageType = (
    minecraftEnum.ActorDamageCause.Contact,
    minecraftEnum.ActorDamageCause.Fireworks,
    minecraftEnum.ActorDamageCause.FlyIntoWall,
)
"""可免疫的伤害"""


class BaseCarAttr(CommonEventRegister):
	"""基地车 属性 服务端"""
	def __init__(self, severHandler, entityId, carObj):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		# 载具对象
		self._carObj = carObj
		# 坐骑id
		self._entityId = entityId

		# config
		self._attrConfig = carConfig.BaseCarAttrConfig
		self._repairConfig = carConfig.RepairConfig

		# region 耐久
		# 耐久
		self._maxDurability = 0
		# 折扣后不足1点伤害的部分累计
		self._floatDamage = 0
		# 火类型伤害的CD
		self._fireDamageCD = 0
		# 天气掉耐久的timer
		self._snowstormDamageTimer = None
		# 2024.9.30 去掉该功能
		# 注册暴风雪的订阅
		# Instance.mEventMgr.RegisterEvent(eventConfig.WeatherSubscribeEvent, self.WeatherSubscribeEvent)
		
		# 维修数据: {durability/已维修的耐久, slot/物品槽位}
		self._repairDict = None
		# endregion

		# region 能源
		# 能源
		self._maxEnergy = 0
		self._energy = self._maxEnergy
		# 当前行驶距离
		self._runDistance = 0.0
		# endregion

		self._attrComp = compFactory.CreateAttr(self._entityId)
		self._extraComp = compFactory.CreateExtraData(self._entityId)
		self._effectComp = compFactory.CreateEffect(self._entityId)
		
		# 延迟初始化（如果生成的同时，存储extraData，就会导致初始化时获取不到extraData）
		engineApiGas.AddTimer(0.1, self.InitAttr)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		# Instance.mEventMgr.UnRegisterEvent(eventConfig.WeatherSubscribeEvent, self.WeatherSubscribeEvent)
		# 存储一次能源（如果此时生物仍存在）
		if self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH) > 0:
			self.SaveAttrData()
		self._server = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def ActuallyHurtServerEvent(self, args):
		"""实际受伤事件"""
		entityId = args.get("entityId")
		srcId = args.get("srcId")
		cause = args.get("cause")
		if entityId == self._entityId:
			# 屏蔽部分伤害、以及伤害来源是驾驶员的伤害
			if cause in _ImmuneDamageType or srcId == self._carObj.GetRider():
				args["damage"] = 0
			else:
				# 掉耐久
				args["damage"] = self.SetHurtDamage(args["damage"], cause)
				# print("________ ActuallyHurtServerEvent", args["damage"])
				if args["damage"] > 0:
					# 判断实体当前血量，如果为1点，则进行锁血
					health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
					if health - args["damage"] <= 1:
						# 需要赋值int类型
						args["damage"] = max(0, int(health - 1))
					if health <= 1 and srcId != "-1":
						# 载具没耐久，则转移仇恨
						rider = self._carObj.GetRider()
						actionComp = serverApi.GetEngineCompFactory().CreateAction(srcId)
						if rider:
							actionComp.SetAttackTarget(rider)
						else:
							actionComp.ResetAttackTarget()
		elif srcId != "-1" and srcId != entityId and entityId in self._carObj.GetRiderList():
			# 乘客受伤，且有伤害来源，才转移（如中毒、饥饿等不会转移）
			# 如果载具没损坏，才将伤害转移到载具
			health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
			if health > 1:
				damage = args["damage"]
				args["damage"] = 0
				self.SetHurtDamage(damage, cause)
		pass

	@EngineEvent()
	def AddEffectServerEvent(self, args):
		"""添加效果事件"""
		entityId = args.get("entityId")
		if entityId == self._entityId:
			# 清除buff
			effectName = args.get("effectName")
			# 缓降不清除
			if effectName != minecraftEnum.EffectType.SLOW_FALLING:
				self._effectComp.RemoveEffectFromEntity(effectName)
		pass

	@EngineEvent()
	def OnFireHurtEvent(self, args):
		"""火焰伤害事件"""
		entityId = args.get("victim")
		if entityId == self._entityId:
			# 取消着火效果（保留伤害）
			args["cancelIgnite"] = True
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.CarClientSystem)
	def CarCtrlEvent(self, args):
		"""载具控制事件"""
		playerId = args.get("__id__")
		stage = args.get("stage")
		entityId = args.get("entityId")
		if entityId == self._entityId:
			if stage == "add_energy":
				# 加能源
				self.SetAddEnergy(playerId, args.get("materials"))
			elif stage == "repair":
				# 修理载具
				self.SetRepairCar(playerId)
			elif stage == "stop_repair":
				# 停止维修，需延迟一帧，和使用物品的时间重叠了
				engineApiGas.AddTimer(0.05, self.SetStopRepairCar, playerId)
			elif stage == "energy_ui":
				# 打开加能源的UI，同步能源值到客户端
				info = {
					"stage": "energy_ui",
					"entityId": self._entityId,
					"energy": self.GetCurrentEnergy(),
					"maxEnergy": self.GetMaxEnergy(),
				}
				self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass
	
	# def WeatherSubscribeEvent(self, args):
	# 	"""天气 订阅事件"""
	# 	weather = args.get("weather")
	# 	if weather == PhaseWeatherEventEnum.SnowStorm:
	# 		state = args.get("state")
	# 		if state:
	# 			# 开启暴风雪，开始timer，监听伤害
	# 			if not self._snowstormDamageTimer:
	# 				param = self._attrConfig.get("snowstormParam")
	# 				if param:
	# 					self._snowstormDamageTimer = engineApiGas.AddRepeatTimer(param[0], self.SetWeatherDeductDurabilityTimer, param)
	# 		else:
	# 			# 暴风雪结束
	# 			if self._snowstormDamageTimer:
	# 				engineApiGas.CancelTimer(self._snowstormDamageTimer)
	# 				self._snowstormDamageTimer = None
	# 	pass
	
	# endregion


	# region 初始化
	def InitAttr(self):
		"""初始化属性"""
		# 优先读取extraData，没有的数据则读取config
		attrData = self.LoadAttrData()
		# 耐久 = 血量
		self._maxDurability = self._attrConfig["maxDurability"]
		# 更新最大血量
		maxHealth = self._attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
		if maxHealth < self._maxDurability:
			self._attrComp.SetAttrMaxValue(minecraftEnum.AttrType.HEALTH, self._maxDurability)
			# 如果当前血量和之前的最大血量一致（即之前是满血），则此时也恢复满血；否则不改当前血量
			health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
			if health == maxHealth:
				self._attrComp.SetAttrValue(minecraftEnum.AttrType.HEALTH, self._maxDurability)
		else:
			self._maxDurability = maxHealth
		# 能源
		self._maxEnergy = attrData.get("maxEnergy", self._attrConfig["maxEnergy"])
		self._energy = attrData.get("energy", self._maxEnergy)

		# 同步能源数据到驾驶员客户端
		rider = self._carObj.GetRider()
		if rider:
			info = {
				"stage": "energy",
				"energy": self.GetCurrentEnergy(),
				"maxEnergy": self.GetMaxEnergy(),
			}
			self.SendMsgToClient(rider, eventConfig.CarCtrlEvent, info)
		pass
	# endregion

	# region 耐久
	def SetRepairCar(self, playerId):
		"""修理载具"""
		# 检测手持的物品，是否是维修工具，如果是，才执行修理逻辑
		itemComp = compFactory.CreateItem(playerId)
		item = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.CARRIED, 0, True)
		if item and item.get("newItemName") == self._repairConfig["itemName"]:
			# 判断载具耐久是否满
			if self.GetCurrentDurability() < self.GetMaxDurability():
				# 恢复载具耐久
				self.SetUpdateDurability(self._repairConfig["repairDurability"], playerId=playerId)
				# 记录耐久数据，等停止修复时再扣除
				if self._repairDict is None:
					self._repairDict = {"durability": 1, "slot": engineApiGas.GetSelectSlotId(playerId)}
				else:
					self._repairDict["durability"] = self._repairDict.get("durability", 1) + 1
					# 如果工具耐久不足，则立即扣除耐久
					if self._repairDict["durability"] >= item.get("durability", 0):
						self.SetStopRepairCar(playerId)
			# 更新客户端进度
			durability = self.GetCurrentDurability()
			info = {
				"stage": "repair",
				"ratio": durability / (self.GetMaxDurability() + 0.0),
				"durability": durability,
			}
			self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass

	def SetStopRepairCar(self, playerId):
		"""停止修理载具"""
		if self._repairDict:
			# 校验格子的物品是否是维修工具
			slot = self._repairDict.get("slot")
			if slot is not None and slot >= 0:
				itemComp = compFactory.CreateItem(playerId)
				item = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slot, True)
				if item and item.get("newItemName") == self._repairConfig["itemName"]:
					durability = item["durability"] - self._repairDict.get("durability", 1)
					if durability <= 0:
						# 扣除物品
						itemComp.SetInvItemNum(slot, 0)
					else:
						# 扣耐久
						itemComp.SetItemDurability(minecraftEnum.ItemPosType.INVENTORY, slot, durability)
			self._repairDict = None
		pass

	def SetHurtDamage(self, damage, cause):
		"""
		设置受伤伤害（根据自定义规则对伤害进行修改）
		:return: int 返回修改后的伤害
		"""
		if cause == minecraftEnum.ActorDamageCause.Fall:
			# 摔伤
			return self.SetFallDamage(damage)
		elif cause in _FireCauses:
			# 火类型
			# 判断cd
			curTime = time.time()
			if self._fireDamageCD == 0 or curTime - self._fireDamageCD > self._attrConfig["fallDamageParam"][0]:
				self._fireDamageCD = curTime
				damage = self._attrConfig["fallDamageParam"][1]
				return damage
			return 0
		else:
			damage = damage * self._attrConfig["attackDamageRatio"]
		# 累计不足1点的部分伤害
		self._floatDamage += damage % 1
		if self._floatDamage > 1:
			damage += 1
			self._floatDamage -= 1
		return int(damage)
	
	def SetFallDamage(self, damage):
		"""
		设置摔落伤害（根据自定义规则对摔落伤害进行修改）
		:return: int 返回修改后的摔落伤害
		"""
		# 原版摔伤逻辑：高于3格的话，每多1格，掉1点血（如4格=1，5格=2）
		height = damage + 3
		if height > self._attrConfig["fallMinHeight"]:
			damage = (height - self._attrConfig["fallMinHeight"]) * self._attrConfig["fallHeightDamageRatio"]
		else:
			damage = 0
		return int(damage)
	
	# def SetWeatherDeductDurabilityTimer(self, param):
	# 	"""设置天气掉耐久"""
	# 	if self._snowstormDamageTimer is None:
	# 		return
		
	# 	# 如果此时有行驶，才会掉耐久
	# 	if self._runDistance > 0 and self._carObj.GetPlayerList():
	# 		self.SetUpdateDurability(-param[1])
	# 	pass

	def SetUpdateDurability(self, durability, playerId=None):
		"""
		设置更新耐久
		:param durability: int 更新的耐久值，小于0表示扣耐久
		"""
		# 扣耐久 = 扣血
		maxHealth = self._attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
		health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
		lastHealth = health
		health = max(1, health + durability)	# 锁血1点
		health = min(health, maxHealth)
		self._attrComp.SetAttrValue(minecraftEnum.AttrType.HEALTH, health)
		# 如果耐久恢复满，则更新任务进度
		if health >= maxHealth and playerId:
			taskSys = self._carObj.GetTaskSystem()
			if taskSys:
				taskSys.IncreaseAccumulationByFullKey(playerId, "Car.repaired", 1)
		# 如果耐久掉为0，则调用方法，同步更新相关逻辑
		if health <= 1 and lastHealth > 1:
			self._carObj.StopSteer()
		pass

	def SetAddMaxDurability(self, durability):
		"""增加最大耐久，负数=减少"""
		self._maxDurability += durability
		self._attrComp.SetAttrMaxValue(minecraftEnum.AttrType.HEALTH, self._maxDurability)
		# 存储数据
		self.SaveAttrData()
		pass

	def GetCurrentDurability(self):
		"""获取当前耐久"""
		health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
		return max(health - 1, 0)

	def GetMaxDurability(self):
		"""获取最大耐久"""
		return self._maxDurability - 1

	# endregion


	# region 能源
	def SetAddMaxEnergy(self, energy):
		"""增加最大能源，负数=减少"""
		self._maxEnergy += energy
		if self._energy > self._maxEnergy:
			self._energy = self._maxEnergy
		# 存储数据
		self.SaveAttrData()
		pass

	def SetAddEnergy(self, playerId, materials):
		"""
		增加能源
		:param playerId 玩家id
		:param maetrials: dict:{(item,aux): count} 材料数据
		"""
		# 校验能源是否满了
		if self.GetCurrentEnergy() < self.GetMaxEnergy():
			# 扣除玩家背包的物品，根据扣除的物品给载具增加能源
			addEnergy = 0
			# 获取玩家背包物品
			itemComp = compFactory.CreateItem(playerId)
			itemListDict = serverApiMgr.GetPlayerInventoryItemList(playerId)
			slot = 0
			for item in itemListDict:
				# 如果该物品是材料物品，则进行扣除
				if item:
					for mat, count in materials.iteritems():
						if count > 0 and item.get("newItemName") == mat[0] and item.get("newAuxValue") == mat[1]:
							# 获取能源值
							energy = carConfig.GetAddEnergyMaterialNum(mat[0])
							if energy > 0:
								# 计算扣除后剩下的数量
								remainingCount = item.get("count", 1) - count
								# 扣除数量
								if remainingCount >= 0:
									itemComp.SetInvItemNum(slot, remainingCount)
									materials.pop(mat, None)
									# 能源
									addEnergy += energy * count
								else:
									itemComp.SetInvItemNum(slot, 0)
									materials[mat] = -remainingCount
									addEnergy += energy * item.get("count", 1)
							break
				slot += 1
				# 如果能源加满了，则停止
				if self.GetCurrentEnergy() + addEnergy >= self.GetMaxEnergy():
					break
			# 更新能源
			self.SetUpdateEnergy(addEnergy)
		# 同步到客户端，更新UI
		info = {
			"stage": "update_mat",
			"energy": self.GetCurrentEnergy(),
			# "maxEnergy": self.GetMaxEnergy(),
		}
		self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass

	def SetRunConsumeEnergy(self, runDistance):
		"""
		行驶消耗能源
		:param runDistance: int 行驶距离
		"""
		# 如果是飞行状态，额外消耗更多能源：加快移动距离的累积
		if self._carObj.GetFlyState():
			skillCfg = GetPartSkillConfig(PartEnum.Fly)
			energyRatio = skillCfg.get("energyRatio", 2)
			runDistance *= energyRatio
		self._runDistance += runDistance
		maxDist = self._attrConfig["energyConsumeParam"][0]
		energy = self._attrConfig["energyConsumeParam"][1]
		if self._runDistance >= maxDist:
			runDist = self._runDistance
			self._runDistance = 0.0
			# 扣能源
			self.SetUpdateEnergy(-energy)
			# 更新任务进度
			taskSys = self._carObj.GetTaskSystem()
			if taskSys:
				# 驾驶员
				playerId = self._carObj.GetRider()
				if playerId:
					taskSys.IncreaseAccumulationByFullKey(playerId, "Car.moved", int(runDist))
		pass

	def SetUpdateEnergy(self, energy):
		"""
		更新能源
		:param energy: int 更新的能源值，小于0表示扣能源
		"""
		lastEnergy = self._energy
		self._energy = max(0, self._energy + energy)
		self._energy = min(self._energy, self._maxEnergy)
		# 更新客户端UI
		rider = self._carObj.GetRider()
		if rider:
			info = {
				"stage": "energy",
				"energy": self._energy,
				"maxEnergy": self._maxEnergy,
			}
			self.SendMsgToClient(rider, eventConfig.CarCtrlEvent, info)
		# 如果耐久掉为0，则调用方法，同步更新相关逻辑
		if self._energy <= 0 and lastEnergy > 0:
			self._carObj.StopSteer()
		pass

	def GetCurrentEnergy(self):
		"""获取当前能源"""
		return self._energy

	def GetMaxEnergy(self):
		"""获取最大能源"""
		return self._maxEnergy
	# endregion

	# region 数据存储
	def LoadAttrData(self):
		"""
		读取属性
		:return: dict: {maxEnergy, energy}
		"""
		attrData = self._extraComp.GetExtraData(carConfig.ExtraDataKeyEnum.AttrData)
		if attrData is None:
			attrData = {}
		return attrData
	
	def SaveAttrData(self):
		"""存储属性"""
		attrData = {
			"maxEnergy": self._maxEnergy,
			"energy": self._energy,
		}
		self._extraComp.SetExtraData(carConfig.ExtraDataKeyEnum.AttrData, attrData)
		pass
	
	def ExportDataToEntity(self, entityId):
		"""导出属性到指定实体"""
		attrData = {
			"maxEnergy": self._maxEnergy,
			"energy": self._energy,
		}
		extraComp = compFactory.CreateExtraData(entityId)
		extraComp.SetExtraData(carConfig.ExtraDataKeyEnum.AttrData, attrData)
		# 设置最大血量为当前载具的血量（耐久）
		attrComp = compFactory.CreateAttr(entityId)
		attrComp.SetAttrMaxValue(minecraftEnum.AttrType.HEALTH, self._maxDurability)
		pass
	# endregion
