# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas



class FeatureServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(FeatureServerSystem, self).__init__(namespace, systemName)

	@EngineEvent
	def PlaceNeteaseStructureFeatureEvent(self, args):
		if args['dimensionId'] is not 0:
			return
		structureName = args['structureName']
		chunkPos = (args['x'], args['y'], args['z'])
		biomeType = args['biomeType']       # 群系类型  type: int
		biomeName = args['biomeName']       # 群系名称

		chunkComp = engineApiGas.compFactory.CreateChunkSource(engineApiGas.levelId)
		chunkIndex = chunkComp.GetChunkPosFromBlockPos(chunkPos)

		self.logger.log("PlaceNeteaseStructureFeatureEvent: %s, %s, %s, %s" % (structureName, biomeType, biomeName, chunkPos))
