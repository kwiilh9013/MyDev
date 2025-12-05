# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.randomEventEnum import RandomEventEnum


"""
生成实体类事件 config
实体触发后的配置, 在entityConfig里, 事件只负责生成触发事件的实体
"""

_SpawnEntityDict = {
	RandomEventEnum.SpawnNPC: MonsterEnum.ZombieSarcoma,
	RandomEventEnum.SpawnWitch: MonsterEnum.ZombieWitch,
	RandomEventEnum.SpawnWitchNormal: MonsterEnum.ZombieWitchNormal,
}
def GetSpawnEngineTypeStr(eventType):
	"""获取实体类事件的生成实体id"""
	return _SpawnEntityDict.get(eventType)


SpawnDistance = 36
"""实体生成距离，单位格"""


