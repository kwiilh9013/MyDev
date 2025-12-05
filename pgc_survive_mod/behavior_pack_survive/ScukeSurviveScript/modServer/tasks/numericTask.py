# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modServer.tasks.gameTask import GameTask
import mod.server.extraServerApi as serverApi

class NumericTask(GameTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(NumericTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
		self._attrSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		self._attrs = self._config['data'].get('attrs', None)
		self._accumulations = self._config['data'].get('accumulations', None)
		self._global_accumulations = self._config['data'].get('global_accumulations', None)

	def CheckCondition(self):
		attrs = self._attrs
		if attrs:
			for key in attrs:
				item = attrs[key]
				op = item['op']
				value = item['value']
				cur = self._attrSystem.GetAttr(self._eid, key)
				ret = False
				if op == '>':
					ret = cur > value
				elif op == '>=':
					ret = cur >= value
				elif op == '<':
					ret = cur < value
				elif op == '<=':
					ret = cur <= value
				if not ret:
					return False
		if not self._CheckAccumulations(self._accumulations, self._eid):
			return False
		if not self._CheckAccumulations(self._global_accumulations, '-1'):
			return False
		return True

	def _CheckAccumulations(self, accumulations, eid):
		if accumulations:
			for group in accumulations:
				groupData = accumulations[group]
				for key in groupData:
					value = groupData[key]
					cur = self._system.GetAccumulation(eid, group, key)
					if cur < value:
						return False
		return True
