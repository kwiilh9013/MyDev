# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.buffServerData import BuffState

class BuffBuilder(object):
	__bindingBuff__ = {}

	@staticmethod
	def BindingBuff(name, cls):
		BuffBuilder.__bindingBuff__[name] = cls

	@staticmethod
	def GetBuff(eid, state, duration=-1, amplifier=0, attrSystem=None, eventHanlder=None):
		tType = state['type']
		if tType not in BuffBuilder.__bindingBuff__:
			return Buff(eid, state, duration, amplifier, attrSystem, eventHanlder)
		cls = BuffBuilder.__bindingBuff__[tType]
		return cls(eid, state, duration, amplifier, attrSystem, eventHanlder)

class Buff(object):
	def __init__(self, eid, state, duration=-1, amplifier=0, attrSystem=None, eventHanlder=None):
		self._eid = eid
		self._type = state['type']
		self._interval = state['interval'] * 1000.0
		self._duration = state['duration'] * 1000.0
		self._amplifier = amplifier
		self._eventHandler = eventHanlder
		if duration >= 0:
			self._duration = duration * 1000.0
		self._attr = state['attr']
		self._value = 0
		self._modifiedFloat = 0.0
		if 'value' in state:
			self._value = state['value']
		if 'percentValue' in state and attrSystem:
			percent = state['percentValue']
			pAttr = percent['attr']
			pValue = percent['value']
			self._value = attrSystem.GetAttr(eid, pAttr) * pValue

		self._undo = False
		if 'undo' in state:
			self._undo = state['undo']
		self._immediate = False
		if 'immediate' in state:
			self._immediate = state['immediate']
		self._modified = 0
		if '_modified' in state:
			self._modified = state['_modified']
		self._passedTime = 0
		if '_passedTime' in state:
			self._passedTime = state['_passedTime']

	@property
	def Eid(self):
		return self._eid

	@property
	def Type(self):
		return self._type

	@property
	def Attr(self):
		return self._attr

	@property
	def AttrValue(self):
		# buff更新的值，需和buff等级结合计算
		return self._value * (1.0 + self._amplifier)

	def ClampAttrValue(self):
		value = self.AttrValue
		if self._attr != AttributeEnum.Health or value > 0:  # 对扣除生命进行处理
			return value
		prev = self._modifiedFloat
		cur = prev + value
		curInt = int(cur)
		delta = curInt - int(prev)
		if delta != 0:
			self._modifiedFloat = float(cur) - curInt
			return delta
		self._modifiedFloat = cur
		return 0


	@property
	def NeedUndo(self):
		return self._undo

	@property
	def Modified(self):
		return self._modified

	@property
	def Duration(self):
		return self._duration / 1000.0

	@property
	def Amplifier(self):
		"""buff等级，从0开始"""
		return self._amplifier

	@property
	def State(self):
		ret = DatasetObj.Build(BuffState)
		ret['eid'] = self._eid
		ret['type'] = self._type
		ret['interval'] = self._interval / 1000.0
		ret['duration'] = self._duration / 1000.0
		ret['amplifier'] = self._amplifier
		ret['attr'] = self._attr
		ret['value'] = self._value
		ret['undo'] = self._undo
		ret['immediate'] = self._immediate
		ret['_modified'] = self._modified
		ret['_passedTime'] = round(self._passedTime)
		return ret

	@property
	def Ended(self):
		return self._passedTime >= self._duration

	# 返回 (buff结束, 是否apply)
	def Tick(self, tickTime):
		nextTime = self._passedTime + tickTime
		n1 = 0 if self._interval <= 0 else int(self._passedTime / self._interval)
		n2 = 0 if self._interval <= 0 else int(nextTime / self._interval)
		active = False
		if self._immediate and self._passedTime == 0:
			active = True
		elif n2 > n1 and (self._duration < 0 or nextTime <= self._duration + 1):
			active = True
		self._passedTime = nextTime
		return (0 <= self._duration <= nextTime), active

	def Apply(self, value):
		self._modified += value


	def Refresh(self, duration, amplifier):
		self._passedTime = 0.01
		self._duration = duration * 1000.0
		self._amplifier = amplifier

	def OnAdded(self):
		pass

	def OnRemoved(self):
		pass
