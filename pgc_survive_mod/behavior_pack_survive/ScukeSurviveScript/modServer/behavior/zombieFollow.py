# -*- encoding: utf-8 -*-
import time

import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3
from ScukeSurviveScript.modCommon import modConfig

CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH


class ZombieFollow(CustomGoalCls):
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)
		self._entityFilters = {}
		self._event = ''
		self._range = 0
		self._following = None
		self._followType = 'filters'
		self._startDistance = 5.0
		self._stopDistance = 3.0
		self._speedMultiplier = 1.0
		self._scanInterval = 0.5
		args = self.GetArgs()
		if 'event' in args:
			self._event = args['event']
		if 'type' in args:
			self._followType = args['filters']
		if 'filters' in args:
			self._entityFilters = args['filters']
		if 'range' in args:
			self._range = args['range']
		if 'speed_multiplier' in args:
			self._speedMultiplier = args['speed_multiplier']
		if 'start_distance' in args:
			self._startDistance = args['start_distance']
		if 'stop_distance' in args:
			self._stopDistance = args['stop_distance']
		if 'scan_interval' in args:
			self._scanInterval = args['scan_interval']

		self._entityId = entityId
		self._levelId = serverApi.GetLevelId()
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self._eventComp = CompFactory.CreateEntityEvent(self._entityId)
		self._gameComp = CompFactory.CreateGame(self._levelId)
		self._setMoveToTime = 0

	def CanUse(self):
		if not self._IsAlive(self._entityId):
			return False
		if not self._IsAlive(self._following):
			self.ResetFollowing()
			return False

		followDis = self.GetFollowDis()
		if not followDis:
			return False
		if followDis <= self._stopDistance:
			return False
		if followDis <= self._startDistance:
			return False
		return True


	def CanContinueToUse(self):
		followDis = self.GetFollowDis()
		if not followDis:
			return False
		if followDis <= self._stopDistance:
			return False
		return self._IsAlive(self._entityId)


	def Start(self):
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self.MoveToEntity(self._following)

	def MoveToEntity(self, eid):
		cruTime = time.time()
		if cruTime - self._setMoveToTime < self._scanInterval:
			return
		comp = serverApi.GetEngineCompFactory().CreateMoveTo(self._entityId)
		followPos = CompFactory.CreatePos(eid).GetPos()
		comp.SetMoveSetting(followPos, self._speedMultiplier, 30)
		self._setMoveToTime = cruTime

	def ClearFollowing(self):
		self._following = None

	def ResetFollowing(self):
		self._following = None
		if self._followType == 'owner':
			self._following = self._GetOwner()
		elif self._followType == 'filters':
			self._following = self._GetFilterTarget()

	def GetFollowDis(self):
		if not self._following:
			return None
		pos = CompFactory.CreatePos(self._entityId).GetPos()
		followPos = CompFactory.CreatePos(self._following).GetPos()
		if not pos or not followPos:
			return None
		a1 = Vector3(pos)
		a2 = Vector3(followPos)
		return (a2 - a1).Length()


	def Stop(self):
		self.MoveToEntity(self._entityId)
		self.ClearFollowing()

	def CanBeInterrupted(self):
		return True

	def Tick(self):
		followDis = self.GetFollowDis()
		if not followDis:
			return False
		if followDis > self._startDistance:
			self.MoveToEntity(self._following)

	def _GetFilterTarget(self):
		ret = self._gameComp.GetEntitiesAround(self._entityId, self._range, self._entityFilters)
		if not ret:
			return None
		for item in ret:
			if item != self._entityId:
				return item
		return None

	def _GetOwner(self):
		comp = CompFactory.CreateActorOwner(self._entityId)
		owner = comp.GetEntityOwner()
		if owner == '-1':
			return None
		return owner

	def _IsAlive(self, id):
		if not id:
			return False
		return self._gameComp.IsEntityAlive(id)
