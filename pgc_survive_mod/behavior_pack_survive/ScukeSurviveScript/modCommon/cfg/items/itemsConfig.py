# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg import molangConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum


"""
道具物品 配置表
"""


class ItemsNameEnum:
    """道具物品名称枚举"""
    
    CarRescue = "scuke_survive:car_rescue"
    """载具救援道具"""

    GrenadeSmall = "scuke_survive:items_grenade_small"
    """小手雷"""
    GrenadeMiddle = "scuke_survive:items_grenade_middle"
    """中手雷"""
    GrenadeLarge = "scuke_survive:items_grenade_large"
    """大手雷"""

    OilDrumSmall = "scuke_survive:items_oil_drum_small"
    """小油桶"""
    OilDrumLarge = "scuke_survive:items_oil_drum_large"
    """大油桶"""

    Landmine = "scuke_survive:items_landmine"
    """地雷"""

    BarricadeWood = "scuke_survive:items_barricade_wood"
    """木拒马"""
    BarricadeIron = "scuke_survive:items_barricade_iron"
    """铁丝网"""

    Trap = "scuke_survive:items_trap"
    """捕兽夹"""

    TimeBomb1 = "scuke_survive:time_bomb1"
    TimeBomb2 = "scuke_survive:time_bomb2"
    TimeBomb3 = "scuke_survive:time_bomb3"
    """定时炸弹"""

    C4Bomb1 = "scuke_survive:c4_bomb1"
    C4Bomb2 = "scuke_survive:c4_bomb2"
    C4Bomb3 = "scuke_survive:c4_bomb3"

    C4Detonator = "scuke_survive:c4_detonator"
    """C4炸弹（遥控）"""

    TombStone = "scuke_survive:tombstone"


# 原版箭矢id
Arrow = "minecraft:arrow"

# 空气方块字典
AirBlockDict = {"name": "minecraft:air", "aux": 0}


# region UI按钮配置
# 道具和UI的映射关系
_ItemsUIConfig = {
    ItemsNameEnum.CarRescue: {
        # 对应的按钮索引（复用控件）
        "buttonIndex": 0,
        # 按钮贴图
        "buttonTexture": "textures/ui/scuke_survive/car/arrow",
        "buttonTexturePress": "textures/ui/scuke_survive/car/arrow",
        # 按钮文字（如果有的话）
        "buttonText": "救援",
        # 按钮响应的订阅事件名
        "subscribeEvent": eventConfig.ItemUseBtnClickedEvent,
        # 订阅事件发送的参数
        "subscribeEventParam": {"stage": "car_rescue"},
    },
}


def GetItemsUIConfig(itemName):
    """获取道具物品的UI配置信息"""
    return _ItemsUIConfig.get(itemName)
# endregion


# region 抛射物道具配置
# 抛射物逻辑相关的配置，写在entity中
_ProjectileDict = {
    ItemsNameEnum.GrenadeSmall: {
        # 抛射物实体id
        "projectile_str": ProjectileEnum.GrenadeSmall,
        # 抛射力度
        "power": 1.2,
        # 抛射物重力
        "gravity": 0.05,
        # 高度偏移
        "height_offset": 0.15,
        # 发射时角度偏移
        "rot_offset": -15,

        # 延迟创建时间，和动画配合使用
        "delay_create": 0.1,
        # 扣除数量，如果不需要扣除，则不设置
        "deduct_item_count": 1,
        # # 使用动画数据
        # "use_anim_cfg": {
        #     # 玩家动画id
        #     "player_anim": "",
        #     # 动画molang
        #     "molang": molangConfig.QueryEnum.UseItem,
        #     # molang重置时间，需比动画时长要短
        #     "molang_reset_time": 0.1,
        # },
    },
    ItemsNameEnum.GrenadeMiddle: {
        "projectile_str": ProjectileEnum.GrenadeMiddle,
        "power": 1.2,
        "gravity": 0.07,
        "height_offset": 0.15,
        "rot_offset": -15,
        "delay_create": 0.1,
        "deduct_item_count": 1,
    },
    ItemsNameEnum.GrenadeLarge: {
        "projectile_str": ProjectileEnum.GrenadeLarge,
        "power": 1.2,
        "gravity": 0.09,
        "height_offset": 0.15,
        "rot_offset": -15,
        "delay_create": 0.1,
        "deduct_item_count": 1,
    },
}


def GetProjectileConfig(itemName):
    """获取抛射物配置信息"""
    return _ProjectileDict.get(itemName)


# 手雷动画
_GrenadeBindAnims = {
    "anims": {
        "first_idle": "animation.scuke_survive_grenade.first_idle",
        "first_throw_prepare": "animation.scuke_survive_grenade.first_throw_prepare",
        "first_throw_release": "animation.scuke_survive_grenade.first_throw_release",
        "throw_prepare": "animation.scuke_survive_grenade.throw_prepare",
        "throw_release": "animation.scuke_survive_grenade.throw_release",
    },
    "anim_ctrls": {
        "grenade_throw_ctrl": "controller.animation.scuke_survive_grenade.throw",
    },
    "ctrl_condition": "query.get_equipped_item_name == '{}' || query.get_equipped_item_name == '{}' || query.get_equipped_item_name == '{}'".format(
        ItemsNameEnum.GrenadeSmall.split(":")[1], ItemsNameEnum.GrenadeMiddle.split(":")[1], ItemsNameEnum.GrenadeLarge.split(":")[1]),
}


def GetGrenadeBindAnims():
    """获取手雷绑定动画信息"""
    return _GrenadeBindAnims
# endregion


# region 功能方块配置
_FunctionalBlockDict = {
    ItemsNameEnum.OilDrumSmall: {
        # 引爆类型（如果不设置，则无法引爆）
        "cause": [ "gun", "fire_projectile" ],
        # 伤害半径
        "damage_radius": 4,
        # 伤害值
        "damage": 5,
        # 爆炸半径
        "explode_radius": 4,
        # 是否着火
        "fire": True,
        # 是否破坏方块
        "breaks": True,
    },
    ItemsNameEnum.OilDrumLarge: {
        "cause": [ "gun", "fire_projectile" ],
        "damage_radius": 7,
        "damage": 10,
        "explode_radius": 7,
        "fire": True,
        "breaks": True,
    },
    ItemsNameEnum.Landmine: {
        "cause": [ "gun", "fire_projectile" ],
        "damage_radius": 4,
        "damage": 4,
        "explode_radius": 4,
        "fire": True,
        "breaks": True,
    },

    ItemsNameEnum.Trap: {
        # 咬合时伤害值
        "damage": 5,
        # 禁锢时长, 秒
        "bite_time": 3,
        # 禁锢tick的cd
        "tick_cd": 0.2,
    },
    
    # 陷阱类
    ItemsNameEnum.BarricadeWood: {
        # 最大耐久
        "durability": 30,
        # 伤害
        "damage": 2,
        # 伤害CD
        "damage_cd": 0.5,
    },
    ItemsNameEnum.BarricadeIron: {
        "durability": 50,
        "damage": 3,
        "damage_cd": 0.5,
    },

    # 炸弹类
    ItemsNameEnum.TimeBomb1: {
        # 引爆类型（如果不设置，则无法引爆）
        "cause": ["gun", "fire_projectile"],
        # 伤害半径
        "damage_radius": 8,
        # 伤害值
        "damage": 12,
        # 爆炸半径
        "explode_radius": 8,
        # 是否着火
        "fire": True,
        # 是否破坏方块
        "breaks": True,
    },
    ItemsNameEnum.C4Bomb1: {
        # 引爆类型（如果不设置，则无法引爆）
        "cause": ["gun", "fire_projectile"],
        # 伤害半径
        "damage_radius": 12,
        # 伤害值
        "damage": 18,
        # 爆炸半径
        "explode_radius": 12,
        # 是否着火
        "fire": True,
        # 是否破坏方块
        "breaks": True,
    },
    ItemsNameEnum.TombStone: {
        'reviveTime': 300,
    },
}
_FunctionalBlockDict[ItemsNameEnum.TimeBomb2] = _FunctionalBlockDict[ItemsNameEnum.TimeBomb1]
_FunctionalBlockDict[ItemsNameEnum.TimeBomb3] = _FunctionalBlockDict[ItemsNameEnum.TimeBomb1]
_FunctionalBlockDict[ItemsNameEnum.C4Bomb2] = _FunctionalBlockDict[ItemsNameEnum.C4Bomb1]
_FunctionalBlockDict[ItemsNameEnum.C4Bomb3] = _FunctionalBlockDict[ItemsNameEnum.C4Bomb1]


def GetFunctionalBlockConfig(itemName):
    """获取功能方块信息"""
    return _FunctionalBlockDict.get(itemName)


# 特殊方块，在放置时需要根据面朝向转换
SpecialBlockDict = {
    ItemsNameEnum.TimeBomb1: {
        0: ItemsNameEnum.TimeBomb2,
        1: ItemsNameEnum.TimeBomb1,
        2: ItemsNameEnum.TimeBomb3,
        3: ItemsNameEnum.TimeBomb3,
        4: ItemsNameEnum.TimeBomb3,
        5: ItemsNameEnum.TimeBomb3
    },
    ItemsNameEnum.C4Bomb1: {
        0: ItemsNameEnum.C4Bomb2,
        1: ItemsNameEnum.C4Bomb1,
        2: ItemsNameEnum.C4Bomb3,
        3: ItemsNameEnum.C4Bomb3,
        4: ItemsNameEnum.C4Bomb3,
        5: ItemsNameEnum.C4Bomb3
    }
}

# 引爆的抛射物类型
_DetonateProjectileTypeList = (
    Arrow,
    "minecraft:fireball",
    "minecraft:small_fireball",
)


def IsDetonateProjectileType(projectileType):
    """判断是否为引爆的抛射物类型"""
    return projectileType in _DetonateProjectileTypeList

# endregion


# region 方块数据存储参数
# blockEntityData存储数据的key
BlockEntityDataKey = "{}_block_entity_data".format(modConfig.ModNameSpace)
# endregion

