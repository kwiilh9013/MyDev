# -*- encoding: utf-8 -*-
import random
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister


class PhaseEvent(CommonEventRegister):
	def __init__(self, system, name, eventStateChangedCall=None):
		CommonEventRegister.__init__(self, system)
		self._name = name
		self._state = -1
		self._startTime = -1
		self._endTime = -1
		self._days = 0
		self._config = None
		self._system = system
		self._eventStateChangedCall = eventStateChangedCall

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)

	@property
	def Name(self):
		return self._name

	@property
	def Config(self):
		return self._config

	@property
	def StartTime(self):
		return self._startTime

	@property
	def EndTime(self):
		return self._endTime

	@property
	def Active(self):
		return self._state == 1

	def TryPlace(self, days, daytime, eventsWeight, config):
		rnd = random.random()
		probability = eventsWeight[self._name] / 100.0
		active = rnd < probability
		return active

	def Place(self, days, daytime, config, rightNow=False):
		self._config = config
		self._startTime = config['startTime']
		self._endTime = config['endTime']
		self._days = days
		if 'random' in config:
			randomConfig = config['random']
			range = randomConfig['duration']
			duration = random.randint(range[0], range[1])
			self._startTime = random.randint(config['startTime'], config['endTime'])
			self._endTime = self._startTime + duration
		if rightNow:
			delta = self._endTime - self._startTime
			self._startTime = daytime
			self._endTime = self._startTime + delta
		self._state = 0

	def Remove(self, days, daytime):
		actived = self.Active
		self._state = -1
		if actived:
			self.OnStateChange(False, days, daytime)
			if self._eventStateChangedCall:
				self._eventStateChangedCall(self, False)


	def Update(self, days, daytime):
		daytime = (days - self._days) * 24000 + daytime
		ret = None
		if self._state < 0:
			return ret
		if self._state == 0 and daytime >= self._startTime:
			ret = True
			self._state += 1
		elif self._state == 1 and (daytime > self._endTime or daytime < self._startTime):
			ret = False
			self._state = -1
		if self._state > 0:
			self.EventUpdate(days, daytime)
		if ret is not None:
			self.OnStateChange(ret, days, daytime)
			if self._eventStateChangedCall:
				self._eventStateChangedCall(self, ret)
		return ret

	def EventUpdate(self, days, daytime):
		pass

	def OnStateChange(self, state, days, daytime):
		pass