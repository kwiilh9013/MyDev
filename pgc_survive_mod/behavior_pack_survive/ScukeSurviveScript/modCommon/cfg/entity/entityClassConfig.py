# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.npcEnum import NPCEnum
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum
from ScukeSurviveScript.modServer.entity.projectile.entityGrenade import EntityGrenade
from ScukeSurviveScript.modServer.entity.npc.npcGoldenCreeper import NPCGoldenCreeper
from ScukeSurviveScript.modServer.entity.npc.npcIgniter import NPCIgniter
from ScukeSurviveScript.modServer.entity.monster.monsterFlyingLava import MonsterFlyingLava
from ScukeSurviveScript.modServer.entity.monster.monsterSpicyChick import MonsterSpicyChickAttack
from ScukeSurviveScript.modServer.entity.monster.monsterHypertensionGrandpa import MonsterHypertensionGrandpa
from ScukeSurviveScript.modServer.entity.monster.monsterFlameVenom import MonsterFlameVenom
from ScukeSurviveScript.modServer.entity.monster.monsterBabyExplose import MonsterBabyExplose
from ScukeSurviveScript.modServer.entity.monster.monsterZombieBigGiant import MonsterZombieBigGiant
from ScukeSurviveScript.modServer.entity.monster.monsterZombieBlackVenom import MonsterZombieBlackVenom
from ScukeSurviveScript.modServer.entity.monster.monsterZombieGiantKing import MonsterZombieGiantKing
from ScukeSurviveScript.modServer.entity.monster.monsterZombieGiantSarcoma import MonsterZombieGiantSarcoma
from ScukeSurviveScript.modServer.entity.projectile.entityHitExplodeProject import EntityHitExplodeProject
from ScukeSurviveScript.modServer.entity.projectile.entityEMMissile import EntityEMMissile
# 第二批怪物
from ScukeSurviveScript.modServer.entitynew.boss.snapKiller import EntitySnapKiller
from ScukeSurviveScript.modServer.entitynew.boss.witch import EntityWitch
from ScukeSurviveScript.modServer.entitynew.rebel.soldier import EntityRebelSoldier
from ScukeSurviveScript.modServer.entitynew.rebel.leader import EntityRebelLeader


# region 实体类
"""
实体 对象映射表
为避免循环引用，单独一个表
"""

_entityClassDict = {
    # 手雷
    ProjectileEnum.GrenadeSmall: EntityGrenade,
    ProjectileEnum.GrenadeMiddle: EntityGrenade,
    ProjectileEnum.GrenadeLarge: EntityGrenade,

    # NPC
    NPCEnum.GoldenCreeper: NPCGoldenCreeper,
    NPCEnum.Igniter: NPCIgniter,

    # 怪物
    MonsterEnum.ZombieFlyingLava: MonsterFlyingLava,
    MonsterEnum.ZombieSpicyChick: MonsterSpicyChickAttack,
    MonsterEnum.ZombieHypertensionGrandpa: MonsterHypertensionGrandpa,
    MonsterEnum.ZombieFlameVenom: MonsterFlameVenom,
    MonsterEnum.ZombieBabyExplose: MonsterBabyExplose,
    MonsterEnum.ZombieBigGiant: MonsterZombieBigGiant,
    MonsterEnum.ZombieBlackVenom: MonsterZombieBlackVenom,
    MonsterEnum.ZombieGiantKing: MonsterZombieGiantKing,
    MonsterEnum.ZombieGiantSarcoma: MonsterZombieGiantSarcoma,

    # 导弹
    ProjectileEnum.Missile: EntityHitExplodeProject,
    # 电磁弹
    ProjectileEnum.EMMissile: EntityEMMissile,

    # 第二批怪物
    MonsterEnum.ZombieSnapKiller: EntitySnapKiller,
    MonsterEnum.ZombieWitch: EntityWitch,
    MonsterEnum.ZombieWitchNormal: EntityWitch,


    # 反叛军
    MonsterEnum.RebelRagman: EntityRebelSoldier,
    MonsterEnum.RebelVagrant: EntityRebelSoldier,
    MonsterEnum.RebelSoilder: EntityRebelSoldier,
    MonsterEnum.RebelLeader: EntityRebelLeader,
}
def GetEntityClass(engineTypeStr):
    """获取实体类"""
    return _entityClassDict.get(engineTypeStr)
# endregion

