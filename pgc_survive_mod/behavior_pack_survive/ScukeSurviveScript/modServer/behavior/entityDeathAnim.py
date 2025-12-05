# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas
CustomGoalCls = serverApi.GetCustomGoalCls()
compFactory = serverApi.GetEngineCompFactory()
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH


class EntityDeathAnim(CustomGoalCls):
	"""播放生物死亡动画"""
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)
		args = self.GetArgs()
		# 触发的事件
		self._event = args.get("event")
		# 动画时长
		self._animTime = args.get("anim_time", 1)
		# 死亡特效
		self._hasDeathEffect = args.get("has_death_effect", True)
		self._deathEffect = args.get("death_effect", "minecraft:egg_destroy_emitter")

		self._entityId = entityId
		self._levelId = serverApi.GetLevelId()

		self._deathTimer = None

		self._attrComp = compFactory.CreateAttr(self._entityId)
		self._hurtComp = compFactory.CreateHurt(self._entityId)
		self._eventComp = compFactory.CreateEntityEvent(self._entityId)
		
		# 记录仇恨目标
		self._targetId = engineApiGas.GetAttackTarget(self._entityId)
		pass

	def CanUse(self):
		return True
	
	def CanContinueToUse(self):
		return self.CanUse()

	def _CountValid(self):
		if self._total < 0:
			return True
		return self._count < self._total

	def Start(self):
		# 血量改为1点
		self._attrComp.SetAttrValue(HealthEnum, 1)
		# 触发event
		if self._event:
			self._eventComp.TriggerCustomEvent(self._entityId, self._event)
		# 开启timer
		self._deathTimer = engineApiGas.AddTimer(self._animTime, self.DeathTimer)
		pass

	def Stop(self):
		if self._deathTimer:
			engineApiGas.CancelTimer(self._deathTimer)
			self._deathTimer = None
		pass

	def CanBeInterrupted(self):
		return False

	def Tick(self):
		pass

	def DeathTimer(self):
		# 对自己设置伤害值
		if self._targetId:
			self._hurtComp.Hurt(2, cause=serverApi.GetMinecraftEnum().ActorDamageCause.Override, attackerId=self._targetId)
		else:
			self._attrComp.SetAttrValue(HealthEnum, 0)
		# 播放死亡特效
		if self._hasDeathEffect:
			pos = engineApiGas.GetEntityPos(self._entityId)
			if pos:
				cmd = "/particle {} {} {} {}".format(self._deathEffect, pos[0], pos[1], pos[2])
				cmdComp = compFactory.CreateCommand(self._levelId)
				cmdComp.SetCommand(cmd)
		# 延迟删除实体
		serverSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.ServerSystem)
		if serverSys:
			engineApiGas.AddTimer(0.01, serverSys.DestroyEntity, self._entityId)
		self._deathTimer = None
		pass
