# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.cfg.entity import entityClassConfig
from ScukeSurviveScript.modCommon.cfg.entity import entityConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityServerSystem(BaseServerSystem):
	"""实体造 服务端"""
	def __init__(self, namespace, systemName):
		super(EntityServerSystem, self).__init__(namespace, systemName)

		self._eventFunctions = {
		}

		pass

	def Destroy(self):
		super(EntityServerSystem, self).Destroy()
		pass

	# region 事件
	@EngineEvent()
	def ServerSpawnMobEvent(self, args):
		"""生成生物事件"""
		# 拦截原版生物的刷新
		dimensionId = args.get("dimensionId")
		if dimensionId == 0:
			# 仅对主世界做处理
			identifier = args.get("identifier")
			if entityConfig.IsSpawnMobBlackList(identifier):
				args["cancel"] = True
				return
		pass

	@EngineEvent()
	def AddEntityServerEvent(self, args):
		"""添加实体事件"""
		entityId = args.get("id")
		engineTypeStr = args.get("engineTypeStr")
		self.CreateEntityObj(entityId, engineTypeStr)
		
		# 拦截生物生成
		dimensionId = args.get("dimensionId")
		if dimensionId == 0:
			entityId = args.get("id")
			# 仅对主世界做处理
			engineTypeStr = args.get("engineTypeStr")
			if entityConfig.IsAddMobBlackList(engineTypeStr):
				self.DestroyEntity(entityId)
		pass

	@EngineEvent()
	def ProjectileDoHitEffectEvent(self, args):
		"""抛射物碰撞事件"""
		projectileId = args.get("id")
		hitTargetType = args.get("hitTargetType")
		if hitTargetType == "ENTITY":
			targetId = args.get("targetId")
			# 抛射物命中加buff
			engineTypeStr = engineApiGas.GetEngineTypeStr(projectileId)
			cfg = entityConfig.GetEntityConfig(engineTypeStr)
			if cfg:
				buff = cfg.get("buff")
				if buff and buff.get("name"):
					engineApiGas.AddEffectToEntity(targetId, buff["name"], buff.get("duration", 10), buff.get("amplifier", 0), buff.get("showParticles", True))
		pass

	# endregion

	# region 逻辑
	def CreateEntityObj(self, entityId, engineTypeStr):
		"""创建实体对象"""
		clazz = entityClassConfig.GetEntityClass(engineTypeStr)
		if clazz:
			entityObj = clazz(self, entityId, engineTypeStr)
			return entityObj
		return None
	# endregion
