# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_planet_booster import Config as Scuke_planetBooster
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum, MosterAbilityEventEnum
from ScukeSurviveScript.modCommon.defines.buffEnum import BuffEnum
from ScukeSurviveScript.modCommon.defines.battleEventEnum import BattleEventEnum
from ScukeSurviveScript.modCommon.defines.entityTagEnum import EntityTagEnum


Config = {
	'GuardPlanetBoosterLevel1': {
		'name': BattleEventEnum.GuardPlanetBooster,
		'player': {
			'forbidSleep': True,
		},
		'posTransformer': {
			'type': 'building',
			'identifier': Scuke_planetBooster['identifier'],
			'filter': 'closest'
		},
		'pos': (238, 13, 234),
		'range': (32.0, 20.0, 25.0),
		'display': 'battle_area_guard_planet_booster',
		'outRangeDuration': 4,
		'duration': 150,
		'phases': [
			{'type': 'entityMove', 'targets': '@entities', 'pos': (238, 13, 234), 'rot': (0, 270, 0)},
			{'type': 'entityMove', 'pos': (250, 13, 234), 'rot': (0, 90, 0)},
			{'type': 'entityBuff', 'targets': '@entities', 'duration': 150, 'op': 'add', 'buff': BuffEnum.EnergyShield},
			{'type': 'entityEventTrigger', 'targets': '@entities', 'events': ['scuke_survive:npc2player_event']},
			{'type': 'entityTag', 'targets': '@entities', 'add': [EntityTagEnum.TaskEntity]},
			{'type': 'spawnMobsWaves', 'targets': '@entities', 'duration': 150, 'events': [], 'waves': [
				{'offset': 0.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 2,
						'mobs': {
							MonsterEnum.ZombieNormal: 50,
							MonsterEnum.ZombieGangs: 50,
							MonsterEnum.ZombieChick: 50,
						}
					},
				]},
				{'offset': 30.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 4,
						'mobs': {
							MonsterEnum.ZombieNormal: 40,
							MonsterEnum.ZombieGangs: 30,
							MonsterEnum.ZombieChick: 50,
							MonsterEnum.ZombieGuard: 30,
						}
					},
				]},
				{'offset': 60.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 4,
						'mobs': {
							MonsterEnum.ZombieGangsCaptain: 30,
							MonsterEnum.ZombieGangs: 50,
							MonsterEnum.ZombieGuard: 30,
							MonsterEnum.ZombieDog: 20,
						}
					},
				]},
				{'offset': 90.0, 'duration': 30, 'areas': [
					# 区域2
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 5,
						'mobs': {
							MonsterEnum.ZombieGangsCaptain: 30,
							MonsterEnum.ZombieGrandpa: 30,
							MonsterEnum.ZombieFat: 50,
							MonsterEnum.ZombieGuard: 30,
							MonsterEnum.ZombieDog: 20,
						}
					},
				]},
				{'offset': 120.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 4,
						'mobs': {
							MonsterEnum.ZombieGrandpa: 30,
							MonsterEnum.ZombieFat: 50,
							MonsterEnum.ZombieGangsCaptain: 30,
							MonsterEnum.ZombieDog: 20,
						}
					},
					# 区域1 Boss
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 1,
						'mobs': {
							MonsterEnum.ZombieWitchNormal: 100,
						}
					},
				]},
			]},
			{'type': 'entityBuff', 'targets': '@entities', 'op': 'remove', 'buff': BuffEnum.EnergyShield},
			{'type': 'entityEventTrigger', 'targets': '@entities', 'events': ['scuke_survive:player2npc_event']},
			{'type': 'entityTag', 'targets': '@entities', 'remove': [EntityTagEnum.TaskEntity]},
			{'type': 'checkAlive', 'targets': '@entities',
				'events': {
					'success': 'OnGuardPlanetBoosterSuccess',
					'fail': 'OnGuardPlanetBoosterFail'
				}
			},
		]
	},
	'GuardPlanetBoosterLevel2': {
		'name': BattleEventEnum.GuardPlanetBooster,
		'player': {
			'forbidSleep': True,
		},
		'posTransformer': {
			'type': 'building',
			'identifier': Scuke_planetBooster['identifier'],
			'filter': 'closest'
		},
		'pos': (238, 13, 234),
		'range': (32.0, 20.0, 25.0),
		'display': 'battle_area_guard_planet_booster',
		'outRangeDuration': 4,
		'duration': 210,
		'phases': [
			{'type': 'entityMove', 'targets': '@entities', 'pos': (238, 13, 234), 'rot': (0, 270, 0)},
			{'type': 'entityMove', 'pos': (250, 13, 234), 'rot': (0, 90, 0)},
			{'type': 'entityBuff', 'targets': '@entities', 'duration': 210, 'op': 'add', 'buff': BuffEnum.EnergyShieldV2},
			{'type': 'entityEventTrigger', 'targets': '@entities', 'events': ['scuke_survive:npc2player_event']},
			{'type': 'entityTag', 'targets': '@entities', 'add': [EntityTagEnum.TaskEntity]},
			{'type': 'spawnMobsWaves', 'targets': '@entities', 'duration': 210, 'events': [], 'waves': [
				{'offset': 0.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 4,
						'mobs': {
							MonsterEnum.ZombieFat: 10,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSpicyChick: 10,
							MonsterEnum.ZombieGangsCaptain: 20,
							MonsterEnum.ZombieExplosive: 20,
							MonsterEnum.ZombieTonsKing: 30,
						}
					},
				]},
				{'offset': 30.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 5,
						'mobs': {
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieChick: 15,
							MonsterEnum.ZombieGuard: 15,
							MonsterEnum.ZombieDog: 10,
							MonsterEnum.ZombieCaptain: 20,
							MonsterEnum.ZombieOtakuBlack: 30,
						}
					},
				]},
				{'offset': 60.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 5,
						'mobs': {
							MonsterEnum.ZombieOtakuBlack: 15,
							MonsterEnum.ZombieJocker: 15,
							MonsterEnum.ZombieGiant: 20,
							MonsterEnum.ZombieHypertensionGrandpa: 25,
							MonsterEnum.ZombieSpecialGuard: 25,
						}
					},
				]},
				{'offset': 90.0, 'duration': 30, 'areas': [
					# 区域2
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 6,
						'mobs': {
							MonsterEnum.ZombieGangsCaptain: 20,
							MonsterEnum.ZombieJocker: 20,
							MonsterEnum.ZombieGiant: 20,
							MonsterEnum.ZombieHypertensionGrandpa: 20,
							MonsterEnum.ZombieSpecialGuard: 20,
							MonsterEnum.ZombieVenom: 20,
						}
					},
					# 区域2 Boss
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 3,
						'mobs': {
							MonsterEnum.RebelSoilder: 100,
						}
					},
				]},
				{'offset': 120.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 6,
						'mobs': {
							MonsterEnum.ZombieOtakuBlack: 15,
							MonsterEnum.ZombieJocker: 25,
							MonsterEnum.ZombieGiant: 15,
							MonsterEnum.ZombieHypertensionGrandpa: 15,
							MonsterEnum.ZombieSpecialGuard: 30,
							MonsterEnum.ZombieSpicyChick: 20,
							MonsterEnum.ZombieBigDog: 15,
							MonsterEnum.ZombieFlameVenom: 30,
						}
					},
				]},
				{'offset': 150.0, 'duration': 30, 'areas': [
					# 区域2
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 7,
						'mobs': {
							MonsterEnum.ZombieOtakuBlack: 15,
							MonsterEnum.ZombieJocker: 15,
							MonsterEnum.ZombieGiant: 25,
							MonsterEnum.ZombieSuperTNT: 15,
							MonsterEnum.ZombieSpecialGuard: 25,
							MonsterEnum.ZombieSpicyChick: 15,
							MonsterEnum.ZombieBigDog: 35,
							MonsterEnum.ZombieFlameVenom: 20,
						}
					},
				]},
				{'offset': 180.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 6,
						'mobs': {
							MonsterEnum.ZombieOtakuBlack: 15,
							MonsterEnum.ZombieJocker: 25,
							MonsterEnum.ZombieGiant: 15,
							MonsterEnum.ZombieHypertensionGrandpa: 15,
							MonsterEnum.ZombieSpecialGuard: 30,
							MonsterEnum.ZombieSpicyChick: 20,
							MonsterEnum.ZombieBigDog: 15,
							MonsterEnum.ZombieFlameVenom: 30,
						}
					},
					# 区域1 Boss
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 1,
						'mobs': {
							MonsterEnum.RebelLeader: 100,
						}
					},
				]},
			]},
			{'type': 'entityBuff', 'targets': '@entities', 'op': 'remove', 'buff': BuffEnum.EnergyShieldV2},
			{'type': 'entityEventTrigger', 'targets': '@entities', 'events': ['scuke_survive:player2npc_event']},
			{'type': 'entityTag', 'targets': '@entities', 'remove': [EntityTagEnum.TaskEntity]},
			{'type': 'checkAlive', 'targets': '@entities',
				'events': {
					'success': 'OnGuardPlanetBoosterSuccess',
					'fail': 'OnGuardPlanetBoosterFail'
				}
			},
		]
	},
	'GuardPlanetBoosterLevel3': {
		'name': BattleEventEnum.GuardPlanetBooster,
		'player': {
			'forbidSleep': True,
		},
		'posTransformer': {
			'type': 'building',
			'identifier': Scuke_planetBooster['identifier'],
			'filter': 'closest'
		},
		'pos': (238, 13, 234),
		'range': (32.0, 20.0, 25.0),
		'display': 'battle_area_guard_planet_booster',
		'outRangeDuration': 4,
		'duration': 300,
		'phases': [
			{'type': 'entityMove', 'targets': '@entities', 'pos': (238, 13, 234), 'rot': (0, 270, 0)},
			{'type': 'entityMove', 'pos': (250, 13, 234), 'rot': (0, 90, 0)},
			{'type': 'entityBuff', 'targets': '@entities', 'duration': 300, 'op': 'add', 'buff': BuffEnum.EnergyShieldV3},
			{'type': 'entityEventTrigger', 'targets': '@entities', 'events': ['scuke_survive:npc2player_event']},
			{'type': 'entityTag', 'targets': '@entities', 'add': [EntityTagEnum.TaskEntity]},
			{'type': 'spawnMobsWaves', 'targets': '@entities', 'duration': 300, 'events': [], 'waves': [
				{'offset': 0.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 6,
						'mobs': {
							MonsterEnum.ZombieJocker: 40,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 20,
							MonsterEnum.ZombieSuperTNT: 10,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 25,
							MonsterEnum.ZombieFlameVenom: 30,
						}
					},
				]},
				{'offset': 30.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 6,
						'mobs': {
							MonsterEnum.ZombieJocker: 40,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 30,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 25,
							MonsterEnum.ZombieFlameVenom: 30,
							MonsterEnum.ZombieNormal: 20,
						}
					},
				]},
				{'offset': 60.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 7,
						'mobs': {
							MonsterEnum.ZombieJocker: 20,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 30,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 25,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
						}
					},
				]},
				{'offset': 90.0, 'duration': 30, 'areas': [
					# 区域2
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 7,
						'mobs': {
							MonsterEnum.ZombieJocker: 20,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 30,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 25,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
						}
					},
					# 区域2 Boss
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 2,
						'mobs': {
							MonsterEnum.RebelLeader: 100,
						}
					},
				]},
				{'offset': 120.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 7,
						'mobs': {
							MonsterEnum.ZombieJocker: 20,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 30,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 25,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
						}
					},
				]},
				{'offset': 150.0, 'duration': 30, 'areas': [
					# 区域2
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 8,
						'mobs': {
							MonsterEnum.ZombieJocker: 10,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 40,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 45,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
							MonsterEnum.ZombieGiant: 10,
						}
					},
				]},
				{'offset': 180.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 8,
						'mobs': {
							MonsterEnum.ZombieJocker: 10,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 40,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 45,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
							MonsterEnum.ZombieGiant: 10,
						}
					},
				]},
				{'offset': 210.0, 'duration': 30, 'areas': [
					# 区域2
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 8,
						'mobs': {
							MonsterEnum.ZombieJocker: 10,
							MonsterEnum.ZombieGoldenChick: 30,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieVenom: 10,
							MonsterEnum.ZombieSuperTNT: 40,
							MonsterEnum.ZombieCaptain: 10,
							MonsterEnum.ZombieSpecialGuard: 45,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
							MonsterEnum.ZombieGiant: 10,
						}
					},
					# 区域2 Boss
					{
						'pos': (208, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 1,
						'mobs': {
							MonsterEnum.ZombieSnapKiller: 100,
						}
					},
				]},
				{'offset': 240.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 8,
						'mobs': {
							MonsterEnum.ZombieJocker: 10,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieSuperTNT: 10,
							MonsterEnum.ZombieSpecialGuard: 45,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
							MonsterEnum.ZombieGiant: 10,
							MonsterEnum.ZombieGangs: 20,
							MonsterEnum.ZombieBlackVenom: 10,
						}
					},
				]},
				{'offset': 270.0, 'duration': 30, 'areas': [
					# 区域1
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 7,
						'mobs': {
							MonsterEnum.ZombieJocker: 10,
							MonsterEnum.ZombieBigDog: 30,
							MonsterEnum.ZombieSuperTNT: 10,
							MonsterEnum.ZombieSpecialGuard: 45,
							MonsterEnum.ZombieFlameVenom: 40,
							MonsterEnum.ZombieNormal: 20,
							MonsterEnum.ZombieGiant: 10,
							MonsterEnum.ZombieGangs: 20,
							MonsterEnum.ZombieBlackVenom: 10,
						}
					},
					# 区域1 Boss
					{
						'pos': (268, 16, 232), 'range': (2, 3, 6), 'interval': 31.0, 'count': 1,
						'mobs': {
							MonsterEnum.ZombieFlyingLava: 100,
						}
					},
				]},
			]},
			{'type': 'entityBuff', 'targets': '@entities', 'op': 'remove', 'buff': BuffEnum.EnergyShieldV3},
			{'type': 'entityEventTrigger', 'targets': '@entities', 'events': ['scuke_survive:player2npc_event']},
			{'type': 'entityTag', 'targets': '@entities', 'remove': [EntityTagEnum.TaskEntity]},
			{'type': 'checkAlive', 'targets': '@entities',
				'events': {
					'success': 'OnGuardPlanetBoosterSuccess',
					'fail': 'OnGuardPlanetBoosterFail'
				}
			},
		]
	}
}
