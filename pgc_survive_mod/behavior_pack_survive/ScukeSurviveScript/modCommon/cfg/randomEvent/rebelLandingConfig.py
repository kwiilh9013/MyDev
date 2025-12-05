# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum


"""
反叛降临事件 config
"""


ProjectileId = ProjectileEnum.EMMissile
"""电磁弹抛射物id"""
ProjectileSpawnDistance = 48
"""抛射物生成距离"""
ProjectileSpawnHeight = 20
"""抛射物生成高度"""
ProjectilePower = 1.0
"""抛射物发射力度"""
ProjectileGravity = 0.0001
"""抛射物重力, 0=使用行为包配置"""

EventStartTimeLimit = 120	# 该值需大于电磁弹延迟爆炸的值
"""事件开始时间限制, 超过时间还没开始, 则结束事件, 单位秒"""

SpawnMobCD = 0.5
"""刷怪CD时间间隔, 单位秒"""
SpawnMobRadius = 24
"""刷怪范围"""
SpawnMobHeight = 24
"""刷怪高度"""


# region 刷怪池
_t4 = {
	# 导弹数量
	"empCount": 2,
	# 导弹生成cd，秒
	"empCD": 1,
	# 怪物数量
	"mobCount": 4,
	# 怪物池
	"mobPool": [
		{"type": MonsterEnum.RebelRagman, "weight": 10},
	],
}
_t3 = {
	"empCount": 2,
	"empCD": 1,
	"mobCount": 5,
	"mobPool": [
		{"type": MonsterEnum.RebelVagrant, "weight": 60},
		{"type": MonsterEnum.RebelRagman, "weight": 40},
	],
}
_t2 = {
	"empCount": 3,
	"empCD": 1,
	"mobCount": 6,
	"mobPool": [
		{"type": MonsterEnum.RebelVagrant, "weight": 40},
		{"type": MonsterEnum.RebelRagman, "weight": 40},
		{"type": MonsterEnum.RebelSoilder, "weight": 40},
	],
}
_t1 = {
	"empCount": 4,
	"empCD": 1,
	"mobCount": 8,
	"mobPool": [
		{"type": MonsterEnum.RebelVagrant, "weight": 40},
		{"type": MonsterEnum.RebelRagman, "weight": 40},
		{"type": MonsterEnum.RebelSoilder, "weight": 40},
		{"type": MonsterEnum.RebelLeader, "weight": 40},
	],
}

_SpawnMobPool = (
	{
		"day": 5,	# t4
		"mobs": _t4,
	},
	{
		"day": 10,	# t3
		"mobs": _t3,
	},
	{
		"day": 16,	# t2
		"mobs": _t2,
	},
	{
		"day": 19,	# t3
		"mobs": _t3,
	},
	{
		"day": 25,	# t1
		"mobs": _t1,
	},
)
__curDay = 0
__curDayPool = None
def GetSpawnMobPool(day):
	"""获取刷怪池"""
	if day <= 0:
		return None
	global __curDay, __curDayPool
	if day != __curDay:
		__curDay = day
		for cfg in _SpawnMobPool:
			if cfg["day"] <= day:
				__curDayPool = cfg["mobs"]
			else:
				break
	return __curDayPool
# endregion
