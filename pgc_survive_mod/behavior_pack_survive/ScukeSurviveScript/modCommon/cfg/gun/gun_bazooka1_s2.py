# -*- encoding: utf-8 -*-
from .gun_bazooka1_base import *

Config = {
	'identifier': 'scuke_survive:gun_bazooka1_s2',
	'clipIdentifier': 'scuke_survive:clip_explosion',
	'gripType': 'twoHand',  # 握持方式 oneHand, twoHand
	'shootType': 'keyDown',  # 射击触发方式 keyDown, keyUp
	'shooter': 'default',  # 射击控制器
	'carrySpeed': -0.035,  # 装备速度修改
	'keyDownMinGap': 0.8,  # 最小按下开枪间隔
	'zoomTime': 0.25,  # 瞄准时间
	'shootDelay': 0.0,  # 射击前摇
	'shootGap': 0.8,  # 射击间隔
	'shootClip': 1,  # 射击消耗子弹
	'zoom': {
		'fovModify': -12.0,
		'fovDuration': 0.12,
		'recoil': {
			'angle': 18.0,
			'maxAngle': 18,
			'fov': 4,
			'maxFov': 4,
			'duration': 0.12,
			'backDuration': 0.6,
		}
	},
	'recoil': {
		'angle': 20.0,
		'maxAngle': 20,
		'fov': 6,
		'maxFov': 6,
		'duration': 0.12,
		'backDuration': 0.6,
	},
	'scatter': {
		'angle': 1,
		'max': 1,
		'backDuration': 0.1,
	},
	'reload': {
		'clip': 2,
		'duration': 3.3,
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
			'knock': 0.8,
			'effects': []
		}
	},
	'shootEffect': {
		'identifier': 'scuke_survive:bullet_bazooka1_s2',
		'type': 'projectile',
		'lifeTime': 10.0,
		'hitEffect': {
			'type': 'explosion',
			'radius': 3,
			'fire': True,
			'breaks': True,
			'addonDamage': 28,
			'effects': [],
		},
		'display': {
			'particle': {
				'__active__': {
					'name': 'minecraft:critical_hit_emitter',
					'bone': 'body',
				}
			},
		}
	},
	'display': {
		'zoomTime': 0.25,
		'crossHair': {
			'type': 'cannon',
			'size': 20,
			'zoomSize': 18,
			'angleSize': 10.0,
		},
		'trailType': 'projectile',
		'animator': {
			'resKey': 'scuke_survive_gun',
			'modelKey': 'scuke_survive_gun_bazooka1',
			'model': 'geometry.scuke_survive_gun_bazooka1',
			'textureKey': 'scuke_survive_gun_bazooka1_s2',
			'texture': 'textures/entity/scuke_survive/gun/gun_bazooka1_grain_s2',
			'renderController': 'controller.render.scuke_survive_gun_bazooka1_s2',
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
			'gun_fire': 'scuke_survive:gun_bazooka1_s2_fire',
			'gun_firespark': 'scuke_survive:gun_bazooka1_s2_firespark',
			'hit_static': 'scuke_survive:gun_bazooka1_s2_hit',
			'hit_target': 'scuke_survive:gun_bazooka1_s2_hit',
		},
		'sound': {
			'fire': 'scuke_survive.gun.bazooka1.fire',
			'hit': 'random.explode',
			'hit_target': 'random.explode',
			'clip_out': 'scuke_survive.gun.common_clip.clip_out',
			'clip_in': 'scuke_survive.gun.common_clip.clip_in',
			'kick': 'game.player.attack.strong',
		}
	}
}