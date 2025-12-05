# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class MonsterFlyingLava(EntityBase):
	"""飞天熔岩僵尸"""
	
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(MonsterFlyingLava, self).__init__(severHandler, entityId, engineTypeStr, param)

		self._attrComp = compFactory.CreateAttr(self.mEntityId)

		# 伤害减免的比例
		self._damageMitigateRate = None
		# 每秒回血逻辑
		self._healthRecoverTimer = None
		self._healthRecoverValue = 0

		if self.mCfg:
			self._damageMitigateRate = self.mCfg.get("damage_mitigate")
			# 每秒回血
			if self.mCfg.get("health_recover"):
				cd = self.mCfg["health_recover"].get("cd", 1)
				value = self.mCfg["health_recover"].get("value")
				if value:
					self._healthRecoverValue = value
					self._healthRecoverTimer = engineApiGas.AddRepeatTimer(cd, self.HealthRecoverTimer)

		pass

	def Destroy(self):
		if self._healthRecoverTimer:
			engineApiGas.CancelTimer(self._healthRecoverTimer)
			self._healthRecoverTimer = None
		super(MonsterFlyingLava, self).Destroy()

	# region 事件
	@EngineEvent()
	def ActuallyHurtServerEvent(self, args):
		entityId = args.get("entityId")
		if entityId == self.mEntityId and self._damageMitigateRate:
			# 如果当前是半血，则减免伤害
			health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
			maxHealth = self._attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
			if health * 2 < maxHealth:
				# 伤害减免
				args["damage_f"] = args["damage_f"] * self._damageMitigateRate
		pass
	# endregion

	# region 回血
	def HealthRecoverTimer(self):
		"""每秒回血逻辑"""
		health = self._attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
		maxHealth = self._attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
		if health < maxHealth:
			self._attrComp.SetAttrValue(minecraftEnum.AttrType.HEALTH, health + self._healthRecoverValue)
		pass
	# endregion
