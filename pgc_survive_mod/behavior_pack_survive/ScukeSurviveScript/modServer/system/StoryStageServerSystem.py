# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.cfg.storyStageConfig import Config as StoryStageConfig
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyStage import StoryStage
from ScukeSurviveScript.modCommon import modConfig

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLineBuilder
from ScukeSurviveScript.modServer.storyline.entityMoving import EntityMovingLine
from ScukeSurviveScript.modServer.storyline.entityDestroy import EntityDestroyLine
from ScukeSurviveScript.modServer.storyline.accumulation import AccumulationLine
from ScukeSurviveScript.modServer.storyline.activatePlanetBooster import ActivatePlanetBoosterLine
from ScukeSurviveScript.modServer.storyline.sendCreeper import SendCreeperLine

StoryLineBuilder.BindingStoryLine('entityMoving', EntityMovingLine)
StoryLineBuilder.BindingStoryLine('entityDestroy', EntityDestroyLine)
StoryLineBuilder.BindingStoryLine('accumulation', AccumulationLine)
StoryLineBuilder.BindingStoryLine('activatePlanetBooster', ActivatePlanetBoosterLine)
StoryLineBuilder.BindingStoryLine('sendCreeper', SendCreeperLine)

UpdateDeltaTime = 1000.0/30.0

class StoryStageServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(StoryStageServerSystem, self).__init__(namespace, systemName)
		self._buildingsInfo = []
		self._playersStoryStage = {}


	def StartStoryStage(self, playerId, name, data):
		config = StoryStageConfig.get(name, None)
		if not config:
			return
		stage = StoryStage(self, playerId, name, config, data, StoryLineEnvEnum.Server)
		self._playersStoryStage[playerId] = stage
		info = {
			'playerId': playerId,
			'name': name,
			'data': data
		}
		self.BroadcastEvent('OnStartStoryStage', info)
		self.NotifyToClient(playerId, 'OnStartStoryStage', info)
		engineApiGas.AddEffectToEntity(playerId, serverApi.GetMinecraftEnum().EffectType.DAMAGE_RESISTANCE, int(round(stage.EndTime)), 32767, False)

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

	def Update(self):
		players = self._playersStoryStage.keys()
		for playerId in players:
			stage = self._playersStoryStage[playerId]
			stage.UpdateStage(UpdateDeltaTime)
			if stage.Completed:
				info = {
					'playerId': playerId,
					'name': stage.Name,
					'data': stage.Data
				}
				self.BroadcastEvent('OnCompleteStoryStage', info)
				self.NotifyToClient(playerId, 'OnCompleteStoryStage', info)
				del self._playersStoryStage[playerId]

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnUpdateBuildingsInfo(self, data):
		buildings = data['buildings']
		for building in buildings:
			self._buildingsInfo.append(building)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def OnDialogueSendGoldenCreeper(self, args):
		playerId = args['fromId']
		npcId = args['targetId']
		state = args['state']
		if state == 'success':
			targets = args['targets']
			data = {}
			data['@creepers'] = targets
			data['@npcId'] = npcId
			self.StartStoryStage(playerId, 'SendGoldenCreeper', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.StoryStageClientSystem)
	def PlayerInCutscene(self, data):
		playerId = data['playerId']
		engineApiGas.AddEffectToEntity(playerId, serverApi.GetMinecraftEnum().EffectType.DAMAGE_RESISTANCE, 20, 32767, False)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BattleEventServerSystem)
	def OnGuardPlanetBoosterSuccess(self, args):
		players = args['players']
		if players and len(players) > 0:
			playerId = players[0]
			data = {}
			self.StartStoryStage(playerId, 'ActivatePlanetBooster', data)

