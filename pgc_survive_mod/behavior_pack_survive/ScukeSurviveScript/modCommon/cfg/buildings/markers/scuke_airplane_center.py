# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum


_MonsterPool = {
	MonsterEnum.ZombieVenom: {"weight": 15, "count": 3},
	MonsterEnum.ZombieChick: {"weight": 15, "count": 4},
	MonsterEnum.ZombieGuard: {"weight": 20, "count": 3},
	MonsterEnum.ZombieDog: {"weight": 20, "count": 4},
	MonsterEnum.ZombieCaptain: {"weight": 30, "count": 2},
}

_ChestPool = {
	BlockEnum.ChestStorageRed: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/relic_middle_1.json'},
	BlockEnum.ChestStorageOrange: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/relic_middle_2.json'},
	BlockEnum.ChestStorageBlue: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/relic_middle_3.json'},
}

Config = {
	'identifier': 'scuke_airplane_center:airplane_center_2_5',
	'structure_name_base': 'scuke_airplane_center:airplane_center',
	'is_feature_rule': True,
	'center': (32, 0, 80),
	'size': (53, 17, 176),
	'posMarkers': [
		{'pos': (35, 11, 122), 'face': 2, 'id': 'scuke_survive:monster_pool',
			'entity_pool': _MonsterPool, 
		},
		{'pos': (31, 8, 84), 'face': 1, 'id': 'scuke_survive:monster_pool',
			'entity_pool': {
				MonsterEnum.ZombieChick: {"weight": 25, "count": 3},
				MonsterEnum.ZombieGuard: {"weight": 25, "count": 2},
				MonsterEnum.ZombieDog: {"weight": 25, "count": 4},
				MonsterEnum.ZombieCaptain: {"weight": 25, "count": 2},
			}, 
		},
		{'pos': (31, 10, 49), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (44, 8, 85), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (33, 11, 117), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		# 宝箱
		{'pos': (33, 10, 89), 'id': 'scuke_survive:chest_pool', 'face': 3, 'chest_pool': _ChestPool},
		{'pos': (32, 3, 54), 'id': 'scuke_survive:chest_pool', 'face': 3, 'chest_pool': _ChestPool},
		{'pos': (10, 8, 87), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (35, 7, 113), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': {
			BlockEnum.ChestMilitary: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/armor_t1.json'},
		}},
	]
}
