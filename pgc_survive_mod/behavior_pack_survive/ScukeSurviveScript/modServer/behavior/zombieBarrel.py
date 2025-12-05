# -*- encoding: utf-8 -*-
import time

import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils

CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()

class ZombieBarrel(CustomGoalCls):
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)
		self._total = 1
		self._count = 0
		self._event = ''
		self._hit_event = ''
		self._hitEnd = False
		self._groundY = 0
		self._onAir = 0
		self._lifeTime = -1
		self._identifier = None
		self._hit_destroy = True
		args = self.GetArgs()
		if 'event' in args:
			self._event = args['event']
		if 'hit_event' in args:
			self._hit_event = args['hit_event']
		if 'speed' in args:
			self._speed = args['speed']
		if 'life_time' in args:
			self._lifeTime = args['life_time']
		if 'hit_destroy' in args:
			self._hit_destroy = args['hit_destroy']
		self._entityId = entityId
		self._levelId = serverApi.GetLevelId()
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		self._gameComp = CompFactory.CreateGame(self._levelId)
		self._blockComp = CompFactory.CreateBlockInfo(self._levelId)
		self._eventComp = CompFactory.CreateEntityEvent(self._entityId)
		self._motionComp = CompFactory.CreateActorMotion(self._entityId)
		self._posComp = CompFactory.CreatePos(self._entityId)
		CompFactory.CreateGravity(self._entityId).SetGravity((-0.08 if 'gravity' not in args else args['gravity']))
		self._dir = serverApi.GetDirFromRot(CompFactory.CreateRot(self._entityId).GetRot())
		self._spawnTime = time.time()
		self._identifier = CompFactory.CreateEngineType(self._entityId).GetEngineTypeStr()


	def CanUse(self):
		return self._IsAlive() and self._count < self._total and not self._hitEnd

	def CanContinueToUse(self):
		return self._IsAlive()

	def Start(self):
		self._dir = serverApi.GetDirFromRot(CompFactory.CreateRot(self._entityId).GetRot())
		self._dimensionId = CompFactory.CreateDimension(self._entityId).GetEntityDimensionId()
		if self._count < self._total:
			self._count += 1
			self._eventComp.TriggerCustomEvent(self._entityId, self._event)

	def Stop(self):
		pass

	def CanBeInterrupted(self):
		return self._hitEnd

	def Tick(self):
		if self._hitEnd:
			return
		# 存活时间
		if self._lifeTime > 0:
			if time.time() - self._spawnTime >= self._lifeTime:
				self._gameComp.KillEntity(self._entityId)
				return

		dir = self._dir
		power = self._speed
		footPos = self._posComp.GetFootPos()
		groundPos = self._IsOnGround(dir)
		if groundPos or (self._onAir > 1 and self._groundY == footPos[1]):
			self._motionComp.SetMotion(MathUtils.TupleMul(dir, power))
			self._onAir = 0
		else:
			self._onAir += 1
		self._groundY = footPos[1]
		hitSomething = self._IsHited(dir)
		if hitSomething:
			self.OnHit(hitSomething)

	def OnHit(self, blockInfo):
		self._eventComp.TriggerCustomEvent(self._entityId, self._hit_event)
		self._hitEnd = True
		if self._hit_destroy:
			self._gameComp.KillEntity(self._entityId)

	def _IsOnGround(self, dir):
		footPos = self._posComp.GetFootPos()
		pos = (footPos[0], footPos[1] + 0.5, footPos[2])
		pos = MathUtils.TupleAddMul(pos, dir, -self._speed)
		blockDictList = serverApi.getEntitiesOrBlockFromRay(
			self._dimensionId, pos, (0, -1, 0), 1, False,
			serverApi.GetMinecraftEnum().RayFilterType.OnlyBlocks
		)
		ret = blockDictList and len(blockDictList) > 0 and (blockDictList[0]['pos'][1] + 1) - footPos[1] == 0
		if ret:
			return blockDictList[0]['pos']
		return None

	def _IsHited(self, dir):
		footPos = self._posComp.GetFootPos()
		pos = (footPos[0], footPos[1] + 0.5, footPos[2])
		blockDictList = serverApi.getEntitiesOrBlockFromRay(
			self._dimensionId, pos, dir, 1, True,
			serverApi.GetMinecraftEnum().RayFilterType.BothEntitiesAndBlock
		)
		if blockDictList and len(blockDictList) > 0:
			for item in blockDictList:
				if 'entityId' in item:
					if item['entityId'] == self._entityId or item['identifier'] == self._identifier:
						continue
				return item
		return None

	def _GetTargetPos(self):
		comp = CompFactory.CreateAction(self._entityId)
		targetId = comp.GetAttackTarget()
		if targetId == '-1':
			return None
		pos = CompFactory.CreatePos(targetId).GetPos()
		return pos

	def _IsAlive(self):
		return self._gameComp.IsEntityAlive(self._entityId)
