# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.buffEnum import BuffEnum

Config = {
	'bodyTemp': 1,
	'bodyTempMin': 0,
	'bodyTempMax': 2,
	'bodyColdResistance': 0,
	'bodyHeatResistance': 0,
	'bodyRadiationResistance': 0,
	'radiationAbsorption': 100,
	'heatResistanceToTemp': -2,
	'coldResistanceToTemp': 2,
	'radiationInterval': 3.0,
	'livingChecking': [
		{
			'type': 'Temperature',
			'value': -1,
			'op': '<=',
			'buffs': [
				BuffEnum.LowTemp,
				BuffEnum.Slowness,
			]
		},
		{
			'type': 'Temperature',
			'value': 3,
			'op': '>=',
			'buffs': [
				BuffEnum.HighTemp,
				BuffEnum.Slowness,
			]
		},
		{
		 	'type': 'Radiation',
		 	'value': 'RadiationAbsorption',
		 	'op': '>',
		 	'buffs': [
		 		BuffEnum.HighRadiation,
		 		BuffEnum.Slowness,
		 	]
		}
	]
}
