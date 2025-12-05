# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLine
import mod.server.extraServerApi as serverApi

CompFactory = serverApi.GetEngineCompFactory()

class ActivatePlanetBoosterLine(StoryLine):
	__env__ = StoryLineEnvEnum.Server

	def OnBegin(self):
		target = self._playerId
		buildingSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildingServerSystem)
		identifier = self.GetConfigValue('identifier')
		buildingInfo = self._system.GetBuildingInfo(target, identifier, 'closest')
		if buildingInfo:
			# 设置点燃记录
			taskSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TaskServerSystem)
			taskSystem.SetAccumulationByFullKey('-1', 'PlanetBooster.activated', 1)
			taskSystem.IncreaseAccumulationByFullKey('-1', 'PlanetBooster.phase_activated', 1)
			dim = buildingInfo['dim']
			pos = buildingInfo['pos']
			#buildingUid = '%s_%d_%d_%d_%d' % (identifier, dim, pos[0], pos[1], pos[2])
			#taskSystem.SetAccumulation(target, 'PlanetBooster', buildingUid, True)
			# 设置建筑状态
			buildingSystem.SetBuildingData(identifier, dim, pos, 'activated', True)
			# 销毁范围目标
			killArea = self.GetConfigValue('killArea')
			startPos = self.GetPos(killArea[0])
			endPos = self.GetPos(killArea[1])
			entities = engineApiGas.GetEntitiesInSquareArea(startPos, endPos, dim)
			if entities:
				for eid in entities:
					comp = CompFactory.CreateAttr(eid)
					familyList = comp.GetTypeFamily()
					if 'mob' in familyList:
						engineApiGas.KillEntity(eid)


	def GetPos(self, pos):
		if self.mPosTransformer:
			pos = self.mPosTransformer.GetPos(pos)
		return pos