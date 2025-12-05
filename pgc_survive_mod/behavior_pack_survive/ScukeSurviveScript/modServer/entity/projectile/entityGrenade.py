# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modServer.entity.projectile.entityProjectile import EntityProjectile
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityGrenade(EntityProjectile):
	"""手雷 实体对象"""
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(EntityGrenade, self).__init__(severHandler, entityId, engineTypeStr, param)
		
		# 创建者id，必须是玩家id
		self._ownerId = None
		# 爆炸位置
		self._explodePos = None

		# 伤害值、伤害范围
		self._damage = self.mCfg.get("damage")
		if self._damage:
			self._damage = int(self._damage)
		self._radius = self.mCfg.get("damage_radius")
		if self._radius:
			self._radius = self._radius ** 2

		self._posComp = compFactory.CreatePos(self.mEntityId)

		# 延迟爆炸
		delayExplodeCD = self.mCfg.get("delay_explode")
		if delayExplodeCD:
			self._delayExplodeTimer = engineApiGas.AddTimer(delayExplodeCD, self.DelayExplodeTimer)
		pass

	def Destroy(self):
		if self._delayExplodeTimer:
			engineApiGas.CancelTimer(self._delayExplodeTimer)
		# 延迟清除对象（damageEvent会持续触发一会，如果提早Destroy，会导致部分伤害值没法修改）
		engineApiGas.AddTimer(0.05, super(EntityGrenade, self).Destroy)
		pass
	
	# region 事件
	@EngineEvent()
	def ProjectileDoHitEffectEvent(self, args):
		"""抛射物碰撞事件"""
		projectileId = args.get("id")
		if projectileId == self.mEntityId:
			# 获取发射者id
			self._ownerId = args.get("srcId")
			# 弹射
			pass
		pass

	@EngineEvent()
	def DamageEvent(self, args):
		"""受到伤害事件"""
		srcId = args.get("srcId")
		entityId = args.get("entityId")
		cause = args.get("cause")
		if cause == minecraftEnum.ActorDamageCause.EntityExplosion:
			if srcId == self._ownerId and entityId != self.mEntityId:
				# 如果是手雷的爆炸伤害，则把伤害值改掉
				if self._damage:
					# 计算距离，如果在距离内，才造成伤害
					targetPos = engineApiGas.GetEntityPos(entityId)
					dist = commonApiMgr.GetDistanceSqrt(self._explodePos, targetPos)
					if dist <= self._radius:
						args["damage"] = self._damage
					else:
						# 超过范围的，免疫伤害
						args["damage"] = 0
		pass
	# endregion

	# region 爆炸
	def DelayExplodeTimer(self):
		"""延迟爆炸"""
		self._delayExplodeTimer = None
		# 如果传递的不是玩家id，则随机选一个玩家id
		if not self._ownerId:
			playerList = serverApi.GetPlayerList()
			if len(playerList) > 0 and self._ownerId not in playerList:
				self._ownerId = playerList[0]
		pos = self._posComp.GetFootPos()
		# 记录爆炸位置
		self._explodePos = pos
		# 执行爆炸逻辑
		radius = self.mCfg.get("explode_radius")
		fire = self.mCfg.get("fire", True)
		breaks = self.mCfg.get("breaks", True)
		serverApiMgr.CreateExplosion(self.mEntityId, self._ownerId, pos, radius, fire, breaks)
		# 销毁自身，此时有可能因爆炸而先执行销毁逻辑
		if self.mServer:
			self.mServer.DestroyEntity(self.mEntityId)
		pass
	# endregion
