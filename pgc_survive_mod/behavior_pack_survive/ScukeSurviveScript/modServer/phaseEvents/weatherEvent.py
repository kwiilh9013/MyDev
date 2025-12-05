# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.phaseEvents.phaseEvent import PhaseEvent

class WeatherEvent(PhaseEvent):
	def __init__(self, system, name, eventStateChangedCall=None):
		super(WeatherEvent, self).__init__(system, name, eventStateChangedCall)
		self._lastTickTime = -1
		self._playerActiveMap = {}

	def TryPlace(self, days, daytime, eventsWeight, config):
		tickTime = days * 24000 + daytime
		if self._lastTickTime < 0:
			self._lastTickTime = tickTime
		if tickTime - self._lastTickTime < 0:
			self._lastTickTime = tickTime
		if tickTime - self._lastTickTime < config['placeInterval']:
			return False
		ret = super(WeatherEvent, self).TryPlace(days, daytime, eventsWeight, config)
		if ret:
			self._lastTickTime = tickTime
		return ret

	def EventUpdate(self, days, daytime):
		players = self._system.GetPlayers()
		for playerId in players:
			dim = engineApiGas.GetEntityDimensionId(playerId)
			dirty = False
			if playerId not in self._playerActiveMap:
				self._playerActiveMap[playerId] = dim
				dirty = True
			else:
				dirty = dim != self._playerActiveMap[playerId]
			dirty = dirty or self.TemperatureUpdate(playerId)
			if dirty:
				state = dim == 0
				info = self.BuildWeatherInfo(playerId, self.Name, state)
				if state:
					info['config'] = self.Config
				self._system.NotifyToClient(playerId, 'OnWeatherUpdate', info)
				self._system.BroadcastEvent('OnWeatherUpdate', info)

			self._playerActiveMap[playerId] = dim

	def TemperatureUpdate(self, playerId):
		return False

	def BuildWeatherInfo(self, playerId, name, state):
		info = {
			'playerId': playerId,
			'weather': name,
			'state': state,
		}
		return info

	def OnStateChange(self, state, days, daytime):
		players = self._system.GetPlayers()
		for playerId in players:
			dim = engineApiGas.GetEntityDimensionId(playerId)
			self._playerActiveMap[playerId] = dim
			state = state and dim == 0
			info = self.BuildWeatherInfo(playerId, self.Name, state)
			if state:
				info['config'] = self.Config
			self._system.NotifyToClient(playerId, 'OnWeatherUpdate', info)
			self._system.BroadcastEvent('OnWeatherUpdate', info)
		# 2024.9.30 去掉该功能
		# # 广播下雪的消息，影响车的行驶逻辑
		# Instance.mEventMgr.NotifyEvent(eventConfig.WeatherSubscribeEvent, info)
