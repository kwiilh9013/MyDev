# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.entity.component.passiveComponentBase import PassiveComponentBase
minecraftEnum = serverApi.GetMinecraftEnum()


ExtraDataKey = "adaptive_immune_damage_data"


class AdaptiveImmuneDamageComp(PassiveComponentBase):
	"""适应性免疫伤害 组件 被动"""
	def __init__(self, entityObj, config):
		super(AdaptiveImmuneDamageComp, self).__init__(entityObj, config)

		config = self.mConfig
		# 触发的伤害类型
		self._damageType = config["damage_type"]
		# 总血量
		maxHealth = engineApiGas.GetAttrMaxValue(self.mEntityId, minecraftEnum.AttrType.HEALTH) + 0.0
		# 适应条件
		# 总伤害比例
		totalDamageRatio = config["damage_ratio_condition"]
		# 触发的总伤害值
		self._triggerMaxDamage = maxHealth * totalDamageRatio
		# 记录已受到该类伤害的总值
		self._curDamage = self.LoadTotalDamage()
		# 检查一遍是否已触发
		if self.IsCanTrigger():
			self.OnTrigger()
		pass
	
	@EngineEvent()
	def ActuallyHurtServerEvent(self, args):
		"""实体受到伤害事件"""
		if args["entityId"] != self.mEntityId:
			return
		# 如果是指定伤害类型
		if args["cause"] in self._damageType or args["customTag"] in self._damageType:
			# 判定是否能触发被动
			if self.IsCanTrigger():
				# 免疫伤害
				args["damage"] = 0
				self.OnTrigger()
			else:
				# 累计伤害
				self._curDamage += args["damage"]
		pass

	def IsCanTrigger(self):
		if self._curDamage >= self._triggerMaxDamage:
			return True
		return False
	
	def OnTrigger(self):
		if self.mIsTrigger:
			return
		self.mIsTrigger = True
		# 执行触发后的逻辑
		# 设置molang，播放动画特效
		config = self.mConfig
		if "molang" in config:
			self.SetMolang(config)
		# 保存值
		self.SaveTotalDamage()
		pass

	def LoadTotalDamage(self):
		"""获取已受到的总伤害值"""
		value = engineApiGas.GetExtraData(self.mEntityId, ExtraDataKey)
		if value is None:
			value = 0
		return value

	def SaveTotalDamage(self):
		"""存储已受到的总伤害值"""
		return engineApiGas.SetExtraData(self.mEntityId, ExtraDataKey, self._curDamage)
