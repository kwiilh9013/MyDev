# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLine


class EntityDestroyLine(StoryLine):
	__env__ = StoryLineEnvEnum.Server

	def OnBegin(self):
		targets = self.GetConfigValue('targets')
		for target in targets:
			self._system.DestroyEntity(target)

