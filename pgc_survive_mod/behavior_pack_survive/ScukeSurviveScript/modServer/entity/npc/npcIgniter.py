# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.goldenCreeperServerData import GoldenCreeperServerData
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.modServer.manager.singletonGas import Instance

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class NPCIgniter(EntityBase):

	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(NPCIgniter, self).__init__(severHandler, entityId, engineTypeStr, param)

	@EngineEvent()
	def MobDieEvent(self, args):
		if args['id'] != self.mEntityId:
			return
		pos = engineApiGas.GetEntityPos(self.mEntityId)
		rot = engineApiGas.GetEntityRot(self.mEntityId)
		if pos:
			pos = MathUtils.TupleFloor2Int(pos)
			dim = engineApiGas.GetEntityDimensionId(self.mEntityId)
			if engineApiGas.SetBlockNew(pos, {'name': 'scuke_survive:tombstone'}, dimensionId=dim):
				engineApiGas.SetBlockStates(pos, {'direction': ((rot[1] + 360) // 90) % 4}, dim)
				self.SetBlockObj(self.mEntityId, pos, rot, dim)


	def SetBlockObj(self, eid, pos, rot, dim):
		blockSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BlocksServerSystem)
		if blockSys:
			blockObj = blockSys.PlaceFunctionalBlockAfter(eid, 'scuke_survive:tombstone', pos, dim)
			if blockObj:
				blockObj.SetReviveData(self.mEngineTypeStr, 180, rot)
