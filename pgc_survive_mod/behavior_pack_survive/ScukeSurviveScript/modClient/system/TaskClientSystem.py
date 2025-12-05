# -*- coding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.common.log.logManager import LogManager
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon.cfg.taskConfig import Config as TaskConfig

from ScukeSurviveScript.modCommon import modConfig


class TaskClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(TaskClientSystem, self).__init__(namespace, systemName)
		self._taskData = {
			'pendingTasks': [],
			'completedTasks': [],
			'receivedTasks': [],
		}
		self._mainTaskData = {
			'pendingTasks': [],
			'completedTasks': [],
			'receivedTasks': [],
		}
		self._taskListData = []
		self._needRebuildTaskListData = True
		self._mainTask = None


	@property
	def CurrentMainTask(self):
		return self._mainTask

	def BuildTaskListData(self):
		def _sort(e):
			return int(e['uid'])
		ret = []
		taskMap = {}
		for k, v in TaskConfig.iteritems():
			taskMap[k] = {
				'uid': k,
				'type': 'sleep'
			}
		pendingTasks = self._taskData['pendingTasks']
		completedTasks = self._taskData['completedTasks']
		receivedTasks = self._taskData['receivedTasks']
		for task in pendingTasks:
			uid = task['uid']
			if uid in taskMap:
				del taskMap[uid]
				ret.append({'uid': uid, 'type': 'pending', 'data': task})
		for task in completedTasks:
			uid = task['uid']
			if uid in taskMap:
				del taskMap[uid]
				ret.append({'uid': uid, 'type': 'completed', 'data': task})
		for task in receivedTasks:
			uid = task['uid']
			if uid in taskMap:
				del taskMap[uid]
				ret.append({'uid': uid, 'type': 'received', 'data': task})
		pendingTasks = self._mainTaskData['pendingTasks']
		completedTasks = self._mainTaskData['completedTasks']
		receivedTasks = self._mainTaskData['receivedTasks']
		for task in pendingTasks:
			uid = task['uid']
			if uid in taskMap:
				del taskMap[uid]
				ret.append({'uid': uid, 'type': 'pending', 'data': task, 'fromMainTask': True})
		for task in completedTasks:
			uid = task['uid']
			if uid in taskMap:
				del taskMap[uid]
				ret.append({'uid': uid, 'type': 'completed', 'data': task, 'fromMainTask': True})
		for task in receivedTasks:
			uid = task['uid']
			if uid in taskMap:
				del taskMap[uid]
				ret.append({'uid': uid, 'type': 'received', 'data': task, 'fromMainTask': True})
		for k in taskMap:
			ret.append(taskMap[k])
		ret.sort(key=_sort)
		return ret

	def GetTaskData(self):
		if self._needRebuildTaskListData:
			self._taskListData = self.BuildTaskListData()
			self._needRebuildTaskListData = False
		return self._taskListData


	def FilterTaskDataByGroup(self, branch, group):
		data = []
		orgData = self.GetTaskData()
		completedCount = 0
		pendingCount = 0
		receivedCount = 0
		for task in orgData:
			uid = task['uid']
			tType = task['type']
			config = TaskConfig.get(uid, None)
			if config:
				branchMatch = branch is None or config['branch'] == branch
				groupMatch = group is None or config['group'] == group
				if branchMatch and groupMatch:
					data.append(task)
					if tType == 'pending':
						pendingCount += 1
					if tType == 'completed':
						completedCount += 1
					if tType == 'received':
						receivedCount += 1
		totalCount = len(data)
		return data, pendingCount, completedCount, receivedCount, totalCount

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnTaskSync(self, data):
		self._taskData = data
		self._needRebuildTaskListData = True

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnMainTaskSync(self, data):
		self._mainTaskData = data
		self._needRebuildTaskListData = True

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnTaskChanged(self, data):
		self._needRebuildTaskListData = True
		state = data['state']
		taskState = data['taskState']
		if state == 'changed':
			self._OnTaskChanged(taskState)
		elif state == 'failed':
			self._OnTaskFailed(taskState)
		elif state == 'completed':
			self._OnTaskCompleted(taskState)


	def _OnTaskChanged(self, taskState):
		pendingTasks = self._taskData['pendingTasks']
		i = 0
		while i < len(pendingTasks):
			task = pendingTasks[i]
			if task['uid'] == taskState['uid']:
				pendingTasks[i] = taskState
				break
			i += 1
		self.BroadcastEvent('OnTaskChanged', taskState)

	def _OnTaskFailed(self, taskState):
		self.BroadcastEvent('OnTaskFailed', taskState)

	def _OnTaskCompleted(self, taskState):
		self.BroadcastEvent('OnTaskCompleted', taskState)
		config = TaskConfig[taskState['uid']]
		Instance.mUIManager.ShowSnackBar({
			'icon': config['icon'],
			'title': '完成任务',
			'content': config['desc'],
			'duration': 3.0
		})

	def TakeTaskRewards(self, uid):
		self.NotifyToServer('TakeTaskRewards', {
			'playerId': self.mPlayerId,
			'uid': uid
		})

	def TakeAllTaskRewards(self, uids):
		self.NotifyToServer('TakeAllTaskRewards', {
			'playerId': self.mPlayerId,
			'uids': uids
		})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnTakeTaskRewards(self, data):
		listData = []
		rewards = data['rewards']
		for k, v in rewards.iteritems():
			listData.append({
				'identifier': k,
				'count': v
			})
		Instance.mUIManager.PushUI(UIDef.UI_RewardsUI, {
			'data': listData
		})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnTakeAllTaskRewards(self, data):
		rewardsList = data['rewardsList']
		ret = {}
		for rewards in rewardsList:
			for k in rewards:
				if k not in ret:
					ret[k] = 0
				ret[k] += rewards[k]
		self.OnTakeTaskRewards({
			'rewards': ret,
		})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnMainTaskChanged(self, data):
		mainTaks = data['taskId']
		state = data['state']
		config = TaskConfig.get(mainTaks, None)
		if not config:
			return
		self._mainTask = mainTaks
		if state == 'start':
			Instance.mUIManager.ShowSnackBar({
				'icon': config['icon'],
				'title': '开启新征程！',
				'content': config['desc'],
				'duration': 5.0
			})
		elif state == 'failed':
			Instance.mUIManager.ShowSnackBar({
				'icon': config['icon'],
				'title': '脱离轨道失败...',
				'content': config['desc'],
				'duration': 3.0
			})
