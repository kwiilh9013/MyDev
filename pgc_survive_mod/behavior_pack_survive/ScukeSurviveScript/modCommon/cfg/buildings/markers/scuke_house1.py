# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum

Config = {
	# structure id
	'identifier': 'scuke_house1:house1_1_1',
	'structure_name_base': 'scuke_house1:house1',
	'is_feature_rule': True,
	'chunkSize': 16,
	'center': (16, 0, 16),
	'size': (40, 18, 24),
	'posMarkers': [
		{
			'pos': (21, 4, 18), 'face': 1, 'id': 'scuke_survive:monster_pool',
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 60, "count": 5},
				MonsterEnum.ZombieGangs: {"weight": 40, "count": 3},
			}, 
		},
		{
			'pos': (9, 4, 10), 'face': 0, 'id': 'scuke_survive:monster_pool',
			'entity_pool': {
				MonsterEnum.ZombieNormal: {"weight": 50, "count": 3},
			}, 
		},
	],
}
