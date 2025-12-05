# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj


class GunServerData(DatasetObj):
	identifier = str
	clip = int

	@staticmethod
	def Update(data, version):
		return data
