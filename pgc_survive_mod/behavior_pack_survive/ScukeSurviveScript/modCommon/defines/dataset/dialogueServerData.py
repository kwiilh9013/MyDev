# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj


class DialogueCurrentState(DatasetObj):
	entryId = str
	nodeId = str
	eid = str
	identifier = str
	sitting = bool

class DialogueServerData(DatasetObj):
	current = None
	history = (list, DialogueCurrentState)

	@staticmethod
	def Update(data, version):
		return data
