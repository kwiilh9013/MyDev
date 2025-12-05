# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum

Config = {
	'identifier': 'scuke_signal_tower:signal_tower_2_1',
	'structure_name_base': 'scuke_signal_tower:signal_tower',
	'is_feature_rule': True,
	'center': (32, 0, 16),
	'size': (55, 70, 30),
	'posMarkers': [
		{'pos': (42, 11, 12), 'id': 'scuke_survive:monster_pool', 'face': 1,
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 50, "count": 4},
				MonsterEnum.ZombieChick: {"weight": 50, "count": 3},

			},
		},
		{'pos': (28, 12, 11), 'id': 'scuke_survive:monster_pool', 'face': 0,
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 50, "count": 4},
				MonsterEnum.ZombieGangs: {"weight": 50, "count": 3},
			},
		},
	]
}
