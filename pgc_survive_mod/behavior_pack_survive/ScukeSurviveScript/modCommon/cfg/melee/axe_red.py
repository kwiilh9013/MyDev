# -*- encoding: utf-8 -*-
from .axe_base import *

Config = {
	'identifier': 'scuke_survive:melee_axe_red',
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
			'type': 'emit',
			'duration': 0.8,
			'cast': 0.2,
			'attack': {
				'shape': {
					'type': 'box',
					'size': (3, 2, 4),
					'offset': (0, 0, 2)
				},
				'damage': 6,
				'knock': 0.3,
				'effects': []
			},
			'recoil': {
				'fov': 2.0,
				'duration': 0.3,
				'backDuration': 0.1,
			}
		},
		{
			'type': 'emit',
			'duration': 1.0,
			'cast': 0.2,
			'attack': {
				'shape': {
					'type': 'box',
					'size': (3, 2, 4),
					'offset': (0, 0, 2)
				},
				'damage': 7,
				'knock': 0.3,
				'effects': []
			},
			'recoil': {
				'fov': 2.0,
				'duration': 0.3,
				'backDuration': 0.1,
			}
		},
		{
			'type': 'emit',
			'duration': 1.0,
			'cast': 0.45,
			'attack': {
				'shape': {
					'type': 'box',
					'size': (2, 2, 4),
					'offset': (0, 0, 2)
				},
				'damage': 9,
				'knock': 0.5,
				'effects': []
			},
			'recoil': {
				'fov': 3.0,
				'duration': 0.45,
				'backDuration': 0.2,
			}
		},

	],
	'display': {
		'takingTime': 0.0,  # 启动时间
		'animator': {
			'resKey': 'scuke_survive_melee_axe',
			'model': 'geometry.scuke_survive_melee_axe',
			'textureKey': 'scuke_survive_melee_axe_red',
			'texture': 'textures/models/scuke_survive/melee/melee_axe_red',
			'renderController': 'controller.render.scuke_survive_melee_axe_red',
			'hands': {
				'resKey': 'scuke_survive_weaponhands',
				'renderController': 'controller.render.scuke_survive_weaponhands',
			},
			'first': FirstAnimator,
			'third': ThirdAnimator
		},
		'particle': {
			'first_swing1': 'scuke_survive:melee_axe_swing1',
			'first_swing2': 'scuke_survive:melee_axe_swing2',
			'first_swing3': 'scuke_survive:melee_axe_swing3',
			'third_swing1': 'scuke_survive:melee_axe_swing1_third',
			'third_swing2': 'scuke_survive:melee_axe_swing2_third',
			'third_swing3': 'scuke_survive:melee_axe_swing3_third',
			'hit_target': 'scuke_survive:hit_target',
		},
		'sound': {
			'swing1': 'scuke_survive.melee.axe.swing1',
			'swing2': 'scuke_survive.melee.axe.swing2',
			'swing3': 'scuke_survive.melee.axe.swing3',
		}
	},
}
