# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBase
import mod.server.extraServerApi as serverApi

CompFactory = serverApi.GetEngineCompFactory()

class EntityMoveBattlePhase(BattlePhaseBase):
	def __init__(self, battleEvent, config, data):
		super(EntityMoveBattlePhase, self).__init__(battleEvent, config, data)
		self._moveSet = False

	def OnStart(self):
		super(EntityMoveBattlePhase, self).OnStart()
		entities = self.GetConfigValue('targets', self._battleEvent.Players)
		pos = self.TransPos(self.GetConfigValue('pos'))
		rot = self.TransRot(self.GetConfigValue('rot'))
		for eid in entities:
			CompFactory.CreatePos(eid).SetFootPos(pos)
			CompFactory.CreateRot(eid).SetRot((rot[0], rot[1]))

		self._moveSet = True

	def Completed(self):
		return self._moveSet
