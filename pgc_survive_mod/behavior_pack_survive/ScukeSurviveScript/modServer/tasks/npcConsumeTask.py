# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.tasks.consumeTask import ConsumeTask


class NpcConsumeTask(ConsumeTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(NpcConsumeTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)

	def OnEvent(self, name, args):
		if name == 'NpcConsumeItem':
			playerId = args['playerId']
			if playerId == self._eid and self._items:
				itemName = args['item']
				count = args['count']
				if itemName in self._items:
					if itemName not in self._progressMap:
						self._progressMap[itemName] = 0
					self._progressMap[itemName] += count
					self._progressMap['item[*]'] += count
					self._changed = True
		elif name == 'NpcConsumeEntity':
			playerId = args['playerId']
			if playerId == self._eid and self._entities:
				entityName = args['entity']
				count = args['count']
				if entityName in self._entities:
					if entityName not in self._progressMap:
						self._progressMap[entityName] = 0
					self._progressMap[entityName] += count
					self._progressMap['entity[*]'] += count
					self._changed = True