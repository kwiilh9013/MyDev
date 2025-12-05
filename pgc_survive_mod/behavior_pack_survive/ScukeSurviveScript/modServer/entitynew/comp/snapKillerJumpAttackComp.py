# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.entity.component.activeComponentBase import ActiveComponentBase
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameActionEnum
import random
import math
compFactory = serverApi.GetEngineCompFactory()
entityTypeEnum = serverApi.GetMinecraftEnum().EntityType

class SnapKillerJumpAttackComp(ActiveComponentBase):
	"""witch生成生物组件 主动"""
	def __init__(self, entityObj, config):
		super(SnapKillerJumpAttackComp, self).__init__(entityObj, config)

		config = self.mConfig
		pass

	@AddActionMapping(GameActionEnum.SnapKillerJumpAttack)
	def SnapKillerJumpAttack(self,cfg):
		"""
		空中飞行伤害组件
		"""
		flyingTime = random.uniform(0.1,cfg.get('flying_time',0.5))
		isFlying = cfg.get('start_flying',False)
		entityId = self.mEntityId
		if "set_gravity" in cfg:
			compFactory.CreateGravity(entityId).SetGravity(cfg["set_gravity"])
			return
		if isFlying:
			targetId = self.mEntityObj.GetAttackTargetId()
			if not targetId:
				return
			targetPos = engineApiGas.GetEntityPos(targetId)
			entityPos = engineApiGas.GetEntityPos(entityId)
			if not entityPos or not targetPos:
				return
			# 获取到生物身上的运动器
			entityMotionsDic= compFactory.CreateActorMotion(entityId).GetEntityMotions()
			if entityMotionsDic.has_key(0):
				compFactory.CreateActorMotion(entityId).RemoveEntityMotion(0)
			compFactory.CreatePlayer(entityId).OpenPlayerHitMobDetection()
			# targetRot = (targetPos[0]-entityPos[0],targetPos[2]-entityPos[2])
			startRot = (targetPos[0]-entityPos[0],targetPos[2]-entityPos[2])
			mid = compFactory.CreateActorMotion(entityId).AddEntityTrackMotion(self.FindPointOnExtension(entityPos,targetPos,1), flyingTime, startPos=None, relativeCoord=False, isLoop=False, targetRot = None, startRot = startRot, useVelocityDir=False, ease = serverApi.GetMinecraftEnum().TimeEaseType.linear)
			compFactory.CreateGravity(entityId).SetGravity(-0.001)
			compFactory.CreateActorMotion(entityId).StartEntityMotion(mid)
		else:
			compFactory.CreatePlayer(entityId).ClosePlayerHitMobDetection()
			compFactory.CreateGravity(entityId).SetGravity(0)
	def FindPointOnExtension(self,A, B, length):
		"""A点到B点的经过length距离后的C点坐标"""
		x1, y1, z1 = A[0],A[1],A[2]
		x2, y2, z2 = B[0],B[1],B[2]
		vectorAB = (x2 - x1, y2 - y1, z2 - z1)
		distanceAB = math.sqrt(vectorAB[0]**2 + vectorAB[1]**2 + vectorAB[2]**2)
		unitVector = (vectorAB[0] / distanceAB, vectorAB[1] / distanceAB, vectorAB[2] / distanceAB)
		c1 = x2 + unitVector[0] * length
		c2 = y2 + unitVector[1] * length
		c3 = z2 + unitVector[2] * length
		return (c1, c2, c3)
