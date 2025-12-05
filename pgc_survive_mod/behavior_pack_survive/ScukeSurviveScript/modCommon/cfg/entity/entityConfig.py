# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.cfg.entity.npc.goldenCreeper import Config as NPCGoldenCreeperConfig
from ScukeSurviveScript.modCommon.defines.npcEnum import NPCEnum
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetPartSkillProjectCfg, PartEnum
from ScukeSurviveScript.modCommon.defines.buffEnum import BuffEnum

"""
实体 配置表
"""


# region 实体配置
_EntityDict = {
    ProjectileEnum.GrenadeSmall: {
        # 伤害半径
        "damage_radius": 4,
        # 伤害值
        "damage": 2,
        # 延迟爆炸
        "delay_explode": 2,
        # 爆炸半径
        "explode_radius": 4,
        # 是否着火
        "fire": True,
        # 是否破坏方块
        "breaks": True,
    },
    ProjectileEnum.GrenadeMiddle: {
        "damage_radius": 7,
        "damage": 3,
        "delay_explode": 2,
        "explode_radius": 7,
        "fire": True,
        "breaks": True,
    },
    ProjectileEnum.GrenadeLarge: {
        "damage_radius": 10,
        "damage": 5,
        "delay_explode": 2,
        "explode_radius": 10,
        "fire": True,
        "breaks": True,
    },
    NPCEnum.GoldenCreeper: NPCGoldenCreeperConfig,

    # 怪物配置
    ###麻辣辣妹僵尸
    MonsterEnum.ZombieSpicyChick: {
        # 火焰伤害和火焰持续时间
        "fire_damage":1,
        "fire_time":3,
    },
    ###火焰毒液僵尸
    MonsterEnum.ZombieFlameVenom: {
        # 火焰伤害和火焰持续时间
        "fire_damage":1,
        "fire_time":5,
    },
    ###黑色毒液僵尸
    MonsterEnum.ZombieBlackVenom: {
        # 攻击命中时给予的效果和效果持续时间
        "effect_name":"mining_fatigue",
        "effect_time":5,
    },
    ###雪崩巨人
    MonsterEnum.ZombieGiantKing: {
        # 攻击命中时给予的效果和效果持续时间
        "effect_name":"wither",
        "effect_time":5,
    },
    ###巨大僵尸团
    MonsterEnum.ZombieGiantSarcoma: {
        # 攻击命中时给予的效果和效果持续时间
        "effect_name":"wither",
        "effect_time":5,
    },
    ###巨型僵尸
    MonsterEnum.ZombieBigGiant: {
        # 巨型僵尸生成时闪电数量
        "lightning_num":5,
        # 巨型僵尸生成时闪电半径
        "lightning_radius":5,
        # 玩家着火距离
        "onfire_radius":8,
        # 玩家着火时间
        "onfire_time":5,
    },
    ###高血压老大爷僵尸
    MonsterEnum.ZombieHypertensionGrandpa: {
        #死亡爆炸
        "explosion":{
        "radius":3,      #爆炸威力
        "fire":False,    #爆炸是否带火
        "breaks":True,   #爆炸是否破坏方块
        },
    },
    ###巨型巨人僵尸扔出的婴儿僵尸
    MonsterEnum.ZombieBabyExplose: {
        #扔出婴儿僵尸死亡爆炸
        "explosion":{
        "radius":3,      #爆炸威力
        "fire":False,    #爆炸是否带火
        "breaks":True,   #爆炸是否破坏方块
        },
    },
    ###飞天岩浆僵尸
    MonsterEnum.ZombieFlyingLava: {
        # 伤害减免
        "damage_mitigate": 0.5,
        # 回血
        "health_recover": {
            "cd": 1,    # 回血间隔
            "value": 1, # 回血值
        },
    },
    
	# 怪物抛射物配置（抛射物添加buff的功能，时间短的buff会加不上，需通过代码添加）
    ProjectileEnum.Venom: {
        "buff": {
            "name": "poison",
            "duration": 3,
            "amplifier": 0,
            "showParticles": True,
		},
	},
     
    # 载具技能：导弹
    ProjectileEnum.Missile: GetPartSkillProjectCfg(PartEnum.Missile),

    # 电磁弹
    ProjectileEnum.EMMissile: {
        # 发射音效
        "shoot_sound": "scuke_survive.skill.emmissle.shoot",
        # 命中音效
        "hit_sound": "scuke_survive.skill.emp",
        # 命中特效
        "hit_particle": "scuke_survive:projectile_em_missile_hit",

        # 瘫痪时长，秒
        "duration": 30,
        # 爆炸伤害
        "damage": 5,
        # 爆炸半径
        "radius": 3,
        # 存活时间，结束后爆炸
        "aliveTime": 10,
        # 导弹追踪矫正次数，增加次数可增强追踪效果
        "traceCount": 5,
        # 添加buff
        "buffs": (
            # "amplifier": 0, "showParticle": True
            {"name": BuffEnum.EMP, "duration": 1, },
        ),
    },
    
}
def GetEntityConfig(itemName):
    """获取实体配置信息"""
    return _EntityDict.get(itemName)
# endregion



# 血条显示黑名单
_HealthBarBlackList = (
    NPCEnum.Zhanjing,
    NPCEnum.Dahua,
    NPCEnum.Keke,
    NPCEnum.Ed,
    NPCEnum.Qiqi,
    NPCEnum.Taojiji,
    NPCEnum.Igniter,
    NPCEnum.Trader,
    "scuke_survive:base_car",
    "scuke_survive:base_car_broken",
    "scuke_survive:fbx_entity",
)
def IsHealthBarBlackList(entityId):
    """判断是否是血条黑名单"""
    return entityId in _HealthBarBlackList
# endregion


# region 怪物刷新黑名单
# 仅部分原版怪物，且仅拦截主世界
_SpawnMobBlackList = (
	"minecraft:zombie",
	"minecraft:zombie_villager_v2",
	"minecraft:husk",
	"minecraft:skeleton",
	"minecraft:stray",
	"minecraft:cave_spider",
	"minecraft:endermite",
	"minecraft:silverfish",
	"minecraft:witch",
	"minecraft:vindicator",
	"minecraft:ravager",
	"minecraft:vex",
	"minecraft:evocation_illager",
	"minecraft:pillager",
	"minecraft:wandering_trader",
	"minecraft:phantom",
)
def IsSpawnMobBlackList(engineTypeStr):
	"""判断是否是怪物黑名单，在黑名单中的不刷新"""
	return engineTypeStr in _SpawnMobBlackList

_AddMobBlackList = (
	"minecraft:phantom",
	"minecraft:wandering_trader",
)
def IsAddMobBlackList(engineTypeStr):
    """判断是否是怪物黑名单，在黑名单中的不刷新"""
    return engineTypeStr in _AddMobBlackList
# endregion
