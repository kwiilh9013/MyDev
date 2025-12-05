# -*- coding: utf-8 -*-
import random

from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.dialogueServerData import DialogueCurrentState, DialogueServerData
from ScukeSurviveScript.modCommon.handler.dialogueHandler import DialogueHandler
from ScukeSurviveScript.modCommon.handler.expressionHandler import evaluate
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon.cfg.dialogueConfig import Config as DialogueConfig
from ScukeSurviveScript.modCommon.cfg.taskConfig import GetTaskConfig
from ScukeSurviveScript.modCommon.cfg.dialogueNodesConfig import Config as DialogueNodesConfig
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_planet_booster import Config as Scuke_planetBooster

ComFactory = serverApi.GetEngineCompFactory()

ValidActivatePlanetBoosters = [
	Scuke_planetBooster['identifier'],
]


class DialogueServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(DialogueServerSystem, self).__init__(namespace, systemName)
		self._playerDialogueContextMap = {}
		self._playerDialogue = {}
		self._entryFilterFuncs = {
			'HasTamed': self._EF_HasTamed,
			'PhasePlanetBoosterActivated': self._EF_PhaseBoosterActivated,
			'PlanetBoosterValid': self._EF_ClosestPlanetBoosterValid,
			'PlanetBoosterActivated': self._EF_ClosestPlanetBoosterActivated,
			'HasNpcConsumeTask': self._EF_HasNpcConsumeTask,
			'HasNpcConsumeCreeperTask': self._EF_HasNpcConsumeCreeperTask,
			'HasGuardPlanetBoosterTask': self._EF_HasGuardPlanetBoosterTask,
			'PlanetBoosterHasCreeper': self._EF_PhaseBoosterHasCreeper,
		}
		self.__buildingSystem__ = None
		self.__taskSystem__ = None
		self.__battleEventSystem__ = None

	@property
	def _buildingSystem(self):
		if not self.__buildingSystem__:
			self.__buildingSystem__ = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildingServerSystem)
		return self.__buildingSystem__

	@property
	def _taskSystem(self):
		if not self.__taskSystem__:
			self.__taskSystem__ = serverApi.GetSystem(modConfig.ModNameSpace,
														  modConfig.ServerSystemEnum.TaskServerSystem)
		return self.__taskSystem__

	@property
	def _battleEventSystem(self):
		if not self.__battleEventSystem__:
			self.__battleEventSystem__ = serverApi.GetSystem(modConfig.ModNameSpace,
													  modConfig.ServerSystemEnum.BattleEventServerSystem)
		return self.__battleEventSystem__

	@EngineEvent()
	def AddServerPlayerEvent(self, data):
		playerId = data['id']
		dialogueData = self.GetDialogueData(playerId)
		currentData = dialogueData.get('current', None)
		if currentData:
			currentData = DatasetObj.Format(DialogueCurrentState, currentData)
			# 暴力解除对话
			comp = ComFactory.CreateEntityDefinitions(currentData['eid'])
			comp.SetSitting(False)
			dialogueData['current'] = None
		self._playerDialogueContextMap[playerId] = dialogueData

	def GetDialogueData(self, eid):
		data = Instance.mDatasetManager.GetEntityData(eid, 'dialogues')
		if not data:
			data = DatasetObj.Build(DialogueServerData)
			Instance.mDatasetManager.SetEntityData(eid, 'dialogues', data)
		else:
			data = DatasetObj.Format(DialogueServerData, data)
		return data

	def FlushDialogueData(self, eid):
		data = self._playerDialogueContextMap[eid]
		Instance.mDatasetManager.SetEntityData(eid, 'dialogues', data)

	@EngineEvent()
	def PlayerDoInteractServerEvent(self, args):
		playerId = args['playerId']
		targetId = args['interactEntityId']
		identifier = engineApiGas.GetIdentifierById(targetId)
		if identifier not in DialogueConfig:
			return
		if self._battleEventSystem:
			if self._battleEventSystem.CheckOnBattleEvent(playerId):
				engineApiGas.NotifyOneMessage(playerId, '§c战斗中无法进行对话')
				return
		config = DialogueConfig[identifier]
		nodeId = self.CheckDialogueEntryNodeId(playerId, targetId, config)
		if nodeId is None:
			return
		dialogueData = self._playerDialogueContextMap[playerId]
		if dialogueData.get('current', None) is not None:
			return
		self.SendMsgToClient(playerId, 'OpenDialogue', {
			'identifier': identifier,
			'entryId': nodeId,
			'entityId': targetId,
		})
		dialogueHandler = DialogueHandler(dialogueData, targetId, nodeId)
		self._playerDialogue[playerId] = dialogueHandler
		comp = ComFactory.CreateEntityDefinitions(targetId)
		isSitting = comp.IsSitting()
		comp.SetSitting(True)
		state = DatasetObj.Build(DialogueCurrentState)
		state['entryId'] = nodeId
		state['nodeId'] = nodeId
		state['eid'] = targetId
		state['identifier'] = identifier
		state['sitting'] = isSitting
		dialogueData['current'] = state
		dialogueHandler.Update()
		self.ApplyDialogueStartAction(playerId, dialogueHandler)
		if nodeId not in dialogueData['history']:
			dialogueData['history'].append(nodeId)
		self.FlushDialogueData(playerId)


	def CheckDialogueEntryNodeId(self, playerId, targetId, config):
		for k, v in config['nodes'].iteritems():
			if isinstance(v, bool):
				if v:
					return k
			elif isinstance(v, str):
				condition = self.CheckEntryFilter(playerId, targetId, v)
				if condition:
					return k
		return None

	def CheckEntryFilter(self, fromId, targetId, data):
		if type(data) == bool:
			return data
		return self.ComputeScukeLang(fromId, targetId, data)

	def ComputeScukeLang(self, fromId, targetId, valueStr):
		data = self.BuildScukeLangData(fromId, targetId)
		ret = evaluate(valueStr, data)
		if type(ret) == float or type(ret) == int:
			ret = ret > 0
		return ret

	def BuildScukeLangData(self, fromId, targetId):
		data = {}
		for k, f in self._entryFilterFuncs.iteritems():
			def wrap(func, a, b):
				return lambda: func(a, b)
			data['@'+k] = wrap(f, fromId, targetId)
		return data

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.DialogueClientSystem)
	def OnDialogueNodeNext(self, data):
		playerId = data['playerId']
		nextNodeId = data['nodeId']
		index = data.get('index', -1)
		if playerId not in self._playerDialogue:
			return
		dialogueHandler = self._playerDialogue[playerId]
		dialogueData = self._playerDialogueContextMap[playerId]
		if nextNodeId == '-1':
			handler = self._playerDialogue.pop(playerId)
			comp = ComFactory.CreateEntityDefinitions(handler.EntityId)
			currentData = dialogueData.get('current', None)
			comp.SetSitting(currentData['sitting'])
			self.ApplyDialogueEndAction(playerId, dialogueHandler)
			del dialogueData['current']
			self.FlushDialogueData(playerId)
			return
		else:
			self.ApplyDialogueEndAction(playerId, dialogueHandler)
			currentData = dialogueData.get('current', None)
			if currentData:
				currentData['nodeId'] = nextNodeId
				if nextNodeId not in dialogueData['history']:
					dialogueData['history'].append(nextNodeId)
				self.FlushDialogueData(playerId)
		info = {
			'entryId': nextNodeId,
		}
		config = DialogueNodesConfig[nextNodeId]
		if config['next'] == '@GetNpcConsumeTasks':  # 获取当前Npc交付任务选项
			npcIdentifier = engineApiGas.GetEngineTypeStr(dialogueHandler.EntityId)
			taskUids = self._taskSystem.GetPendingTasksByGroup(playerId, npcIdentifier, 'npcConsume')
			nextData = []
			for uid in taskUids:
				taskConfig = GetTaskConfig(uid)
				if taskConfig:
					items = taskConfig['data'].get('items', [])
					for item, count in items.iteritems():
						dConfig = {
							'_index': len(nextData),
							'_template': '@NpcConsumeTaskTemplate',
							'text': taskConfig['desc'],
							'phases': [
								{
									'type': 'text',
									'text': taskConfig['info'],
								}
							],
							'next': None,
							'startActionData': None,
							'endActionData': {
								'ConsumeItemToNpc': {
									'item': item,
									'value': count
								}
							},
						}
						nextData.append(dConfig)
			if len(nextData) <= 0:
				nextData = None
			info['override'] = {
				'next': nextData
			}
		elif config['next'] == '@GetNpcConsumeCreeperTasks':  # 为交付苦力怕实体定制
			npcIdentifier = engineApiGas.GetEngineTypeStr(dialogueHandler.EntityId)
			taskUids = self._taskSystem.GetPendingTasksByGroup(playerId, npcIdentifier, 'npcConsumeCreeper')
			nextData = []
			for uid in taskUids:
				taskConfig = GetTaskConfig(uid)
				if taskConfig:
					entities = taskConfig['data'].get('entities', [])
					for item, count in entities.iteritems():
						dConfig = {
							'_index': len(nextData),
							'_template': '@NpcConsumeTaskTemplate',
							'text': taskConfig['desc'],
							'phases': [
								{
									'type': 'text',
									'text': taskConfig['info'],
								}
							],
							'next': None,
							'startActionData': None,
							'endActionData': {
								'SendGoldenCreeper': {
									'value': count
								}
							},
						}
						nextData.append(dConfig)
			if len(nextData) <= 0:
				nextData = None
			info['override'] = {
				'next': nextData
			}
		elif index > -1:
			info['override'] = dialogueHandler.NodeConfig['next'][index]
		self.SendMsgToClient(playerId, 'NextDialogue', info)
		dialogueHandler.ChangeNode(nextNodeId, info.get('override', None))
		dialogueHandler.Update()
		self.ApplyDialogueStartAction(playerId, dialogueHandler)


	def ApplyDialogueStartAction(self, playerId, handler):
		self._ApplyDialogueAction(playerId, handler.EntityId, handler.NodeConfig.get('startActionData', None))

	def ApplyDialogueEndAction(self, playerId, handler):
		self._ApplyDialogueAction(playerId, handler.EntityId, handler.NodeConfig.get('endActionData', None))

	def _ApplyDialogueAction(self, fromId, targetId, actionData):
		if not actionData:
			return
		for op in actionData:
			data = actionData[op]
			value = data['value']
			if op == 'SetSitting':
				comp = ComFactory.CreateEntityDefinitions(targetId)
				comp.SetSitting(value)
			elif op == 'SetCarrying':
				if value:
					comp = ComFactory.CreateRide(fromId)
					comp.SetRiderRideEntity(targetId, fromId)
				else:
					comp = ComFactory.CreateRide(targetId)
					comp.StopEntityRiding()
			elif op == 'UseItemToNpc':
				targetItem = data['item']
				itemName = data.get('name', None)
				if itemName is None:
					itemName = engineApiGas.GetChinese('item.%s.name' % targetItem.replace('minecraft:', ''))
				ItemPosType = serverApi.GetMinecraftEnum().ItemPosType
				itemComp = serverApi.GetEngineCompFactory().CreateItem(fromId)
				invItems = itemComp.GetPlayerAllItems(ItemPosType.INVENTORY, True)
				carryId = engineApiGas.GetSelectSlotId(fromId)
				itemDict = None
				replaceIndex = -1
				i = 0
				while i < len(invItems):
					item = invItems[i]
					if item and item['newItemName'] == targetItem:
						replaceIndex = i
						itemDict = item
						break
					i += 1
				if itemDict:
					if replaceIndex > -1:
						itemComp.SetInvItemExchange(carryId, replaceIndex)
					comp = serverApi.GetEngineCompFactory().CreateBlockInfo(fromId)
					comp.PlayerUseItemToEntity(targetId)
					if replaceIndex > -1:
						itemComp.SetInvItemExchange(carryId, replaceIndex)
					engineApiGas.NotifyOneMessage(fromId, '已使用物品：%s' % itemName)
				else:
					engineApiGas.NotifyOneMessage(fromId, '§c缺少物品：%s' % itemName)
			elif op == 'ConsumeItemToNpc':
				targetItem = data['item']
				itemName = data.get('name', None)
				if itemName is None:
					itemName = engineApiGas.GetChinese('item.%s.name' % targetItem.replace('minecraft:', ''))
				ret = self.ReduceItem(fromId, targetItem, value)
				if ret:
					self.BroadcastEvent('OnNpcConsumeItem', {
						'playerId': fromId,
						'npcId': targetId,
						'item': targetItem,
						'count': value,
					})
					engineApiGas.NotifyOneMessage(fromId, '已交付物品：%sx%d' % (itemName, value))
				else:
					engineApiGas.NotifyOneMessage(fromId, '§c物品不足：%sx%d' % (itemName, value))
			elif op == 'SendGoldenCreeper':
				entities = engineApiGas.GetEntitiesAround(targetId, 5, True)
				entityIdentifier = 'scuke_survive:npc_golden_creeper'
				validTargets = []
				if entities and len(entities) > 0:
					for eid in entities:
						if engineApiGas.GetEngineTypeStr(eid) == entityIdentifier:
							validTargets.append(eid)
							if len(validTargets) >= value:
								break
				# TODO 运送逻辑
				if len(validTargets) >= value:
					self.BroadcastEvent('OnNpcConsumeEntity', {
						'playerId': fromId,
						'npcId': targetId,
						'entity': entityIdentifier,
						'count': value,
					})
					self.BroadcastEvent('OnDialogueSendGoldenCreeper', {
						'fromId': fromId,
						'targetId': targetId,
						'state': 'success',
						'targets': validTargets
					})
					engineApiGas.NotifyOneMessage(fromId, '已交付：黄金苦力怕x%d' % value)
				else:
					self.BroadcastEvent('OnDialogueSendGoldenCreeper', {
						'fromId': fromId,
						'targetId': targetId,
						'state': 'failed'
					})
					engineApiGas.NotifyOneMessage(fromId, '§c周围没有足够的 黄金苦力怕x%d' % value)
			elif op == 'SpawnCar':
				entities = engineApiGas.GetEntitiesAround(targetId, 64, True)
				entityIdentifier = 'scuke_survive:base_car'
				brokenCarIdentifier = 'scuke_survive:base_car_broken'
				validTargets = []
				if entities and len(entities) > 0:
					for eid in entities:
						identifier = engineApiGas.GetEngineTypeStr(eid)
						if identifier == entityIdentifier or identifier == brokenCarIdentifier:
							validTargets.append(eid)
				if len(validTargets) <= 0:
					if self.SpawnEntityAround(targetId, entityIdentifier, (10, 10), 8, 5):
						engineApiGas.NotifyOneMessage(fromId, '附近生成基地车')
					else:
						engineApiGas.NotifyOneMessage(fromId, '§c无法生成基地车')
				else:
					engineApiGas.NotifyOneMessage(fromId, '§c附近有基地车了，不要贪心')
			elif op == 'SpawnGoldenCreeper':
				entities = engineApiGas.GetEntitiesAround(targetId, 16, True)
				entityIdentifier = 'scuke_survive:npc_golden_creeper'
				validTargets = []
				if entities and len(entities) > 0:
					for eid in entities:
						if engineApiGas.GetEngineTypeStr(eid) == entityIdentifier:
							validTargets.append(eid)
				if len(validTargets) <= 0:
					if self.SpawnEntityAround(targetId, entityIdentifier, (6, 6), 8, 2):
						engineApiGas.NotifyOneMessage(fromId, '附近生成黄金苦力怕')
					else:
						engineApiGas.NotifyOneMessage(fromId, '§c无法生成黄金苦力怕')
				else:
					engineApiGas.NotifyOneMessage(fromId, '§c附近有黄金苦力怕了，不要贪心')
			elif op == 'StartGuardPlanetBooster':
				self.BroadcastEvent('StartGuardPlanetBooster', {
					'playerId': fromId,
					'target': targetId,
				})

	def SpawnEntityAround(self, eid, identifier, range, yRange, height):
		dir = (1 if random.random() > 0.5 else -1, 1 if random.random() > 0.5 else -1)
		footPos = engineApiGas.GetEntityFootPos(eid)
		dim = engineApiGas.GetEntityDimensionId(eid)
		x = int(footPos[0] + dir[0] * random.randint(range[0], range[1]))
		z = int(footPos[2] + dir[1] * random.randint(range[0], range[1]))
		y = int(footPos[1])
		offsetY = y - yRange
		yRanges = engineApiGas.GetValidYRanges(dim, x, y, z, yRange, height)
		minYDis = -1
		minYRange = None
		for range in yRanges:
			dis = abs(range[0] - offsetY)
			if minYDis < 0 or dis < minYDis:
				minYDis = dis
				minYRange = range
		if minYRange is not None:
			pos = (x, minYRange[0], z)
			return self.CreateEngineEntityByTypeStr(identifier, pos, (0, 0), dim) != '-1'
		return False

	def ReduceItem(self, eid, identifier, count):
		itemComp = serverApi.GetEngineCompFactory().CreateItem(eid)
		allItems = itemComp.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
		remainingCount = count
		for slotPos, itemDict in enumerate(allItems):
			if itemDict and itemDict['itemName'] == identifier:
				item_count = itemDict['count']
				if item_count >= remainingCount:
					itemComp.SetInvItemNum(slotPos, item_count - remainingCount)
					return True
				else:
					itemComp.SetInvItemNum(slotPos, 0)
					remainingCount -= item_count

		return False

	# region scukelang函数
	def _EF_HasTamed(self, fromId, targetId):
		comp = ComFactory.CreateActorOwner(targetId)
		return comp.GetEntityOwner() == fromId

	def __GetClosestPlanetBooster(self, fromId, targetId):
		pos = engineApiGas.GetEntityPos(targetId)
		buildings = self._buildingSystem.GetAllBuildings()
		closestBuilding = None
		minDis = -1
		for building in buildings:
			if building['identifier'] not in ValidActivatePlanetBoosters:
				continue
			buildingPos = building['pos']
			dis = MathUtils.TupleLength(MathUtils.TupleSub(buildingPos, pos))
			if minDis < 0 or dis < minDis:
				closestBuilding = building
				minDis = dis
		if minDis > 48:
			return None
		return closestBuilding

	def _EF_ClosestPlanetBoosterValid(self, fromId, targetId):
		return self.__GetClosestPlanetBooster(fromId, targetId) is not None

	def _EF_ClosestPlanetBoosterActivated(self, fromId, targetId):
		building = self.__GetClosestPlanetBooster(fromId, targetId)
		if not building:
			return False
		return building['data'].get('activated', False)

	def _EF_PhaseBoosterActivated(self, fromId, targetId):
		return self._taskSystem.GetAccumulationByFullKey('-1', 'PlanetBooster.phase_activated')

	def _EF_HasNpcConsumeTask(self, fromId, targetId):
		npcIdentifier = engineApiGas.GetEngineTypeStr(targetId)
		taskUids = self._taskSystem.GetPendingTasksByGroup(fromId, npcIdentifier, 'npcConsume')
		return len(taskUids) > 0

	def _EF_HasNpcConsumeCreeperTask(self, fromId, targetId):
		npcIdentifier = engineApiGas.GetEngineTypeStr(targetId)
		taskUids = self._taskSystem.GetPendingTasksByGroup(fromId, npcIdentifier, 'npcConsumeCreeper')
		return len(taskUids) > 0

	def _EF_HasGuardPlanetBoosterTask(self, fromId, targetId):
		npcIdentifier = engineApiGas.GetEngineTypeStr(targetId)
		taskUids = self._taskSystem.GetPendingTasksByGroup(fromId, npcIdentifier, 'guardPlanetBooster')
		return len(taskUids) > 0

	def _EF_PhaseBoosterHasCreeper(self, fromId, targetId):
		building = self.__GetClosestPlanetBooster(fromId, targetId)
		if not building:
			return False
		return building['data'].get('consumeCreeper', False)
	# endregion

	@EngineEvent()
	def AddEntityServerEvent(self, args):
		id = args['id']
		identifier = args['engineTypeStr']
		if identifier.startswith(modConfig.NPCIdentifierPrefix):
			comp = serverApi.GetEngineCompFactory().CreateName(id)
			comp.SetName(engineApiGas.GetChinese('entity.%s.name' % identifier))
