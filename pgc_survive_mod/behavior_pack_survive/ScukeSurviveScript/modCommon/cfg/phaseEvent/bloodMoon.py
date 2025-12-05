# -*- encoding: utf-8 -*-
# 血月固定触发间隔天数
BloodMoonIntervalDays = 10
''' 血月配置说明
	{
		'days': 1,					# 该血月生效的起始天数
		'desc': '',					# 血月出现时的描述显示
		'startTime': 13500,			# 血月开始时间 [0-24000]
		'endTime': 23000,			# 血月结束时间 [0-24000]
		'spawnerSpeedUp': 10.0		# 血月对 怪物生成器 perMinuteGen 的加成百分比
	}
'''
BloodMoon = [
	{
		'days': 1,
		'name': '赤潮',
		'desc': '',
		'startTime': 13500,
		'endTime': 23000,
		# 倍率数值，仅保留需要修改的值
		'spawner': {
			'perMinuteGen': 1.5,
			'mobLimit': 1.5,
			# 'healthCoef': 1.0,
			# 'armorCoef': 1.0,
			# 'damageCoef': 1.0,
			'speedCoef': 1.1,
		},
		'forbidSleep': True,
	},
	{
		'days': 14,
		'name': '赤潮',
		'desc': '',
		'startTime': 13500,
		'endTime': 23000,
		# 倍率数值，仅保留需要修改的值
		'spawner': {
			'perMinuteGen': 1.5,
			'mobLimit': 1.8,
			# 'healthCoef': 1.5,
			# 'armorCoef': 1.5,
			# 'damageCoef': 1.5,
			'speedCoef': 1.2,
		},
		'forbidSleep': True,
	},
	{
		'days': 25,
		'name': '赤潮',
		'desc': '',
		'startTime': 13500,
		'endTime': 23000,
		# 倍率数值，仅保留需要修改的值
		'spawner': {
			'perMinuteGen': 1.5,
			'mobLimit': 2.0,
			# 'healthCoef': 2.0,
			# 'armorCoef': 2.0,
			# 'damageCoef': 2.0,
			'speedCoef': 1.25,
		},
		'forbidSleep': True,
	},
]