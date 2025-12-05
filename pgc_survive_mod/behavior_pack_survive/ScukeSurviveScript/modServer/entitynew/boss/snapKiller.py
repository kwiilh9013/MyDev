# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modServer.entitynew.gameEntityBase import GameEntityBase
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameCompEnum
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent

import random
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()

class EntitySnapKiller(GameEntityBase):
	"""boss 瞬杀者"""
	def __init__(self, server, entityId, engineTypeStr):
		super(EntitySnapKiller, self).__init__(server, entityId, engineTypeStr)

		# 上一个组件的类型
		self._lastCompType = None

		config = self.mConfig
		# 近战攻击距离
		self._attackDist = config["attack_dist"] ** 2
		self._teleportStartDist = config["teleport_start_dist"] ** 2
		self._teleportEndDist = config["teleport_end_dist"] ** 2
		self._jumpCd = config['jump_cd']
		self._jumpHeight = config['jump_height']
		self._jumpHitDamge = config.get('jump_hit_damge',5)
		self._canJump = False
		self._time = 0
		pass

	# region 事件
	@EngineEvent()
	def OnMobHitMobServerEvent(self,args):
		"""跳跃攻击时对发生碰撞的敌对生物造成伤害"""
		if self.mEntityId == args['mobId']:
			entityId = self.mEntityId
			hittedMobList = args['hittedMobList']
			for hitEntityId in hittedMobList:
				if self.IsCanHit(hitEntityId):
					cause = minecraftEnum.ActorDamageCause.EntityAttack
					engineApiGas.Hurt(hitEntityId, entityId, self._jumpHitDamge, cause, customTag=None)
	@EngineEvent()
	def ActuallyHurtServerEvent(self,args):
		"""免疫所有衰落伤害"""
		if args['entityId'] == self.mEntityId and args['cause'] == minecraftEnum.ActorDamageCause.Fall:
			args['damage'] = 0
	# endregion
	
	def GetNextComponent(self):
		# 距离近就近战，距离远就瞬移
		targetId = self.GetAttackTargetId()
		entityId = self.mEntityId
		if not targetId:
			compType = GameCompEnum.SnapKillerCancelJumpReady
			if self._lastCompType == compType:
				return
			else:
				self._lastCompType = compType
				return self.GetComponent(compType)
		else:
			targetPosY = engineApiGas.GetEntityPos(targetId)[1]
			entityPosY = engineApiGas.GetEntityPos(entityId)[1]
			# 可以跳跃时优先跳跃攻击，进行跳跃攻击Y轴距离检测
			if self._canJump and self._jumpHeight[0]<=targetPosY-entityPosY<=self._jumpHeight[1]:
				if self._lastCompType and self._lastCompType in (GameCompEnum.SnapKillerJumpReady):
					compType = GameCompEnum.SnapKillerJumpFly
					self._canJump = False
				else:
					compType = GameCompEnum.SnapKillerJumpReady
				self._lastCompType = compType
				return self.GetComponent(compType)
			dist = self.GetTargetDistanceXZ(targetId)
			if dist <= self._attackDist:
				# 随机两种攻击模式
				if random.randint(0,1) == 0:
					compType = GameCompEnum.SnapKillerMeleeAttack1
				else:
					compType = GameCompEnum.SnapKillerMeleeAttack2
				self._lastCompType = compType
				return self.GetComponent(compType)
			elif dist > self._teleportStartDist:
				compType = GameCompEnum.Teleport
				self._lastCompType = compType
				return self.GetComponent(compType)
			elif dist > self._teleportEndDist and self._lastCompType == GameCompEnum.Teleport:
				# 连续瞬移
				compType = GameCompEnum.Teleport
				self._lastCompType = compType
				return self.GetComponent(compType)
	def IsCanHit(self, targetId):
		"""重写是否可以造成伤害"""
		# 判断是否为同类生物，是则范围攻击不会造成伤害
		if self.mEntityId == targetId or compFactory.CreateEngineType(targetId).GetEngineType()==compFactory.CreateEngineType(self.mEntityId).GetEngineType():
			return False
		return True
	
	def Update(self):
		if self._jumpCd != 0:
			if not self._canJump:
				self._time+=1
			if self._time == self._jumpCd:
				self._canJump =True
				self._time = 0
		else:
			self._jumpCd =True
		return super(EntitySnapKiller,self).Update()
	
 