# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi

CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH

class ZombieLowHealth(CustomGoalCls):
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)
		self._lowHealth = 0
		self._event = ''
		args = self.GetArgs()
		if 'event' in args:
			self._event = args['event']
		if 'value' in args:
			self._lowHealth = args['value']
		self._entityId = entityId
		self._levelId = serverApi.GetLevelId()
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self._attrComp = CompFactory.CreateAttr(self._entityId)
		self._gameComp = CompFactory.CreateGame(self._levelId)
		self._eventComp = CompFactory.CreateEntityEvent(self._entityId)
		self._health = self._attrComp.GetAttrValue(HealthEnum)


	def CanUse(self):
		if self._IsAlive() and self._HealthChanged():
			cur = self._attrComp.GetAttrValue(HealthEnum)
			ret = cur <= self._lowHealth < self._health
			if not ret:
				self._health = cur
			return ret
		return False

	def CanContinueToUse(self):
		return self.CanUse()

	def Start(self):
		cur = self._attrComp.GetAttrValue(HealthEnum)
		if cur < self._health:
			self._health = cur
			self._eventComp.TriggerCustomEvent(self._entityId, self._event)
			print self._event

	def Stop(self):
		pass

	def CanBeInterrupted(self):
		return True

	def Tick(self):
		pass

	def _HasTarget(self):
		comp = serverApi.GetEngineCompFactory().CreateAction(self._entityId)
		targetId = comp.GetAttackTarget()
		hasTarget = targetId != "-1"
		return hasTarget

	def _IsAlive(self):
		return self._gameComp.IsEntityAlive(self._entityId)

	def _HealthChanged(self):
		cur = self._attrComp.GetAttrValue(HealthEnum)
		return cur != self._health
