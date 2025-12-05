# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.tasks.numericTask import NumericTask


class GuardPlanetBoosterTask(NumericTask):
	def __init__(self, system, eid, taskId, completedCall, failedCall, changedCall):
		super(GuardPlanetBoosterTask, self).__init__(system, eid, taskId, completedCall, failedCall, changedCall)
