# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon.storyline.posTransformer import PosTransformer
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLineBuilder


class StoryStage(object):
	def __init__(self, system, playerId, name, config, data, env):
		self._name = name
		self._playerId = playerId
		self._system = system
		self._lines = []
		self._time = 0.0
		self._beginTime = 0.0
		self._endTime = config['duration'] * 1000
		self._data = data
		for lineConfig in config['lines']:
			storyLine = StoryLineBuilder.GetStoryLine(system, playerId, lineConfig, data, env)
			if storyLine:
				self._lines.append(storyLine)
				self._endTime = max(self._endTime, storyLine.EndTime)
		posTransConfig = config.get('posTransformer', None)
		posTransformer = None
		if posTransConfig:
			posTransformer = PosTransformer(system, playerId, posTransConfig)
		for line in self._lines:
			line.SetPosTransformer(posTransformer)

	def UpdateStage(self, deltaTime):
		prev = self._time
		cur = prev + deltaTime
		if prev < self._beginTime <= cur:
			self.OnBegin()
		for storyLine in self._lines:
			storyLine.Update(deltaTime)
		if prev < self._endTime <= cur:
			self.OnEnd()
		self._time = cur

	@property
	def Data(self):
		return self._data

	@property
	def Name(self):
		return self._name

	@property
	def PlayerId(self):
		return self._playerId

	@property
	def EndTime(self):
		return self._endTime / 1000.0

	@property
	def Completed(self):
		return self._time >= self._endTime

	def OnBegin(self):
		pass

	def OnEnd(self):
		pass

