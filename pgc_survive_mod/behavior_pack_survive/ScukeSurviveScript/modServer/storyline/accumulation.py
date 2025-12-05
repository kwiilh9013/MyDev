# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLine
import mod.server.extraServerApi as serverApi

class AccumulationLine(StoryLine):
	__env__ = StoryLineEnvEnum.Server

	def OnBegin(self):
		target = self._playerId
		op = self.GetConfigValue('op')
		fullKey = self.GetConfigValue('fullKey')
		value = self.GetConfigValue('value')
		taskSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TaskServerSystem)
		if op == 'Set':
			taskSystem.SetAccumulationByFullKey(target, fullKey, value)
		elif op == 'Increase':
			taskSystem.IncreaseAccumulationByFullKey(target, fullKey, value)
