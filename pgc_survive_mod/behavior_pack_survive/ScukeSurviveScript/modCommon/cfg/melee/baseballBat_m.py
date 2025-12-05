# -*- encoding: utf-8 -*-
from .baseballBat_base import *

Config = {
	'identifier': 'scuke_survive:melee_baseball_bat_m',
	'gripType': '',  # 握持方式 oneHand, twoHand
	'carrySpeed': -0.01,  # 装备速度修改
	'cooldownTime': 0.3,  # combo冷却时间
	'takingTime': 0.0,  # 启动时间
	'meleeDelay': 0.0,  # 前摇
	'kick': {
		'duration': 0.5,
		'damage': 5,
		'radius': 1,
	},
	'meleeEffects': [
		{
			'type': 'charge',
			'duration': 0.7,
			'cast': 0.1,
			'levels': [
				0.5,
				1.2,
				2.0,
			],
			'attacks': [
				{
					'level': 1,
					'shape': {
						'type': 'box',
						'size': (3, 2, 4),
						'offset': (0, 0, 2)
					},
					'damage': 6,
					'knock': 0.3,
					'effects': []
				},
				{
					'level': 2,
					'shape': {
						'type': 'box',
						'size': (3, 2, 4),
						'offset': (0, 0, 2)
					},
					'damage': 9,
					'knock': 0.5,
					'effects': []
				},
				{
					'level': 3,
					'shape': {
						'type': 'box',
						'size': (3, 2, 4),
						'offset': (0, 0, 2)
					},
					'damage': 12,
					'knock': 1,
					'effects': []
				}
			],
			'recoil': {
				'fov': 4.0,
				'duration': 0.25,
				'backDuration': 0.1,
			}
		},
	],
	'display': {
		'takingTime': 0.0,  # 启动时间
		'animator': {
			'resKey': 'scuke_survive_melee_baseball_bat',
			'model': 'geometry.scuke_survive_melee_baseball_bat',
			'textureKey': 'scuke_survive_melee_baseball_bat_m',
			'texture': 'textures/models/scuke_survive/melee/melee_baseball_bat_m',
			'renderController': 'controller.render.scuke_survive_melee_baseball_bat_m',
			'hands': {
				'resKey': 'scuke_survive_weaponhands',
				'renderController': 'controller.render.scuke_survive_weaponhands',
			},
			'first': FirstAnimator,
			'third': ThirdAnimator
		},
		'particle': {
			'first_swing1': 'scuke_survive:melee_baseball_bat_swing1',
			'first_swing2': 'scuke_survive:melee_baseball_bat_swing2',
			'first_swing3': 'scuke_survive:melee_baseball_bat_swing3',
			'third_swing1': 'scuke_survive:melee_baseball_bat_swing1_third',
			'third_swing2': 'scuke_survive:melee_baseball_bat_swing1_third',
			'third_swing3': 'scuke_survive:melee_baseball_bat_swing1_third',
			'hit_target': 'scuke_survive:hit_target',
		},
		'sound': {
			'swing1': 'scuke_survive.melee.baseball_bat.swing1',
			'swing2': 'scuke_survive.melee.baseball_bat.swing2',
			'swing3': 'scuke_survive.melee.baseball_bat.swing3',
		}
	},
}
