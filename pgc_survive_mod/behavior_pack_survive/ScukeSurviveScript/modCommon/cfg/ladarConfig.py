# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.npcEnum import NPCEnum
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.cfg.molangConfig import QueryEnum


"""
雷达配置表
"""


# region 参数

# 雷达道具id


LadarItemName = "scuke_survive:items_ladar"

# 位置刷新频率，秒
LadarRefreshTime = 0.5
# 显示的位置数量上限（除发动机外），如果要修改上限，则同时修改模型、动画、注册molang
TargetMaxCount = 3

# 雷达扫描范围，格
ScanRangeSqrt = 1000 ** 2
# 扫描坐标点的频率
ScanPosTime = 15
# 地图缩放比例：大概是 10(模型长度) 比 128(小地图和模型同样大小下，对应世界的长度（大概值）)
MapScales = 0.01

# 地图最大尺寸，单位为动画中的像素单位
MapMaxX = 9.5
MapMaxY = 11.5

# 地图实际长宽最大值，用于计算icon缩放
MapActualLength = max(MapMaxX / MapScales, MapMaxY / MapScales)
# icon缩放的scale范围
MapIconScaleRange = (0.5, 1)
# 地图缩放计算的判定长度（转换为小数，从而不计算除法）(5008是发动机和破损发动机的距离)
MapScaleDecisionLenghtRate = 1 / ((5008 - MapActualLength) / (1 - MapIconScaleRange[0]))

# 死机CD，秒
OutOfOrderCD = 30
# 死机概率，每[LadarRefreshTime]触发一次
OutOfOrderProb = 0.1
# 恢复概率
OutOfOrderRecoverProb = 0.25

# 发动机的到达距离判断
EngineArriveDistSqrt = 100 ** 2

# endregion


# region 目标类型
# 这些枚举的值一旦确定不能再修改，否则会影响存储的数据
class TargetTypeEnum:
    """雷达目标类型枚举"""
    Default = 1
    """默认"""
    NormalCreeper = 2
    """普通苦力怕"""
    GoldCreeper = 3
    """黄金苦力怕"""
    TreasureBox = 4
    """宝箱"""
    Boss = 5
    """boss"""

    # 发动机枚举id，需给其他类型预留空间
    Engine1 = 101
    """发动机1"""
    Engine2 = 102
    """发动机2"""
    Engine3 = 103
    """发动机3"""


# 实体engineTypeStr对应的目标类型
_EngineTypeToTargetTypeDict = {
    # # 普通苦力怕
    # "minecraft:creeper": TargetTypeEnum.NormalCreeper,
    # 黄金苦力怕
    # NPCEnum.GoldenCreeper: TargetTypeEnum.GoldCreeper,
    # 原版boss
    # "minecraft:ender_dragon": TargetTypeEnum.Boss,
    # "minecraft:wither": TargetTypeEnum.Boss,
    # 惊变boss
    # MonsterEnum.ZombieGiant: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieSarcoma: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieFlyingLava: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieJockerKing: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieGiantKing: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieGiantSarcoma: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieBigGiant: TargetTypeEnum.Boss,
    # MonsterEnum.ZombieBlackVenom: TargetTypeEnum.Boss,
}
def GetTargetType(engineTypeStr):
    """获取目标类型，获取不到表示不监听该实体"""
    return _EngineTypeToTargetTypeDict.get(engineTypeStr)
# endregion


# region 发动机
_EngineConfig = [
    {"pos": (5008, 64, 0), "molang": (QueryEnum.LadarEngine1DistX, QueryEnum.LadarEngine1DistZ),},
    {"pos": (0, 64, -5008), "molang": (QueryEnum.LadarEngine2DistX, QueryEnum.LadarEngine2DistZ),},
    {"pos": (0, 64, 5008), "molang": (QueryEnum.LadarEngine3DistX, QueryEnum.LadarEngine3DistZ),},
]

def GetEngineCfg(indexEnum):
    """获取发动机配置, indexEnum -> TargetTypeEnum"""
    index = indexEnum - TargetTypeEnum.Engine1
    if index < 0 or index >= len(_EngineConfig):
        return None
    return _EngineConfig[index]

def IsEngineEnum(targetEnum):
    """是否是发动机枚举"""
    if targetEnum >= TargetTypeEnum.Engine1:
        return True
    return False

_EngineKeyList = []
def GetEngineKeyList():
    """获取发动机key列表, key=(dim, pos, type)"""
    if not _EngineKeyList:
        for i in xrange(len(_EngineConfig)):
            cfg = _EngineConfig[i]
            # (dim, pos, type)
            key = (0, cfg["pos"], TargetTypeEnum.Engine1 + i)
            _EngineKeyList.append(key)
    return _EngineKeyList
# endregion


# region 音效
# 目标类型的音效
_TargetSounds = {
    # TargetTypeEnum.NormalCreeper: {"sound": "scuke_survive.ladar.creeper", },
    TargetTypeEnum.GoldCreeper: {"sound": "scuke_survive.ladar.gold_creeper", },
    TargetTypeEnum.TreasureBox: {"sound": "scuke_survive.ladar.chest", },
    TargetTypeEnum.Boss: {"sound": "scuke_survive.ladar.boss", },
    # 默认的音效
    TargetTypeEnum.Default: {"sound": "scuke_survive.ladar.creeper",},
}
def GetTargetSound(targetType):
    """获取音效数据"""
    return _TargetSounds.get(targetType, _TargetSounds[TargetTypeEnum.Default])


# 音效播放逻辑：越近，音效播放频率越快
_TargetSoundPlayRules = [
    {"mht_dist": (MapActualLength * 0.1) ** 2, "cd": 1},
    {"mht_dist": (MapActualLength * 0.5) ** 2, "cd": 2},
    # 最后一个是默认的配置
    {"mht_dist": MapActualLength ** 2, "cd": 5},
]
def GetTargetSoundPlayRule(dist, targetType):
    """获取音效播放规则"""
    if dist is not None:
        for rule in _TargetSoundPlayRules:
            if dist <= rule["mht_dist"]:
                # 根据目标获取音效类型
                rule["sound"] = GetTargetSound(targetType)
                return rule

    rule = _TargetSoundPlayRules[-1]
    rule["sound"] = GetTargetSound(targetType)
    return rule
# endregion
