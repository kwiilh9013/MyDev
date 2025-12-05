# -*- encoding: utf-8 -*-
import random

import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.modCommon import modConfig

CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH


class ZombieTame(CustomGoalCls):
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)
		self._entityFilters = {}
		self._event = ''
		self._range = 0
		self._owner = None
		args = self.GetArgs()
		if 'event' in args:
			self._event = args['event']
		if 'filters' in args:
			self._entityFilters = args['filters']
		if 'range' in args:
			self._range = args['range']

		self._entityId = entityId
		self._levelId = serverApi.GetLevelId()
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self._eventComp = CompFactory.CreateEntityEvent(self._entityId)
		self._gameComp = CompFactory.CreateGame(self._levelId)
		self._actorOwnerComp = CompFactory.CreateActorOwner(self._entityId)

	def CanUse(self):
		return self._IsAlive(self._entityId) and not self._IsAlive(self._owner)

	def CanContinueToUse(self):
		return self.CanUse()

	def Start(self):
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()

	def Stop(self):
		pass

	def CanBeInterrupted(self):
		return True

	def Tick(self):
		if not self._HasOwner() or not self._IsAlive(self._owner):
			self._owner = None
			owner = self._GetRandomOwner()
			if owner:
				self._SetOwner(owner)
				self._eventComp.TriggerCustomEvent(self._entityId, self._event)

	def _GetRandomOwner(self):
		ret = self._gameComp.GetEntitiesAround(self._entityId, self._range, self._entityFilters)
		if not ret:
			return None
		for item in ret:
			if item != self._entityId:
				return item
		return None

	def _SetOwner(self, owner):
		self._owner = owner
		comp = CompFactory.CreateActorOwner(self._entityId)
		comp.SetEntityOwner(owner)

	def _HasOwner(self):
		comp = CompFactory.CreateActorOwner(self._entityId)
		owner = comp.GetEntityOwner()
		return owner != '-1'

	def _IsAlive(self, id):
		if not id:
			return False
		return self._gameComp.IsEntityAlive(id)
