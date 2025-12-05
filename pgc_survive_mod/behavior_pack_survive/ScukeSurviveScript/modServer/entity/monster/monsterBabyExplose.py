# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
compFactory = serverApi.GetEngineCompFactory()
EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType


class MonsterBabyExplose(EntityBase):
	"""巨型巨人僵尸所扔出的爆炸婴儿僵尸"""
	
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(MonsterBabyExplose, self).__init__(severHandler, entityId, engineTypeStr, param)

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
		super(MonsterBabyExplose, self).Destroy()
	
	# region 事件
	@EngineEvent()
	def MobDieEvent(self, args):
		entityId,attackerId = args.get("id"),args.get("attacker")
		attackerType = compFactory.CreateEngineType(attackerId).GetEngineType()
		if entityId == self.mEntityId and attackerType == EntityTypeEnum.Player: 
			entityPos = compFactory.CreatePos(entityId).GetFootPos()
			serverApiMgr.CreateExplosion(entityId, attackerId, entityPos, self._radius, self._fire, self._breaks)
	# endregion