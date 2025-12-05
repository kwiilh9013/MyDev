# -*- coding: utf-8 -*-
import time

from ScukeSurviveScript.ScukeCore.server.api.serverApiMgr import SpawnItemsToInventory
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.taskServerData import TaskServerData, TaskCompletedState, \
	TaskReceivedState, TaskAccumulationsData
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.taskConfig import Config as TaskConfig
from ScukeSurviveScript.modCommon.cfg.taskConfig import GetTaskConfig
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.modCommon import eventConfig

CompFactory = serverApi.GetEngineCompFactory()

from ScukeSurviveScript.modServer.tasks.gameTask import GameTask
from ScukeSurviveScript.modServer.tasks.compoundTask import CompoundTask
from ScukeSurviveScript.modServer.tasks.deliverTask import DeliverTask
from ScukeSurviveScript.modServer.tasks.gameTask import TaskBuilder
from ScukeSurviveScript.modServer.tasks.arriveTask import ArriveTask
from ScukeSurviveScript.modServer.tasks.numericTask import NumericTask
from ScukeSurviveScript.modServer.tasks.searchTask import SearchTask
from ScukeSurviveScript.modServer.tasks.consumeTask import ConsumeTask
from ScukeSurviveScript.modServer.tasks.npcConsumeTask import NpcConsumeTask
from ScukeSurviveScript.modServer.tasks.operateTask import OperateTask
from ScukeSurviveScript.modServer.tasks.guardPlanetBoosterTask import GuardPlanetBoosterTask

TaskBuilder.BindingTask('default', GameTask)  # 默认走手动完成
TaskBuilder.BindingTask('arrive', ArriveTask)  # 到达
TaskBuilder.BindingTask('deliver', DeliverTask)  # 运送
TaskBuilder.BindingTask('search', SearchTask)  # 搜寻
TaskBuilder.BindingTask('compound', CompoundTask)  # 合成放置
TaskBuilder.BindingTask('consume', ConsumeTask)  # 消耗破坏击杀
TaskBuilder.BindingTask('npcConsume', NpcConsumeTask)  # NPC交付
TaskBuilder.BindingTask('npcConsumeCreeper', NpcConsumeTask)  # NPC交付Creeper
TaskBuilder.BindingTask('guardPlanetBooster', GuardPlanetBoosterTask)  # 守卫发动机任务
TaskBuilder.BindingTask('operate', OperateTask)  # 使用物品、方块、实体交互
TaskBuilder.BindingTask('numeric', NumericTask)  # 数值累计类

TaskUpdateInterval = 30

AutoPendingTasks = []


class TaskServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(TaskServerSystem, self).__init__(namespace, systemName)
		self._tick = 0
		self._lastUpdateTime = time.time()
		self._tasksDataMap = {}
		self._tasksFlushTime = {}
		self._tasksSyncData = {}
		self._accumulationsDataMap = {}
		self._tasksMap = {}
		self._tickTasks = []
		self._eventTasks = []
		self._phaseConfig = None  # 主线任务相关
		self._accumulationsDataMap['-1'] = self.GetAccumulationData('-1')
		self._hostPlayer = None  # 房主
		# 初始化事件相关
		comp = serverApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(self.mLevelId)
		comp.AddBlockItemListenForUseEvent('minecraft:crafting_table')
		# 初始化自动任务
		for uid, item in TaskConfig.iteritems():
			auto = item.get('auto', False)
			if auto:
				AutoPendingTasks.append(uid)

		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.GetRewardsPopupEvent, self.GetRewardsPopupEvent)

	def Destroy(self):
		# 取消订阅
		Instance.mEventMgr.UnRegisterEvent(eventConfig.GetRewardsPopupEvent, self.GetRewardsPopupEvent)
		return super(TaskServerSystem, self).Destroy()

	def GetTaskData(self, eid):
		data = Instance.mDatasetManager.GetEntityData(eid, 'tasks')
		if not data:
			data = DatasetObj.Build(TaskServerData)
			Instance.mDatasetManager.SetEntityData(eid, 'tasks', data)
		else:
			data = DatasetObj.Format(TaskServerData, data)
		return data

	def GetAccumulationData(self, eid):
		data = None
		if eid == '-1':
			data = Instance.mDatasetManager.GetLevelData('accumulations')
		else:
			data = Instance.mDatasetManager.GetEntityData(eid, 'accumulations')
		if not data:
			data = DatasetObj.Build(TaskAccumulationsData)
			if eid == '-1':
				Instance.mDatasetManager.SetLevelData('accumulations', data)
			else:
				Instance.mDatasetManager.SetEntityData(eid, 'accumulations', data)
		else:
			data = DatasetObj.Format(TaskAccumulationsData, data)
		return data

	def FlushTaskData(self, eid):
		data = self._tasksDataMap[eid]
		Instance.mDatasetManager.SetEntityData(eid, 'tasks', data)
		self._tasksFlushTime[eid] = time.time()
		self.SyncClientTask(eid)

	def FlushAccumulationData(self, eid):
		data = self._accumulationsDataMap[eid]
		Instance.mDatasetManager.SetEntityData(eid, 'accumulations', data)

	@EngineEvent()
	def AddServerPlayerEvent(self, data):
		playerId = data['id']
		if self._hostPlayer is None:
			self._hostPlayer = playerId
		self._tasksFlushTime[playerId] = 0
		self._accumulationsDataMap[playerId] = self.GetAccumulationData(playerId)
		#self.logger.debug('Player %r Accumulations %r' % (playerId, self._accumulationsDataMap[playerId]))
		tasksData = self.GetTaskData(playerId)
		pendingTasks = tasksData['pendingTasks']
		completedTasks = tasksData['completedTasks']
		receivedTasks = tasksData['receivedTasks']
		tasks = []
		self._tasksDataMap[playerId] = tasksData
		self._tasksMap[playerId] = tasks
		curTaskUids = []
		completedTaskUids = []
		mainTask = None
		mainTaskConfig = None
		mainTaskDepends = None
		if self._phaseConfig:
			mainTask = self._phaseConfig['task']
			mainTaskConfig = GetTaskConfig(mainTask)
			if mainTaskConfig:
				mainTaskDepends = mainTaskConfig.get('depends', [])
		needRemoveStates = []
		for state in pendingTasks:
			uid = state['uid']
			task = TaskBuilder.GetTask(self, playerId, uid, self.OnTaskCompleted, self.OnTaskFailed, self.OnTaskChanged)
			if task:
				# 主线任务对齐
				if mainTaskConfig:
					taskBranch = task.Config.get('branch', '')
					if taskBranch == 'main' and uid != mainTask:
						needRemoveStates.append(state)
						continue
					if taskBranch == 'main_depends' and task.Uid not in mainTaskDepends:
						needRemoveStates.append(state)
						continue
					if playerId != self._hostPlayer and (taskBranch == 'main' or taskBranch == 'main_depends'):
						needRemoveStates.append(state)
						continue
				task.FromData(state)
				tasks.append(task)
				self._PendingTaskWithType(task)
				curTaskUids.append(uid)
		for state in needRemoveStates:
			pendingTasks.remove(state)
		for state in completedTasks:
			uid = state['uid']
			completedTaskUids.append(uid)
		for state in receivedTasks:
			uid = state['uid']
			completedTaskUids.append(uid)
		# 加入自动任务
		for uid in AutoPendingTasks:
			if uid in curTaskUids or uid in completedTaskUids:
				continue
			self.PendingTask(playerId, uid)
		# 主线任务加入
		notifyMainTask = False
		if mainTaskConfig and mainTask not in curTaskUids and mainTask not in completedTaskUids:
			if playerId == self._hostPlayer:
				self.PendingTask(playerId, mainTask)
				notifyMainTask = True
		if mainTaskConfig and mainTask not in completedTaskUids:  # 依赖任务刷新
			if playerId == self._hostPlayer:
				self.PendingDependsTask(playerId, mainTaskConfig)
		syncData = self.GetSyncClientTaskData(playerId)
		syncData['notifyMainTask'] = notifyMainTask
		self.FlushTaskData(playerId)
		#self.logger.debug('Player %r PendingTasks %r' % (playerId, pendingTasks))
		#self.logger.debug('Player %r CompletedTasks %r' % (playerId, tasksData['completedTasks']))

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, data):
		playerId = data['playerId']
		syncData = self.GetSyncClientTaskData(playerId)
		self.NotifyToClient(playerId, 'OnMainTaskChanged', {
			'taskId': self._phaseConfig['task'],
			'state': 'start' if syncData.get('notifyMainTask', False) else 'update',
		})
		self.SyncClientTask(playerId, True)
		if playerId != self._hostPlayer:
			self.SyncClientMainTask(playerId)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnPlaceShelter(self, args):
		# 第一次避难所取消start提示
		for data in self._tasksSyncData.itervalues():
			data['notifyMainTask'] = False

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnPlayerOutShelter(self, args):
		# 玩家出避难所后重新弹一次
		playerId = args['playerId']
		self.NotifyToClient(playerId, 'OnMainTaskChanged', {
			'taskId': self._phaseConfig['task'],
			'state': 'start',
		})
		self.SyncClientTask(playerId, True)
		if playerId != self._hostPlayer:
			self.SyncClientMainTask(playerId)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnInitPhaseConfig(self, args):
		self._phaseConfig = args

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnApplyPhaseConfig(self, args):
		self.UpdatePhaseMainTaskChanged(args)

	def UpdatePhaseMainTaskChanged(self, phase):
		oldTask = self._phaseConfig['task']
		self._phaseConfig = phase
		mainTask = self._phaseConfig['task']
		if oldTask != mainTask:
			eid = self._hostPlayer
			tasks = self._tasksMap[eid]
			i = 0
			failed = False
			while i < len(tasks):
				task = tasks[i]
				if task.Uid == oldTask:
					self.CompletedPendingTask(eid, oldTask, 'failed')
					failed = True
					break
				i += 1
			if failed:
				self.BroadcastToAllClient('OnMainTaskChanged', {
					'taskId': oldTask,
					'state': 'failed'
				})
			self.PendingTask(eid, mainTask)
			self.FlushTaskData(eid)
			self.BroadcastToAllClient('OnMainTaskChanged', {
				'taskId': mainTask,
				'state': 'start'
			})

	def Update(self):
		for task in self._tickTasks:
			task.Tick()
		self._tick = (self._tick + 1) % TaskUpdateInterval
		if self._tick == 0:
			curTime = time.time()
			deltaTime = curTime - self._lastUpdateTime
			for eid, tasks in self._tasksMap.iteritems():
				dirty = False
				taskMap = {}
				removed = []
				for task in tasks:
					dirty = dirty or task.Update(deltaTime)
					taskMap[task.Uid] = task
					if not task.Active:
						removed.append(task)
				if curTime - self._tasksFlushTime[eid] > 3:
					self._UpdateTaskStateByTasksMap(eid, taskMap, 'pendingTasks')
					dirty = True
				if dirty:
					self.FlushTaskData(eid)
				for item in removed:
					tasks.remove(item)
			self._lastUpdateTime = curTime

	def GetTaskState(self, playerId, uid):
		if playerId not in self._tasksDataMap:
			return None
		taskStates = self._tasksDataMap[playerId]
		pendingTasks = taskStates['pendingTasks']
		for item in pendingTasks:
			if item['uid'] == uid:
				return 'pending'
		completedTasks = taskStates['completedTasks']
		for item in completedTasks:
			if item['uid'] == uid:
				return 'completed'
		receivedTasks = taskStates['receivedTasks']
		for item in receivedTasks:
			if item['uid'] == uid:
				return 'received'
		return None

	def PendingTask(self, playerId, uid):
		taskState = self.GetTaskState(playerId, uid)
		if taskState is not None:
			self.logger.warning('PendingTask ignore! %s %s %s' % (playerId, uid, taskState))
			return
		task = TaskBuilder.GetTask(self, playerId, uid, self.OnTaskCompleted, self.OnTaskFailed, self.OnTaskChanged)
		if task:
			if task.Config.get('branch', '') == 'main':  # 主线任务开始后，清空轨道记录
				self.SetAccumulationByFullKey('-1', 'PlanetBooster.phase_activated', 0)
			tasks = self._tasksMap[playerId]
			pendingTasks = self._tasksDataMap[playerId]['pendingTasks']
			tasks.append(task)
			self._PendingTaskWithType(task)
			pendingTasks.append(task.State)
			# 同步开始依赖任务
			self.PendingDependsTask(playerId, task.Config)
		return task

	def PendingDependsTask(self, playerId, config):
		depends = config.get('depends', None)
		if depends is None:
			return
		for duid in depends:
			self.PendingTask(playerId, duid)


	def GetPendingTask(self, playerId, uid):
		tasks = self._tasksMap[playerId]
		for task in tasks:
			if task.Uid == uid:
				return task
		return None

	def GetPendingTasksByGroup(self, playerId, group, type=None):
		tasks = self._tasksMap[playerId]
		ret = []
		for task in tasks:
			if task.Config['group'] == group and (type is None or task.Config['type'] == type):
				ret.append(task.Uid)
		return ret

	def CompletedPendingTask(self, playerId, uid, state):
		task = self.GetPendingTask(playerId, uid)
		if not task:
			return
		if state == 'completed':
			task.OnTaskCompleted()
		elif state == 'failed':
			task.OnTaskFailed()
		self.FlushTaskData(playerId)

	def _PendingTaskWithType(self, task):
		if hasattr(task, 'Tick'):
			self._tickTasks.append(task)
		if hasattr(task, 'OnEvent'):
			self._eventTasks.append(task)

	def _RemoveTaskState(self, eid, uid, stateKey):
		data = self._tasksDataMap[eid]
		pTasks = data[stateKey]
		i = 0
		while i < len(pTasks):
			taskState = pTasks[i]
			if taskState['uid'] == uid:
				return pTasks.pop(i)
			else:
				i += 1
		return None

	def _AddTaskState(self, task, stateKey, state=None):
		eid = task.Eid
		data = self._tasksDataMap[eid]
		pTasks = data[stateKey]
		if not state:
			state = task.State
		pTasks.append(state)
		return True

	def _AddTaskStateByEid(self, eid, stateKey, state):
		data = self._tasksDataMap[eid]
		pTasks = data[stateKey]
		if not state:
			return False
		pTasks.append(state)
		return True

	def _UpdateTaskState(self, task, stateKey):
		eid = task.Eid
		data = self._tasksDataMap[eid]
		pTasks = data[stateKey]
		i = 0
		while i < len(pTasks):
			taskState = pTasks[i]
			if taskState['uid'] == task.Uid:
				pTasks[i] = task.State
				return True
			i += 1
		return False

	def _UpdateTaskStateByTasksMap(self, eid, tasksMap, stateKey):
		data = self._tasksDataMap[eid]
		pTasks = data[stateKey]
		i = 0
		dirty = False
		while i < len(pTasks):
			taskState = pTasks[i]
			if taskState['uid'] in tasksMap:
				pTasks[i] = tasksMap[taskState['uid']].State
				dirty = True
			i += 1
		return dirty

	def OnTaskCompleted(self, task):
		eid = task.Eid
		if task in self._tickTasks:
			self._tickTasks.remove(task)
		self._RemoveTaskState(eid, task.Uid, 'pendingTasks')
		completedState = DatasetObj.Build(TaskCompletedState)
		completedState['uid'] = task.Uid
		completedState['t'] = task.PassedTime
		self._AddTaskState(task, 'completedTasks', completedState)
		self.logger.debug('Player %r TaskCompleted %r' % (eid, completedState))
		self.NotifyClientTaskChanged(task, 'completed')

		opConfig = task.Config.get('completed', None)
		self.ApplyTaskOperations(eid, task.Uid, opConfig)

	def OnTaskFailed(self, task):
		eid = task.Eid
		if task in self._tickTasks:
			self._tickTasks.remove(task)
		self._RemoveTaskState(eid, task.Uid, 'pendingTasks')
		depends = task.Config.get('depends', None)
		if depends:
			for duid in depends:
				self.CompletedPendingTask(eid, duid, 'failed')
		self.logger.debug('Player %r TaskFailed %r' % (eid, task.Uid))
		self.NotifyClientTaskChanged(task, 'failed')
		opConfig = task.Config.get('failed', None)
		self.ApplyTaskOperations(eid, task.Uid, opConfig)

	def OnTaskChanged(self, task):
		self._UpdateTaskState(task, 'pendingTasks')
		self.FlushTaskData(task.Eid)
		self.NotifyClientTaskChanged(task, 'changed')

	def _ParseFullKey(self, fullKey):
		splited = fullKey.split('.')
		if len(splited) < 2:
			self.logger.error('SetAccumulations Error %r' % fullKey)
			return
		return splited[0], splited[1]

	def GetAccumulation(self, eid, group, key):
		data = self._accumulationsDataMap[eid]
		if group not in data:
			return -1
		if key not in data[group]:
			return -1
		return data[group][key]

	def GetAccumulationByFullKey(self, eid, fullKey):
		group, k = self._ParseFullKey(fullKey)
		return self.GetAccumulation(eid, group, k)

	def SetAccumulation(self, eid, group, key, value, flush=True):
		data = self._accumulationsDataMap[eid]
		if group not in data:
			data[group] = {}
		data[group][key] = value
		if flush:
			self.FlushAccumulationData(eid)

	def SetAccumulationByFullKey(self, eid, fullKey, value, flush=True):
		group, k = self._ParseFullKey(fullKey)
		self.SetAccumulation(eid, group, k, value, flush)

	def IncreaseAccumulation(self, eid, group, key, value=1, flush=True):
		data = self._accumulationsDataMap[eid]
		if group not in data:
			data[group] = {}
		if key not in data[group]:
			data[group][key] = 0
		data[group][key] += value
		if flush:
			self.FlushAccumulationData(eid)

	def IncreaseAccumulationByFullKey(self, eid, fullKey, value=1, flush=True):
		group, k = self._ParseFullKey(fullKey)
		self.IncreaseAccumulation(eid, group, k, value, flush)


	def NotifyClientTaskChanged(self, task, state):
		if task.Config.get('hide', False):
			return
		self.NotifyToClient(task.Eid, 'OnTaskChanged', {
			'state': state,
			'taskState': task.State
		})

	def GetSyncClientTaskData(self, eid):
		if eid not in self._tasksSyncData:
			self._tasksSyncData[eid] = {
				'pendingCount': 0,
				'completedCount': 0,
				'receivedCount': 0,
			}
		return self._tasksSyncData[eid]

	def _IsMainTask(self, uid):
		config = GetTaskConfig(uid)
		if config is None:
			return False
		branch = config.get('branch', '')
		return branch == 'main' or branch == 'main_depends'

	def SyncClientTask(self, eid, force=False):
		syncData = self.GetSyncClientTaskData(eid)
		data = self._tasksDataMap[eid]
		pCount = len(data['pendingTasks'])
		cCount = len(data['completedTasks'])
		rCount = len(data['receivedTasks'])
		spCount = syncData['pendingCount']
		scCount = syncData['completedCount']
		srCount = syncData['receivedCount']
		if pCount != spCount or cCount != scCount or rCount != srCount or force:
			syncData['pendingCount'] = pCount
			syncData['completedCount'] = cCount
			syncData['receivedCount'] = rCount
			self.NotifyToClient(eid, 'OnTaskSync', data)
			if eid == self._hostPlayer:
				self.SyncClientMainTask()

	def SyncClientMainTask(self, eid=None):
		data = self._tasksDataMap[self._hostPlayer]
		mainTask = DatasetObj.Build(TaskServerData)
		for state in data['pendingTasks']:
			if self._IsMainTask(state['uid']):
				mainTask['pendingTasks'].append(state)
		for state in data['completedTasks']:
			if self._IsMainTask(state['uid']):
				mainTask['completedTasks'].append(state)
		for state in data['receivedTasks']:
			if self._IsMainTask(state['uid']):
				mainTask['receivedTasks'].append(state)
		if eid is None:
			self.BroadcastToAllClient('OnMainTaskSync', mainTask)
		else:
			self.NotifyToClient(eid, 'OnMainTaskSync', mainTask)

	def NotifyTaskEvent(self, name, data):
		for task in self._eventTasks:
			task.OnEvent(name, data)

	def _TakeTaskRewards(self, playerId, uid):
		config = GetTaskConfig(uid)
		# Checking
		task = self._RemoveTaskState(playerId, uid, 'completedTasks')
		if not config or not task:
			self.logger.error('Player %r TaskTaskRewards Error! %r' % (playerId, uid))
			return
		rewards = config['rewards']
		listItems = []
		for identifier in rewards:
			listItems.append({
				'newItemName': identifier,
				'newAuxValue': 0,
				'count': rewards[identifier]
			})
		SpawnItemsToInventory(self, playerId, listItems)
		state = DatasetObj.Build(TaskReceivedState)
		state['uid'] = uid
		self._AddTaskStateByEid(playerId, 'receivedTasks', state)
		self.logger.debug('Player %r TaskTaskRewards %r' % (playerId, uid))
		return rewards

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.TaskClientSystem)
	def TakeTaskRewards(self, data):
		playerId = data['playerId']
		uid = data['uid']
		rewards = self._TakeTaskRewards(playerId, uid)
		if rewards:
			self.FlushTaskData(playerId)
			self.NotifyToClient(playerId, 'OnTakeTaskRewards', {
				'uid': uid,
				'rewards': rewards
			})

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.TaskClientSystem)
	def TakeAllTaskRewards(self, data):
		playerId = data['playerId']
		uids = data['uids']
		ret = False
		rewardsList = []
		validUids = []
		for uid in uids:
			rewards = self._TakeTaskRewards(playerId, uid)
			if rewards:
				ret = True
				validUids.append(uid)
				if len(rewards) > 0:
					rewardsList.append(rewards)
		if ret:
			self.FlushTaskData(playerId)
			self.NotifyToClient(playerId, 'OnTakeAllTaskRewards', {
				'uids': validUids,
				'rewardsList': rewardsList
			})
	
	def GetRewardsPopupEvent(self, data):
		"""显示获得物品弹窗的订阅事件
		rewards格式 = {itemName: count, ...}
		"""
		playerId = data['playerId']
		rewards = data['rewards']
		self.NotifyToClient(playerId, 'OnTakeTaskRewards', {
			'rewards': rewards
		})
		pass

	def ApplyTaskOperations(self, eid, uid, opConfig):
		if not opConfig:
			return
		op = opConfig['op']
		value = opConfig.get('value', None)
		info = {'playerId': eid, 'taskId': uid}
		if op == 'SetAccumulations':
			if opConfig.get('global', False):
				eid = '-1'
			for key in value:
				self.SetAccumulationByFullKey(eid, key, value[key])
		elif op == 'ActivatePlanetBooster':
			# 清空激活数量
			self.SetAccumulationByFullKey('-1', 'PlanetBooster.activated', 0)
			self.SetAccumulationByFullKey('-1', 'PlanetBooster.guard', 0)
			# 跳转到下一阶段
			self.BroadcastToAllClient('OnJumpToNextPhase', info)
			self.BroadcastEvent('OnJumpToNextPhase', info)
		elif op == 'EscapeFailed':
			self.SetAccumulationByFullKey('-1', 'PlanetBooster.activated', 0)
			self.SetAccumulationByFullKey('-1', 'PlanetBooster.guard', 0)
			# 广播逃离失败
			self.BroadcastToAllClient('OnEscapeFailed', info)
			self.BroadcastEvent('OnEscapeFailed', info)


	# region 任务依赖的相关事件
	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ItemsClientSystem)
	def OnClientShapedRecipe(self, args):
		recipeId = args['recipeId']
		recipeResult = CompFactory.CreateRecipe(serverApi.GetLevelId()).GetRecipeResult(recipeId)
		self.NotifyTaskEvent('RecipeCompound', {
				'playerId': args['playerId'],
				'results': recipeResult
			})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.ElectricServerSystem)
	def ElectricCraftingItemsEvent(self, args):
		self.NotifyTaskEvent('ElectricCraftingCompound', args)

	@EngineEvent()
	def EntityPlaceBlockAfterServerEvent(self, args):
		self.NotifyTaskEvent('PlaceBlock', args)

	@EngineEvent()
	def DestroyBlockEvent(self, args):
		self.NotifyTaskEvent('DestroyBlock', args)

	@EngineEvent()
	def ItemUseAfterServerEvent(self, args):
		self.NotifyTaskEvent('UseItem', args)

	@EngineEvent()
	def ServerBlockUseEvent(self, args):
		self.NotifyTaskEvent('UseBlock', args)

	@EngineEvent()
	def PlayerDoInteractServerEvent(self, args):
		self.NotifyTaskEvent('OperateEntity', args)
	# endregion

	# region 记录累计数据
	# 击杀
	@EngineEvent()
	def MobDieEvent(self, args):
		playerId = args['attacker']
		if playerId == '-1':
			return
		if playerId not in self._accumulationsDataMap:
			return
		targetId = args['id']
		comp = CompFactory.CreateEngineType(targetId)
		identifier = comp.GetEngineTypeStr()
		self.IncreaseAccumulation(playerId, 'KillEntity', identifier)
		self.NotifyTaskEvent('KillEntity', {
			'playerId': playerId,
			'identifier': identifier,
		})

	# 吃食物
	@EngineEvent()
	def PlayerEatFoodServerEvent(self, args):
		playerId = args['playerId']
		if playerId not in self._accumulationsDataMap:
			return
		identifier = args['itemDict']['newItemName']
		self.IncreaseAccumulation(playerId, 'EatFood', identifier)
		self.NotifyTaskEvent('EatFood', {
			'playerId': playerId,
			'identifier': identifier,
		})

	# 天数变化
	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnDayChanged(self, args):
		gameComp = CompFactory.CreateGame(self.mLevelId)
		for playerId in self._accumulationsDataMap:
			if gameComp.IsEntityAlive(playerId):
				self.IncreaseAccumulation(playerId, 'Record', 'livingDays')

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def OnNpcConsumeItem(self, args):
		self.NotifyTaskEvent('NpcConsumeItem', args)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def OnNpcConsumeEntity(self, args):
		self.NotifyTaskEvent('NpcConsumeEntity', args)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BattleEventServerSystem)
	def OnGuardPlanetBoosterSuccess(self, args):
		self.IncreaseAccumulationByFullKey('-1', 'PlanetBooster.guard', 1)
	# endregion

	# region 发动机特效
	def SetLoginPlayEngineEffects(self, playerId):
		"""登录时播放发动机特效，仅该玩家播放"""
		# TODO: 这里获取到所有已启动的发动机坐标列表
		# [(dimension, pos), ...]
		enginePosList = []
		info = {
			"stage": "multi_engine",
			"engine_list": enginePosList,
		}
		self.SendMsgToClient(playerId, eventConfig.EffectPlayEvent, info)
		pass

	def SetTaskPlayEngineEffects(self, dimension, pos):
		"""完成任务时播放发动机特效，仅播放一个"""
		info = {
			"stage": "engine",
			"dimension": dimension,
			"pos": pos,
		}
		self.SendMsgToAllClient(eventConfig.EffectPlayEvent, info)
		pass
	# endregion
