# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum

Config = {
	'identifier': 'scuke_train_workshop:train_workshop_7_1',
	'structure_name_base': 'scuke_train_workshop:train_workshop',
	'is_feature_rule': True,
	'center': (112, 0, 16),
	'size': (218, 39, 47),
	'posMarkers': [
		{'pos': (183, 11, 16), 'id': 'scuke_survive:monster_pool', 'face': 2,
			'entity_pool': {
				MonsterEnum.ZombieTonsKing: {"weight": 20, "count": 2},
				MonsterEnum.ZombieSpecialGuard: {"weight": 30, "count": 3},
				MonsterEnum.ZombieBigDog: {"weight": 20, "count": 4},
				MonsterEnum.ZombieJocker: {"weight": 20, "count": 4},
				MonsterEnum.ZombieVenom: {"weight": 20, "count": 5},
			},
		},
		{'pos': (172, 11, 30), 'id': 'scuke_survive:monster_pool', 'face': 0,
			'entity_pool': {
				MonsterEnum.ZombieTonsKing: {"weight": 20, "count": 4},
				MonsterEnum.ZombieSpecialGuard: {"weight": 40, "count": 3},
				MonsterEnum.ZombieSuperTNT: {"weight": 20, "count": 4},
				MonsterEnum.ZombieHypertensionGrandpa: {"weight": 20, "count": 5},
				MonsterEnum.ZombieSpicyChick: {"weight": 20, "count": 5},
			},
		},
		{'pos': (208, 11, 20), 'id': 'scuke_survive:monster_pool', 'face': 3,
			'entity_pool': {
				MonsterEnum.ZombieFlameVenom: {"weight": 20, "count": 4},
				MonsterEnum.ZombieSpecialGuard: {"weight": 40, "count": 5},
				MonsterEnum.ZombieSuperTNT: {"weight": 40, "count": 4},
				MonsterEnum.ZombieHypertensionGrandpa: {"weight": 20, "count": 3},
				MonsterEnum.ZombieGoldenChick: {"weight": 20, "count": 3},
			},
		},
	]
}
