# -*- encoding: utf-8 -*-
from .gun_rifle1_base import *

Config = {
	'identifier': 'scuke_survive:gun_rifle1_s2',
	'clipIdentifier': 'scuke_survive:clip_advanced',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.014,  # 装备速度修改
	'keyDownMinGap': 0.25,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.2,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -6.0,
		'fovDuration': 0.12,
		'recoil': {
			'angle': 0.8,
			'maxAngle': 30,
			'fov': 0.5,
			'maxFov': 4,
			'duration': 0.06,
			'backDuration': 0.2,
		}
	},
	'recoil': {
		'angle': 1.0,
		'maxAngle': 75,
		'fov': 0.8,
		'maxFov': 5,
		'duration': 0.06,
		'backDuration': 0.2,
	},
	'scatter': {
		'angle': 0.6,
		'max': 3,
		'backDuration': 0.4,
	},
	'reload': {
		'clip': 30,
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
		'zoomTime': 0.23,
		'crossHair': {
			'type': 'rifle',
			'size': 25,
			'zoomSize': 20,
			'angleSize': 2.0,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_rifle1',
			'model': 'geometry.scuke_survive_gun_rifle1',
			'textureKey': 'scuke_survive_gun_rifle1_s2',
			'texture': 'textures/entity/scuke_survive/gun/gun_rifle1_grain_s2',
			'renderController': 'controller.render.scuke_survive_gun_rifle1_s2',
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
					'name': 'scuke_survive:gun_rifle1_s2_trail',
					'offset': [0, 0.25, 0]
				},
				'first_zoom': {
					'name': 'scuke_survive:gun_rifle1_s2_trail_zoom',
					'offset': [0, 0.25, 0]
				},
				'third': {
					'name': 'scuke_survive:gun_rifle1_s2_trail',
					'offset': [0, 0.25, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_rifle1_s2_fire',
			'gun_firespark': 'scuke_survive:gun_rifle1_s2_firespark',
			'hit_static': 'scuke_survive:gun_rifle1_s2_hit',
			'hit_drop': 'scuke_survive:gun_rifle1_s2_hitdrop',
			'hit_target': 'scuke_survive:gun_rifle1_s2_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.rifle1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'clip_out': 'scuke_survive.gun.common_clip.middle_out3',
			'clip_in': 'scuke_survive.gun.common_clip.middle_in1',
			'kick': 'game.player.attack.strong',
		}
	}
}