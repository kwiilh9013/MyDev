# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum

_MonsterPool = {
	MonsterEnum.ZombieExplosive: {"weight": 20, "count": 1},
	MonsterEnum.ZombieFat: {"weight": 20, "count": 2},
	MonsterEnum.ZombieGuard: {"weight": 10, "count": 3},
	MonsterEnum.ZombieDog: {"weight": 20, "count": 4},
	MonsterEnum.ZombieCaptain: {"weight": 20, "count": 2},
	MonsterEnum.ZombieChick: {"weight": 10, "count": 4},
}

_ChestPool = {
	BlockEnum.ChestStorageRed: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/relic_middle_1.json'},
	BlockEnum.ChestStorageOrange: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/relic_middle_2.json'},
	BlockEnum.ChestStorageBlue: {'weight': 40, 'loot_table': 'loot_tables/scuke_survive/chest/relic_middle_3.json'},
	BlockEnum.ChestMilitary: {'weight': 10, 'loot_table': 'loot_tables/scuke_survive/chest/relic_hight_1.json'},
}


Config = {
	'identifier': 'scuke_offices:offices_2_4',
	'structure_name_base': 'scuke_offices:offices',
	'is_feature_rule': True,
	'center': (32, 0, 64),
	'size': (80, 39, 121),
	'posMarkers': [
		{
			'pos': (43, 4, 14), 'face': 0, 'id': 'scuke_survive:monster_pool',
			'entity_pool': _MonsterPool, 
		},
		{
			'pos': (27, 4, 10), 'face': 0, 'id': 'scuke_survive:monster_pool',
			'entity_pool': _MonsterPool, 
		},
		{
			'pos': (12, 4, 71), 'face': 0, 'id': 'scuke_survive:monster_pool',
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 10, "count": 5},
				MonsterEnum.ZombieGangs: {"weight": 20, "count": 4},
				MonsterEnum.ZombieChick: {"weight": 20, "count": 4},
				MonsterEnum.ZombieGuard: {"weight": 20, "count": 3},
				MonsterEnum.ZombieDog: {"weight": 30, "count": 4},
			}, 
		},
		{'pos': (18, 5, 29), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (14, 26, 22), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (17, 26, 78), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (18, 32, 80), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (16, 32, 28), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (16, 19, 28), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (15, 19, 72), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		# 宝箱
		{'pos': (24, 29, 38), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (16, 38, 19), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': {
			BlockEnum.ChestMilitary: {'weight': 10, 'loot_table': 'loot_tables/scuke_survive/chest/weapon_t2.json'},
			BlockEnum.ChestMilitary: {'weight': 10, 'loot_table': 'loot_tables/scuke_survive/chest/armor_t2.json'},
		}},
		{'pos': (30, 31, 87), 'id': 'scuke_survive:chest_pool', 'face': 1, 'chest_pool': _ChestPool},
		{'pos': (29, 25, 88), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (30, 26, 18), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (3, 15, 45), 'id': 'scuke_survive:chest_pool', 'face': 3, 'chest_pool': _ChestPool},
		{'pos': (28, 21, 97), 'id': 'scuke_survive:chest_pool', 'face': 1, 'chest_pool': _ChestPool},
		{'pos': (28, 4, 77), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (9, 4, 40), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
	]
}
