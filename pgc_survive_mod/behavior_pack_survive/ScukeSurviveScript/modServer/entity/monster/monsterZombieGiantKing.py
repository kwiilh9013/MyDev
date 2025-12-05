# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()
EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType


class MonsterZombieGiantKing(EntityBase):
	"""黑色毒液僵尸"""
	
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(MonsterZombieGiantKing, self).__init__(severHandler, entityId, engineTypeStr, param)

		self._attrComp = compFactory.CreateAttr(self.mEntityId)
		# 给予效果名称
		self._effectName = None
		# 给予效果持续时间
		self._effectTime = 0
		if self.mCfg:
			self._effectName = self.mCfg['effect_name']
			self._effectTime = self.mCfg['effect_time']
		pass

	def Destroy(self):
		super(MonsterZombieGiantKing, self).Destroy()

	# region 事件
	@EngineEvent()
	def ActuallyHurtServerEvent(self, args):
		entityId,srcId = args.get("entityId"),args.get("srcId")
		if srcId == self.mEntityId:
			srcType = compFactory.CreateEngineType(entityId).GetEngineType()
			if srcType == EntityTypeEnum.Player:
				compFactory.CreateEffect(entityId).AddEffectToEntity(self._effectName, self._effectTime, 0, True)
	# endregion