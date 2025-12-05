# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modServer.phaseEvents.weatherEvent import WeatherEvent
import mod.server.extraServerApi as serverApi
import random

PlaceSnowInterval = 30

class WeatherSnowEvent(WeatherEvent):
	def __init__(self, system, name, eventStateChangedCall=None):
		super(WeatherSnowEvent, self).__init__(system, name, eventStateChangedCall)
		self._placeMap = {}
		self._blockInfoComp = serverApi.GetEngineCompFactory().CreateBlockInfo(system.mLevelId)
		self._tick = 0


	def OnStateChange(self, state, days, daytime):
		super(WeatherSnowEvent, self).OnStateChange(state, days, daytime)
		self._tick = 0

	def EventUpdate(self, days, daytime):
		super(WeatherSnowEvent, self).EventUpdate(days, daytime)
		interval = int(PlaceSnowInterval / self.Config.get('placeSnowSpeed', 1.0))
		if self._tick % interval == 0:
			self._placeMap = {}
			for playerId in self._playerActiveMap:
				dim = self._playerActiveMap[playerId]
				if dim == 0:
					self.RandomPlaceSnow(playerId, dim)
		self._tick += 1

	def RandomPlaceSnow(self, playerId, dim):
		range = (-64, 64)
		comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
		footPos = comp.GetFootPos()
		if footPos is None:
			return
		i = 0
		while i < 4:
			x = int(footPos[0] + random.randint(range[0], range[1]))
			z = int(footPos[2] + random.randint(range[0], range[1]))
			y = self._blockInfoComp.GetTopBlockHeight((x, z), dim)
			if y is not None:
				uid = '%d-%d-%d' % (x, y, z)
				if uid in self._placeMap:
					i += 1
					continue
				self._placeMap[uid] = True
				blockDict = self._blockInfoComp.GetBlockNew((x, y, z), dim)
				if blockDict['name'] != 'minecraft:snow_layer' and blockDict['name'].startswith('minecraft:'):
					collision = self._blockInfoComp.GetBlockCollision((x, y, z), dim)
					if collision['max'][1] - collision['min'][1] < 1:
						i += 1
						continue
					y += 1
					placeName = 'minecraft:snow_layer'
					if blockDict["name"] == "minecraft:water":
						placeName = 'minecraft:ice'
						y -= 1

					blockDict = {
						'name': placeName,
						'aux': 0
					}
					self._blockInfoComp.SetBlockNew((x, y, z), blockDict, 0, dim, updateNeighbors=False)
			i += 1
