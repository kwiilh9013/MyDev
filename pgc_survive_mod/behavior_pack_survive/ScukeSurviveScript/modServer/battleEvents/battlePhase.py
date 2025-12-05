# -*- coding: utf-8 -*-

class BattlePhaseBuilder(object):
	__bindingBattlePhase__ = {}

	@staticmethod
	def BindingBattlePhase(name, cls):
		BattlePhaseBuilder.__bindingBattlePhase__[name] = cls

	@staticmethod
	def GetBattlePhase(battleEvent, config, data):
		tType = config['type']
		if tType not in BattlePhaseBuilder.__bindingBattlePhase__:
			return None
		cls = BattlePhaseBuilder.__bindingBattlePhase__[tType]
		return cls(battleEvent, config, data)


class BattlePhaseBase(object):
	def __init__(self, battleEvent, config, data):
		self._battleEvent = battleEvent
		self._config = config
		self._data = data
		self._inited = False
		self._posTransformer = None

	@property
	def State(self):
		return None

	def SetState(self, states):
		pass


	def OnStart(self):
		self._inited = True

	def OnUpdate(self):
		if not self._inited:
			self.OnStart()
		return True

	def OnEnd(self):
		pass

	def Completed(self):
		return True

	def SetPosTransformer(self, posTransformer):
		self._posTransformer = posTransformer

	def TransPos(self, pos):
		if self._posTransformer is None:
			return pos
		return self._posTransformer.GetPos(pos)

	def TransRot(self, rot):
		if self._posTransformer is None:
			return rot
		return self._posTransformer.GetRot(rot)

	def GetConfigValue(self, name, defaultValue=None):
		if name not in self._config:
			return defaultValue
		ret = self._config[name]
		if type(ret) == str and ret.startswith('@'):
			ret = self._data.get(ret, defaultValue)
		return ret

	def OnOutRange(self):
		pass