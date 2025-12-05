# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modServer.entity.projectile.entityProjectile import EntityProjectile
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.eventConfig import ElectromagnetismSubscribeEvent, EntityEffectEvent, EntityDataSubscribeEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.damageTagEnum import DamageTagEnum
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityEMMissile(EntityProjectile):
	"""电磁弹 实体对象"""
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(EntityEMMissile, self).__init__(severHandler, entityId, engineTypeStr, param)
		# 碰撞状态
		self._hitState = False
		# 追踪目标
		self._traceId = None
		self._traceOffset = None
		self._traceTimer = None
		self._traceCount = self.mCfg.get("traceCount", 5)

		self._posComp = compFactory.CreatePos(self.mEntityId)
		self._rotComp = None
		self._motionComp = None
		self._targetPosComp = None

		# 绑定音效
		info = {
			"stage": "sound",
			"path": self.mCfg["shoot_sound"],
			"loop": True,
			"volume": 3.0,
			"entityId": self.mEntityId,
		}
		self.mServer.SendMsgToAllClient(EntityEffectEvent, info)

		# 延迟销毁
		self._delayExplodeTimer = engineApiGas.AddTimer(self.mCfg.get("aliveTime", 5), self.DelayExplode)

		# 订阅
		Instance.mEventMgr.RegisterEvent(EntityDataSubscribeEvent, self.EntityDataSubscribeEvent)
		pass

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(EntityDataSubscribeEvent, self.EntityDataSubscribeEvent)
		super(EntityEMMissile, self).Destroy()
		pass
	
	# region 事件
	@EngineEvent()
	def ProjectileDoHitEffectEvent(self, args):
		"""抛射物碰撞事件"""
		projectileId = args["id"]
		if projectileId == self.mEntityId and not self._hitState:
			self.DoHit(args)
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体被销毁事件"""
		if args["id"] == self.mEntityId:
			self.DelayExplode()
			super(EntityEMMissile, self).Destroy()
		pass

	def EntityDataSubscribeEvent(self, args):
		"""订阅 实体数据事件"""
		if args["entityId"] == self.mEntityId:
			stage = args["stage"]
			if stage == "trace_target":
				# 追踪目标
				self.SetTraceTarget(args["target"], offset=args.get("offset"))
		pass
	# endregion

	# region 逻辑
	def SetTraceTarget(self, targetId, offset=None):
		"""设置追踪目标"""
		# 如果目标不是载具，则追踪次数改为1
		carSys = self.GetCarSys()
		if carSys:
			if not carSys.GetCarLogicObj(targetId):
				self._traceCount = int(self._traceCount * 0.7)
		
		self._traceId = targetId
		self._traceOffset = offset
		self._targetPosComp = compFactory.CreatePos(targetId)
		self._rotComp = compFactory.CreateRot(self.mEntityId)
		self._motionComp = compFactory.CreateActorMotion(self.mEntityId)
		# 启动timer
		if not self._traceTimer:
			self._traceTimer = engineApiGas.AddRepeatTimer(0.5, self.TraceTargetTimer)
		pass

	def TraceTargetTimer(self):
		"""追踪目标的tick"""
		# 有限次数的追踪，让玩家能躲避一下
		if not self._traceId or self._hitState or self._traceCount <= 0:
			self._cancelTrace()
			return
		pos = self._posComp.GetPos()
		tpos = self._targetPosComp.GetFootPos()
		if pos is None or tpos is None:
			self._cancelTrace()
			return
		offset = self._traceOffset
		tpos = (tpos[0] + offset[0], tpos[1] + offset[1], tpos[2] + offset[2])
		# 计算新的方向
		rotVector = commonApiMgr.GetVector(pos, tpos)
		rotVector = commonApiMgr.VectorNormalize(rotVector)
		# 修改朝向
		self._motionComp.SetMotion(rotVector)
		self._traceCount -= 1
		pass

	def _cancelTrace(self):
		if self._traceTimer:
			engineApiGas.CancelTimer(self._traceTimer)
			self._traceTimer = None
		pass

	def DoHit(self, args):
		"""命中逻辑"""
		self._hitState = True
		hitPos = None
		hitType = args["hitTargetType"]
		if hitType == "ENTITY":
			hitPos = (args["x"], args["y"], args["z"])
		elif hitType == "BLOCK":
			hitPos = (args["blockPosX"], args["blockPosY"], args["blockPosZ"])
		if hitPos:
			# 范围伤害
			damage = self.mCfg.get("damage", 0)
			radius = self.mCfg.get("radius", 3)
			# buff
			buffs = self.mCfg.get("buffs")
			if damage > 0:
				entityId = self.mEntityId
				entityList = serverApiMgr.GetNearbyHurtEntityList(entityId, radius)
				cause = minecraftEnum.ActorDamageCause.Custom
				playerList = serverApi.GetPlayerList()
				for entity in entityList:
					if entity == entityId:
						continue
					hurtComp = compFactory.CreateHurt(entity)
					hurtComp.Hurt(damage, cause, attackerId=self.mEntityId, customTag=DamageTagEnum.EMP)
					# 加buff（目前电磁buff仅对玩家生效，如需对其他生物生效，需加逻辑）
					if buffs and entity in playerList:
						effectComp = compFactory.CreateEffect(entity)
						for buff in buffs:
							effectComp.AddEffectToEntity(buff["name"], buff["duration"], buff.get("amplifier", 0), buff.get("showParticle", True))
			# 广播订阅，使附近的电器、载具瘫痪
			duration = self.mCfg.get("duration", 10)
			info = {
				"stage": "inhibit",
				"dimension": engineApiGas.GetEntityDimensionId(self.mEntityId),
				"pos": hitPos,
				"radius": radius,
				"duration": duration,
			}
			Instance.mEventMgr.NotifyEvent(ElectromagnetismSubscribeEvent, info)
			# 客户端播放命中特效
			info = {
				"stage": "em_effect",
				"pos": hitPos,
			}
			self.mServer.SendMsgToAllClient(EntityEffectEvent, info)

		# 取消追踪
		self._cancelTrace()
		# 取消延迟爆炸
		if self._delayExplodeTimer:
			engineApiGas.CancelTimer(self._delayExplodeTimer)
			self._delayExplodeTimer = None
		
		# 延迟销毁抛射物
		engineApiGas.AddTimer(0.1, self.mServer.DestroyEntity, self.mEntityId)
		pass

	def DelayExplode(self):
		"""延迟销毁"""
		if not self._hitState:
			pos = self._posComp.GetPos()
			if pos:
				info = {
					"hitTargetType": "ENTITY",
					"x": pos[0],
					"y": pos[1],
					"z": pos[2],
				}
				self.DoHit(info)
		pass
	# endregion

	def GetCarSys(self):
		"""获取阶段服务端系统"""
		return serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.CarServerSystem)
