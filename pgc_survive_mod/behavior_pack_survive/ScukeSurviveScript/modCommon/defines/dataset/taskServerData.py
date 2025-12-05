# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj

class TaskPendingState(DatasetObj):
	uid = str
	t = float
	p = dict

class TaskCompletedState(DatasetObj):
	uid = str
	t = float

class TaskReceivedState(DatasetObj):
	uid = str

class TaskAccumulationsData(DatasetObj):
	@staticmethod
	def Update(data, version):
		return data

class TaskServerData(DatasetObj):
	pendingTasks = (list, TaskPendingState)
	completedTasks = (list, TaskCompletedState)
	receivedTasks = (list, TaskReceivedState)

	@staticmethod
	def Update(data, version):
		return data
