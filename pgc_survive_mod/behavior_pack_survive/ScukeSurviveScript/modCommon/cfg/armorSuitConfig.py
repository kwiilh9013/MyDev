# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.buffEnum import BuffEnum

Config = [
	{
		'name': '雪地迷彩套装',
		'tag': 'suit_snow02',
		'armors': [
			'scuke_survive:armor_snow02_helmet',
			'scuke_survive:armor_snow02_chest',
			'scuke_survive:armor_snow02_legs',
			'scuke_survive:armor_snow02_boots',
		],
		'buffs': [
			{'type': 'speed', 'amplifier': 0},
		]
	},
	{
		'name': '金星MK1套装',
		'tag': 'suit_safety',
		'armors': [
			'scuke_survive:armor_safety_helmet',
			'scuke_survive:armor_safety_chest',
			'scuke_survive:armor_safety_legs',
			'scuke_survive:armor_safety_boots',
		],
		'buffs': [
			{'type': 'absorption', 'amplifier': 0},
		]
	},
	{
		'name': '火星MK1救援套装',
		'tag': 'suit_red_rescue',
		'armors': [
			'scuke_survive:armor_red_rescue_helmet',
			'scuke_survive:armor_red_rescue_chest',
			'scuke_survive:armor_red_rescue_legs',
			'scuke_survive:armor_red_rescue_boots',
		],
		'buffs': [
			{'type': 'strength', 'amplifier': 0},
			{'type': 'speed', 'amplifier': 0},
		]
	},
	{
		'name': '月球MK1救援套装',
		'tag': 'suit_black_rescue',
		'armors': [
			'scuke_survive:armor_black_rescue_helmet',
			'scuke_survive:armor_black_rescue_chest',
			'scuke_survive:armor_black_rescue_legs',
			'scuke_survive:armor_black_rescue_boots',
		],
		'buffs': [
			{'type': 'health_boost', 'amplifier': 0},
			{'type': 'speed', 'amplifier': 0},
		]
	},
	{
		'name': '光晕MK1套装',
		'tag': 'suit_armor01',
		'armors': [
			'scuke_survive:armor_armor01_helmet',
			'scuke_survive:armor_armor01_chest',
			'scuke_survive:armor_armor01_legs',
			'scuke_survive:armor_armor01_boots',
		],
		'buffs': [
			{'type': BuffEnum.GunDamage, 'amplifier': 0},
			{'type': 'health_boost', 'amplifier': 0},
		]
	},
	{
		'name': '白矮星MK1套装',
		'tag': 'suit_armor02',
		'armors': [
			'scuke_survive:armor_armor02_helmet',
			'scuke_survive:armor_armor02_chest',
			'scuke_survive:armor_armor02_legs',
			'scuke_survive:armor_armor02_boots',
		],
		'buffs': [
			{'type': BuffEnum.GunDamage, 'amplifier': 0},
			{'type': 'health_boost', 'amplifier': 0},
			{'type': 'speed', 'amplifier': 0},
		]
	},
]
