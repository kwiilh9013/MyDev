# -*- encoding: utf-8 -*-
from .gun_hmg1_base import *

Config = {
	'identifier': 'scuke_survive:gun_hmg1',
	'clipIdentifier': 'scuke_survive:clip_energy',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.028,  # 装备速度修改
	'keyDownMinGap': 0.1,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.05,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -7.0,
		'fovDuration': 0.23,
		'recoil': {
			'angle': 0.1,
			'maxAngle': 70,
			'fov': 0.2,
			'maxFov': 3,
			'duration': 0.07,
			'backDuration': 0.5,
		}
	},
	'recoil': {
		'angle': 0.25,
		'maxAngle': 70,
		'fov': 0.4,
		'maxFov': 4,
		'duration': 0.07,
		'backDuration': 0.5,
	},
	'scatter': {
		'angle': 0.3,
		'max': 4,
		'backDuration': 0.6,
	},
	'reload': {
		'clip': 120,
		'duration': 4.3,
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
			'damage': 9,
			'knock': 0.7,
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
			'type': 'machine',
			'size': 55,
			'zoomSize': 50,
			'angleSize': 1,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_hmg1',
			'model': 'geometry.scuke_survive_gun_hmg1',
			'textureKey': 'scuke_survive_gun_hmg1_s3',
			'texture': 'textures/entity/scuke_survive/gun/gun_hmg1_grain',
			'renderController': 'controller.render.scuke_survive_gun_hmg1_s3',
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
					'name': 'scuke_survive:gun_hmg1_s3_trail',
					'offset': [0, 0.18, 0]
				},
				'first_zoom': {
					'name': 'scuke_survive:gun_hmg1_s3_trail_zoom',
					'offset': [0, 0.18, 0]
				},
				'third': {
					'name': 'scuke_survive:gun_hmg1_s3_trail',
					'offset': [0, 0.18, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_hmg1_s3_fire',
			'gun_firespark': 'scuke_survive:gun_hmg1_s3_firespark',
			'hit_static': 'scuke_survive:gun_hmg1_s3_hit',
			'hit_drop': 'scuke_survive:gun_hmg1_s3_hitdrop',
			'hit_target': 'scuke_survive:gun_hmg1_s3_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.hmg1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'clip_out1': 'scuke_survive.gun.common_clip.heavy_out',
			'clip_out2': 'scuke_survive.gun.common_clip.light_out',
			'clip_in1': 'scuke_survive.gun.common_clip.light_in',
			'clip_in2': 'scuke_survive.gun.common_clip.heavy_in',
			'kick': 'game.player.attack.strong',
		}
	}
}