# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.cfg.molangConfig import QueryEnum
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum


"""
载具 改造 配置表
"""

RemoldUIRange = 16 ** 2
"""改造UI显示的范围要求"""

# region 枚举
class RemoldTypeEnum:
    """改造类型枚举"""

    Engine = "engine"
    """引擎"""
    FrontBumper = "front_bumper"
    """前杠"""
    CarBody = "carBody"
    """车身"""
    CarBothSides = "car_both_sides"
    """车体两侧"""
    CarWheel = "car_wheel"
    """车轮"""

    Module1 = "module1"
    """变形模块1"""
    Module2 = "module2"
    """变形模块2"""

class PartEnum:
    """改造配件枚举"""
    OldEngine = "old_engine"
    """旧引擎"""
    EfficientEngine = "efficient_engine"
    """混动引擎"""
    RedEngine = "red_engine"
    """红头引擎"""
    OldBumper = "old_bumper"
    """金属前铲"""
    AlloyBumper = "alloy_bumper"
    """越野前铲"""
    BullBar = "bull_bar"
    """合金冲击铲"""
    SafetyCage = "safety_cage"
    """合金防滚架"""
    EMP = "emp"
    """电磁脉冲"""
    Missile = "missile"
    """导弹"""
    Thruster = "thruster"
    """推进器"""
    ArmorProfile = "armor_profile"
    """合金轮廓"""
    SpikeProfile = "spike_profile"
    """尖刺轮廓"""

    # 变形模块
    RunWater = "run_water"
    """水上行驶"""
    Fly = "fly"
    """飞行"""
# endregion

# region UI相关
# 分页顺序列表
_RemoldTypeTabsList = (
    RemoldTypeEnum.Engine,
    RemoldTypeEnum.FrontBumper,
    RemoldTypeEnum.CarBody,
    RemoldTypeEnum.CarBothSides,
    RemoldTypeEnum.CarWheel,
    RemoldTypeEnum.Module1,
    RemoldTypeEnum.Module2,
)
def GetRemoldTypeTabsList():
    """获取分页顺序列表"""
    return _RemoldTypeTabsList
# endregion


# 改造类型对应的molang表达式
_RemoldTypeMolangConfig = {
    RemoldTypeEnum.FrontBumper: QueryEnum.FrontBumper,
    RemoldTypeEnum.CarBody: QueryEnum.CarBody,
    RemoldTypeEnum.CarBothSides: QueryEnum.CarBothSides,
    RemoldTypeEnum.CarWheel: QueryEnum.CarWheel,
    RemoldTypeEnum.Module1: QueryEnum.Module1,
    RemoldTypeEnum.Module2: QueryEnum.Module2,
}
def GetRemoldTypeMolangConfig(remoldType):
    """获取改造类型对应的molang表达式"""
    return _RemoldTypeMolangConfig.get(remoldType)

# 改造类型对应的配件数据
_RemoldTypeDict = {
    RemoldTypeEnum.Engine: [
        PartEnum.OldEngine,
        PartEnum.EfficientEngine,
        PartEnum.RedEngine,
    ],
    RemoldTypeEnum.FrontBumper: [
        PartEnum.OldBumper,
        PartEnum.AlloyBumper,
        PartEnum.BullBar,
    ],
    RemoldTypeEnum.CarBody: [
        PartEnum.SafetyCage,
        PartEnum.EMP,
        PartEnum.Missile,
    ],
    RemoldTypeEnum.CarBothSides: [
        PartEnum.Thruster,
    ],
    RemoldTypeEnum.CarWheel: [
        PartEnum.ArmorProfile,
        PartEnum.SpikeProfile,
    ],

    # 变形模块，所有变形模块使用同一个配件列表
    RemoldTypeEnum.Module1: [
        PartEnum.RunWater,
        PartEnum.Fly,
    ],
    RemoldTypeEnum.Module2: [
        PartEnum.RunWater,
        PartEnum.Fly,
    ],
}
def GetRemoldParts(remoldType):
    """
    获取改造类型对应的配件
    return: list
    """
    return _RemoldTypeDict.get(remoldType)

# region 配件的配置
# 改造配件的配置信息
_PartConfig = {
    PartEnum.OldEngine: {
        # 配件物品id
        "itemName": "scuke_survive:carpart_old_engine",
        # 配件描述
        "info": "小幅增加载具的能源上限",
        # 配件实际功能
        "attrs": {
            "max_energy": 100,
        },
    },
    PartEnum.EfficientEngine: {
        "itemName": "scuke_survive:carpart_efficient_engine",
        "info": "中幅增加载具的能源上限",
        "attrs": {
            "max_energy": 300,
        },
    },
    PartEnum.RedEngine: {
        "itemName": "scuke_survive:carpart_red_engine",
        "info": "大幅增加载具的能源上限",
        "attrs": {
            "max_energy": 600,
        },
    },
    PartEnum.OldBumper: {
        "itemName": "scuke_survive:carpart_old_bumper",
        "info": "小幅增加载具的耐久度和攻击",
        # # 配件molang值（key由配件类型决定）
        "molangValue": 0,
        # 老旧保险杠默认装配，所以实际不需要加数值
        # "attrs": {
        #     "max_durability": 100,
        #     "hit_max_damage": 0,
        # },
        # 默认解锁
        "unlock": True,
        # 默认使用
        "use": True,
    },
    PartEnum.AlloyBumper: {
        "itemName": "scuke_survive:carpart_alloy_bumper",
        "info": "中幅增加载具的耐久度和攻击",
        "molangValue": 1,
        "attrs": {
            "max_durability": 250,
            "hit_max_damage": 40,   # 撞击最大伤害值
        },
    },
    PartEnum.BullBar: {
        "itemName": "scuke_survive:carpart_bullbar",
        "info": "大幅增加载具的耐久度和攻击、击退",
        "molangValue": 2,
        "attrs": {
            "max_durability": 500,
            "knockback": 8,
            "hit_max_damage": 80,
        },
    },
    PartEnum.SafetyCage: {
        "itemName": "scuke_survive:carpart_safety_cage",
        "info": "中幅增加载具的耐久度",
        "molangValue": 1,
        "attrs": {
            "max_durability": 250,
        },
    },
    PartEnum.EMP: {
        "itemName": "scuke_survive:carpart_emp",
        "info": "对附近所有敌人造成伤害\n§c配件正在研发中，敬请期待！",
        "molangValue": 2,
        "skill": {
            "damage": 40,
            "radius": 8,
        },
    },
    PartEnum.Missile: {
        "itemName": "scuke_survive:carpart_missile",
        "info": "使载具发射导弹",
        "molangValue": 3,
        "skill": {
            # 技能按钮索引
            "btnIndex": 0,
            "btnIconPath": "textures/ui/scuke_survive/icon/part_missile",
            "btnName": "发射",
            # 功能
            # 锁定目标数量
            "maxCount": 6,
            # 锁定半径
            "radius": 32,
            # 视野范围的角度
            "viewRot": 60,
            # 锁定频率，秒
            "lockFrequency": 0.5,
            # 锁定后的特效资源
            "lockEffect": "scuke_survive:car_locked_target",

            # 技能CD
            "cd": 10,
            # 技能消耗
            "energy": 20,

            # 导弹抛射物
            "projectile": ProjectileEnum.Missile,
            "power": 0.8,
            # 抛射物发射位置的bone名字
            "boneNames": ["rocket1", "rocket2", "rocket3", "rocket4", "rocket5", "rocket6", ],
            # 预置，如果获取不到bone，则使用这里的数据
            "boneOffsets": [(-135, 5.5, 6), (-135, 5.8, 5.5), (-135, 6, 5), (135, 5.5, 6), (135, 5.8, 5.5), (135, 6, 5), ],
            # 导弹命中的数据
            "projectCfg": {
                "damage_radius": 5,
                "damage": 50,
                "explode_radius": 5,
                "fire": False,
                "breaks": True,
                "hit_sound": "scuke_survive.skill.missile.hit",
            },
        },
    },
    PartEnum.ArmorProfile: {
        "itemName": "scuke_survive:carpart_armor_profile",
        "info": "中幅增加载具的耐久度",
        "molangValue": 1,
        "attrs": {
            "max_durability": 200,
        },
    },
    PartEnum.SpikeProfile: {
        "itemName": "scuke_survive:carpart_spike_profile",
        "info": "对两侧敌人造成伤害\n§c配件正在研发中，敬请期待！",
        "molangValue": 2,
    },
    PartEnum.Thruster: {
        "itemName": "scuke_survive:carpart_thruster",
        "info": "推进器\n§c配件正在研发中，敬请期待！",
        "molangValue": 1,
    },

    PartEnum.RunWater: {
        "itemName": "scuke_survive:carpart_run_water",
        "info": "载具可变形为水上形态",
        "molangValue": 0,
        "unlock": True,
        "use": True,
        # 装载到指定的模块
        "use_to_remold": RemoldTypeEnum.Module1,
    },
    PartEnum.Fly: {
        "itemName": "scuke_survive:carpart_fly",
        "info": "载具可变形为飞行形态",
        "molangValue": 1,
        "skill": {
            # 氮气飞行UI
            "btnIndex": 2,
            # 功能
            # 上下飞行的速度参数（不等于实际速度）
            "upSpeed": 0.5,
            "downSpeed": -0.5,
            # 移动的飞行速度参数
            "flySpeedRatio": 19,
            # 飞行消耗能源的倍率参数
            "energyRatio": 4,
            # 悬浮音效
            "hover_sound": "scuke_survive.skill.fly.hover",
            # 上升下降
            "updown_sound": "scuke_survive.skill.fly.updown",
            # 加速
            "speedup_sound": "scuke_survive.skill.fly.speedup",

            # cd
            "cd": 60,
            # 持续时间
            "duration": 60,
            # 飞行状态的icon图
            "icons": [
                "textures/ui/scuke_survive/icon/icon_fly",
                "textures/ui/scuke_survive/icon/icon_nofly",
            ]
        },
    },
}
def GetPartConfig(partName):
    """获取改造配件的配置信息"""
    return _PartConfig.get(partName)

def GetPartSkillConfig(partName):
    """获取改造配件的配置信息"""
    partCfg = GetPartConfig(partName)
    if partCfg:
        return partCfg.get("skill")
    return None

def GetPartSkillProjectCfg(partName):
    """获取改造配件的技能抛射物配置"""
    partCfg = GetPartConfig(partName)
    if partCfg:
        skill = partCfg.get("skill")
        if skill:
            return skill.get("projectCfg")
    return None
# endregion
