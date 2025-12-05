# -*- encoding: utf-8 -*-
from .pan_base import *

Config = {
	'identifier': 'scuke_survive:melee_pan_golden',
	'gripType': '',  # 握持方式 oneHand, twoHand
	'carrySpeed': 0.0,  # 装备速度修改
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
			'duration': 0.6,
			'cast': 0.1,
			'attack': {
				'shape': {
					'type': 'box',
					'size': (3, 2, 4),
					'offset': (0, 0, 2)
				},
				'damage': 10,
				'knock': 0.3,
				'effects': []
			},
			'recoil': {
				'fov': 1.0,
				'duration': 0.2,
				'backDuration': 0.1,
			}
		},
		{
			'type': 'emit',
			'duration': 0.8,
			'cast': 0.1,
			'attack': {
				'shape': {
					'type': 'box',
					'size': (3, 2, 4),
					'offset': (0, 0, 2)
				},
				'damage': 10,
				'knock': 0.3,
				'effects': []
			},
			'recoil': {
				'fov': 1.0,
				'duration': 0.2,
				'backDuration': 0.1,
			}
		}

	],
	'display': {
		'takingTime': 0.0,  # 启动时间
		'animator': {
			'resKey': 'scuke_survive_melee_pan',
			'model': 'geometry.scuke_survive_melee_pan',
			'textureKey': 'scuke_survive_melee_pan_golden',
			'texture': 'textures/models/scuke_survive/melee/melee_pan_golden',
			'renderController': 'controller.render.scuke_survive_melee_pan_golden',
			'hands': {
				'resKey': 'scuke_survive_weaponhands',
				'renderController': 'controller.render.scuke_survive_weaponhands',
			},
			'first': FirstAnimator,
			'third': ThirdAnimator
		},
		'particle': {
			'first_swing1': 'scuke_survive:melee_pan_swing1',
			'first_swing2': 'scuke_survive:melee_pan_swing2',
			'third_swing1': 'scuke_survive:melee_pan_swing1_third',
			'third_swing2': 'scuke_survive:melee_pan_swing2_third',
			'hit_target': 'scuke_survive:hit_target',
		},
		'sound': {
			'swing1': 'scuke_survive.melee.pan.swing',
			'swing2': 'scuke_survive.melee.pan.swing',
			'hit_target': 'scuke_survive.melee.pan.hit',
		}
	},
}
