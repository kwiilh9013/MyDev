# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum


_MonsterPool = {
	MonsterEnum.ZombieNormal: {"weight": 20, "count": 4},
	MonsterEnum.ZombieGangs: {"weight": 30, "count": 3},
	MonsterEnum.ZombieChick: {"weight": 30, "count": 3},
	MonsterEnum.ZombieGuard: {"weight": 20, "count": 2},
}


_ChestPool = {
	BlockEnum.ChestStorageRed: {'weight': 10, 'loot_table': 'loot_tables/scuke_survive/chest/box_t3.json'},
	BlockEnum.ChestStorageOrange: {'weight': 10, 'loot_table': 'loot_tables/scuke_survive/chest/box_t2.json'},
}


Config = {
	'identifier': 'scuke_railwaystation:railwaystation_2_5',
	'structure_name_base': 'scuke_railwaystation:railwaystation',
	'is_feature_rule': True,
	'center': (32, 0, 80),
	'size': (74, 31, 158),
	'posMarkers': [
		{'pos': (28, 4, 45), 'face': 1, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{
			'pos': (56, 7, 92), 'face': 1, 'id': 'scuke_survive:monster_pool',
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 60, "count": 4},
				MonsterEnum.ZombieGangs: {"weight": 40, "count": 3},
			}, 
		},
		{
			'pos': (56, 9, 125), 'face': 2, 'id': 'scuke_survive:monster_pool',
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 20, "count": 4},
				MonsterEnum.ZombieGangs: {"weight": 40, "count": 3},
				MonsterEnum.ZombieChick: {"weight": 40, "count": 3},
			}, 
		},
		{'pos': (55, 6, 32), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (55, 6, 55), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (55, 6, 83), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (56, 9, 125), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (24, 4, 72), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (18, 4, 51), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		{'pos': (35, 4, 39), 'face': 0, 'id': 'scuke_survive:monster_pool', 'entity_pool': _MonsterPool, },
		# 宝箱
		{'pos': (10, 4, 79), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (42, 4, 50), 'id': 'scuke_survive:chest_pool', 'face': 3, 'chest_pool': _ChestPool},
		{'pos': (27, 4, 62), 'id': 'scuke_survive:chest_pool', 'face': 3, 'chest_pool': _ChestPool},
		{'pos': (13, 5, 36), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': _ChestPool},
		{'pos': (24, 22, 43), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': {
			BlockEnum.ChestStorageRed: {'weight': 10, 'loot_table': 'loot_tables/scuke_survive/chest/armor_t3.json'},
		}},
		
	]
}
