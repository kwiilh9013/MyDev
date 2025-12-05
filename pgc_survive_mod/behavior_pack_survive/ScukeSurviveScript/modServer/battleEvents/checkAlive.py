# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBase

HealthAttrEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH

class CheckAliveBattlePhase(BattlePhaseBase):
	def __init__(self, battleEvent, config, data):
		super(CheckAliveBattlePhase, self).__init__(battleEvent, config, data)
		self._checked = False
		self._aliveTargets = []

	def OnStart(self):
		super(CheckAliveBattlePhase, self).OnStart()
		self._events = self.GetConfigValue('events')
		entities = self.GetConfigValue('targets')
		for eid in entities:
			health = engineApiGas.GetAttrValue(eid, HealthAttrEnum)
			if health > 0:
				self._aliveTargets.append(eid)
		self._checked = True

	def Completed(self):
		return self._checked

	def OnEnd(self):
		if self._events is None:
			return
		eventHandler = self._battleEvent.EventHandler
		eventName = None
		if len(self._aliveTargets) > 0:
			eventName = self._events.get('success', None)
		else:
			eventName = self._events.get('fail', None)
		if eventName is None:
			return
		eventHandler.BroadcastEvent(eventName, {'players': self._battleEvent.Players, 'alive': self._aliveTargets})