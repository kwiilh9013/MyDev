# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.server.entity.component.passiveComponentBase import PassiveComponentBase
compFactory = serverApi.GetEngineCompFactory()
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH


class AvoidMobComp(PassiveComponentBase):
	"""躲避怪物 组件 被动"""
	def __init__(self, entityObj, config):
		super(AvoidMobComp, self).__init__(entityObj, config)

		config = self.mConfig
		# 总血量
		self._attrComp = compFactory.CreateAttr(self.mEntityId)
		maxHealth = self._attrComp.GetAttrMaxValue(HealthEnum)
		# 触发的血量
		ratio = config["avoid_ratio"]
		self._triggerHealth = maxHealth * ratio
		# 检查一遍是否已触发
		if self.IsCanTrigger():
			self.OnTrigger()
		pass
	
	@EngineEvent()
	def HealthChangeServerEvent(self, args):
		"""生命值改变事件"""
		if args["entityId"] != self.mEntityId:
			return
		health = args["to"]
		if health > 0:
			# 判定是否能触发被动
			if self.IsCanTrigger(health):
				self.OnTrigger()
			else:
				# 取消被动
				self.OnCancelTrigger()
		pass

	def IsCanTrigger(self, health=None):
		if health is None:
			health = self._attrComp.GetAttrValue(HealthEnum)
		if health <= self._triggerHealth:
			return True
		return False
	
	def OnTrigger(self):
		if self.mIsTrigger:
			return
		self.mIsTrigger = True
		# 执行触发后的逻辑
		for actionCfg in self.mConfig["trigger"]:
			func = self.GetActionFunction(actionCfg["type"])
			func(actionCfg)
		pass

	def OnCancelTrigger(self):
		if not self.mIsTrigger:
			return
		self.mIsTrigger = False
		# 执行取消触发后的逻辑
		for actionCfg in self.mConfig["trigger_cancel"]:
			func = self.GetActionFunction(actionCfg["type"])
			func(actionCfg)
		pass
