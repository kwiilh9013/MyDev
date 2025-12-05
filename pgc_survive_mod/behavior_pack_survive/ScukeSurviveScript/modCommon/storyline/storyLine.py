# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum


class StoryLineBuilder(object):
	__bindingStoryLine__ = {}

	@staticmethod
	def BindingStoryLine(name, cls):
		StoryLineBuilder.__bindingStoryLine__[name] = cls

	@staticmethod
	def GetStoryLine(system, playerId, config, data, env):
		tType = config['type']
		if tType not in StoryLineBuilder.__bindingStoryLine__:
			return None
		cls = StoryLineBuilder.__bindingStoryLine__[tType]
		if (cls.__env__ & env) == 0:
			return None
		return cls(system, playerId, config, data)


class StoryLine(object):
	__env__ = StoryLineEnvEnum.Client

	def __init__(self, system, playerId, config, data):
		self._playerId = playerId
		self._system = system
		self._config = config
		offset = config['offset']
		duration = config['duration']
		self._time = 0
		self._beginTime = offset * 1000.0
		self._duration = duration * 1000.0
		self._endTime = self._beginTime + self._duration
		self._data = data
		self.mPosTransformer = None

	@property
	def BeginTime(self):
		return self._beginTime

	@property
	def EndTime(self):
		return self._endTime

	def OnBegin(self):
		pass

	def OnEnd(self):
		pass

	def Update(self, deltaTime):
		prev = self._time
		cur = prev + deltaTime
		if self._beginTime <= cur <= self._endTime:
			self.OnUpdate(cur, (cur-self._beginTime)/self._duration)
		if prev < self._beginTime <= cur:
			self.OnBegin()
			self.OnUpdate(0, 0.0)
		if prev < self._endTime <= cur:
			self.OnEnd()
		self._time = cur

	def OnUpdate(self, curTime, percent):
		pass

	def SetPosTransformer(self, posTrans):
		self.mPosTransformer = posTrans

	def SetData(self, data):
		self._data = data

	def GetConfigValue(self, name):
		if name not in self._config:
			return None
		ret = self._config[name]
		if type(ret) == str and ret.startswith('@'):
			ret = self._data.get(ret)
		return ret
