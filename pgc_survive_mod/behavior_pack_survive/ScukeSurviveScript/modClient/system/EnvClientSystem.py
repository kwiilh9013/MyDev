# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.envConfig import Config as EnvConfig
from ScukeSurviveScript.modCommon.defines.phaseEventEnum import PhaseWeatherEventEnum
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler

CompFactory = clientApi.GetEngineCompFactory()


class EnvClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(EnvClientSystem, self).__init__(namespace, systemName)
		self._currentWeatherState = None
		self._currentEnvDisplay = None
		self._currentEnvDisplaySkybox = None
		self._currentEnvDisplaySkyboxActive = False
		self._lastPos = None
		self._lastRot = None
		self._lastPers = 0
		self._particleComp = None
		self._playerPosComp = None
		self._playerRotComp = None
		self._cameraComp = None
		self._playerViewComp = None
		self._playerId = None
		self._lastWeatherMoveDis = 0
		self._levelModelComp = CompFactory.CreateModel(self.mLevelId)

		self._weatherStates = []

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.EnvServerSystem)
	def OnEnvStateUpdate(self, data):
		ui = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
		if not ui:
			return
		ui.DebugUpdateEnv(data)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnUpdatePhaseInfo(self, data):
		self.SetEnvDisplay(data)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnWeatherUpdate(self, data):
		config = data.get('config')
		display = None
		if config:
			display = config.get('display')
		self.SetWeather(data['weather'], display)

	@EngineEvent()
	def UiInitFinished(self, args):
		self._playerId = clientApi.GetLocalPlayerId()
		self._particleComp = CompFactory.CreateParticleSystem(self._playerId)
		self._playerPosComp = CompFactory.CreatePos(self._playerId)
		self._playerRotComp = CompFactory.CreateRot(self._playerId)
		self._cameraComp = CompFactory.CreateCamera(self._playerId)
		self._playerViewComp = CompFactory.CreatePlayerView(self._playerId)

	def SetSkyBox(self, skyboxImgs):
		skyBoxTextures = skyboxImgs
		if skyBoxTextures is None:
			skyBoxTextures = []
		texs = []
		for img in skyBoxTextures:
			texs.append('textures/environment/scuke_survive/'+img)
		CompFactory.CreateSkyRender(self.mLevelId).SetSkyTextures(texs)

	def SetWeather(self, name, weather):
		if self._currentWeatherState:
			self.RemoveWeatherState(self._currentWeatherState)
			# Reset
			if weather is None:
				self._currentWeatherState = None
				return
		if weather is None:
			return
		self.AddWeatherState(name, weather)

	def AddWeatherState(self, name, weather):
		modelComp = self._levelModelComp
		tween = None
		modelId = None
		state = {
			'name': name,
			'config': weather,
			'active': True
		}
		if name == PhaseWeatherEventEnum.SnowStorm or name == PhaseWeatherEventEnum.ModerateSnow:
			modelId = modelComp.CreateFreeModel(weather['model'])
			modelComp.SetModelMaterial(modelId, 'scuke_survive_weather')
			pos = self._playerPosComp.GetFootPos()
			modelComp.SetFreeModelPos(modelId, pos[0], pos[1], pos[2])
			density = weather.get('density', 1.0)
			speed = weather.get('speed', 1.0)
			fade = weather.get('fade', 5.0)
			color = weather.get('color', (1.0, 1.0, 1.0, 1.0))
			modelComp.SetExtraUniformValue(modelId, 1, (0.0, speed, 0.0, 0.0))
			modelComp.SetExtraUniformValue(modelId, 2, color)
			def _Update(state):
				return lambda value: self._SnowTweenUpdate(state, value)
			tween = TweenHandler('linear', fade, 0.0, density, _Update(state))
		state['tween'] = tween
		state['model'] = modelId
		self._currentWeatherState = state
		self._weatherStates.append(state)

	def RemoveWeatherState(self, state):
		modelComp = self._levelModelComp
		name = state['name']
		config = state['config']
		state['active'] = False
		if name == PhaseWeatherEventEnum.SnowStorm or name == PhaseWeatherEventEnum.ModerateSnow:
			modelId = state['model']
			extraValue = modelComp.GetExtraUniformValue(modelId, 1)
			density = float(extraValue[0])
			fade = config.get('fade', 5.0)
			def _Update(state):
				return lambda value: self._SnowTweenUpdate(state, value)
			def _End(state):
				return lambda : self._SnowTweenEnd(state)
			tween = TweenHandler('linear', fade, density, 0.0, _Update(state), _End(state))
			state['tween'] = tween

	def _SnowTweenUpdate(self, state, value):
		modelComp = self._levelModelComp
		if state and 'model' in state:
			modelId = state['model']
			config = state['config']
			speed = config.get('speed', 1.0)
			modelComp.SetExtraUniformValue(modelId, 1, (value, speed, 0.0, 0.0))

	def _SnowTweenEnd(self, state):
		modelComp = self._levelModelComp
		if 'model' in state:
			modelComp.RemoveFreeModel(state['model'])
			state['model'] = None

	def Update(self):
		self.UpdateSkyboxDisplay()
		self.DoPlayerWeatherMove()
		i = 0
		while i < len(self._weatherStates):
			state = self._weatherStates[i]
			removed = False
			tween = state['tween']
			if tween:
				tween.Update()
				if tween.Completed and not state['active']:
					removed = True
			else:
				removed = not state['active']
			if removed:
				self._weatherStates.pop(i)
			else:
				i += 1

	def DoPlayerWeatherMove(self):
		if not self._currentWeatherState or not self._playerPosComp:
			return
		pos = self._playerPosComp.GetFootPos()
		rot = self._playerRotComp.GetRot()

		pers = self._playerViewComp.GetPerspective()
		if self._lastPos:
			if 'model' in self._currentWeatherState:
				modelId = self._currentWeatherState['model']
				self._levelModelComp.SetFreeModelPos(modelId, pos[0], pos[1], pos[2])

		self._lastPos = pos
		self._lastRot = rot
		self._lastPers = pers

	def SetEnvDisplay(self, data):
		days = data['days']
		skyboxDisplays = EnvConfig['skybox']
		self._currentEnvDisplaySkybox = None
		for skyboxConfig in skyboxDisplays:
			if skyboxConfig['days'] <= days:
				self._currentEnvDisplaySkybox = skyboxConfig
		if self._currentEnvDisplaySkybox:
			self._currentEnvDisplaySkyboxActive = False
			if days > self._currentEnvDisplaySkybox['days']:
				self.SetSkyBox(self._currentEnvDisplaySkybox['end'])
				self._currentEnvDisplaySkybox = None

	def UpdateSkyboxDisplay(self):
		daytime = engineApiGac.GetTime() % 24000
		if self._currentEnvDisplaySkybox:
			startTime = self._currentEnvDisplaySkybox['startTime']
			endTime = self._currentEnvDisplaySkybox['endTime']
			if daytime >= startTime and not self._currentEnvDisplaySkyboxActive:
				self._currentEnvDisplaySkyboxActive = True
				self.SetSkyBox(self._currentEnvDisplaySkybox['start'])
			if daytime > endTime and self._currentEnvDisplaySkyboxActive:
				self._currentEnvDisplaySkyboxActive = False
				self.SetSkyBox(self._currentEnvDisplaySkybox['end'])
				self._currentEnvDisplaySkybox = None