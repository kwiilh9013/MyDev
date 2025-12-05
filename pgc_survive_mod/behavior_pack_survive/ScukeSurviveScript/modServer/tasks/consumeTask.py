# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.tasks.gameTask import GameTask


class ConsumeTask(GameTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(ConsumeTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._blocks = self._config['data'].get('blocks', None)
		self._items = self._config['data'].get('items', None)
		self._entities = self._config['data'].get('entities', None)

	@property
	def State(self):
		ret = super(ConsumeTask, self).State
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
		if name == 'EatFood' and self._items:
			playerId = args['playerId']
			if playerId == self._eid:
				itemName = args['identifier']
				if itemName in self._items:
					if itemName not in self._progressMap:
						self._progressMap[itemName] = 0
					self._progressMap[itemName] += 1
					self._progressMap['item[*]'] += 1
					self._changed = True
		elif name == 'KillEntity' and self._entities:
			playerId = args['playerId']
			if playerId == self._eid:
				identifier = args['identifier']
				if identifier in self._entities:
					if identifier not in self._progressMap:
						self._progressMap[identifier] = 0
					self._progressMap[identifier] += 1
					self._progressMap['entity[*]'] += 1
					self._changed = True
		elif name == 'DestroyBlock' and self._blocks:
			playerId = args['playerId']
			if playerId == self._eid:
				identifier = args['fullName']
				if identifier in self._blocks:
					if identifier not in self._progressMap:
						self._progressMap[identifier] = 0
					self._progressMap[identifier] += 1
					self._progressMap['block[*]'] += 1
					self._changed = True