# -*- encoding: utf-8 -*-
import time

import ScukeSurviveScript.ScukeCore.common.tweening as tweening
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils


class DelayTween(object):
	def __init__(self, duration, completedCallback=None):
		self._duration = duration
		self._completed = False
		self._time = 0
		self.__updateTime = -1
		self._completedCallback = completedCallback

	def UpdateWithTime(self, deltaTime):
		if self._completed:
			return
		self._time += deltaTime
		if self._time >= self._duration:
			self._completed = True
			if self._completedCallback:
				self._completedCallback()

	def Update(self):
		curTime = time.time()
		if self.__updateTime < 0:
			self.__updateTime = curTime
		self.UpdateWithTime(curTime-self.__updateTime)
		self.__updateTime = curTime

	@property
	def Completed(self):
		return self._completed


class TweenList(object):
	def __init__(self, tweens, completedCallback=None):
		self._tweenList = tweens
		self._tweenIndex = -1
		self._curTween = None
		self._completedCallback = completedCallback
		if len(tweens) > 0:
			self._tweenIndex = 0
			self._curTween = tweens[0]

	def UpdateWithTime(self, deltaTime):
		if self._curTween:
			self._curTween.UpdateWithTime(deltaTime)
			if self._curTween.Completed:
				self.NextTween()

	def Update(self):
		if self._curTween:
			self._curTween.Update()
			if self._curTween.Completed:
				self.NextTween()

	def NextTween(self):
		index = self._tweenIndex + 1
		if index < len(self._tweenList):
			self._tweenIndex = index
			self._curTween = self._tweenList[index]
		else:
			if not self.Completed:
				self._tweenIndex = -1
				if self._completedCallback:
					self._completedCallback()

	def Reset(self):
		if len(self._tweenList) > 0:
			self._tweenIndex = 0
			self._curTween = self._tweenList[0]
			for tween in self._tweenList:
				tween.Reset()

	@property
	def Completed(self):
		return self._tweenIndex == -1


class TweenHandler(object):
	def __init__(self, tweenFuncName, duration, fromValue, toValue, updateCallback=None, completedCallback=None):
		self._tweenFunc = TweeningFuncFactory.Get(tweenFuncName)
		self._fromValue = fromValue
		self._currentValue = fromValue
		if isinstance(fromValue, tuple):
			self._moveDeltaValue = MathUtils.TupleSub(toValue, fromValue)
		else:
			self._moveDeltaValue = toValue - fromValue
		self._targetValue = toValue
		self._getter = self.__Getter__
		self._setter = self.__Setter__
		self._updateCallback = updateCallback
		self._completedCallback = completedCallback
		self._time = 0
		self._timeK = 1.0/max(duration, 0.0001)
		self._completed = False
		self.__updateTime = -1

	@property
	def Current(self):
		return self._currentValue

	def __Getter__(self):
		return self._currentValue

	def __Setter__(self, value):
		return value

	def UpdateWithTime(self, deltaTime):
		if self._tweenFunc is None or self._completed:
			return
		self._time += deltaTime*self._timeK
		if self._time < 1.0:
			if isinstance(self._fromValue, tuple):
				newValue = MathUtils.TupleAddMul(self._fromValue, self._moveDeltaValue, self._tweenFunc(self._time))
			else:
				newValue = self._fromValue + self._tweenFunc(self._time) * self._moveDeltaValue
		else:
			newValue = self._targetValue
		self.__Setter__(newValue)
		if self._updateCallback:
			self._updateCallback(newValue)
		if self._time >= 1.0:
			self._completed = True
			if self._completedCallback:
				self._completedCallback()

	def Update(self):
		curTime = time.time()
		if self.__updateTime < 0:
			self.__updateTime = curTime
		self.UpdateWithTime(curTime-self.__updateTime)
		self.__updateTime = curTime

	def Reset(self):
		self._time = 0
		self._completed = False
		self.__updateTime = -1

	@property
	def Completed(self):
		return self._completed

class TweeningFuncFactory(object):

	@staticmethod
	def Get(typeName):
		if typeName == 'linear':
			return tweening.linear
		if typeName == 'easeInQuad':
			return tweening.easeInQuad
		if typeName == 'easeOutQuad':
			return tweening.easeOutQuad
		if typeName == 'easeInOutQuad':
			return tweening.easeInOutQuad
		if typeName == 'easeInCubic':
			return tweening.easeInCubic
		if typeName == 'easeOutCubic':
			return tweening.easeOutCubic
		if typeName == 'easeInOutCubic':
			return tweening.easeInOutCubic
		if typeName == 'easeInQuart':
			return tweening.easeInQuart
		if typeName == 'easeOutQuart':
			return tweening.easeOutQuart
		if typeName == 'easeInOutQuart':
			return tweening.easeInOutQuart
		if typeName == 'easeInQuint':
			return tweening.easeInQuint
		if typeName == 'easeOutQuint':
			return tweening.easeOutQuint
		if typeName == 'easeInOutQuint':
			return tweening.easeInOutQuint
		if typeName == 'easeInSine':
			return tweening.easeInSine
		if typeName == 'easeOutSine':
			return tweening.easeOutSine
		if typeName == 'easeInOutSine':
			return tweening.easeInOutSine
		if typeName == 'easeInExpo':
			return tweening.easeInExpo
		if typeName == 'easeOutExpo':
			return tweening.easeOutExpo
		if typeName == 'easeInOutExpo':
			return tweening.easeInOutExpo
		if typeName == 'easeInCirc':
			return tweening.easeInCirc
		if typeName == 'easeOutCirc':
			return tweening.easeOutCirc
		if typeName == 'easeInOutCirc':
			return tweening.easeInOutCirc
		if typeName == 'easeInElastic':
			return tweening.easeInElastic
		if typeName == 'easeOutElastic':
			return tweening.easeOutElastic
		if typeName == 'easeInOutElastic':
			return tweening.easeInOutElastic
		if typeName == 'easeInBack':
			return tweening.easeInBack
		if typeName == 'easeOutBack':
			return tweening.easeOutBack
		if typeName == 'easeInOutBack':
			return tweening.easeInOutBack
		if typeName == 'easeInBounce':
			return tweening.easeInBounce
		if typeName == 'easeOutBounce':
			return tweening.easeOutBounce
		if typeName == 'easeInOutBounce':
			return tweening.easeInOutBounce
