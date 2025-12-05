# -*- encoding: utf-8 -*-

class LerpHandler(object):
	def __init__(self, value, duration, backDuration, maxValue=None):
		self._value = value
		self._maxValue = maxValue
		self._duration = max(0.001, duration)
		self._backDuration = max(0.001, backDuration)
		self._moveDir = 0
		self._moveStart = 0
		self._moveToValue = 0
		self._moveCurValue = 0
		self._ca = 0
		self._cb = 0
		self._forward = 1 if value > 0 else -1

	@property
	def Current(self):
		return self._moveCurValue

	def SetCurrent(self, value):
		self._moveCurValue = value

	def Reset(self):
		self._moveDir = 0
		self._moveStart = 0
		self._moveToValue = 0
		self._moveCurValue = 0

	def ResetParams(self, value, duration, backDuration, maxValue=None):
		self._value = value
		self._maxValue = maxValue
		self._duration = max(0.001, duration)
		self._backDuration = max(0.001, backDuration)

	def Update(self, time, dTime, active, autoDir=True, dir=None):
		movedValue = 0.0
		nextDir = self._moveDir
		if self._moveStart > 0:
			d = max(0, time - self._moveStart - dTime)
			k = self._ca * d / 1000.0 + self._cb
			movedValue = dTime / 1000.0 * k
			tempV = self._moveToValue - (self._moveCurValue + movedValue)
			if k * self._moveDir * self._forward <= 0 or tempV * self._moveDir * self._forward <= 0:
				movedValue = self._moveToValue - self._moveCurValue
				if autoDir:
					if nextDir > 0:
						nextDir = -1
					elif nextDir < 0:
						nextDir = 0
				else:
					nextDir = 0
		self._moveCurValue += movedValue
		if not autoDir and dir is not None:
			nextDir = dir
		moveTime = 0.0
		# move to
		if active:
			nextDir = 1
			moveTime = self._duration
			self._moveToValue = self._moveCurValue + self._value
			if self._maxValue is not None:
				if self._maxValue >= 0:
					self._moveToValue = min(self._maxValue, self._moveToValue)
				else:
					self._moveToValue = max(self._maxValue, self._moveToValue)
		# move back
		if nextDir != self._moveDir and nextDir == -1:
			moveTime = self._backDuration
			self._moveToValue = 0
		# move lerp args
		if moveTime > 0:
			moveDelta = self._moveToValue - self._moveCurValue
			self._moveStart = time
			self._ca = -2.0 * moveDelta / (moveTime * moveTime)
			self._cb = 2.0 * moveDelta / moveTime
		# move end
		if nextDir == 0:
			self._moveStart = 0
		self._moveDir = nextDir
		return movedValue

	def GetRestore(self):
		return -self._moveCurValue
