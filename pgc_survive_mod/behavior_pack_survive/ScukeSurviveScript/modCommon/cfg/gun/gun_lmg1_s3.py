# -*- encoding: utf-8 -*-
from .gun_lmg1_base import *

Config = {
	'identifier': 'scuke_survive:gun_lmg1',
	'clipIdentifier': 'scuke_survive:clip_energy',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.018,  # 装备速度修改
	'keyDownMinGap': 0.15,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.11,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -8.0,
		'fovDuration': 0.18,
		'recoil': {
			'angle': 0.4,
			'maxAngle': 70,
			'fov': 0.2,
			'maxFov': 2,
			'duration': 0.1,
			'backDuration': 0.3,
		}
	},
	'recoil': {
		'angle': 0.5,
		'maxAngle': 70,
		'fov': 0.2,
		'maxFov': 2,
		'duration': 0.1,
		'backDuration': 0.3,
	},
	'scatter': {
		'angle': 0.2,
		'max': 2.5,
		'backDuration': 1.0,
	},
	'reload': {
		'clip': 40,
		'duration': 2.3,
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
			'damage': 8,
			'knock': 0.6,
			'effects': []
		}
	},
	'shootEffect': {
		'type': 'hitscan',
		'distance': 100,
		'hardness': 0.6,  # 硬度
		'hitEffect': {
			'type': 'damage',
			'damage': 3,
			'critical': 3,
			'effects': [],
		},
	},
	'display': {
		'zoomTime': 0.24,
		'crossHair': {
			'type': 'rifle',
			'size': 25,
			'zoomSize': 20,
			'angleSize': 2.0,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_lmg1',
			'model': 'geometry.scuke_survive_gun_lmg1',
			'textureKey': 'scuke_survive_gun_lmg1_s3',
			'texture': 'textures/entity/scuke_survive/gun/gun_lmg1_grain',
			'renderController': 'controller.render.scuke_survive_gun_lmg1_s3',
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
					'name': 'scuke_survive:gun_lmg1_s3_trail',
					'offset': [0, 0.2, 0]
				},
				'first_zoom': {
					'name': 'scuke_survive:gun_lmg1_s3_trail_zoom',
					'offset': [0, 0.2, 0]
				},
				'third': {
					'name': 'scuke_survive:gun_lmg1_s3_trail',
					'offset': [0, 0.2, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_lmg1_s3_fire',
			'gun_firespark': 'scuke_survive:gun_lmg1_s3_firespark',
			'hit_static': 'scuke_survive:gun_lmg1_s3_hit',
			'hit_drop': 'scuke_survive:gun_lmg1_s3_hitdrop',
			'hit_target': 'scuke_survive:gun_lmg1_s3_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.lmg1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'clip_out': 'scuke_survive.gun.common_clip.middle_out3',
			'clip_in': 'scuke_survive.gun.common_clip.light_out',
			'kick': 'game.player.attack.strong',
		}
	}
}