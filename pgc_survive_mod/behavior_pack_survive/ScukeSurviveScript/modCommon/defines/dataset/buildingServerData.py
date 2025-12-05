# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj


class BuildingState(DatasetObj):
	dim = int
	pos = tuple
	rot = int
	identifier = str
	group = str
	size = tuple
	data = dict

class BuildingTaskState(DatasetObj):
	uid = int
	pos = tuple
	rot = int
	dim = int
	identifier = str
	index = int
	total = int

class BuildingPosMarkerTaskState(DatasetObj):
	id = str
	pos = tuple
	rot = int
	dim = int
	size = tuple
	sp = dict


class BuildingServerData(DatasetObj):
	uid = int
	buildings = (list, BuildingState)
	buildingTasks = (list, BuildingTaskState)
	buildingPosMarkerTasks = (list, BuildingPosMarkerTaskState)
	shelterBorn = (list, str)
	outShelter = (list, str)

	@staticmethod
	def Update(data, version):
		return data
