# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum
from ScukeSurviveScript.modCommon.defines.buffEnum import BuffEnum

Config = {
	BuffEnum.Slowness: {
		'type': BuffEnum.Slowness,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.Speed,
		'value': -0.01,
		'undo': True,
		'immediate': True,
	},
	BuffEnum.LowTemp: {
		'type': BuffEnum.LowTemp,
		'interval': 1,
		'duration': -1,
		'attr': AttributeEnum.Health,
		'undo': False,
		'immediate': True,
		'percentValue': {
			'attr': AttributeEnum.MaxHealth,
			'value': -0.01
		},
		'display': [
			'render_low_temp',
			'screen_low_temp',
			'texture_low_temp',
		]
	},
	BuffEnum.HighTemp: {
		'type': BuffEnum.HighTemp,
		'interval': 1,
		'duration': -1,
		'attr': AttributeEnum.Health,
		'undo': False,
		'immediate': True,
		'percentValue': {
			'attr': AttributeEnum.MaxHealth,
			'value': -0.01
		},
		'display': [
			'render_high_temp',
			'screen_high_temp',
		]
	},
	BuffEnum.HighRadiation: {
		'type': BuffEnum.HighRadiation,
		'interval': 1,
		'duration': -1,
		'attr': AttributeEnum.Health,
		'undo': False,
		'immediate': True,
		'percentValue': {
			'attr': AttributeEnum.MaxHealth,
			'value': -0.01
		}
	},
	
	# 抗寒度
	BuffEnum.ColdResistance: {
		'type': BuffEnum.ColdResistance,    # 类型，和key一致
		'interval': 0,						# tick执行间隔，单位秒
		'duration': -1,						# 持续时间，-1表示永久
		'attr': AttributeEnum.BodyColdResistance,			# 修改的属性类型
		'value': 1,						# 每次修改的属性值= value * (level + 1)
		'undo': True,						# 当buff消失时，回退属性值（如加移速的buff，在消失时移速需要重置回去）
		'immediate': True,					# 加buff时立即触发
		'mutex_buff': [
			BuffEnum.HotResistance,
		],
		# 'percentValue': {					# 以百分比形式修改
		# 	'attr': 'ColdResistance',			# 属性类型
		# 	'value': -1							# 百分比例
		# },
	},
	# 耐热度
	BuffEnum.HotResistance: {
		'type': BuffEnum.HotResistance,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.BodyHeatResistance,
		'value': 1,
		'undo': True,
		'immediate': True,
		'mutex_buff': [
			BuffEnum.ColdResistance,
		],
	},
	# 免疫冷
	BuffEnum.ImmuneCold: {
		'type': BuffEnum.ImmuneCold,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.BodyColdResistance,
		'value': 1,
		'undo': True,
		'immediate': True,
	},
	# 免疫热
	BuffEnum.ImmuneHot: {
		'type': BuffEnum.ImmuneHot,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.BodyHeatResistance,
		'value': 1,
		'undo': True,
		'immediate': True,
	},
	# 清除辐射
	BuffEnum.ScavengingRadiation: {
		'type': BuffEnum.ScavengingRadiation,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.Radiation,
		'value': -50,
		'undo': False,
		'immediate': True,
	},
	# 枪械伤害
	BuffEnum.GunDamage: {
		'type': BuffEnum.GunDamage,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.GunDamage,
		'value': 1,
		'undo': True,
		'immediate': True,
	},
	# 近战伤害
	BuffEnum.MeleeDamage: {
		'type': BuffEnum.MeleeDamage,
		'interval': 0,
		'duration': -1,
		'attr': AttributeEnum.MeleeDamage,
		'value': 1,
		'undo': True,
		'immediate': True,
	},
	# 能量护盾
	BuffEnum.EnergyShield: {
		'type': BuffEnum.EnergyShield,
		'interval': 0.3,
		'duration': -1,
		'attr': '',
		'value': 1,
		'undo': False,
		'immediate': True,
		# buff功能参数
		'radius': 5,
		'energy': 800.0,
		'energy_reduce': 1.0,
		'power': 0.8,
		'display': [
			'energy_shield',
		]
	},
	BuffEnum.EnergyShieldV2: {
		'type': BuffEnum.EnergyShieldV2,
		'interval': 0.3,
		'duration': -1,
		'attr': '',
		'value': 1,
		'undo': False,
		'immediate': True,
		# buff功能参数
		'radius': 5,
		'energy': 1200.0,
		'energy_reduce': 1.0,
		'power': 0.8,
		'display': [
			'energy_shield',
		]
	},
	BuffEnum.EnergyShieldV3: {
		'type': BuffEnum.EnergyShieldV3,
		'interval': 0.3,
		'duration': -1,
		'attr': '',
		'value': 1,
		'undo': False,
		'immediate': True,
		# buff功能参数
		'radius': 5,
		'energy': 1600.0,
		'energy_reduce': 1.0,
		'power': 0.8,
		'display': [
			'energy_shield',
		]
	},
	# EMP
	BuffEnum.EMP: {
		'type': BuffEnum.EMP,
		'interval': 0,
		'duration': -1,
		'attr': '',
		'value': 1,
		'undo': False,
		'immediate': True,
		# buff功能参数
		'display': [
			'emp_particle',
			'cancel_all_ctrl',
		]
	},
}
