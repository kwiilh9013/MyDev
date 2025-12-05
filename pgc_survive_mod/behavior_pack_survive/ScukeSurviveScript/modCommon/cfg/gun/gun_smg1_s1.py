# -*- encoding: utf-8 -*-
from .gun_smg1_base import *

Config = {
	'identifier': 'scuke_survive:gun_smg1',
	'clipIdentifier': 'scuke_survive:clip_normal',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.002,  # 装备速度修改
	'keyDownMinGap': 0.15,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.1,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -3.0,
		'fovDuration': 0.12,
		'recoil': {
			'angle': 0.8,
			'maxAngle': 60,
			'fov': 0.4,
			'maxFov': 3,
			'duration': 0.1,
			'backDuration': 0.5,
		}
	},
	'recoil': {
		'angle': 1.0,
		'maxAngle': 60,
		'fov': 0.5,
		'maxFov': 4,
		'duration': 0.1,
		'backDuration': 0.5,
	},
	'scatter': {
		'angle': 1,
		'max': 5,
		'backDuration': 0.6,
	},
	'reload': {
		'clip': 12,
		'duration': 1.90,
	},
	'kick': {
		'duration': 0.5,
		'cast': 0.1,
		'attack': {
			'shape': {
				'type': 'box',
				'size': (3, 2, 4),
				'offset': (0, 0, 2)
			},
			'damage': 5,
			'knock': 0.4,
			'effects': []
		}
	},
	'shootEffect': {
		'type': 'hitscan',
		'distance': 70,
		'hardness': 0.6,  # 硬度
		'hitEffect': {
			'type': 'damage',
			'damage': 1,
			'critical': 1,
			'effects': [],
		},
	},
	'display': {
		'zoomTime': 0.25,
		'crossHair': {
			'type': 'submachine',
			'size': 25,
			'zoomSize': 20,
			'angleSize': 1.5,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_smg1',
			'model': 'geometry.scuke_survive_gun_smg1',
			'textureKey': 'scuke_survive_gun_smg1_s1',
			'texture': 'textures/entity/scuke_survive/gun/gun_smg1_grain',
			'renderController': 'controller.render.scuke_survive_gun_smg1_s1',
			'mat': {
				"ssg_normal": "scuke_survive_gun_normal"
			},
			'hands': {
				'resKey': 'scuke_survive_weaponhands',
				'renderController': 'controller.render.scuke_survive_weaponhands',
			},
			'first': FirstAnimator,
			'third': ThirdAnimator
		},
		'particle': {
			'trail': {
				'first': {
					'name': 'scuke_survive:gun_smg1_s1_trail',
					'offset': [0, 0.375, 0]
				},
				'first_zoom': {
					'name': 'scuke_survive:gun_smg1_s1_trail_zoom',
					'offset': [0, 0.375, 0]
				},
				'third': {
					'name': 'scuke_survive:gun_smg1_s1_trail',
					'offset': [0, 0.375, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_smg1_s1_fire',
			'gun_firespark': 'scuke_survive:gun_smg1_s1_firespark',
			'hit_static': 'scuke_survive:gun_smg1_s1_hit',
			'hit_drop': 'scuke_survive:gun_smg1_s1_hitdrop',
			'hit_target': 'scuke_survive:gun_smg1_s1_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.smg1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'clip_out': 'scuke_survive.gun.common_clip.middle_out1',
			'clip_in1': 'scuke_survive.gun.common_clip.clip_rot3',
			'clip_in2': 'scuke_survive.gun.common_clip.clip_rot4',
			'kick': 'game.player.attack.strong',
		}
	}
}