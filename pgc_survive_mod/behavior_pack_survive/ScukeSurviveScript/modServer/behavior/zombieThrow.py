# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.modCommon import modConfig
import time

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3

CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH

class ZombieThrow(CustomGoalCls):
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)
		self._item = None
		self._total = -1
		self._count = 0
		self._event = ''
		self._throwOffset = (0, 0, 0)
		self._projectile = False
		self._interval = 1
		args = self.GetArgs()
		if 'event' in args:
			self._event = args['event']
		if 'count' in args:
			self._total = args['count']
		if 'projectile' in args:
			self._projectile = args['projectile']
		if 'throw_item' in args:
			self._item = args['throw_item']
		if 'interval' in args:
			self._interval = args['interval']
		if 'throw_offset' in args:
			offset = args['throw_offset']
			self._throwOffset = (offset['x'], offset['y'], offset['z'])
		self._entityId = entityId
		self._levelId = serverApi.GetLevelId()
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self._eventComp = CompFactory.CreateEntityEvent(self._entityId)
		self._gameComp = CompFactory.CreateGame(self._levelId)
		self._castTime = -1


	def CanUse(self):
		return self._IsAlive() and self._CountValid() and self._GetTargetPos()

	def CanContinueToUse(self):
		return self.CanUse()

	def _CountValid(self):
		if self._total < 0:
			return True
		return self._count < self._total

	def Start(self):
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self._castTime = time.time()

	def Stop(self):
		self._castTime = -1

	def CanBeInterrupted(self):
		return self._castTime <= 0

	def Tick(self):
		curTime = time.time()
		if curTime - self._castTime > self._interval:
			self._Cast()
			self._castTime = curTime

	def _Cast(self):
		if self._CountValid():
			if self._item:
				pos = self._GetTargetPos()
				if pos:
					curPos = CompFactory.CreatePos(self._entityId).GetPos()
					rotDir = MathUtils.TupleSub(pos, curPos)
					rotDir = (rotDir[0], 0, rotDir[2])
					throwPos = MathUtils.TupleAdd(curPos, self._Rot(self._throwOffset, rotDir))
					dir = MathUtils.TupleSub(pos, throwPos)
					self._Throw(throwPos, dir)

			self._count += 1
			self._eventComp.TriggerCustomEvent(self._entityId, self._event)

	def _GetTargetPos(self):
		comp = CompFactory.CreateAction(self._entityId)
		targetId = comp.GetAttackTarget()
		if targetId == '-1':
			return None
		pos = CompFactory.CreatePos(targetId).GetPos()
		return pos

	def _IsAlive(self):
		return self._gameComp.IsEntityAlive(self._entityId)

	def _Rot(self, v, rotDir):
		dir = Vector3(rotDir)
		dir.Normalize()
		_v = Vector3(v)
		rot = MathUtils.LookDirection(dir)
		return (rot * _v).ToTuple()

	def _Throw(self, throwPos, dir):
		if self._projectile:
			projectile = CompFactory.CreateProjectile(self._levelId)
			projectile.CreateProjectileEntity(self._entityId, self._item, {
				'position': throwPos,
				'direction': dir,
			})
		else:
			serverSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.ServerSystem)
			if serverSystem:
				serverSystem.CreateEngineEntityByTypeStr(self._item, throwPos, serverApi.GetRotFromDir(dir),
														   self._dimensionId)
