# -*- encoding: utf-8 -*-
from .gun_sniper1_base import *

Config = {
	'identifier': 'scuke_survive:gun_sniper1_s2',
	'clipIdentifier': 'scuke_survive:clip_energy',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyUp',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.02,  # 装备速度修改
	'keyDownMinGap': 0.12,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.25,  # 射击前摇
	'shootGap': 0.9,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -5.0,
		'fovDuration': 0.12,
		'recoil': {
			'angle': 9.0,
			'maxAngle': 20,
			'fov': 4,
			'maxFov': 4,
			'duration': 0.20,
			'backDuration': 0.3,
		}
	},
	'recoil': {
		'angle': 10.0,
		'maxAngle': 20,
		'fov': 5,
		'maxFov': 5,
		'duration': 0.20,
		'backDuration': 0.3,
	},
	'scatter': {
		'angle': 12,
		'max': 12,
		'backDuration': 0.5,
	},
	'reload': {
		'clip': 5,
		'duration': 3.30,
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
			'knock': 0.7,
			'effects': []
		}
	},
	'charge': {
		'levels': [
			{'time': 0.9, 'coef': 0.6},
			{'time': 0.9, 'coef': 1.0},
			{'time': 0.9, 'coef': 1.2},
		]
	},
	'shootEffect': {
		'type': 'level',
		'levels': [
			{
				'type': 'laser',
				'distance': 60,
				'size': (1, 1),
				'splitSize': 0.3,
				'hardness': 2.0,  # 硬度
				'hitEffect': {
					'type': 'damage',
					'damage': 28,
					'critical': 28,
					'effects': [],
				}
			},
			{
				'type': 'laser',
				'distance': 80,
				'size': (1, 1),
				'splitSize': 0.7,
				'hardness': 2.0,  # 硬度
				'hitEffect': {
					'type': 'damage',
					'damage': 28,
					'critical': 28,
					'effects': [],
				}
			},
			{
				'type': 'laser',
				'distance': 100,
				'size': (2, 2),
				'splitSize': 0.3,
				'hardness': 2.0,  # 硬度
				'hitEffect': {
					'type': 'damage',
					'damage': 28,
					'critical': 28,
					'effects': [],
				}
			},
		]
	},
	'display': {
		'zoomTime': 0.3,
		'crossHair': {
			'type': 'charger',
			'size': 50,
			'zoomSize': 45,
			'angleSize': 1.0,
		},
		'trailType': 'hitscan',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_sniper1',
			'model': 'geometry.scuke_survive_gun_sniper1',
			'textureKey': 'scuke_survive_gun_sniper1_s2',
			'texture': 'textures/entity/scuke_survive/gun/gun_sniper1_grain_s2',
			'renderController': 'controller.render.scuke_survive_gun_sniper1_s2',
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
					'name': [
						'scuke_survive:gun_sniper1_trail_1',
						'scuke_survive:gun_sniper1_trail_2',
						'scuke_survive:gun_sniper1_trail_3',
					],
					'offset': [0, 0.1, 0]
				},
				'first_zoom': {
					'name': [
						'scuke_survive:gun_sniper1_trail_zoom_1',
						'scuke_survive:gun_sniper1_trail_zoom_2',
						'scuke_survive:gun_sniper1_trail_zoom_3',
					],
					'offset': [0, 0.1, 0]
				},
				'third': {
					'name': [
						'scuke_survive:gun_sniper1_trail_1',
						'scuke_survive:gun_sniper1_trail_2',
						'scuke_survive:gun_sniper1_trail_3',
					],
					'offset': [0, 0.1, 0]
				}
			},
			'gun_fire': 'scuke_survive:gun_sniper1_fire',
			'charge_loop': 'scuke_survive:gun_sniper1_firecharge',
			'gun_firespark': 'scuke_survive:gun_sniper1_firespark',
			'hit_static': 'scuke_survive:gun_sniper1_hit',
			'hit_drop': 'scuke_survive:gun_sniper1_hitdrop',
			'hit_target': 'scuke_survive:gun_sniper1_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.sniper1.fire',
			'hit': 'scuke_survive.gun.common_hit.hit',
			'hit_target': 'scuke_survive.gun.common_hit.hit_target',
			'charge_loop': 'scuke_survive.gun.common_clip.charge_loop',
			'clip_out': 'scuke_survive.gun.common_clip.heavy_out',
			'clip_in1': 'scuke_survive.gun.common_clip.middle_in1',
			'clip_in2': 'scuke_survive.gun.common_clip.middle_in2',
			'kick': 'game.player.attack.strong',
		}
	}
}