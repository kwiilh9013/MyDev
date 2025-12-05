# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.randomEventEnum import RandomEventEnum
from ScukeSurviveScript.modServer.randomEvents.rebelLandingEvent import RebelLandingEvent
from ScukeSurviveScript.modServer.randomEvents.spawnEntityEvent import SpawnEntityEvent


"""
随机事件 总config
"""

# region 全局配置
# 这里存放所有的事件class
_RandomEventClass = {
	RandomEventEnum.RebelLanding: RebelLandingEvent,
	# RandomEventEnum.SpawnNPC: SpawnEntityEvent,
	RandomEventEnum.SpawnWitch: SpawnEntityEvent,
}
def GetRandomEventClass(eventEnum):
	"""获取随机事件的类"""
	if eventEnum:
		return _RandomEventClass.get(eventEnum)
	return None

TriggerEventCD = 60 * 30
"""事件触发判断的轮询频率，单位tick（1秒30tick）"""

TriggerEventMinDistance = 100
"""事件触发判断的最小距离，单位格"""

EventDimensions = (0, )
"""事件触发的维度限制"""

# endregion


# region 阶段配置
# key=天数, val={}事件配置; 如果某些天数没配置，则沿用上一个有配置的天数数据
_PhaseEventCfg = (
	{
		# 天数
		"day": 5,
		# 事件触发概率的成长参数: 每移动1格成长的概率、每1次使用方块成长的概率
		"eventProbRatio": {
			# 载具行驶
			"car": 0.001,
			# 人移动
			"human": 0.002,
			# 打开工作方块
			"open_workbench": 0.001,
			# 使用工作方块
			"use_workbench": 0.002,
		},
		# 距离类事件列表
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 20,
			},
		],
		# 操作类事件列表
	},
	{
		"day": 7,
		"eventProbRatio": {
			"car": 0.001,
			"human": 0.002,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 70,
			},
		],
	},
	{
		"day": 8,
		"eventProbRatio": {
			"car": 0.001,
			"human": 0.002,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 40,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 60,
			},
		],
	},
	{
		"day": 10,
		"eventProbRatio": {
			"car": 0.001,
			"human": 0.002,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 40,
			},
		],
	},
	{
		"day": 11,
		"eventProbRatio": {
			"car": 0.001,
			"human": 0.002,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.SpawnWitchNormal,
				"weight": 40,
			},
		],
	},
	{
		"day": 12,
		"eventProbRatio": {
			"car": 0.002,
			"human": 0.004,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.SpawnWitchNormal,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 40,
			},
		],
	},
	{
		"day": 14,
	},
	{
		"day": 15,
		"eventProbRatio": {
			"car": 0.002,
			"human": 0.004,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.SpawnWitchNormal,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 40,
			},
		],
	},
	{
		"day": 16,
		"eventProbRatio": {
			"car": 0.002,
			"human": 0.004,
			"open_workbench": 0.003,
			"use_workbench": 0.004,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 100,
			},
		],
	},
	{
		"day": 17,
	},
	{
		"day": 19,
		"eventProbRatio": {
			"car": 0.002,
			"human": 0.005,
			"open_workbench": 0.005,
			"use_workbench": 0.006,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.SpawnWitchNormal,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 40,
			},
		],
	},
	{
		"day": 20,
	},
	{
		"day": 21,
		"eventProbRatio": {
			"car": 0.0025,
			"human": 0.005,
			"open_workbench": 0.005,
			"use_workbench": 0.006,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.SpawnWitchNormal,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 40,
			},
		],
	},
	{
		"day": 22,
	},
	{
		"day": 23,
		"eventProbRatio": {
			"car": 0.0025,
			"human": 0.005,
			"open_workbench": 0.009,
			"use_workbench": 0.01,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.SpawnWitchNormal,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 40,
			},
		],
	},
	{
		"day": 24,
	},
	{
		"day": 25,
		"eventProbRatio": {
			"car": 0.003,
			"human": 0.006,
			"open_workbench": 0.009,
			"use_workbench": 0.01,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 50,
			},
		],
	},
	{
		"day": 26,
		"eventProbRatio": {
			"car": 0.003,
			"human": 0.006,
			"open_workbench": 0.009,
			"use_workbench": 0.01,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.SpawnWitch,
				"weight": 50,
			},
		],
	},
	{
		"day": 27,
		"eventProbRatio": {
			"car": 0.003,
			"human": 0.006,
			"open_workbench": 0.009,
			"use_workbench": 0.01,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 70,
			},
		],
	},
	{
		"day": 28,
		"eventProbRatio": {
			"car": 0.003,
			"human": 0.006,
			"open_workbench": 0.009,
			"use_workbench": 0.01,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.SpawnWitch,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 70,
			},
		],
	},
	{
		"day": 29,
	},
	{
		"day": 30,
		"eventProbRatio": {
			"car": 0.003,
			"human": 0.006,
			"open_workbench": 0.013,
			"use_workbench": 0.015,
		},
		"distEvents": [
			{
				"event": RandomEventEnum.RebelLanding,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.SpawnWitch,
				"weight": 30,
			},
			{
				"event": RandomEventEnum.Empty,
				"weight": 40,
			},
		],
	},
)
__curDay = 0
__curDayEventCfg = None
def GetRandomPhaseEventCfg(day):
	"""获取某一天的阶段事件配置"""
	if day <= 0:
		return None
	global __curDay, __curDayEventCfg
	if day != __curDay:
		__curDay = day
		for cfg in _PhaseEventCfg:
			if cfg["day"] <= day:
				__curDayEventCfg = cfg
			else:
				break
	return __curDayEventCfg

# endregion


# region 工作方块列表
# 自定义工作方块、原版工作方块
# endregion
