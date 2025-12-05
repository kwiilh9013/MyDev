# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.npcEnum import NPCEnum

# 血月固定触发间隔天数
TraderIntervalDays = 3

NpcTrader = [
	{
		'days': 1,
		'name': '流浪商人',
		'desc': '一个捡垃圾的人...',
		'startTime': 0,
		'endTime': 24000,
		'identifier': NPCEnum.Trader,
		'spawnRange': (16, 32),
		'spawnYRange': 30
	}
]