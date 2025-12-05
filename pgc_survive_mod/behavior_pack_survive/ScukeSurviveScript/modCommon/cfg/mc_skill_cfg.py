# -*- coding: utf-8 -*-

# 输入：技能表.xlsx - 角色技能
# 输出：mc_skill_cfg.py

data = {
	10001: {
		'cd': 30, 
		'name': '向前冲刺', 
		'skill_id': 10001, 
		'timeline': {
			'task_list': [{'params': {'speed': 1, 'dir': 'face'}, 'end_frame': 15, 'class': 'Dash', 'start_frame': 0}], 
			'total_frame': 15, 
		}, 
	}, 
	10002: {
		'cd': 30, 
		'name': '生成方块', 
		'skill_id': 10002, 
		'timeline': {
			'task_list': [{'params': {}, 'end_frame': 11, 'class': 'CreateBlock', 'start_frame': 10}, {'params': {'speed': 0.5, 'dir': 'up'}, 'end_frame': 1, 'class': 'Dash', 'start_frame': 0}], 
			'total_frame': 11, 
		}, 
	}, 
	10003: {
		'cd': 30, 
		'name': '近战', 
		'skill_id': 10003, 
		'timeline': {
			'task_list': [{'params': {'length': 2}, 'end_frame': 2, 'class': 'HitFrame', 'start_frame': 1}], 
			'total_frame': 5, 
		}, 
	}, 
}

_reload_all = True

