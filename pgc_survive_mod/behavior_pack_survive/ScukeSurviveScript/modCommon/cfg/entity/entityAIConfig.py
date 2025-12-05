# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.entity.enum.actionEnum import ActionEnum
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameActionEnum, GameCompEnum
from ScukeSurviveScript.modCommon.defines.damageTagEnum import DamageTagEnum
from ScukeSurviveScript.modServer.entitynew.comp.weaponComps import WeaponComp
from ScukeSurviveScript.modServer.entitynew.comp.avoidMobComp import AvoidMobComp
from ScukeSurviveScript.ScukeCore.server.entity.component.meleeAttackComp import MeleeAttackComp
from ScukeSurviveScript.ScukeCore.server.entity.component.teleportComp import TeleportComp
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modServer.entitynew.comp.adaptiveImmuneComp import AdaptiveImmuneDamageComp
from ScukeSurviveScript.modServer.entitynew.comp.witchEntityComp import WitchEtityComp
from ScukeSurviveScript.modServer.entitynew.comp.snapKillerJumpAttackComp import SnapKillerJumpAttackComp
from ScukeSurviveScript.modServer.entitynew.comp.summonEntityComp import SummonEntityComp
ActorDamageCause = serverApi.GetMinecraftEnum().ActorDamageCause()



"""
实体AI 配置表
"""


# region 组件配置
_WeaponComponents = {
    GameCompEnum.Shoot1: {
        "type": WeaponComp,
        "timeline": {
            0: {"type": GameActionEnum.GunShoot, "state": True,},
            30: {"type": GameActionEnum.GunShoot, "state": False,},
        },
    },
    GameCompEnum.Reload: {
        "type": WeaponComp,
        "timeline": {
            0: {"type": GameActionEnum.GunReload,},
            20: {},
        },
    },
    GameCompEnum.MeleeAttack1: {
        "type": WeaponComp,
        "timeline": {
            0: {"type": GameActionEnum.WeaponMelee, "state": True,},
            10: {"type": GameActionEnum.WeaponMelee, "state": False,},
            20: {},
        },
    },
    # 显示降落伞
    GameCompEnum.ShowParachute: {
        "actions": [
            {"type": GameActionEnum.SetMolang, "molang": {"query.mod.attack2": 1},},
        ],
    },
    # 隐藏降落伞
    GameCompEnum.HideParachute: {
        "actions": [
            {"type": GameActionEnum.SetMolang, "molang": {"query.mod.attack2": 0},},
        ],
    },
}
_SoilderComonents = dict(_WeaponComponents.items() + {
    # 低生命回血
    GameCompEnum.HealthRecover: {
        "actions": [
            {"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_drink_potion_event"},
        ],
    },
    # 被动：低血量躲避怪物
    GameCompEnum.AvoidMob: {
        "type": AvoidMobComp,
        # 低血量躲避怪物
        "avoid_ratio": 0.2,
        "trigger": [
            {"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_avoid_mob_event"},
            {"type": GameActionEnum.ResetAttackTarget, },
        ],
        "trigger_cancel": [
            {"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:cancel_avoid_mob_event"},
        ],
    },
}.items())

# witch生成的怪物池
_WitchSummonPool = {
    "normal": [
        {"type": MonsterEnum.ZombieVenom, "weight": 10,},
        {"type": MonsterEnum.ZombieOtaku, "weight": 10,},
        {"type": MonsterEnum.ZombieCaptain, "weight": 10,},
        {"type": MonsterEnum.ZombieGuard, "weight": 10,},
        {"type": MonsterEnum.ZombieExplosive, "weight": 10,},
        {"type": MonsterEnum.ZombieFat, "weight": 10,},
        {"type": MonsterEnum.ZombieDog, "weight": 10,},
    ],
    "boss": [
        {"type": MonsterEnum.ZombieTonsKing, "weight": 10,},
        {"type": MonsterEnum.ZombieJocker, "weight": 10,},
        {"type": MonsterEnum.ZombieBigDog, "weight": 10,},
        {"type": MonsterEnum.ZombieSuperTNT, "weight": 10,},
        {"type": MonsterEnum.ZombieSpecialGuard, "weight": 10,},
        {"type": MonsterEnum.ZombieBlackVenom, "weight": 10,},
        {"type": MonsterEnum.ZombieGoldenChick, "weight": 10,},
        {"type": MonsterEnum.ZombieGangs, "weight": 10,},
    ],
}

_EntityComponentDict = {
    # region 瞬杀者
    MonsterEnum.ZombieSnapKiller: {
        # 攻击距离判定
        "attack_dist": 3,
        # 瞬移距离判定
        "teleport_start_dist": 16,
        "teleport_end_dist": 6,
        # 跳跃攻击Y轴检测，高低差在以下范围时才执行跳跃攻击
        "jump_height":(0,5),
        # 跳跃cd
        "jump_cd" :15 * 30,
        # 跳跃攻击伤害
        "jump_hit_damge":10,
        # query.mod.action 1是蹲下 2是蹲下准备 3是蹲下后飞扑 4是飞扑空中飞行 5是抓挠
        "components": {
            # 近战攻击
            GameCompEnum.SnapKillerMeleeAttack1: {
                "type": MeleeAttackComp,
                # timeline
                "timeline": {
                    # 第0帧
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 1}, },
                    10: {"type": ActionEnum.AreaAttack, "radius": 1, },  # 伤害=代码获取实体的配置数值
                    22: {"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 0}, },
                },
            },
            GameCompEnum.SnapKillerMeleeAttack2: {
                "type": MeleeAttackComp,
                # timeline
                "timeline": {
                    # 第0帧
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.attack2": 1}, },
                    10: {"type": ActionEnum.AreaAttack, "radius": 1, },
                    22: {"type": ActionEnum.SetMolang, "molang": {"query.mod.attack2": 0}, },
                },
            },
            GameCompEnum.SnapKillerJumpReady:{
                "timeline": {
                    # 第0帧
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 1}, },
                    5: {"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:jump_event"},
                    15: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 2}, },
                    35: {},
                },
            },
            GameCompEnum.SnapKillerCancelJumpReady:{
                "timeline": {
                    0:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:cancel_jump_event"},
                    5: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 0}, },
                },
           },
            GameCompEnum.SnapKillerJumpFly:{
                "type": SnapKillerJumpAttackComp,
                "timeline": {
                    # 第0帧
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 3}, },
                    7: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 4}, },
                    # flying_time float 飞扑时在空中飞行时间的最大值，飞行时间取[0.1,flying_time]
                    # start_flying bool 组件将会根据是否是飞行状态设置生物重力，开启碰撞检测等等
                    # set_gravity int 当存在set_gravity字段时，代表组件只会设置实体重力，不会执行其他功能
                    8:{"type": GameActionEnum.SnapKillerJumpAttack, "flying_time": 0.3, "start_flying":True },
                    15:{"type": GameActionEnum.SnapKillerJumpAttack, "flying_time": 0.3, "start_flying":True ,"set_gravity":0},# 提前设置生物重力为世界重力，好让跳跃有下落感
                    30:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:cancel_jump_event"},
                    38:{"type": GameActionEnum.SnapKillerJumpAttack, "flying_time": 0.3, "start_flying":False},
                    40: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 0}, },
                },
            },
            GameCompEnum.SnapKillerCoerceAttack:{
                "timeline": {
                    # 第0帧
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 5}, },
                    37: {"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 0}, },
                },
            },
            GameCompEnum.Teleport: {
                "type": TeleportComp,
                "timeline": {
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.teleport": 1}, },
                    3: {"type": ActionEnum.TeleportToTarget, "max_dist": 5, "target_min_dist": 1, },
                    5: {"type": ActionEnum.SetMolang, "molang": {"query.mod.teleport": 0}, },
                },
                # cd，tick
                "cd": 2 * 30,
            },
            # 被动
            GameCompEnum.ImmuneProjectile: {
                "type": AdaptiveImmuneDamageComp,
                # 可触发的伤害类型
                "damage_type": (ActorDamageCause.Projectile, DamageTagEnum.Bullet),
                # 适应条件：伤害比例(适应后免疫该类伤害)
                "damage_ratio_condition": 0.33,
                # 触发后设置molang(仅设置一次)
                "molang": {"query.mod.adaptive_immune_damage": 1},
            },
        },
    },
    # endregion
    
    # region 尖叫者
    MonsterEnum.ZombieWitch:{
        # 攻击距离判定
        "attack_dist": 3,
        # 生成cd
        "summon_cd": 30 * 30,
        # 生成生物上限
        "summon_maximum":10,
        # 检测玩家行动范围
        "can_find_distance":16,
        # 玩家惊扰witch最近距离
        "can_startle_witch_distance":5,

        # 出生自带的效果
        "effects": {
            "fog": {"strength": 4},
        },

        # query.mod.action 1是坐下，2是坐下哭泣，3是坐下起身，4是移动头低下，5是移动哭，6是移动头抬起，7是召唤尖叫
        "components": {
            GameCompEnum.WitchSummonEtity:{
                "type":WitchEtityComp,
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 7},},
                    5:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:cancel_set_can_move_to_attack"},
                    30:{"type": GameActionEnum.WitchSummonEtity, "summon_radius": 5, "summon_count": 6, "summon_pool": _WitchSummonPool["boss"]},
                    35:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_can_move_to_attack"},
                    40:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 0},}
                },
            },
            GameCompEnum.WitchSitUp:{
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 3},},
                    45:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_move_quickly"},
                    50:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_can_move_to_attack"},
                    55:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 0},}
                },
            },
            GameCompEnum.WitchSitDownToCry:{
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 1},},
                    5:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:cancel_set_can_move_to_attack"},
                    55:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 2},}
                },
            },
            GameCompEnum.WitchMoveUp:{
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 6},},
                    45:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_move_quickly"},
                    50:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_can_move_to_attack"},
                    55:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 0},}
                },
            },
            GameCompEnum.WitchMoveDownToCry:{
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 4},},
                    5:{"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_move_slowly"},
                    55:{"type": ActionEnum.SetMolang, "molang": {"query.mod.action": 5},}
                },
            },
            GameCompEnum.WitchMeleeAttack1:{
                "type": MeleeAttackComp,
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 1},},
                    10: {"type": ActionEnum.AreaAttack, "radius": 2, },
                    20:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 0},}
                },
            },
            GameCompEnum.WitchMeleeAttack2:{
                "type": MeleeAttackComp,
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack2": 1},},
                    10: {"type": ActionEnum.AreaAttack, "radius": 2, },
                    20:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack2": 0},}
                },
            },
        },
    },
    # endregion

    # region 反叛军、盗贼
    MonsterEnum.RebelRagman: {
        "attack_dist": 3,
        "shoot_dist": 10,
        # 低于多少生命(%)才触发回血
        "recover_ratio": 0.5,
        # 回血cd
        "recover_cd": 5 * 30,

        # 手持物品（该列表内的物品，需在行为包json中也配置一份，否则不会拾取；如不需要拾取，则不需配置）
        "item_pool": [
            {"itemName": "scuke_survive:melee_axe", "weight": 10,},
            {"itemName": "scuke_survive:gun_pistol1", "weight": 10,},
            {"itemName": "scuke_survive:gun_smg1", "weight": 10,},
        ],
        # 盔甲
        "has_armor_prob": 0.5,
        "head_armor_pool": [
            {"itemName": "scuke_survive:armor_soviet_tig_helmet_black", "weight": 10,},
            {"itemName": "scuke_survive:armor_green_helmet", "weight": 10,},
            {"itemName": "scuke_survive:armor_lead_helme", "weight": 10,},
        ],
        "chest_armor_pool": [
            {"itemName": "scuke_survive:armor_tattered_chest", "weight": 10,},
        ],

        "components": _SoilderComonents,
    },
    MonsterEnum.RebelVagrant: {
        "attack_dist": 3,
        "shoot_dist": 10,
        # 低于多少生命(%)才触发回血
        "recover_ratio": 0.5,
        # 回血cd
        "recover_cd": 5 * 30,

        # 手持物品（该列表内的物品，需在行为包json中也配置一份，否则不会拾取；如不需要拾取，则不需配置）
        "item_pool": [
            {"itemName": "scuke_survive:melee_chainsaw_old", "weight": 10,},
            {"itemName": "scuke_survive:gun_lmg1_s1", "weight": 10,},
            {"itemName": "scuke_survive:gun_pistol1_s2", "weight": 10,},
        ],
        # 盔甲
        "has_armor_prob": 0.5,
        "head_armor_pool": [
            {"itemName": "scuke_survive:armor_green_helmet", "weight": 10,},
            {"itemName": "scuke_survive:armor_red_mask_helmet", "weight": 10,},
            {"itemName": "scuke_survive:armor_lithium_helme", "weight": 10,},
        ],
        "chest_armor_pool": [
            {"itemName": "scuke_survive:armor_tattered_chest", "weight": 10,},
            {"itemName": "scuke_survive:armor_lithium_chest", "weight": 10,},
        ],

        "components": _SoilderComonents,
    },
    MonsterEnum.RebelSoilder: {
        "attack_dist": 3,
        "shoot_dist": 10,
        # 低于多少生命(%)才触发回血
        "recover_ratio": 0.5,
        # 回血cd
        "recover_cd": 5 * 30,

        # 手持物品（该列表内的物品，需在行为包json中也配置一份，否则不会拾取；如不需要拾取，则不需配置）
        "item_pool": [
            {"itemName": "scuke_survive:melee_pan", "weight": 10,},
            {"itemName": "scuke_survive:gun_rifle1_s2", "weight": 10,},
            {"itemName": "scuke_survive:gun_lmg1_s2", "weight": 10,},
        ],
        # 盔甲
        "has_armor_prob": 0.5,
        "head_armor_pool": [
            {"itemName": "scuke_survive:armor_military_helmet", "weight": 10,},
            {"itemName": "scuke_survive:armor_soviet_tig_helmet_gold", "weight": 10,},
            {"itemName": "scuke_survive:armor_snow02_helmet", "weight": 10,},
        ],
        "chest_armor_pool": [
            {"itemName": "scuke_survive:armor_snow02_chest", "weight": 10,},
        ],
        "leg_armor_pool": [
            {"itemName": "scuke_survive:armor_rare_earth_legs", "weight": 10,},
        ],

        "components": _SoilderComonents,
    },
    MonsterEnum.RebelLeader: {
        "attack_dist": 3,
        "shoot_dist": 10,
        # 低于多少生命(%)才触发回血
        "recover_ratio": 0.5,
        # 回血cd
        "recover_cd": 5 * 30,
        # 召唤士兵的血量值
        "summon_ratio": 0.5,
        # 无人机的cd
        "flyingdrone_cd": 50 * 30,

        # 手持物品（该列表内的物品，需在行为包json中也配置一份，否则不会拾取；如不需要拾取，则不需配置）
        "item_pool": [
            {"itemName": "scuke_survive:melee_axe_golden", "weight": 10,},
            {"itemName": "scuke_survive:gun_shotgun1_s3", "weight": 10,},
            {"itemName": "scuke_survive:gun_rifle1", "weight": 10,},
        ],
        # 盔甲
        "has_armor_prob": 0.5,
        "head_armor_pool": [
            {"itemName": "scuke_survive:armor_red_rescue_helmet", "weight": 10,},
            {"itemName": "scuke_survive:armor_soviet_tig_helmet_gold", "weight": 10,},
            {"weight": 5,},
        ],
        "chest_armor_pool": [
            {"itemName": "scuke_survive:armor_red_rescue_chest", "weight": 10,},
            {"weight": 5,},
        ],
        "leg_armor_pool": [
            {"itemName": "scuke_survive:armor_red_rescue_legs", "weight": 10,},
            {"weight": 5,},
        ],
        "boot_armor_pool": [
            {"itemName": "scuke_survive:armor_red_rescue_boots", "weight": 10,},
            {"weight": 5,},
        ],

        "components": dict(_WeaponComponents.items() + {
            # 低生命回血
            GameCompEnum.HealthRecover: {
                "actions": [
                    {"type": GameActionEnum.TriggerAddEvent, "event": "scuke_survive:set_drink_potion_event"},
                ],
            },
            # # 低生命召唤反叛军
            # GameCompEnum.SummonRebel: {
            #     "type": SummonEntityComp,
            #     "timeline":{
            #         0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 1},},
            #         12:{"type": GameActionEnum.SummonEntity, "radius": 0, "count": 1, "engineTypeStr": "minecraft:fireworks_rocket",},
            #         25:{"type": GameActionEnum.SummonEntity, "radius": 2, "count": 3, "engineTypeStr": MonsterEnum.RebelSoilder, "phase_enhance": True,},
            #         30:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 0},},
            #     },
            # },
            # 召唤无人机
            GameCompEnum.SummonFlyingdrone: {
                "type": SummonEntityComp,
                "timeline":{
                    0:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 1},},
                    12:{"type": GameActionEnum.SummonEntity, "radius": 0, "count": 1, "engineTypeStr": "minecraft:fireworks_rocket",},
                    25:{"type": GameActionEnum.SummonEntity, "radius": 2, "height": 2, "count": 1, "engineTypeStr": MonsterEnum.RebelFlyingdrone,},
                    30:{"type": ActionEnum.SetMolang, "molang": {"query.mod.attack1": 0},},
                },
            },
        }.items()),
    },
    # endregion
}
_EntityComponentDict[MonsterEnum.ZombieWitchNormal] = commonApiMgr.DeepCopy(_EntityComponentDict[MonsterEnum.ZombieWitch])
_EntityComponentDict[MonsterEnum.ZombieWitchNormal]["components"][GameCompEnum.WitchSummonEtity]["timeline"][30] = {
    "type": GameActionEnum.WitchSummonEtity, "summon_radius":5, "summon_count":4, "summon_pool": _WitchSummonPool["normal"]}
_EntityComponentDict[MonsterEnum.ZombieWitchNormal].pop("effects", None)

def GetEntityConfig(engineTypeStr):
    """获取实体组件 配置信息"""
    return _EntityComponentDict.get(engineTypeStr)

def GetAllEntityFogCfg():
    cfg = {}
    for engineType, val in _EntityComponentDict.iteritems():
        if "effects" in val:
            if "fog" in val["effects"]:
                cfg[engineType] = val["effects"]["fog"]
    return cfg

def GetAllEntityParticleCfg():
    cfg = {}
    for engineType, val in _EntityComponentDict.iteritems():
        if "effects" in val:
            if "particle" in val["effects"]:
                cfg[engineType] = val["effects"]["particle"]
    return cfg

# endregion


