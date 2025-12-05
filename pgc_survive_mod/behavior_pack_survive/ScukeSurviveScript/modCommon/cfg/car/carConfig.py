# -*- coding: UTF-8 -*-
import math
from ScukeSurviveScript.modCommon.modConfig import ModNameSpace
from ScukeSurviveScript.modCommon.cfg.energyConfig import GetAddEnergyMaterialNum as GetAddEnergyMaterialNumByEnergyConfig
from ScukeSurviveScript.modCommon.cfg.molangConfig import QueryEnum
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum


"""
载具配置表
"""


# 载具英文id
CarEngineTypeStr = "scuke_survive:base_car"
BrokenCarEngineTypeStr = "scuke_survive:base_car_broken"


# region 载具操作相关的数据
# 速度参考：玩家走路速度=0.1
def GetAddonSpeed(kmsSpeed):
    """
    根据时速计算行为组件中的速度值
    :param kmsSpeed: float 时速km/h
    :return: float 行为组件中的速度值
    """
    # speed * 2.203 = 格/帧，1秒=20帧；即 speed * 2.203 * 20 = 格/秒
    # 格/秒 * 3.6 = 千格/时
    return (kmsSpeed / 3.6 * 0.05) / 2.203

def GetRealSpeed(kmsSpeed):
    """
    根据时速计算每帧的速度值
    :param kmsSpeed: float 时速km/h
    :return: float 每帧的速度值
    """
    # speed * 2.203 = 格/帧，1秒=20帧；即 speed * 2.203 * 20 = 格/秒
    # 格/秒 * 3.6 = 千格/时
    return kmsSpeed / 3.6 * 0.05

# 载具配置数据
BaseCarConfig = {
    # 相机偏移，x=左右，y=上下，z=前后
    "cameraOffset": (0, 0, 10),
    
    # 最大时速，用于计算行为包设置的速度、显示UI
    "maxSpeedKmh": 100.0,

    # 最大加速度
    "maxASpeed": 0.5,
    # 刹车最大加速度
    "cutASpeed": 0.75,
    # 前进摩擦力（用来控制不踩油门时能滑多久）
    "frictionSpeed": 1.0,
    # 倒退的摩擦力（倒退时能滑距离更短，所以需要单独设置）
    "cutFrictionSpeed": 1.2,

    # 山地速度倍率(山地速度=陆地速度)，默认0.5
    "mountainSpeed": 0.35,
    # 水上速度倍率(水速度*0.5=陆地速度)，默认0.25
    "waterSpeed": 0.4,
    # 岩浆上速度倍率(岩浆速度=陆地速度)，默认0.5
    "lavaSpeed": 0.5,
    # 倒车速度倍率（原版倒车时速度会变慢，需再乘倍率，从而提高速度）
    "backSpeed": 2.0,

    # 转向速度/秒
    "turnSpeed": 160,
    
    # 相机跟随的速度 度/帧；如果帧率低，则转的慢
    "cameraFollowSpeed": 0.2,

    # 撞到实体后，速度倍率，默认为当前速度的95%
    "knockEntitySpeed": 0.95,
    # 破坏方块后，速度倍率，默认为当前速度的90%
    "breakBlockSpeed": 0.9,
    # 破坏方块后，速度倍率，默认为当前速度的90%
    "crashBlockSpeed": 0.5,

    # tick更新频率/秒（最低0.05，即20帧）
    "tickCD": 0.05,

    # 载具宽高
    "collision": (5, 4),
}
# 最大速度，代码中使用到的速度值
BaseCarConfig["maxSpeed"] = GetAddonSpeed(BaseCarConfig["maxSpeedKmh"])
# 计算最大速度的转换参数，用于计算加速度
BaseCarConfig["maxSpeedParam"] = math.acos(0) / BaseCarConfig["maxSpeed"]

# 1档=[0,20], 2=[21,50], 3=[51,80], 4=[81,100], 5=[101,120], 6=[121,200]
_GearsLimit = [0.0, 20.0, 50.0, 80.0, 100.0, 120.0, 200.0]
# endregion


# region 载具行驶的函数
def GetASpeed(speed):
    """
    获取加速度，往前和往后，加速度不一样
    speed = 载具当前移速
    """
    # 随当前的移速变大，加速度变小
    # 公式一：y = a ^ -(speed + b), a影响加速度衰减速率(不能为1), b 影响加速度初始最大值(b越大，加速度越大)
    # 公式二：y = cos(speed * a) * b; speed = [0, maxSpeed], a加速度为0时速度最大值, b = 最大加速度
    a = BaseCarConfig["maxSpeedParam"]
    b = BaseCarConfig["maxASpeed"]
    if speed >= -0.1:
        aspeed = math.cos(speed * a) * b
    else:
        aspeed = abs(math.sin(speed * a) * b)
    return max(aspeed, 0)   # 限制在0-maxASpeed之间

def GetCutASpeed(speed):
    """
    获取倒退的加速度，往前和往后，加速度不一样
    speed = 载具当前移速
    """
    a = BaseCarConfig["maxSpeedParam"]
    if speed > 0.1:
        b = BaseCarConfig["cutASpeed"]
        aspeed = - math.sin(speed * a) * b
    else:
        b = BaseCarConfig["maxASpeed"]
        aspeed = - math.cos(speed * a) * b
    return aspeed

def GetGearNum(speed):
    """获取当前速度的档位"""
    max = len(_GearsLimit)
    for i in range(max):
        if speed <= _GearsLimit[i]:
            return i
    return max

def GetGearSpeedLimit(gear):
    """获取档位对应的速度"""
    speed = 0
    if gear >= 0 and gear < len(_GearsLimit):
        speed = _GearsLimit[gear]
    return speed

# 破坏方块的行为包event
_BreakBlockEvents = [
    (0, "scuke:cancel_break_event", ),
    (GetRealSpeed(10), "scuke:break_blocks_v1_event", ),
    (GetRealSpeed(30), "scuke:break_blocks_v2_event", ),
]
def GetBreakBlockEvent(realSpeed):
    """获取破坏方块的行为包event"""
    setEvent = _BreakBlockEvents[0][1]
    if realSpeed >= _BreakBlockEvents[1][0]:
        return _BreakBlockEvents[1][1]
    return setEvent
# endregion


# region 耐久、能源、撞击伤害
BaseCarAttrConfig = {
    # 耐久上限
    "maxDurability": 100,
    # 能源上限
    "maxEnergy": 100,

    # 摔伤最低高度
    "fallMinHeight": 6,
    # 每一格高度，扣耐久的比例
    "fallHeightDamageRatio": 2,

    # 被攻击时的耐久损耗比例
    "attackDamageRatio": 0.5,
    # 撞到方块时的耐久损耗比例: {speed: durability}。填写速度差值，如从50掉到0扣20耐久
    "crashDamageRatios": [
        # speed = 格/帧，durability = 耐久损耗值
        (GetRealSpeed(50), 0), # 最低速度要求，低于该速度不会掉耐久
        (GetRealSpeed(80), 2),
        (GetRealSpeed(130), 5),
        (GetRealSpeed(200), 10),
    ],
    # 在火、岩浆上，掉耐久的频率: (cd, 掉耐久值)
    "fallDamageParam": (10, 1),
    # 暴风雪的掉耐久频率: (cd, 掉耐久值)
    "snowstormParam": (10, 1),

    # 载具行驶的能源消耗: (距离/格, 损耗值)
    "energyConsumeParam": (100, 1),

    # 撞飞生物的参数
    "crashHurtParam": {
        "knockSpeed": GetRealSpeed(20),  # 撞飞的最低速度要求
        "knockbackPower": 8, # 根据载具速度，决定撞飞距离的参数，默认4

        "hurtSpeed": GetRealSpeed(50),  # 撞伤的最低速度要求
        "damageRatio": 0.4, # 伤害比例（总血量的百分比）
        "maxDamage": 20,    # 最高伤害
    },
}

def GetCrashDamage(speed):
    """获取撞击时的耐久损耗"""
    for speedLimit, damage in BaseCarAttrConfig["crashDamageRatios"]:
        if speed <= speedLimit:
            # print("_____________ GetCrashDamage", speed, speedLimit, damage)
            return damage
    return 0

# endregion


# region 能源

def GetAddEnergyMaterialNum(itemName):
    """获取材料增加的能源值"""
    return GetAddEnergyMaterialNumByEnergyConfig(itemName)

# endregion


# region 维修相关
RepairConfig = {
    # 工具id
    "itemName": "scuke_survive:car_repair",
    # 维修CD/秒（多久恢复一次耐久）
    "repairCD": 0.25,
    # 维修一次，载具恢复多少耐久
    "repairDurability": 1,
    # 维修一次，工具损耗耐久
    "itemDurability": 1,
}

# 修复损坏的载具，所需的材料
_RepairNeedItems = [
    {"newItemName": "minecraft:iron_ingot", "newAuxValue": 0, "count": 5},
    {"newItemName": "minecraft:copper_ingot", "newAuxValue": 0, "count": 5},
    {"newItemName": "scuke_survive:ingot_lead", "newAuxValue": 0, "count": 5},
    {"newItemName": "minecraft:glass", "newAuxValue": 0, "count": 3},
    {"newItemName": "scuke_survive:mat_plastic_board", "newAuxValue": 0, "count": 5},
]
def GetRepairNeedItems():
    """获取修复损坏的载具，所需的材料"""
    return _RepairNeedItems


# 使用维修道具时，需给玩家挂上的动画
AddAnimations = {
    "animKey": "car_repair_in_hand_idle",
    "animName": "animation.scuke_survive_player.third_hand_up",
    "condition": "!variable.is_first_person && query.get_equipped_item_name == '{}'".format(RepairConfig["itemName"].split(":")[1]),
}
# endregion


# region 救援载具相关
_RescueConfig = {
    # 载具和玩家的最大距离，超过距离的无法救援，单位格
    "maxDistance": 64,
    # 救援功能消耗道具的耐久值，道具最大耐久=512
    "durability": -100,
    # 延迟tp载具的时间，需配合UI的表现，单位秒
    "delayTPTime": 1.0,
    # UI动画的参数
    "uiAnimParam": {
        # 全透明到不透明的持续时间
        "0_1_time": 1.0,
        "1_1_time": 0.5,
        "1_0_time": 0.5,
    },
}
def GetRescueConfig():
    """获取救援相关配置信息"""
    return _RescueConfig

# 射线检测应该忽略的方块
_RescueRayIngoreBlocks = (
    "minecraft:lava",
    "minecraft:flowing_lava",
)
def IsNotRescueRayBlock(blockName):
    """检测救援时，如果是这些方块，就不让救援。用于检测脚底方块"""
    return blockName in _RescueRayIngoreBlocks

# endregion


# region 瘫痪数据
InhibitParticle = "scuke_survive:car_emp_inhibit"
# endregion


# region 载具乘骑相关数据
# x+ = 往左, z+ = 往前, y+ = 往上
_RiderConfig = {
    # 载具乘骑的位置偏移，需与行为包json保持一致
    0: {"pos": (0.8, 2.6, 2.2)},
    1: {"pos": (-0.8, 2.6, 2.2)},
    2: {"pos": (-0.8, 2.6, -0.2)},
    3: {"pos": (-0.8, 2.6, -0.2)},
}
# 预处理各种数据
for val in _RiderConfig.values():
    # x偏移 与 y偏移的角度值
    pos = val["pos"]
    val["xyRot"] = math.degrees(math.atan2(pos[1], pos[0]))
    val["xyLen"] = math.sqrt(pos[0] ** 2 + pos[1] ** 2)
    val["zyRot"] = math.degrees(math.atan2(pos[1], pos[2]))
    val["zyLen"] = math.sqrt(pos[2] ** 2 + pos[1] ** 2)
    
def GetRidePos(seatId):
    """获取载具乘骑的位置"""
    # 如果seatId不对，则设置为副驾驶位置
    return _RiderConfig.get(seatId, _RiderConfig[1])
# endregion


# region 不常修改的内容

# 提示信息文字
_TipsDict = {
    # 能源添加相关
    1: "能源已满，不用再补充了",
    2: "已选择材料可添加满能源,不用再一键选择了",
    3: "已选择全部已有材料",
    # 救援相关
    12: "附近没有载具，请先到载具附近，再进行救援",
    13: "您站的位置太危险了、或者太窄了，不能把载具救援到这里，请换个地方",
    14: "载具上仍有乘客，无法救援",
}
def GetTips(tipsId):
    return _TipsDict.get(tipsId, "")

# extraData的key
class ExtraDataKeyEnum:
    InitState = "{}_init_state".format(ModNameSpace)
    """初始状态"""
    AttrData = "{}_attr_data".format(ModNameSpace)
    """属性值"""
    RemoldData = "{}_remold_data".format(ModNameSpace)
    """改造数据"""

# 射线检测应该忽略的方块
_RayIngoreBlocks = (
    "minecraft:water",
    "minecraft:flowing_water",
    "minecraft:lava",
    "minecraft:flowing_lava",
)
def IsRayIngoreBlock(blockName):
    """是否是射线检测应该忽略的方块"""
    return blockName in _RayIngoreBlocks
# endregion
