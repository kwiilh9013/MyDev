# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum

Config = {
	'identifier': 'scuke_community01:community01_3_5',
	'structure_name_base': 'scuke_community01:community01',
	'is_feature_rule': True,
	'center': (48, 0, 80),
	'size': (107, 56, 168),
	'posMarkers': [
		{'pos': (22, 16, 115), 'id': 'scuke_survive:monster_pool', 'face': 0,
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 40, "count": 4},
				MonsterEnum.ZombieGangs: {"weight": 30, "count": 3},
				MonsterEnum.ZombieChick: {"weight": 30, "count": 2},
			},
		},
		{'pos': (85, 21, 113), 'id': 'scuke_survive:monster_pool', 'face': 2,
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 50, "count": 4},
				MonsterEnum.ZombieChick: {"weight": 40, "count": 3},
				MonsterEnum.ZombieExplosive: {"weight": 30, "count": 5},
			},
		},
		{'pos': (85, 16, 68), 'id': 'scuke_survive:monster_pool', 'face': 1,
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 50, "count": 5},
				MonsterEnum.ZombieDog: {"weight": 40, "count": 6},
				MonsterEnum.ZombieExplosive: {"weight": 40, "count": 4},
			},
		},
	]
}
