# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum


Config = {
	'identifier': 'scuke_airplane_bottom:airplane_bottom_2_2',
	'structure_name_base': 'scuke_airplane_bottom:airplane_bottom',
	'is_feature_rule': True,
	'center': (32, 0, 32),
	'size': (72, 20, 56),
	'posMarkers': [
		{'pos': (49, 8, 30), 'face': 2, 'id': 'scuke_survive:monster_pool',
            'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 10, "count": 4},
				MonsterEnum.ZombieGangs: {"weight": 20, "count": 3},
				MonsterEnum.ZombieChick: {"weight": 20, "count": 3},
				MonsterEnum.ZombieGuard: {"weight": 20, "count": 2},
				MonsterEnum.ZombieDog: {"weight": 30, "count": 4},
			}, 
        },
	]
}
