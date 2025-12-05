# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.tasks.arriveTask import ArriveTask
from ScukeSurviveScript.ScukeCore.server import engineApiGas
import mod.server.extraServerApi as serverApi

ItemPosType = serverApi.GetMinecraftEnum().ItemPosType

class DeliverTask(ArriveTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(DeliverTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._items = self._config['data'].get('items', None)
		self._entities = self._config['data'].get('entities', None)

	def CheckCondition(self):
		ret = super(DeliverTask, self).CheckCondition()
		if ret:
			self._progressMap = {'entity[*]': 0, 'item[*]': 0, 'block[*]': 0}
			items = self._items
			if items:
				itemsMap = self._progressMap
				self._GetItemsMap(ItemPosType.INVENTORY, items, itemsMap)
				self._GetItemsMap(ItemPosType.OFFHAND, items, itemsMap)
				self._GetItemsMap(ItemPosType.CARRIED, items, itemsMap)
				if not self._CheckProgress(items):
					return False
			entities = self._entities
			if entities:
				aroundEntities = engineApiGas.GetEntitiesAround(self._eid, 5)  # 自己范围内的实体
				if aroundEntities and len(aroundEntities) > 0:
					entitiesMap = self._progressMap
					for entityId in aroundEntities:
						comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
						identifier = comp.GetEngineTypeStr()
						if identifier in entities:
							if identifier not in entitiesMap:
								entitiesMap[identifier] = 0
							entitiesMap[identifier] += 1
							entitiesMap['entity[*]'] += 1
					if not self._CheckProgress(entities):
						return False
				else:
					return False

		return ret

	def _GetItemsMap(self, posType, targetItems, itemsMap):
		items = engineApiGas.GetPlayerAllItems(self._eid, posType)
		if items and len(items) > 0:
			for item in items:
				if item and item['newItemName'] in targetItems:
					itemName = item['newItemName']
					if itemName not in itemsMap:
						itemsMap[itemName] = 0
					itemsMap[itemName] += item['count']
					itemsMap['item[*]'] += item['count']
