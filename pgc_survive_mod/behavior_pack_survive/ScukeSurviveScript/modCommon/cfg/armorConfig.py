# -*- encoding: utf-8 -*-

from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.armor.armor02_chest import Config as Armor02_Chest

__armorList__ = [
	#Armor02_Chest,
]

__armorDic__ = {}
for config in __armorList__:
	__armorDic__[config['identifier']] = config


def GetConfig(identifier):
	if identifier in __armorDic__:
		return __armorDic__[identifier]
	return None


ArmorIdentifierPrefix = modConfig.ModNameSpace + ':armor_'
