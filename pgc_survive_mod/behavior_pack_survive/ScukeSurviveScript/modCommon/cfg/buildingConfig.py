# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.buildings.planet_booster import Config as PlanetBooster

__buildingList__ = [
	PlanetBooster
]

__buildingDic__ = {}

from ScukeSurviveScript.modCommon import modConfig

for config in __buildingList__:
	__buildingDic__[config['identifier']] = config


def GetConfig(identifier):
	if identifier in __buildingDic__:
		return __buildingDic__[identifier]
	return None

