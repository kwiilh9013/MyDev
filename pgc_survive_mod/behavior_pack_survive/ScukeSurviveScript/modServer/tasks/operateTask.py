# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.tasks.gameTask import GameTask


class OperateTask(GameTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(OperateTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._blocks = self._config['data'].get('blocks', None)
		self._items = self._config['data'].get('items', None)
		self._entities = self._config['data'].get('entities', None)

	@property
	def State(self):
		ret = super(OperateTask, self).State
		ret['p'] = self.ProgressMap
		return ret

	def CheckCondition(self):
		if self._changed and self._changedCall:
			self._changedCall(self)
			self._changed = False
		if self._items:
			if not self._CheckProgress(self._items):
				return False
		if self._blocks:
			if not self._CheckProgress(self._blocks):
				return False
		if self._entities:
			if not self._CheckProgress(self._entities):
				return False
		return True

	def OnEvent(self, name, args):
		if name == 'UseItem' and self._items:
			playerId = args['entityId']
			if playerId == self._eid:
				itemName = args['itemDict']['newItemName']
				if itemName in self._items:
					if itemName not in self._progressMap:
						self._progressMap[itemName] = 0
					self._progressMap[itemName] += 1
					self._progressMap['item[*]'] += 1
					self._changed = True
		elif name == 'OperateEntity' and self._entities:
			playerId = args['playerId']
			if playerId == self._eid:
				eid = args['interactEntityId']
				identifier = engineApiGas.GetIdentifierById(eid)
				if identifier in self._entities:
					if identifier not in self._progressMap:
						self._progressMap[identifier] = 0
					self._progressMap[identifier] += 1
					self._progressMap['entity[*]'] += 1
					self._changed = True
		elif name == 'UseBlock' and self._blocks:
			playerId = args['playerId']
			if playerId == self._eid:
				identifier = args['blockName']
				if identifier in self._blocks:
					if identifier not in self._progressMap:
						self._progressMap[identifier] = 0
					self._progressMap[identifier] += 1
					self._progressMap['block[*]'] += 1
					self._changed = True