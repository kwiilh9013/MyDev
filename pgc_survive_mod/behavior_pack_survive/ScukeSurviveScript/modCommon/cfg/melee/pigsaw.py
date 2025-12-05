# -*- encoding: utf-8 -*-
from .pigsaw_base import *

Config = {
	'identifier': 'scuke_survive:melee_pigsaw',
	'gripType': '',  # 握持方式 oneHand, twoHand
	'carrySpeed': -0.02,  # 装备速度修改
	'cooldownTime': 0.45,  # 冷却时间
	'takingTime': 1.5,  # 启动时间
	'meleeDelay': 0.09,  # 前摇
	'kick': {
		'duration': 0.5,
		'damage': 5,
		'radius': 1,
	},
	'meleeEffects': [
		{
			'type': 'loop',
			'duration': 0.09,
			'cast': 0.03,
			'attack': {
				'shape': {
					'type': 'box',
					'size': (2, 1, 3),
					'offset': (0, 0, 1.5)
				},
				'damage': 2,
				'knock': 0.1,
				'effects': []
			},
			'recoil': {
				'fov': 0.5,
				'maxFov': 1.0,
				'duration': 0.03,
				'backDuration': 0.06,
			}
		},
	],
	'display': {
		'takingTime': 1.5,  # 启动时间
		'animator': {
			'resKey': 'scuke_survive_melee_pigsaw',
			'model': 'geometry.scuke_survive_melee_pigsaw',
			'textureKey': 'scuke_survive_melee_pigsaw',
			'texture': 'textures/models/scuke_survive/melee/melee_pigsaw',
			'renderController': 'controller.render.scuke_survive_melee_pigsaw',
			'hands': {
				'resKey': 'scuke_survive_weaponhands',
				'renderController': 'controller.render.scuke_survive_weaponhands',
			},
			'first': FirstAnimator,
			'third': ThirdAnimator
		},
		'particle': {
			'hit_target': 'scuke_survive:hit_target',
		},
		'sound': {
			'using': 'scuke_survive.melee.chainsaw.using',
			'using1': 'mob.pig.say',
			'using2': 'mob.pig.say',
		}
	},
}
