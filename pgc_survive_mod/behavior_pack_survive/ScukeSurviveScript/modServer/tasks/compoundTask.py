# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.tasks.gameTask import GameTask


class CompoundTask(GameTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(CompoundTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._blocks = self._config['data'].get('blocks', None)
		self._items = self._config['data'].get('items', None)
		self._entities = self._config['data'].get('entities', None)

	@property
	def State(self):
		ret = super(CompoundTask, self).State
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
		if name == 'RecipeCompound' and self._items:
			playerId = args['playerId']
			results = args['results']
			if playerId == self._eid:
				for item in results:
					itemName = item['fullItemName']
					if itemName in self._items:
						if itemName not in self._progressMap:
							self._progressMap[itemName] = 0
						self._progressMap[itemName] += item['num']
						self._progressMap['item[*]'] += item['num']
						self._changed = True
		elif name == 'ElectricCraftingCompound' and self._items:
			playerId = args['playerId']
			if playerId == self._eid:
				itemName = args['itemName']
				count = args['count']
				if itemName in self._items:
					if itemName not in self._progressMap:
						self._progressMap[itemName] = 0
					self._progressMap[itemName] += count
					self._progressMap['item[*]'] += count
					self._changed = True
		elif name == 'PlaceBlock' and self._blocks:
			playerId = args['entityId']
			blockName = args['fullName']
			if playerId == self._eid:
				if blockName in self._blocks:
					if blockName not in self._progressMap:
						self._progressMap[blockName] = 0
					self._progressMap[blockName] += 1
					self._progressMap['block[*]'] += 1
					self._changed = True