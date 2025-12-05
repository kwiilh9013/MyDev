# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.npcEnum import NPCEnum
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum

_MonsterPool = {
	MonsterEnum.ZombieNormal: {"weight": 30, "count": 5},
	MonsterEnum.ZombieGangs: {"weight": 40, "count": 3},
	MonsterEnum.ZombieChick: {"weight": 30, "count": 4},
}
_BossPool = {
	MonsterEnum.ZombieGiant: {"weight": 30, "count": 1},
}

Config = {
	'identifier': 'scuke_planet_booster:pb1_e_e',
	'structure_name_base': 'scuke_planet_booster:pb1',
	'is_feature_rule': True,
	'center': (224, 0, 224),
	'size': (462, 223, 462),
	'spawnDistance': 48,
	'posMarkers': [
		{'pos': (228, 68, 231), 'id': 'scuke_survive:pos3', 'face': 2},
		{'pos': (233, 15, 232), 'id': 'scuke_survive:pos1', 'face': 3},
		{'pos': (233, 21, 231), 'id': 'scuke_survive:pos2', 'face': 3},
		{'pos': (238, 13, 234), 'id': NPCEnum.Igniter, 'face': 3},
		{'pos': (241, 3, 240), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _BossPool},
		{'pos': (205, 13, 229), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (164, 13, 233), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (161, 3, 218), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (163, 3, 230), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (156, 3, 242), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (189, 3, 228), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (187, 3, 212), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (206, 3, 215), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (234, 3, 215), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (273, 3, 231), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (291, 3, 219), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (335, 3, 265), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (292, 13, 231), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (360, 3, 184), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (338, 13, 124), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (311, 3, 92), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (257, 3, 69), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (228, 17, 51), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (191, 3, 57), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (163, 3, 94), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (120, 13, 123), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (112, 12, 130), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (91, 3, 146), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (96, 13, 230), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (164, 13, 233), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (98, 3, 302), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (125, 8, 330), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (184, 3, 362), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (262, 3, 388), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (334, 13, 340), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		# 宝箱
		{'pos': (214, 4, 230), 'id': 'scuke_survive:chest_pool', 'face': 2, 'chest_pool': {
			BlockEnum.ChestMilitary: {'weight': 100, 'loot_table': 'loot_tables/scuke_survive/chest/weapon_t3.json'},
		}},
	]
}
