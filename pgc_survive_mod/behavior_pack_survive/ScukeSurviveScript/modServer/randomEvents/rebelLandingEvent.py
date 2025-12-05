# -*- encoding: utf-8 -*-
import random
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.randomEvents.randomEventBase import RandomEventBase
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modCommon.eventConfig import EntityDataSubscribeEvent
from ScukeSurviveScript.modCommon.cfg.randomEvent import rebelLandingConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.defines.damageTagEnum import DamageTagEnum
compFactory = serverApi.GetEngineCompFactory()


class RebelLandingEvent(RandomEventBase):
	"""反叛降临 事件"""
	
	def __init__(self, system, eventType, targetId):
		super(RebelLandingEvent, self).__init__(system, eventType, targetId)
		# 命中状态
		self._isProjectileHit = False
		# 抛射物数据
		self._projectileList = []
		self._spawnProjectileDict = None
		self._projectileId = None

		# 导弹发射、怪物生成 的相对位置的角度
		self._spawnAngle = None
		self._targetHeight = 1

		# 刷怪的数据
		self._spanwMobDict = None
		# 怪物池
		self._mobPool = None

		# 怪物生成的rot，固定值
		self._spanwRot = (0, 0)
		# 事件结束时间（以防抛射物一直没有触发碰撞）
		self._eventEndTick = self.GetTickTime(rebelLandingConfig.EventStartTimeLimit)
		pass

	# region 生命周期、事件
	def Start(self):
		super(RebelLandingEvent, self).Start()
		if self.mTargetId:
			# 获取刷怪池
			day = self.mSystem.GetCurrentDay()
			self._mobPool = rebelLandingConfig.GetSpawnMobPool(day)
			if self._mobPool:
				# 计算目标高度
				size = engineApiGas.GetEntitySize(self.mTargetId)
				if size:
					self._targetHeight = size[1] * 0.5
				
				# 启动timer，负责持续生成抛射物
				self._spawnProjectileDict = {
					"count": self._mobPool["empCount"],
					"cd": self.GetTickTime(self._mobPool["empCD"]),
				}
		pass

	@EngineEvent()
	def ActuallyHurtServerEvent(self, args):
		"""实体受伤事件"""
		# 根据是否受到电磁伤害，来判断是否被电磁弹命中
		if self._isProjectileHit:
			return
		customTag = args.get("customTag")
		# 仅处理电磁伤害
		if customTag == DamageTagEnum.EMP:
			if args["srcId"] in self._projectileList:
				self.SetHitTarget()
		pass
	
	def Update(self):
		super(RebelLandingEvent, self).Update()
		# 生成抛射物
		self.SpawnProjectile()

		# 如果没有命中，则不执行逻辑
		if self._isProjectileHit is False:
			# 如果长时间没有命中，则事件触发失败
			if self.mSystem and self.mTick >= self._eventEndTick:
				for pid in self._projectileList:
					self.mSystem.DestroyEntity(pid)
				self.End()
			return
		
		# 结束判断
		if self._isProjectileHit and self._spanwMobDict is None:
			self.End()
			return
		
		# 刷怪
		val = self._spanwMobDict
		if val and self._mobPool:
			if self.GetUpdateTime(val["tick"]) >= rebelLandingConfig.SpawnMobCD:
				val["tick"] = 0
				# 刷怪池版本
				spawnLimit = self._mobPool.get("mobCount", 10)
				if val["count"] < spawnLimit:
					val["count"] += 1
					# 生成怪物
					self.SpawnMob()
				else:
					# 结束刷怪逻辑
					self.End()
					return
			val["tick"] += 1
		pass
	# endregion

	# region 逻辑
	def SpawnProjectile(self):
		"""生成抛射物"""
		if self._spawnProjectileDict is None:
			return
		val = self._spawnProjectileDict
		if self.mTick % val["cd"] != 0:
			return
		if val["count"] < 0:
			self._spawnProjectileDict = None
			return
		# 更新数量
		val["count"] -= 1

		pos = self.GetTargetPos()
		spawnPos = self.GetProjectileSpawnPos(pos)
		if not spawnPos:
			return
		# 打向目标中间
		rot = serverApi.GetRotFromDir(commonApiMgr.GetVector(spawnPos, pos))
		# 生成电磁弹抛射物，用目标id来创建，参数改为会对创建者造成伤害
		targetId = self.mTargetId
		projectileId = serverApiMgr.SpawnProjectile(targetId, rebelLandingConfig.ProjectileId, spawnPos, rot, 
								power=rebelLandingConfig.ProjectilePower, gravity=rebelLandingConfig.ProjectileGravity, isDamageOwner=True)
		self._projectileList.append(projectileId)
		# 通过订阅，将导弹追踪的目标给到实体对象
		info = {
			"entityId": projectileId,
			"stage": "trace_target",
			"target": targetId,
			"offset": (0, self._targetHeight, 0),
		}
		Instance.mEventMgr.NotifyEvent(EntityDataSubscribeEvent, info)
		pass

	def GetProjectileSpawnPos(self, targetPos):
		"""获取抛射物生成位置"""
		distance = rebelLandingConfig.ProjectileSpawnDistance
		angle = self._spawnAngle
		if angle is None:
			# angle = random.uniform(0, 2 * math.pi)
			# 从目标正面发射过来
			rot = self.GetTargetRot()
			if not rot:
				return None
			self._spawnAngle = rot[1] + random.uniform(-15, 15)
		offset = commonApiMgr.GetNextPosByRot(targetPos, (0, self._spawnAngle), distance)
		y = targetPos[1] + rebelLandingConfig.ProjectileSpawnHeight
		return (offset[0], y, offset[2])

	def SetHitTarget(self):
		"""设置击中目标"""
		# 电磁弹的效果，由电磁弹的entity来处理
		# 标记为命中
		self._isProjectileHit = True
		# 停止生成新的电磁弹
		self._spawnProjectileDict = None
		# 刷怪池版本
		self._spanwMobDict = {
			"count": 0,
			"tick": 0,
		}
		pass

	def SpawnMob(self):
		"""生成怪物"""
		cfg = self._mobPool
		if not cfg:
			return
		# 获取目标位置
		pos = self.GetTargetPos()
		if not pos:
			return
		phaseSys = self.mSystem.GetPhaseSys()
		if not phaseSys:
			return

		# 在附近随机一个点
		radius = rebelLandingConfig.SpawnMobRadius
		height = rebelLandingConfig.SpawnMobHeight
		randomRot = self._spawnAngle + random.uniform(-15, 15)
		offset = commonApiMgr.GetNextPosByRot(pos, (0, randomRot), radius)
		x, z = offset[0], offset[2]
		y = engineApiGas.GetTopBlockHeight((x, z), self.mDimension)
		if y is None:
			return
		
		# 获取怪物类型
		weight = cfg.get("mobWeight")
		if not weight:
			weight = commonApiMgr.GetTotalWeight(cfg["mobPool"])
			cfg["mobWeight"] = weight
		mobCfg = commonApiMgr.GetValueFromWeightPool(cfg["mobPool"], weight)
		# 生成怪物(需根据天数对怪物属性进行强化)
		phaseSys.SetSpawnMonsterFromAttrRatio(mobCfg["type"], self.mDimension, (x, y + height, z), self._spanwRot)
		pass

	# endregion