# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.defines.phaseEventEnum import PhaseWeatherEventEnum
from ScukeSurviveScript.modServer.phaseEvents.weatherEvent import WeatherEvent
import mod.server.extraServerApi as serverApi
import random

SnowBiomes = {
	'frozen_river': -1,
	'frozen_ocean': -1,
	'ice_plains': -1,
	'ice_plains_spikes': -1,
	'grove': -1,
	'snowy_slopes': -1,
	'jagged_peaks': -1,
	'frozen_peaks': -1,
	'cold_taiga': -1,
	'cold_beach': -1,
	'extreme_hills': 130,
	'extreme_hills_plus_trees': 130,
	'extreme_hills_mutated': 130,
	'stone_beach': 130,
	'dripstone_caves': 130,
	'taiga': 160,
	'redwood_taiga_mutated': 160,
	'mega_taiga': 200,
	'meadow': 200,
	'cherry_grove': 200,
}

class WeatherRainEvent(WeatherEvent):
	def __init__(self, system, name, eventStateChangedCall=None):
		super(WeatherRainEvent, self).__init__(system, name, eventStateChangedCall)
		self._biomeComp = serverApi.GetEngineCompFactory().CreateBiome(serverApi.GetLevelId())
		self._weatherComp = serverApi.GetEngineCompFactory().CreateWeather(serverApi.GetLevelId())
		self._playerSnowing = {}

	def OnStateChange(self, state, days, daytime):
		super(WeatherRainEvent, self).OnStateChange(state, days, daytime)
		isThunder = self.Name == PhaseWeatherEventEnum.Thunder
		density = self.Config.get('density', 1.0)
		if state:
			self._playerSnowing = {}
		else:
			density = 0.0
		self._weatherComp.SetRaining(density, self.EndTime - self.StartTime)
		if isThunder:
			self._weatherComp.SetThunder(density, self.EndTime - self.StartTime)


	def BuildWeatherInfo(self, playerId, name, state):
		if playerId not in self._playerSnowing:
			self._playerSnowing[playerId] = False
		ret = super(WeatherRainEvent, self).BuildWeatherInfo(playerId, name, state)
		ret['snowing'] = self._playerSnowing[playerId]
		return ret

	def TemperatureUpdate(self, playerId):
		if playerId not in self._playerSnowing:
			self._playerSnowing[playerId] = False
		prevSnowing = self._playerSnowing[playerId]
		pos = engineApiGas.GetEntityFootPos(playerId)
		if pos is None:
			return False
		biomeName = self._biomeComp.GetBiomeName(pos, 0)
		snowing = False
		if biomeName in SnowBiomes:
			snowing = SnowBiomes[biomeName] < 0 or pos[1] > SnowBiomes[biomeName]
		self._playerSnowing[playerId] = snowing
		return prevSnowing != snowing
