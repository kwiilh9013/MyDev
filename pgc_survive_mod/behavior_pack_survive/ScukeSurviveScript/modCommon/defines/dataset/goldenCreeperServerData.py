# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.cfg.entity.npc.goldenCreeper import Config as NPCGoldenCreeperConfig


class GoldenCreeperServerData(DatasetObj):
	pleasure = NPCGoldenCreeperConfig['pleasure']

	@staticmethod
	def Update(data, version):
		return data
