# -*- encoding: utf-8 -*-

Config = {
	'render_low_temp': {
		'priority': 0,
		'molang': {
			'scuke_survive_render_effect': 1,
			'scuke_survive_low_temp_shaking': 1,
		}
	},
	'render_high_temp': {
		'priority': 0,
		'molang': {
			'scuke_survive_render_effect': 2,
		}
	},
	'screen_high_temp': {
		'priority': 1,
		'vignette': True,
		'center': (0.5, 0.5),
		'rgb': (252, 141, 0),
		'radius': 1.0,
		'smoothness': 0.7,
	},
	'screen_low_temp': {
		'priority': 1,
		'vignette': True,
		'center': (0.5, 0.5),
		'rgb': (100, 200, 200),
		'radius': 1.0,
		'smoothness': 0.7,
	},
	'texture_low_temp': {
		'priority': 1,
		'texture': True,
		'path': 'textures/ui/scuke_survive/screen/frozen_effect',
		'alpha': 1.0,
		'blend': 0.5,
	},
	'energy_shield': {
		'fbx': True,
		'type': 'energy_shield',
		'uid': 'scuke_energy_shield_fbx',
		'model': 'scuke_energy_shield',
		'mat': 'scuke_survive_energy_shield',
		'scale': (5.0, 5.0, 5.0),
		'color': (0.6, 0.88, 0.88, 0.7)
	},
	'battle_area_guard_planet_booster': {
		'fbx': True,
		'type': 'battle_area',
		'uid': 'scuke_battle_area_guard_planet_booster',
		'model': 'scuke_battle_area',
		'mat': 'scuke_survive_battle_area',
		'scale': (32.0, 20.0, 25.0),
		'color': (0.9, 0.88, 0.2, 0.8)
	},
	# 电磁特效
	'emp_particle': {
		'type': 'emp_particle',	# 这里的type对应特效id的存储key，需每一种特效唯一key
		# 必须项、标记位
		'particles': [
			{
				'path': 'scuke_survive:entity_emp_inhibit',
				'bind_entity': True,
			}
		],
	},
	# 取消所有操作
	'cancel_all_ctrl': {
		'type': 'cancel_all_ctrl',	# 这里的type对应逻辑类的映射，可不同的display对应一个type，而配置项可不同（需代码支持）
		'ctrl': True,	# 标记位
		'cancel_move': True,	# 取消移动
		'cancel_drag': True,	# 取消拖动屏幕
		'cancel_jump': True,	# 取消跳跃
		'cancel_blocks': True,	# 取消方块相关（破坏、放置、点击）
		'cancel_ui_response': True,	# 取消自定义UI响应
	},
}
