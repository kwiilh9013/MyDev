# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MosterAbilityEventEnum, MonsterEnum
from ScukeSurviveScript.modCommon.defines.phaseEventEnum import PhaseEventEnum, PhaseWeatherEventEnum
from ScukeSurviveScript.modCommon.defines.phaseTagEnum import PhaseTagEnum

# 一天分钟数
OneDayMinutes = 20
# 结束天数
EndDays = 45
EndTimeSeconds = EndDays * OneDayMinutes * 60

BossLimit = 3
"""所有boss的刷新上限，按加载区域的数量来算"""

def IsSelfMonster(engineTypeStr):
	"""判断是否是本模组的怪物，用于统计刷怪上限"""
	if engineTypeStr.startswith("scuke_survive:zombie"):
		return True
	return False

''' 惊变阶段配置说明
	{
		'days': 5,						# 阶段起始天数
		'desc': '', 					# 阶段文本描述显示
		'bloodMoon': 10,				# 血月概率
		'spawner': {					# ------怪物生成器配置------
			'startTime': 13000,			# 开始生成时间 [0-24000]
			'endTime': 24000,			# 结束生成时间 [0-24000]
			'perMinuteGen': 50,			# 每分钟生成数量
			'area': {					# ------生成区域配置------
				'type': 'box',			# 区域类型 [box(x,z),...]
				'x': 50,
				'z': 50,
			},
		},
		'mobs': [									# ------生成怪物配置------
			{
				'type': 'scuke_survive:zombie',		# 怪物类型 Identifier
				'probability': 50.0,				# 怪物占比 [0-100] (总和不超100)
				'attrs': {							# ------怪物属性配置------ https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/AttrType.html
					'SPEED': 0.5,					# '属性名': 数值
				},
				'effects': [						# ------怪物效果配置------ 
					{
						'type': 'FIRE_RESISTANCE',	# 效果名 https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EffectType.html
						'duration': 5,				# 效果持续时间 (秒)
						'amplifier': 0				# 效果等级 [0-255]
					}
				],
			},
		]
	},
'''

Phases = [
	{
		'days': 1,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
		},
		'weathers': {},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 6,
			'mobLimit': 10,
			'healthCoef': 1.0,
			'armorCoef': 1.0,
			'damageCoef': 1.0,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 100,
			}
		]
	},
	{
		'days': 2,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 100,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 6,
			'mobLimit': 10,
			'healthCoef': 1.0,
			'armorCoef': 1.0,
			'damageCoef': 1.0,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 60,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 40,
			}
		]
	},
	{
		'days': 3,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 20,
			PhaseWeatherEventEnum.Thunder: 30,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 6,
			'mobLimit': 10,
			'healthCoef': 1.1,
			'armorCoef': 1.0,
			'damageCoef': 1.0,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 30,
			}
		]
	},
	{
		'days': 4,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 50,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 25,
			PhaseWeatherEventEnum.Thunder: 30,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 8,
			'mobLimit': 11,
			'healthCoef': 1.1,
			'armorCoef': 1.0,
			'damageCoef': 1.0,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 40,
			}
		]
	},
	{
		'days': 5,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 28,
			PhaseWeatherEventEnum.Thunder: 40,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 8,
			'mobLimit': 11,
			'healthCoef': 1.15,
			'armorCoef': 1.0,
			'damageCoef': 1.0,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 20,
			}
		]
	},
	{
		'days': 6,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 30,
			PhaseWeatherEventEnum.Thunder: 40,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 10,
			'mobLimit': 12,
			'healthCoef': 1.2,
			'armorCoef': 1.0,
			'damageCoef': 1.1,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 40,
			}
		]
	},
	{
		'days': 7,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 20,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 35,
			PhaseWeatherEventEnum.Thunder: 30,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 10,
			'mobLimit': 12,
			'healthCoef': 1.2,
			'armorCoef': 1.0,
			'damageCoef': 1.1,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 30,
			}
		]
	},
	{
		'days': 8,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -2,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
			PhaseEventEnum.MobSpawn: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 40,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 12,
			'mobLimit': 13,
			'healthCoef': 1.3,
			'armorCoef': 1.0,
			'damageCoef': 1.1,
			'speedCoef': 1.0,
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 25,
			}
		]
	},
	{
		'days': 9,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -2,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
			PhaseEventEnum.MobSpawn: 40,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 60,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 12,
			'mobLimit': 13,
			'healthCoef': 1.3,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.0,
			'abilities': [MosterAbilityEventEnum.Swimming],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 30,
			}
		]
	},
	{
		'days': 10,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -2,
		'task': '100010',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
			PhaseEventEnum.MeteoriteImpact: 40,
			PhaseEventEnum.MobSpawn: 50,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 50,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 14,
			'mobLimit': 14,
			'healthCoef': 1.4,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieExplosive,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieFat,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 10,
			}
		]
	},
	{
		'days': 11,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -2,
		'task': '100010',
		'keyPoint': True,
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MobSpawn: 60,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 60,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 14,
			'mobLimit': 14,
			'healthCoef': 1.4,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtaku,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangsCaptain,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieExplosive,
				'probability': 20,
			}
		]
	},
	{
		'days': 12,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 70,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 12,
			'mobLimit': 12,
			'healthCoef': 1.45,
			'armorCoef': 1.1,
			'damageCoef': 1.1,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieExplosive,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieFat,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 15,
			}
		]
	},
	{
		'days': 13,
		'desc': '火星',
		'tag': PhaseTagEnum.Mars,
		'temperature': -1,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 12,
			'mobLimit': 12,
			'healthCoef': 1.45,
			'armorCoef': 1.1,
			'damageCoef': 1.1,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 20,
			}
		]
	},
	{
		'days': 14,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -2,
		'task': '100020',
		'events': {
			PhaseEventEnum.MeteoriteImpact: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 14,
			'mobLimit': 13,
			'healthCoef': 1.45,
			'armorCoef': 1.1,
			'damageCoef': 1.1,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtaku,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangsCaptain,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieExplosive,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieTonsKing,
				'probability': 30,
			}
		]
	},
	{
		'days': 15,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -2,
		'task': '100020',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
			PhaseEventEnum.MeteoriteImpact: 80,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 60,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 14,
			'mobLimit': 13,
			'healthCoef': 1.5,
			'armorCoef': 1.1,
			'damageCoef': 1.1,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 30,
			}
		]
	},
	{
		'days': 16,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -2,
		'task': '100020',
		'events': {
			PhaseEventEnum.BloodMoon: 20,
			PhaseEventEnum.MeteoriteImpact: 20,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 14,
			'mobLimit': 13,
			'healthCoef': 1.5,
			'armorCoef': 1.1,
			'damageCoef': 1.1,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
		]
	},
	{
		'days': 17,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '100020',
		'events': {
			PhaseEventEnum.BloodMoon: 60,
			PhaseEventEnum.MeteoriteImpact: 50,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 50,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 16,
			'mobLimit': 14,
			'healthCoef': 1.6,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 20,
			},
		]
	},
	{
		'days': 18,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '100020',
		'events': {
			PhaseEventEnum.BloodMoon: 10,
			PhaseEventEnum.MeteoriteImpact: 50,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 50,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 16,
			'mobLimit': 14,
			'healthCoef': 1.6,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 20,
			},
		]
	},
	{
		'days': 19,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '100020',
		'events': {
			PhaseEventEnum.MeteoriteImpact: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 80,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 16,
			'mobLimit': 14,
			'healthCoef': 1.6,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock, MosterAbilityEventEnum.FireResistance],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 20,
			},
		]
	},
	{
		'days': 20,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '100020',
		'events': {
			PhaseEventEnum.BloodMoon: 60,
			PhaseEventEnum.MeteoriteImpact: 20,
			PhaseEventEnum.MobSpawn: 40,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.7,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock, MosterAbilityEventEnum.FireResistance],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 30,
			},
		]
	},
	{
		'days': 21,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '100020',
		'events': {
			PhaseEventEnum.BloodMoon: 70,
			PhaseEventEnum.MeteoriteImpact: 40,
			PhaseEventEnum.MobSpawn: 50,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.7,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock, MosterAbilityEventEnum.FireResistance],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 35,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 20,
			},
		]
	},
	{
		'days': 22,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '100020',
		'keyPoint': True,
		'events': {
			PhaseEventEnum.BloodMoon: 80,
			PhaseEventEnum.MeteoriteImpact: 50,
			PhaseEventEnum.MobSpawn: 60,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 40,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.7,
			'armorCoef': 1.1,
			'damageCoef': 1.2,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock, MosterAbilityEventEnum.FireResistance],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 20,
			},
		]
	},
	{
		'days': 23,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 30,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 16,
			'mobLimit': 14,
			'healthCoef': 1.7,
			'armorCoef': 1.1,
			'damageCoef': 1.25,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock, MosterAbilityEventEnum.FireResistance],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 20,
			},
		]
	},
	{
		'days': 24,
		'desc': '小行星带',
		'tag': PhaseTagEnum.AsteroidBelt,
		'temperature': -3,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 80,
		},
		'weathers': {
			PhaseWeatherEventEnum.SnowStorm: 30,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 16,
			'mobLimit': 14,
			'healthCoef': 1.75,
			'armorCoef': 1.1,
			'damageCoef': 1.25,
			'speedCoef': 1.1,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock, MosterAbilityEventEnum.FireResistance],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 15,
			},
			{
				'type': MonsterEnum.ZombieGrandpa,
				'probability': 30,
			},
		]
	},
	{
		'days': 25,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -4,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 30,
			PhaseEventEnum.MeteoriteImpact: 20,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.75,
			'armorCoef': 1.1,
			'damageCoef': 1.3,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 30,
			},
		]
	},
	{
		'days': 26,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -4,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteImpact: 20,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.8,
			'armorCoef': 1.1,
			'damageCoef': 1.3,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 30,
			},
		]
	},
	{
		'days': 27,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -4,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 50,
			PhaseEventEnum.MeteoriteImpact: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.8,
			'armorCoef': 1.1,
			'damageCoef': 1.3,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 50,
			},
		]
	},
	{
		'days': 28,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -5,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 60,
			PhaseEventEnum.MeteoriteImpact: 40,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 15,
			'healthCoef': 1.8,
			'armorCoef': 1.1,
			'damageCoef': 1.3,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
		]
	},
	{
		'days': 29,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -5,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 18,
			'mobLimit': 16,
			'healthCoef': 1.85,
			'armorCoef': 1.1,
			'damageCoef': 1.3,
			'speedCoef': 1.2,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
		]
	},
	{
		'days': 30,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -6,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 80,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 20,
			'mobLimit': 16,
			'healthCoef': 1.85,
			'armorCoef': 1.1,
			'damageCoef': 1.4,
			'speedCoef': 1.3,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
		]
	},
	{
		'days': 31,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -6,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 20,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 20,
			'mobLimit': 16,
			'healthCoef': 1.85,
			'armorCoef': 1.1,
			'damageCoef': 1.4,
			'speedCoef': 1.3,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
		]
	},
	{
		'days': 32,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -6,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 60,
			PhaseEventEnum.MeteoriteRain: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 20,
			'mobLimit': 16,
			'healthCoef': 1.9,
			'armorCoef': 1.1,
			'damageCoef': 1.4,
			'speedCoef': 1.3,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
		]
	},
	{
		'days': 33,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -6,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 80,
			PhaseEventEnum.MeteoriteRain: 40,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 22,
			'mobLimit': 17,
			'healthCoef': 1.9,
			'armorCoef': 1.1,
			'damageCoef': 1.4,
			'speedCoef': 1.3,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
		]
	},
	{
		'days': 34,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -7,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 90,
			PhaseEventEnum.MeteoriteRain: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 22,
			'mobLimit': 17,
			'healthCoef': 1.9,
			'armorCoef': 1.1,
			'damageCoef': 1.4,
			'speedCoef': 1.3,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
		]
	},
	{
		'days': 35,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -7,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 80,
			PhaseEventEnum.MeteoriteRain: 40,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 24,
			'mobLimit': 18,
			'healthCoef': 1.9,
			'armorCoef': 1.1,
			'damageCoef': 1.4,
			'speedCoef': 1.3,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
		]
	},
	{
		'days': 36,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 70,
			PhaseEventEnum.MeteoriteRain: 50,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 26,
			'mobLimit': 18,
			'healthCoef': 2.0,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
		]
	},
	{
		'days': 37,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 80,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 80,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 26,
			'mobLimit': 18,
			'healthCoef': 2.0,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
		]
	},
	{
		'days': 38,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 80,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 80,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 26,
			'mobLimit': 18,
			'healthCoef': 2.0,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 25,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
		]
	},
	{
		'days': 39,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 80,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 80,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 28,
			'mobLimit': 20,
			'healthCoef': 2.1,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 10,
			},
		]
	},
	{
		'days': 40,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 80,
			PhaseEventEnum.MeteoriteRain: 40,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 70,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 28,
			'mobLimit': 20,
			'healthCoef': 2.2,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 10,
			},
		]
	},
	{
		'days': 41,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -9,
		'task': '100030',
		'events': {
			PhaseEventEnum.BloodMoon: 40,
			PhaseEventEnum.MeteoriteRain: 80,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 80,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 28,
			'mobLimit': 20,
			'healthCoef': 2.3,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGiantKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 20,
			},
		]
	},
	{
		'days': 42,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -9,
		'task': '100030',
		'keyPoint': True,
		'events': {
			PhaseEventEnum.BloodMoon: 60,
			PhaseEventEnum.MeteoriteRain: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 28,
			'mobLimit': 21,
			'healthCoef': 2.4,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGiantKing,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 30,
			},
		]
	},
	{
		'days': 43,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 50,
			PhaseEventEnum.MeteoriteRain: 30,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 26,
			'mobLimit': 19,
			'healthCoef': 2.3,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGiantKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 10,
			},
		]
	},
	{
		'days': 44,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 70,
			PhaseEventEnum.MeteoriteRain: 30,
			PhaseEventEnum.MobSpawn: 100,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 26,
			'mobLimit': 19,
			'healthCoef': 2.3,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGiantKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 10,
			},
		]
	},
	{
		'days': 45,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '-1',
		'events': {
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 26,
			'mobLimit': 19,
			'healthCoef': 2.3,
			'armorCoef': 1.1,
			'damageCoef': 1.5,
			'speedCoef': 1.4,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 30,
			},
			{
				'type': MonsterEnum.ZombieGiantKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 45,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 40,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 20,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 10,
			},
		]
	},
	{
		'days': 46,
		'desc': '木星',
		'tag': PhaseTagEnum.Jupiter,
		'temperature': -8,
		'task': '-1',
		'events': {
			PhaseEventEnum.BloodMoon: 50,
			PhaseEventEnum.MeteoriteRain: 50,
		},
		'weathers': {
			PhaseWeatherEventEnum.ModerateSnow: 50,
			PhaseWeatherEventEnum.SnowStorm: 60,
			PhaseWeatherEventEnum.Thunder: 20,
		},
		'spawner': {
			'startTime': 0,
			'endTime': 24000,
			'perMinuteGen': 30,
			'mobLimit': 22,
			'healthCoef': 2.4,
			'armorCoef': 1.1,
			'damageCoef': 1.6,
			'speedCoef': 1.5,
			'abilities': [MosterAbilityEventEnum.Swimming, MosterAbilityEventEnum.BreakBlock,  MosterAbilityEventEnum.FireResistance, MosterAbilityEventEnum.PutBlock],
		},
		'mobs': [
			{
				'type': MonsterEnum.ZombieBaby,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieNormal,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieDog,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGuard,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieChick,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangs,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieExplosive,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFat,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieOtaku,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGrandpa,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieJocker,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGangsCaptain,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpicyChick,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieHypertensionGrandpa,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlameVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBabyExplose,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSuperTNT,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieTonsKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSpecialGuard,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBig,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBigDog,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGoldenChick,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieBlackVenom,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGiantKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGiantSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieOtakuBlack,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieJockerKing,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieGiant,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieSarcoma,
				'probability': 10,
			},
			{
				'type': MonsterEnum.ZombieFlyingLava,
				'probability': 10,
			},
		]
	},
	
]
