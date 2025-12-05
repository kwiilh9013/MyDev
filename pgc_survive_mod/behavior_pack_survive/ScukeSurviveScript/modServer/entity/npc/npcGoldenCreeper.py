# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.goldenCreeperServerData import GoldenCreeperServerData
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.modServer.manager.singletonGas import Instance

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class NPCGoldenCreeper(EntityBase):

	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(NPCGoldenCreeper, self).__init__(severHandler, entityId, engineTypeStr, param)
		data = Instance.mDatasetManager.GetEntityData(entityId, 'golden_creeper')
		if not data:
			data = DatasetObj.Build(GoldenCreeperServerData)
			Instance.mDatasetManager.SetEntityData(entityId, 'golden_creeper', data)
		else:
			data = DatasetObj.Format(GoldenCreeperServerData, data)
		self._data = data

	def Destroy(self):
		super(NPCGoldenCreeper, self).Destroy()

# region 事件
	@EngineEvent()
	def PlayerFeedEntityServerEvent(self, args):
		playerId = args['playerId']
		if args['entityId'] == self.mEntityId:
			healthRecovery = self.mCfg['tameHealth']
			pleasureRecovery = self.mCfg['tamePleasure']
			pleasureRange = self.mCfg['pleasureRange']
			prev = self._data['pleasure']
			cur = prev + pleasureRecovery
			curHealth = engineApiGas.GetAttrValue(self.mEntityId, minecraftEnum.AttrType.HEALTH)
			if cur > pleasureRange[1]:
				# 高兴爆炸
				args['cancel'] = True
				engineApiGas.Hurt(self.mEntityId, playerId, int(curHealth), minecraftEnum.ActorDamageCause.EntityAttack, False)
				return
			engineApiGas.SetAttrValue(self.mEntityId, minecraftEnum.AttrType.HEALTH, curHealth + healthRecovery)
			self._data['pleasure'] = cur
			Instance.mDatasetManager.SetEntityData(self.mEntityId, 'golden_creeper', self._data)
# endregion

# region 逻辑入口
# endregion
