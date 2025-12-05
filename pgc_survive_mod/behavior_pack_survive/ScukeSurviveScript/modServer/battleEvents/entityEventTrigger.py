# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBase


class EntityEventTriggerBattlePhase(BattlePhaseBase):
	def __init__(self, battleEvent, config, data):
		super(EntityEventTriggerBattlePhase, self).__init__(battleEvent, config, data)
		self._triggered = False

	def OnStart(self):
		super(EntityEventTriggerBattlePhase, self).OnStart()
		self._events = self.GetConfigValue('events')
		self._triggered = True

	def Completed(self):
		return self._triggered

	def OnEnd(self):
		if self._events is None:
			return
		entities = self.GetConfigValue('targets')
		for target in entities:
			for event in self._events:
				engineApiGas.TriggerCustomEvent(target, event)
