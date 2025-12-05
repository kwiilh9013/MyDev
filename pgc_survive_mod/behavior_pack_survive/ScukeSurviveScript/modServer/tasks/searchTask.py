# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.tasks.boxCheckTask import BoxCheckTask
from ScukeSurviveScript.modServer.tasks.gameTask import GameTask
from ScukeSurviveScript.ScukeCore.server import engineApiGas
import mod.server.extraServerApi as serverApi

class SearchTask(GameTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(SearchTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._blockBoxCheckTask = None
		self._posComp = serverApi.GetEngineCompFactory().CreatePos(self._eid)
		self._blocks = self._config['data'].get('blocks', None)
		self._entities = self._config['data'].get('entities', None)
		self._progressMap = {'entity[*]': [], 'block[*]': []}
		if self._blocks:
			self._blockBoxCheckTask = BoxCheckTask(self._eid, self._BlockFilterCall, self._BlockTaskCompleted)
			self._StartBoxCheck()

	@property
	def State(self):
		ret = super(SearchTask, self).State
		ret['p'] = self.ProgressMap
		return ret

	def CheckCondition(self):
		data = self._config['data']
		radius = data['radius']
		blocks = self._blocks
		entities = self._entities
		if entities:
			aroundEntities = engineApiGas.GetEntitiesAround(self._eid, radius)
			if aroundEntities and len(aroundEntities) > 0:
				for entityId in aroundEntities:
					comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
					identifier = comp.GetEngineTypeStr()
					if identifier in entities:
						if identifier not in self._progressMap:
							self._progressMap[identifier] = []
						if entityId not in self._progressMap[identifier]:
							self._progressMap[identifier].append(entityId)
							self._progressMap['entity[*]'].append(entityId)
							self._changed = True
		if self._changed and self._changedCall:
			self._changedCall(self)
			self._changed = False
		if blocks:
			if not self._CheckProgress(blocks):
				return False
		if entities:
			if not self._CheckProgress(entities):
				return False
		return True

	def _CheckProgress(self, items):
		for key in items:
			if key.find('|') > -1:
				c = 0
				for k in self._progressMap:
					if key.find(k) > -1:
						c += len(self._progressMap[k])
				if items[key] > c:
					return False
			else:
				if key not in self._progressMap:
					return False
				if items[key] > len(self._progressMap[key]):
					return False
		return True

	def Tick(self):
		if self._blockBoxCheckTask:
			self._blockBoxCheckTask.Tick()

	def _BlockFilterCall(self, pos, block):
		blockName = block['name']
		if blockName in self._blocks:
			if blockName not in self._progressMap:
				self._progressMap[blockName] = []
			uid = str(pos)
			if uid not in self._progressMap[blockName]:
				self._progressMap[blockName].append(uid)
				self._progressMap['block[*]'].append(uid)
				self._changed = True

	def _BlockTaskCompleted(self, eid, blocks):
		self._StartBoxCheck()

	def _StartBoxCheck(self):
		if not self._blockBoxCheckTask:
			return
		dim = engineApiGas.GetEntityDimensionId(self._eid)
		data = self._config['data']
		radius = data['radius']
		self._blockBoxCheckTask.Start(dim, self._posComp.GetFootPos(), radius, 100)
