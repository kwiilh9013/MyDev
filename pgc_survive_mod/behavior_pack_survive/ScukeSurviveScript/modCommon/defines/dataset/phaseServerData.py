# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj


class PhaseServerData(DatasetObj):
	startTime = int
	phaseOffset = int
	endDays = int

	@staticmethod
	def Update(data, version):
		return data
