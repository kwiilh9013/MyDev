# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.tasks.gameTask import GameTask
import mod.server.extraServerApi as serverApi

CompFactory = serverApi.GetEngineCompFactory()

class ArriveTask(GameTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(ArriveTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._posComp = CompFactory.CreatePos(eid)

	def CheckCondition(self):
		data = self._config['data']
		targetData = data['target']
		if 'minPos' in targetData:
			dim = engineApiGas.GetEntityDimensionId(self._eid)
			if dim != targetData['dim']:
				return False
			minPos = targetData['minPos']
			maxPos = targetData['maxPos']
			pos = self._posComp.GetFootPos()
			for i in range(0, 3):
				if pos[i] < minPos[i] or pos[i] > maxPos[i]:
					return False
		elif 'biomes' in targetData:
			biomes = targetData['biomes']
			pos = self._posComp.GetFootPos()
			dim = engineApiGas.GetEntityDimensionId(self._eid)
			biomeName = engineApiGas.GetBiomeName(pos, dim)
			if biomeName not in biomes:
				return False
		return True
