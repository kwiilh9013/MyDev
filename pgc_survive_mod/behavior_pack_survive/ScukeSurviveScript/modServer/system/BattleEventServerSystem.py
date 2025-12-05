# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.battleEventConfig import Config as BattleEventConfig


import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.modServer.battleEvents.battleEvent import BattleEvent
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBuilder
from ScukeSurviveScript.modServer.battleEvents.entityBuff import EntityBuffBattlePhase
from ScukeSurviveScript.modServer.battleEvents.spawnMobsWaves import SpawnMobsWavesBattlePhase
from ScukeSurviveScript.modServer.battleEvents.checkAlive import CheckAliveBattlePhase
from ScukeSurviveScript.modServer.battleEvents.entityEventTrigger import EntityEventTriggerBattlePhase
from ScukeSurviveScript.modServer.battleEvents.entityMove import EntityMoveBattlePhase
from ScukeSurviveScript.modServer.battleEvents.entityTag import EntityTagBattlePhase

BattlePhaseBuilder.BindingBattlePhase('entityBuff', EntityBuffBattlePhase)
BattlePhaseBuilder.BindingBattlePhase('spawnMobsWaves', SpawnMobsWavesBattlePhase)
BattlePhaseBuilder.BindingBattlePhase('checkAlive', CheckAliveBattlePhase)
BattlePhaseBuilder.BindingBattlePhase('entityEventTrigger', EntityEventTriggerBattlePhase)
BattlePhaseBuilder.BindingBattlePhase('entityMove', EntityMoveBattlePhase)
BattlePhaseBuilder.BindingBattlePhase('entityTag', EntityTagBattlePhase)

from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_planet_booster import Config as Scuke_planetBooster

class BattleEventServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(BattleEventServerSystem, self).__init__(namespace, systemName)
		self._buildingsInfo = []
		self._battleEvents = {}
		self._updateTimer = engineApiGas.AddRepeatTimer(0.5, self.OnUpdate)

	def CheckOnBattleEvent(self, playerId):
		for battleEvent in self._battleEvents.itervalues():
			if playerId in battleEvent.Players:
				return True
		return False

	def StartBattleEvent(self, playerId, configId, data):
		if configId not in BattleEventConfig:
			return
		config = BattleEventConfig[configId]
		battleEvent = BattleEvent(self, playerId, config, data)
		if battleEvent:
			uid = '%s_%s' % (configId, playerId)
			if uid in self._battleEvents:
				self._battleEvents[uid].End()
			self._battleEvents[uid] = battleEvent
			battleEvent.Start()

	def EndBattleEvent(self, playerId, configId):
		battleKey = '%s_%s' % (configId, playerId)
		battleEvent = self._battleEvents.get(battleKey, None)
		if battleEvent:
			battleEvent.End()

	def OnUpdate(self):
		endedEvents = []
		for battleKey in self._battleEvents:
			battleEvent = self._battleEvents[battleKey]
			if not battleEvent.Ended:
				battleEvent.Update()
			else:
				endedEvents.append(battleKey)
		for battleKey in endedEvents:
			del self._battleEvents[battleKey]

	def OnDestroy(self):
		super(BattleEventServerSystem, self).OnDestroy()
		if self._updateTimer:
			engineApiGas.CancelTimer(self._updateTimer)
			self._updateTimer = None

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnUpdateBuildingsInfo(self, data):
		buildings = data['buildings']
		for building in buildings:
			self._buildingsInfo.append(building)

	def GetBuildingInfo(self, playerId, identifier, filter):
		buildings = []
		for building in self._buildingsInfo:
			if building['identifier'] == identifier:
				buildings.append(building)
		ret = None
		if len(buildings) > 0:
			ret = buildings[0]
		if filter == 'closest':
			pos = engineApiGas.GetEntityPos(playerId)
			if pos:
				minDis = -1
				for building in buildings:
					dis = MathUtils.TupleLength(MathUtils.TupleSub(building['pos'], pos))
					if minDis < 0 or dis < minDis:
						minDis = dis
						ret = building
		return ret

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.StoryStageServerSystem)
	def OnCompleteStoryStage(self, args):
		playerId = args['playerId']
		name = args['name']
		data = args['data']
		if name == 'SendGoldenCreeper':  # 交付苦力怕后自动开始守护发动机事件
			target = data['@npcId']
			self.StartGuardPlanetBooster({
				'playerId': playerId,
				'target': target,
			})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def StartGuardPlanetBooster(self, args):
		playerId = args['playerId']
		target = args['target']
		# 获取当前点燃的发动机个数
		buildingSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildingServerSystem)
		buildings = buildingSystem.GetBuildingById(Scuke_planetBooster['identifier'], 0)
		activated = 0
		for building in buildings:
			data = building['data']
			if data and data.get('activated', False):
				activated += 1
		# 准备战斗事件
		battleEventId = 'GuardPlanetBoosterLevel%d' % (activated+1)
		battleData = {
			'@entities': [target]
		}
		self.StartBattleEvent(playerId, battleEventId, battleData)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BattleEventServerSystem)
	def OnGuardPlanetBoosterSuccess(self, args):
		players = args['players']
		for playerId in players:
			self.NotifyToClient(playerId, 'OnGuardPlanetBoosterSuccess', args)


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BattleEventServerSystem)
	def OnGuardPlanetBoosterFail(self, args):
		players = args['players']
		for playerId in players:
			self.NotifyToClient(playerId, 'OnGuardPlanetBoosterFail', args)
