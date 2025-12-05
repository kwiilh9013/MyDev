# -*- coding: UTF-8 -*-
import random
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modServer.entitynew.gameEntityBase import GameEntityBase
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.cfg.gunConfig import GunIdentifierPrefix
from ScukeSurviveScript.modCommon.cfg.meleeConfig import MeleeIdentifierPrefix
from ScukeSurviveScript.modCommon.cfg.meleeConfig import MeleeIdentifierPrefix
from ScukeSurviveScript.modCommon.modConfig import ModNameSpace, ServerSystemEnum
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameCompEnum
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
compFactory = serverApi.GetEngineCompFactory()
ItemPosType = serverApi.GetMinecraftEnum().ItemPosType
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH


EventNames = {
	True: "scuke_survive:set_ranged_attack_event",
	False: "scuke_survive:set_melee_attack_event",
}


class EntityRebelSoldier(GameEntityBase):
	"""反叛军 士兵"""
	def __init__(self, server, entityId, engineTypeStr):

		# 这些数据在组件中会用到
		# 当前武器
		self.mCurItem = None
		# 当前攻击模式：True=远程，False=近战
		self.mIsRangedAttack = False
		self.mGunSystem = serverApi.GetSystem(ModNameSpace, ServerSystemEnum.GunServerSystem)
		self.mMeleeSystem = serverApi.GetSystem(ModNameSpace, ServerSystemEnum.MeleeServerSystem)

		super(EntityRebelSoldier, self).__init__(server, entityId, engineTypeStr)

		# 轮询加快
		self.mCheckCompCD = 30

		cfg = self.mConfig
		# 近战攻击距离
		self._attackDist = cfg["attack_dist"] ** 2
		self._shootDist = cfg["shoot_dist"] ** 2
		# 低生命回血的参数
		recoverRatio = cfg["recover_ratio"]
		# 回血的频率
		self._recoverCD = cfg["recover_cd"]
		self._recoverTick = 0

		self._gameComp = compFactory.CreateGame(entityId)
		self._attrComp = compFactory.CreateAttr(entityId)
		self._maxHealth = self._attrComp.GetAttrMaxValue(HealthEnum)
		self._lowHealth = self._maxHealth * recoverRatio

		# 获取一次主手物品
		item = engineApiGas.GetEntityItem(entityId, ItemPosType.CARRIED, 0)
		if not item:
			# 初始化手持物品
			if "item_pool" in cfg:
				itemPool = cfg["item_pool"]
				poolWeight = cfg.get("item_pool_weight")
				if not poolWeight:
					poolWeight = commonApiMgr.GetTotalWeight(itemPool)
					cfg["item_pool_weight"] = poolWeight
				itemCfg = commonApiMgr.GetValueFromWeightPool(itemPool, poolWeight)
				engineApiGas.SetEntityItem(entityId, ItemPosType.CARRIED, {"newItemName": itemCfg["itemName"], "newAuxValue": 0, "count": 1}, 0)
				
			# 判断是否穿盔甲的概率
			hasArmor = True
			if "has_armor_prob" in cfg:
				hasArmor = False
				if random.random() < cfg["has_armor_prob"]:
					hasArmor = True
			if hasArmor:
				# 初始化盔甲
				if "armor_pool" in cfg:
					# 多套盔甲之间随机
					self.SetPutOnArmor(cfg, "armor_pool")
				else:
					# 每个部位单独随机
					if "head_armor_pool" in cfg:
						self.SetPutOnArmor(cfg, "head_armor_pool", 0)
					if "chest_armor_pool" in cfg:
						self.SetPutOnArmor(cfg, "chest_armor_pool", 1)
					if "leg_armor_pool" in cfg:
						self.SetPutOnArmor(cfg, "leg_armor_pool", 1)
					if "boot_armor_pool" in cfg:
						self.SetPutOnArmor(cfg, "boot_armor_pool", 1)
		
		# 延迟获取手持物品
		engineApiGas.AddTimer(1, self.DelayInitCarriedItemModel)
		
		# 显示降落伞
		self._onGroundTimer = None
		self._dim = engineApiGas.GetEntityDimensionId(self.mEntityId)

		self.TryShowParachute()
		pass

	def SetPutOnArmor(self, cfg, armorPoolKey, slot=None):
		armorPool = cfg[armorPoolKey]
		poolWeightKey = armorPoolKey + "_weight"
		poolWeight = cfg.get(poolWeightKey)
		if not poolWeight:
			poolWeight = commonApiMgr.GetTotalWeight(armorPool)
			cfg[poolWeightKey] = poolWeight
		armorCfg = commonApiMgr.GetValueFromWeightPool(armorPool, poolWeight)
		if slot is None:
			slot = 0
			for armorName in armorCfg["armors"]:
				engineApiGas.SetEntityItem(self.mEntityId, ItemPosType.ARMOR, {"newItemName": armorName, "newAuxValue": 0, "count": 1}, slot)
				slot += 1
		elif "itemName" in armorCfg:
			engineApiGas.SetEntityItem(self.mEntityId, ItemPosType.ARMOR, {"newItemName": armorCfg["itemName"], "newAuxValue": 0, "count": 1}, slot)
		pass

	def Destroy(self):
		self.mGunSystem = None
		self.mMeleeSystem = None
		super(EntityRebelSoldier, self).Destroy()

	# region 事件
	def DelayInitCarriedItemModel(self):
		"""延迟初始化主手物品模型"""
		entityId = self.mEntityId
		item = engineApiGas.GetEntityItem(entityId, ItemPosType.CARRIED, 0)
		if item:
			self.EntityPickupItemServerEvent({"entityId": entityId, "itemDict": item})
		pass

	@EngineEvent()
	def EntityPickupItemServerEvent(self, args):
		"""实体拾取物品事件"""
		if args["entityId"] != self.mEntityId:
			return
		item = args["itemDict"]
		if not item:
			return
		itemName = item["newItemName"]
		if itemName == self.mCurItem:
			return
		entityId = self.mEntityId
		# 卸下武器
		if self.mCurItem:
			if self.mCurItem.startswith(GunIdentifierPrefix):
				self.mGunSystem.Remove(entityId)
			elif self.mCurItem.startswith(MeleeIdentifierPrefix):
				self.mMeleeSystem.Remove(entityId)
		
		if itemName.startswith(GunIdentifierPrefix):
			# 枪械
			self.mGunSystem.EntityTake(entityId, item)
			# 切换为远程攻击
			self.ChangeRangedAttackModel(True)
		elif itemName.startswith(MeleeIdentifierPrefix):
			# 近战武器
			self.mMeleeSystem.EntityTake(entityId, item)
			self.ChangeRangedAttackModel(False)
		self.mCurItem = itemName
		pass
	# endregion
	
	def GetNextComponent(self):
		# 根据当前手持的武器，执行不同的逻辑
		targetId = self.GetAttackTargetId()
		if not targetId:
			# 回满血
			return self.RecoverHealth(False)
		
		dist = self.GetTargetDistanceXZ(targetId)
		if dist <= self._attackDist:
			# 近战
			return self.GetComponent(GameCompEnum.MeleeAttack1)
		elif dist <= self._shootDist:
			if self.mIsRangedAttack:
				# 射击
				# 判断是否可看见目标
				entityId = self.mEntityId
				canSee = self._gameComp.CanSee(entityId, targetId, 24.0, True, 90.0, 60.0)
				if canSee:
					return self.GetComponent(GameCompEnum.Shoot1)
				
		# 非攻击时间
		# 尝试治疗
		return self.RecoverHealth()

	def ChangeRangedAttackModel(self, isRangedAttack):
		"""切换远程、近战模式"""
		self.mIsRangedAttack = isRangedAttack
		engineApiGas.TriggerCustomEvent(self.mEntityId, EventNames[isRangedAttack])
		pass

	def RecoverHealth(self, hasTarget=True):
		"""回血"""
		if self.mTick - self._recoverTick < self._recoverCD:
			return
		if hasTarget:
			lowHealth = self._lowHealth
		else:
			lowHealth = self._maxHealth
		if self._attrComp.GetAttrValue(HealthEnum) < lowHealth:
			self._recoverTick = self.mTick
			return self.GetComponent(GameCompEnum.HealthRecover)
		return None

	def TryShowParachute(self):
		"""尝试显示降落伞"""
		state = engineApiGas.GetExtraData(self.mEntityId, "isShowParachut")
		if not state:
			engineApiGas.SetExtraData(self.mEntityId, "isShowParachut", True)
			# 判断当前是否着地
			if not self.IsOnGround():
				# 缓降buff
				engineApiGas.AddEffectToEntity(self.mEntityId, "slow_falling", 10, 0, False)
				# 设置molang
				comp = self.GetComponent(GameCompEnum.ShowParachute)
				comp.Start()
				# 开启着地检测
				self._onGroundTimer = engineApiGas.AddRepeatTimer(0.5, self.OnGroundTimer)
		pass

	def OnGroundTimer(self):
		if self.IsOnGround():
			# 设置molang
			comp = self.GetComponent(GameCompEnum.HideParachute)
			comp.Start()
			engineApiGas.CancelTimer(self._onGroundTimer)
			self._onGroundTimer = None
		pass

	def IsOnGround(self):
		pos = engineApiGas.GetEntityPos(self.mEntityId)
		block = engineApiGas.GetBlock(commonApiMgr.GetBlockPosByEntityPos((pos[0], pos[1] - 0.5, pos[2])), self._dim)
		if block and block["name"] != "minecraft:air":
			return True
		return False


