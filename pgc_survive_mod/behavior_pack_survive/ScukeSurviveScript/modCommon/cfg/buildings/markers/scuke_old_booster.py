# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.npcEnum import NPCEnum
from ScukeSurviveScript.modCommon.defines.blockEnum import BlockEnum

_MonsterPool = {
	MonsterEnum.ZombieNormal: {'weight': 30, 'count': 5},
	MonsterEnum.ZombieGangs: {'weight': 40, 'count': 3},
	MonsterEnum.ZombieChick: {'weight': 30, 'count': 4},
}
_BossPool = {
	MonsterEnum.ZombieGiant: {'weight': 30, 'count': 1},
}

Config = {
	'identifier': 'scuke_old_booster:pb0_e_e',
	'structure_name_base': 'scuke_old_booster:pb0',
	'is_feature_rule': True,
	'center': (224, 0, 224),
	'size': (454, 235, 460),
	'spawnDistance': 48,
	'posMarkers': [
		{'pos': (424, 21, 170), 'id': 'scuke_survive:base_car_broken', 'face': 3},
		{'pos': (447, 2, 200), 'id': 'scuke_survive:pos2', 'face': 1},
		{'pos': (236, 30, 235), 'id': NPCEnum.Taojiji, 'face': 3},
		{'pos': (237, 30, 238), 'id': NPCEnum.GoldenCreeper, 'face': 3},
		{'pos': (233, 30, 239), 'id': NPCEnum.GoldenCreeper, 'face': 3},
		{'pos': (237, 30, 241), 'id': NPCEnum.GoldenCreeper, 'face': 3},
		{'pos': (435, 2, 201), 'id': NPCEnum.Keke, 'face': 3},
		{'pos': (430, 21, 165), 'id': 'scuke_survive:npc_zhanjing', 'face': 0},
		{'pos': (241, 20, 240), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _BossPool},
		{'pos': (205, 30, 229), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (164, 30, 233), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (161, 20, 218), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (163, 20, 230), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (156, 20, 242), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (189, 20, 228), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (187, 20, 212), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (206, 20, 215), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (234, 20, 215), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (273, 20, 231), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (291, 20, 219), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (335, 20, 265), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (292, 30, 231), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (360, 20, 184), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (338, 30, 124), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (311, 20, 92), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (257, 20, 69), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (228, 34, 51), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (191, 20, 57), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (163, 20, 94), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (120, 30, 123), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (112, 29, 130), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (91, 20, 146), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (96, 30, 230), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (164, 30, 233), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (98, 20, 302), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (125, 25, 330), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (184, 20, 362), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (262, 20, 388), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		{'pos': (334, 30, 340), 'id': 'scuke_survive:monster_pool', 'face': 0, 'entity_pool': _MonsterPool},
		# 奖励箱
		{'pos': (434, 3, 199), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': {
			BlockEnum.ShulkerBox: {'weight': 100, 'loot_table': 'loot_tables/scuke_survive/chest/init_0.json'},
		}},
		{'pos': (239, 20, 234), 'id': 'scuke_survive:chest_pool', 'face': 0, 'chest_pool': {
			BlockEnum.ChestPaperTag: {'weight': 100, 'loot_table': 'loot_tables/scuke_survive/chest/init_pb.json', 'isIgnore_spilt': True},
		}},
		{'pos': (212, 21, 229), 'id': 'scuke_survive:chest_pool', 'face': 2, 'chest_pool': {
			BlockEnum.ChestMilitary: {'weight': 100, 'loot_table': 'loot_tables/scuke_survive/chest/weapon_t3.json'},
		}},
		# 改造台
		{'pos': (426, 21, 164), 'id': 'scuke_survive:chest_pool', 'face': 2, 'chest_pool': {BlockEnum.CarRemold: {'weight': 100,},}},
	]
}
