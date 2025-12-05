# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBase
import mod.server.extraServerApi as serverApi


class EntityBuffBattlePhase(BattlePhaseBase):
	def __init__(self, battleEvent, config, data):
		super(EntityBuffBattlePhase, self).__init__(battleEvent, config, data)
		self._buffSet = False

	def OnStart(self):
		super(EntityBuffBattlePhase, self).OnStart()
		entities = self.GetConfigValue('targets')
		op = self.GetConfigValue('op')
		duration = self.GetConfigValue('duration', 0)
		amplifier = self.GetConfigValue('amplifier', 0)
		buff = self.GetConfigValue('buff')
		buffSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuffServerSystem)
		if entities and len(entities) > 0:
			for entityId in entities:
				if op == 'add':
					if buffSystem:
						buffSystem.RegisterEntityBuffState(entityId)
					engineApiGas.AddEffectToEntity(entityId, buff, int(duration), amplifier, True)
				elif op == 'remove':
					engineApiGas.RemoveEffectFromEntity(entityId, buff)
		self._buffSet = True

	def Completed(self):
		return self._buffSet
