# -*- encoding: utf-8 -*-
from .gun_shotgun1_base import *

Config = {
	'identifier': 'scuke_survive:gun_shotgun1_s2',
	'clipIdentifier': 'scuke_survive:clip_advanced',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.018,  # 装备速度修改
	'keyDownMinGap': 0.55,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.5,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -5.0,
		'fovDuration': 0.12,
		'recoil': {
			'angle': 4.0,
			'maxAngle': 12,
			'fov': 3,
			'maxFov': 3,
			'duration': 0.07,
			'backDuration': 0.3,
		}
	},
	'recoil': {
		'angle': 5.0,
		'maxAngle': 12,
		'fov': 5,
		'maxFov': 5,
		'duration': 0.07,
		'backDuration': 0.3,
	},
	'scatter': {
		'angle': 10,
		'max': 12,
		'backDuration': 0.4,
	},
	'reload': {
		'clip': 8,
		'duration': 2.30,
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
			'damage': 7,
			'knock': 0.5,
			'effects': []
		}
	},
	'shootEffect': {
		'type': 'shot',
		'distance': 30,
		'hardness': 0.6,  # 硬度
		'angle': 12,
		'count': 8,
		'hitEffect': {
			'type': 'damage',
			'damage': 1,
			'critical': 1,
			'effects': [],
		},
	},
	'display': {
		'zoomTime': 0.3,
		'crossHair': {
			'type': 'shot',
			'size': 55,
			'zoomSize': 50,
			'angleSize': 2.0,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_shotgun1',
			'model': 'geometry.scuke_survive_gun_shotgun1',
			'textureKey': 'scuke_survive_gun_shotgun1_s2',
			'texture': 'textures/entity/scuke_survive/gun/gun_shotgun1_grain_s2',
			'renderController': 'controller.render.scuke_survive_gun_shotgun1_s2',
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
					'name': 'scuke_survive:gun_shotgun1_s2_trail',
					'offset': [0, 0.25, 0]
				},
				'first_zoom': {
					'name': 'scuke_survive:gun_shotgun1_s2_trail_zoom',
					'offset': [0, 0.25, 0]
				},
				'third': {
					'name': 'scuke_survive:gun_shotgun1_s2_trail',
					'offset': [0, 0.25, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_shotgun1_s2_fire',
			'gun_firespark': 'scuke_survive:gun_shotgun1_s2_firespark',
			'hit_static': 'scuke_survive:gun_shotgun1_s2_hit',
			'hit_drop': 'scuke_survive:gun_shotgun1_s2_hitdrop',
			'hit_target': 'scuke_survive:gun_shotgun1_s2_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.shotgun1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'clip_out': 'scuke_survive.gun.common_clip.shotgun_out',
			'clip_in': 'scuke_survive.gun.common_clip.shotgun_in',
			'kick': 'game.player.attack.strong',
		}
	}
}