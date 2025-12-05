# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.taskConfig import GetTaskConfig
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.taskServerData import TaskPendingState


class TaskBuilder(object):
	__bindingTask__ = {}

	@staticmethod
	def BindingTask(name, cls):
		TaskBuilder.__bindingTask__[name] = cls

	@staticmethod
	def GetTask(system, eid, taskId, completedCall, failedCall, changedCall):
		config = GetTaskConfig(taskId)
		if config is None:
			return None
		tType = config['type']
		if tType not in TaskBuilder.__bindingTask__:
			return None
		cls = TaskBuilder.__bindingTask__[tType]
		return cls(system, eid, taskId, completedCall, failedCall, changedCall)


class GameTask(object):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		config = GetTaskConfig(taskId)
		self._state = 0
		self._eid = eid
		self._passedTime = 0.0
		self._uid = taskId
		self._config = config
		self._completedCall = completedCall
		self._failedCall = failedCall
		self._changedCall = changedCall
		self._system = system
		self._changed = False
		self._recordAnyEntity = False
		self._recordAnyItem = False
		self._recordAnyBlock = False
		self._progressMap = {'entity[*]': 0, 'item[*]': 0, 'block[*]': 0}


	def _InitAnyRecord(self):
		data = self._config['data']
		if 'items' in data:
			self._recordAnyItem = 'item[*]' in data['items']
		if 'entities' in data:
			self._recordAnyEntity = 'entity[*]' in data['entities']
		if 'blocks' in data:
			self._recordAnyBlock = 'block[*]' in data['blocks']

	@property
	def ProgressMap(self):
		ret = {}
		for k, v in self._progressMap.iteritems():
			ret[k] = v
		if not self._recordAnyItem:
			del ret['item[*]']
		if not self._recordAnyEntity:
			del ret['entity[*]']
		if not self._recordAnyBlock:
			del ret['block[*]']
		return ret

	@property
	def Config(self):
		return self._config

	def FromData(self, data):
		if data:
			self._passedTime = data['t']
			p = data.get('p', None)
			if p:
				for k, v in p.iteritems():
					self._progressMap[k] = v


	@property
	def Eid(self):
		return self._eid

	@property
	def Uid(self):
		return self._uid

	@property
	def PassedTime(self):
		return round(self._passedTime, 1)

	@property
	def State(self):
		ret = DatasetObj.Build(TaskPendingState)
		ret['uid'] = self._uid
		ret['t'] = round(self._passedTime, 1)
		return ret

	@property
	def Active(self):
		return self._state == 0

	def Update(self, deltaTime):
		if self._state > 0:
			return False
		dirty = self._changed
		self._passedTime += deltaTime
		totalTime = self._config['time']
		ret = self.CheckCondition()
		if ret:
			if self.CheckDepends():
				self.OnTaskCompleted()
				dirty = True
			else:
				ret = False
		if totalTime > 0 and self._passedTime > totalTime:
			if not ret:
				self.OnTaskFailed()
				dirty = True
		return dirty

	def CheckCondition(self):
		return False

	def CheckDepends(self):
		depends = self.Config.get('depends', None)
		if depends is None:
			return True
		for uid in depends:
			state = self._system.GetTaskState(self._eid, uid)
			if state is None or state == 'pending':
				return False
		return True


	def OnTaskFailed(self):
		self._state = 1
		if self._failedCall:
			self._failedCall(self)
		self.Release()

	def OnTaskCompleted(self):
		self._state = 2
		if self._completedCall:
			self._completedCall(self)
		self.Release()

	def Release(self):
		pass

	def KeyMatch(self, key, k):
		import re
		p = re.compile(key)
		m = p.match(k)
		if m:
			return True
		return False

	def _CheckProgress(self, items):
		for key in items:
			if key.startswith('^'):
				c = 0
				for k in self._progressMap:
					if self.KeyMatch(key, k):
						c += self._progressMap[k]
				if items[key] > c:
					return False
			else:
				if key not in self._progressMap:
					return False
				if items[key] > self._progressMap[key]:
					return False
		return True
