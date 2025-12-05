# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLine
import mod.server.extraServerApi as serverApi

class SendCreeperLine(StoryLine):
	__env__ = StoryLineEnvEnum.Server

	def OnBegin(self):
		target = self._playerId
		buildingSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildingServerSystem)
		identifier = self.GetConfigValue('identifier')
		buildingInfo = self._system.GetBuildingInfo(target, identifier, 'closest')
		if buildingInfo:
			targets = self.GetConfigValue('targets')
			for target in targets:
				self._system.DestroyEntity(target)
			dim = buildingInfo['dim']
			pos = buildingInfo['pos']
			buildingSystem.SetBuildingData(identifier, dim, pos, 'consumeCreeper', True)
