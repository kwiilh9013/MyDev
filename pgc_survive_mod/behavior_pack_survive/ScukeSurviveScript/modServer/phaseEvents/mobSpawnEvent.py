# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.phaseEvents.phaseEvent import PhaseEvent
import mod.server.extraServerApi as serverApi
import random


class MobSpawnEvent(PhaseEvent):
	def __init__(self, system, name, eventStateChangedCall=None):
		super(MobSpawnEvent, self).__init__(system, name, eventStateChangedCall)
		self._spawnEid = None

	def OnStateChange(self, state, days, daytime):
		dim = 0
		if state:
			range = self.Config['spawnRange']
			yRange = self.Config['spawnYRange']
			emptyHeight = self.Config['emptyHeight']
			mobs = self.Config['mobs']
			identifier = None
			r = random.random() * 100
			temp = 0
			for k, v in mobs.iteritems():
				temp += v
				if r <= temp:
					identifier = k
					break
			if identifier is None:
				return
			players = self._system.GetPlayers()
			for playerId in players:
				comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
				if engineApiGas.GetEntityDimensionId(playerId) != dim:
					continue
				footPos = comp.GetFootPos()
				if footPos is None:
					continue
				i = 0
				while i < 2:  # 尝试生成次数
					dir = (1 if random.random() > 0.5 else -1, 1 if random.random() > 0.5 else -1)
					x = int(footPos[0] + dir[0] * random.randint(range[0], range[1]))
					z = int(footPos[2] + dir[1] * random.randint(range[0], range[1]))
					y = int(footPos[1])
					offsetY = y - yRange
					yRanges = engineApiGas.GetValidYRanges(dim, x, y, z, yRange, emptyHeight)
					minYDis = -1
					minYRange = None
					for range in yRanges:
						dis = abs(range[0] - offsetY)
						if minYDis < 0 or dis < minYDis:
							minYDis = dis
							minYRange = range
					if minYRange is not None:
						pos = (x, minYRange[0], z)
						self._spawnEid = self._system.CreateEngineEntityByTypeStr(identifier, pos, (0, 0), dim)
						return
					i += 1
