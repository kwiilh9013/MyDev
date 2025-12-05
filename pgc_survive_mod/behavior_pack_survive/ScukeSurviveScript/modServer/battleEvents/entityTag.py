# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBase

CompFactory = serverApi.GetEngineCompFactory()

class EntityTagBattlePhase(BattlePhaseBase):
	def __init__(self, battleEvent, config, data):
		super(EntityTagBattlePhase, self).__init__(battleEvent, config, data)
		self._triggered = False

	def OnStart(self):
		super(EntityTagBattlePhase, self).OnStart()
		self._add = self.GetConfigValue('add')
		self._remove = self.GetConfigValue('remove')
		self._triggered = True

	def Completed(self):
		return self._triggered

	def OnEnd(self):
		entities = self.GetConfigValue('targets')
		for target in entities:
			tagComp = CompFactory.CreateTag(target)
			if self._add:
				for tag in self._add:
					tagComp.AddEntityTag(tag)
			if self._remove:
				for tag in self._remove:
					tagComp.RemoveEntityTag(tag)
