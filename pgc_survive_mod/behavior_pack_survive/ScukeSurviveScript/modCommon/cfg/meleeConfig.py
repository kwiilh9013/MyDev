# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.melee.axe import Config as Axe
from ScukeSurviveScript.modCommon.cfg.melee.axe_red import Config as Axe_Red
from ScukeSurviveScript.modCommon.cfg.melee.axe_golden import Config as Axe_Golden
from ScukeSurviveScript.modCommon.cfg.melee.chainsaw import Config as Chainsaw
from ScukeSurviveScript.modCommon.cfg.melee.chainsaw_old import Config as Chainsaw_Old
from ScukeSurviveScript.modCommon.cfg.melee.chainsaw_golden import Config as Chainsaw_Golden
from ScukeSurviveScript.modCommon.cfg.melee.baseballBat import Config as BaseballBat
from ScukeSurviveScript.modCommon.cfg.melee.baseballBat_m import Config as BaseballBat_M
from ScukeSurviveScript.modCommon.cfg.melee.baseballBat_golden import Config as BaseballBat_Golden
from ScukeSurviveScript.modCommon.cfg.melee.pigsaw import Config as Pigsaw
from ScukeSurviveScript.modCommon.cfg.melee.pigsaw_golden import Config as Pigsaw_Golden
from ScukeSurviveScript.modCommon.cfg.melee.pan_copper import Config as Pan_Copper
from ScukeSurviveScript.modCommon.cfg.melee.pan import Config as Pan
from ScukeSurviveScript.modCommon.cfg.melee.pan_golden import Config as Pan_Golden

__meleeList__ = [
	Axe,
	Axe_Red,
	Axe_Golden,
	Chainsaw,
	Chainsaw_Old,
	Chainsaw_Golden,
	BaseballBat,
	BaseballBat_M,
	BaseballBat_Golden,
	Pigsaw,
	Pigsaw_Golden,
	Pan_Copper,
	Pan,
	Pan_Golden,
]

__meleeDic__ = {}
for config in __meleeList__:
	__meleeDic__[config['identifier']] = config


def GetConfig(identifier):
	if identifier in __meleeDic__:
		return __meleeDic__[identifier]
	return None


MeleeIdentifierPrefix = modConfig.ModNameSpace + ':melee_'

ForbidTakeMeleeRides = [
	'scuke_survive:base_car'
]
