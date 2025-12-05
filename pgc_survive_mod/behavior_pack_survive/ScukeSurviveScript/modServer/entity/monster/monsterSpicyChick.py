# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()
EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType


class MonsterSpicyChickAttack(EntityBase):
	"""麻辣辣妹僵尸"""
	
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(MonsterSpicyChickAttack, self).__init__(severHandler, entityId, engineTypeStr, param)

		self._attrComp = compFactory.CreateAttr(self.mEntityId)
		# 火焰伤害
		self._fireDamage = 0
		# 火焰持续时间
		self._fireTime = 0
		if self.mCfg:
			self._fireDamage = self.mCfg['fire_damage']
			self._fireTime = self.mCfg['fire_time']
		pass

	def Destroy(self):
		super(MonsterSpicyChickAttack, self).Destroy()

	# region 事件
	@EngineEvent()
	def ActuallyHurtServerEvent(self, args):
		entityId,srcId = args.get("entityId"),args.get("srcId")
		if srcId == self.mEntityId:
			compFactory.CreateAttr(entityId).SetEntityOnFire(self._fireTime, self._fireDamage)
	# endregion