# -*- encoding: utf-8 -*-
from .gun_pistol1_base import *

Config = {
	'identifier': 'scuke_survive:gun_pistol1_s3',
	'clipIdentifier': 'scuke_survive:clip_normal',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.00,  # 装备速度修改
	'keyDownMinGap': 0.25,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.25,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -3.0,
		'fovDuration': 0.12,
		'recoil': {
			'angle': 1.0,
			'maxAngle': 12,
			'fov': 1,
			'maxFov': 2,
			'duration': 0.1,
			'backDuration': 0.2,
		}
	},
	'recoil': {
		'angle': 1.0,
		'maxAngle': 12,
		'fov': 1,
		'maxFov': 2,
		'duration': 0.1,
		'backDuration': 0.2,
	},
	'scatter': {
		'angle': 1,
		'max': 6,
		'backDuration': 0.4,
	},
	'reload': {
		'clip': 25,
		'duration': 1.55,
	},
	'kick': {
		'duration': 0.5,
		'cast': 0.1,
		'attack': {
			'shape': {
				'type': 'box',
				'size': (3, 2, 3),
				'offset': (0, 0, 1.5)
			},
			'damage': 7,
			'knock': 0.4,
			'effects': []
		}
	},
	'shootEffect': {
		'type': 'hitscan',
		'distance': 50,
		'hardness': 0.6,  # 硬度
		'hitEffect': {
			'type': 'damage',
			'damage': 4,
			'critical': 4,
			'effects': [],
		},
	},
	'display': {
		'zoomTime': 0.2,
		'crossHair': {
			'type': 'rifle',
			'size': 25,
			'zoomSize': 20,
			'angleSize': 1.0,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_pistol1',
			'model': 'geometry.scuke_survive_gun_pistol1',
			'textureKey': 'scuke_survive_gun_pistol1_s3',
			'texture': 'textures/entity/scuke_survive/gun/gun_pistol1_grain_s3',
			'renderController': 'controller.render.scuke_survive_gun_pistol1_s3',
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
					'name': 'scuke_survive:gun_pistol1_s3_trail',
					'offset': [0, 0.3, 0]
				},
				'first_zoom': {
					'name': 'scuke_survive:gun_pistol1_s3_trail_zoom',
					'offset': [0, 0.3, 0]
				},
				'third': {
					'name': 'scuke_survive:gun_pistol1_s3_trail',
					'offset': [0, 0.3, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_pistol1_s3_fire',
			'gun_firespark': 'scuke_survive:gun_pistol1_s3_firespark',
			'hit_static': 'scuke_survive:gun_pistol1_s3_hit',
			'hit_drop': 'scuke_survive:gun_pistol1_s3_hitdrop',
			'hit_target': 'scuke_survive:gun_pistol1_s3_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.pistol1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'clip_out': 'scuke_survive.gun.common_clip.light_out',
			'clip_in': 'scuke_survive.gun.common_clip.light_in',
			'pick_rot1': 'scuke_survive.gun.common_clip.clip_rot1',
			'pick_rot2': 'scuke_survive.gun.common_clip.clip_rot2',
			'kick': 'game.player.attack.strong',
		}
	}
}