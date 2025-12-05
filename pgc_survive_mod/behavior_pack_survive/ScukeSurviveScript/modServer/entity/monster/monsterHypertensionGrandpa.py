# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()
EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType
LVID = serverApi.GetLevelId()


class MonsterHypertensionGrandpa(EntityBase):
	"""高血压老大爷僵尸"""
	
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(MonsterHypertensionGrandpa, self).__init__(severHandler, entityId, engineTypeStr, param)

		self._attrComp = compFactory.CreateAttr(self.mEntityId)
		# 爆炸威力
		self._radius = 0
		# 爆炸是否带火
		self._fire = True
  		#爆炸是否破坏方块
		self._breaks = True
		if self.mCfg:
			explosion= self.mCfg['explosion']
			self._radius = explosion.get("radius",3)
			self._fire = explosion.get("fire")
			self._breaks = explosion.get("breaks")
		pass

	def Destroy(self):
		super(MonsterHypertensionGrandpa, self).Destroy()

	# region 事件
	@EngineEvent()
	def MobDieEvent(self, args):
		entityId,attackerId = args.get("id"),args.get("attacker")
		attackTarget = compFactory.CreateAction(entityId).GetAttackTarget()
		if entityId == self.mEntityId and attackTarget == attackerId: 
			entityPos = compFactory.CreatePos(entityId).GetFootPos()
			serverApiMgr.CreateExplosion(entityId, attackerId, entityPos, self._radius, self._fire, self._breaks)
	# endregion