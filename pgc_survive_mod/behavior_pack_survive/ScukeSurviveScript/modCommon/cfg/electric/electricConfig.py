# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.energyConfig import GetAddEnergyMaterialNum as GetAddEnergyMaterialNumByEnergyConfig
from ScukeSurviveScript.modCommon.cfg import buffConfig
from ScukeSurviveScript.modCommon.defines.electricEnum import ElectricEnum


"""
道具物品 配置表
"""


# region 能源消耗计算
# 扣能源逻辑的执行间隔，单位秒
DeductEnergyCD = 5

# 消耗能源的系数
DeductEnergyRate = 0.1

# 根据功率计算能源消耗的公式
def GetEnergyConsumption(kw, cd=DeductEnergyCD):
    """获取能源消耗
    :param kw: 功率
    :param cd: 扣能源逻辑的执行间隔，单位秒
    """
    # 能源消耗 = 功率 * 系数 * 时间
    energy = kw * cd * DeductEnergyRate
    return energy

# endregion


# region 电器属性
_ElectricDict = {
    ElectricEnum.DynamoSmall: {
        # 功率
        "kw": 200,
        # 范围/半径
        "radius": 12,
        # 最大能源值
        "max_energy": 2000,
    },
    ElectricEnum.DynamoMiddle: {
        "kw": 400,
        "radius": 24,
        "max_energy": 6000,
    },
    ElectricEnum.DynamoLarge: {
        "kw": 800,
        "radius": 36,
        "max_energy": 12000,
    },

    ElectricEnum.HeaterSmall: {
        "kw": 10,
        "radius": 10,
        # 每多少秒扣除一次能源
        "kw_time":6,
        # 添加的buff
        "add_buff": [
            # buffId, 持续时间，等级，是否显示粒子
            (buffConfig.BuffEnum.ColdResistance, 20, 1, True)
        ],
    },
    ElectricEnum.HeaterLarge: {
        "kw": 20,
        "radius": 20,
        "kw_time": 6,
        "add_buff": [
            (buffConfig.BuffEnum.ColdResistance, 20, 2, True)
        ],
    },
    ElectricEnum.RefrigerationSmall: {
        "kw": 10,
        "radius": 12,
        "add_buff": [
            (buffConfig.BuffEnum.HotResistance, 20, 1, True)
        ],
    },
    ElectricEnum.RefrigerationLarge: {
        "kw": 20,
        "radius": 24,
        "add_buff": [
            (buffConfig.BuffEnum.HotResistance, 20, 2, True)
        ],
    },

    #地刺
    ElectricEnum.SpikeTrap:{
        "kw":30,
        "hurt_cd":0.5,
        "hurt_damage":4,
        "hurt_knocked":True
    },
    
    ElectricEnum.Printer: {
        "kw": 100,
    },
    ElectricEnum.Photoetching: {
        "kw": 300,
    },
    ElectricEnum.Machinery: {
        "kw": 200,
    },
    
}
def GetElectricConfig(blockName):
    """获取电器的配置信息"""
    return _ElectricDict.get(blockName)


def GetAddEnergyMaterialNum(itemName):
    """获取材料增加的能源值"""
    # 复用载具的染料数据
    return GetAddEnergyMaterialNumByEnergyConfig(itemName)
# endregion


# region UI相关

# 点击一次添加的物品数量，用于发电机选择材料时
SelectMaterialCount = 1

# 发电机启动后的进度图
NormalBarTexture1 = "textures/ui/scuke_survive/progress_bar/bar_battery03"
NormalBarTexture2 = "textures/ui/scuke_survive/progress_bar/bar_battery05"
WorkBarTexture1 = "textures/ui/scuke_survive/progress_bar/bar_battery01"
WorkBarTexture2 = "textures/ui/scuke_survive/progress_bar/bar_battery02"

# 供电状态改变的文字、背景图颜色
WorkTextColor1 = (0.91, 0.91, 0.91)
WorkTextColor2 = (0.03, 0.21, 0.31)
WorkTextBgColor1 = (0.81, 0.28, 0.28)
WorkTextBgColor2 = (1, 0.97, 0.3)

# 灰色文字
GrayTextColor = (0.7, 0.7, 0.7)
# 正常文字
NormalTextColor = (0.5, 1.0, 0.92)
# 工作时的文字
WorkTextColor = (0.99, 1.0, 0.64)

# 显示范围的按钮图
ShowRangeBtnTextureOff = "textures/ui/scuke_survive/common/border04"
ShowRangeBtnTextureOn = "textures/ui/scuke_survive/common/border05"

# 打印机选中时的文字颜色
PrinterSelectTextColor = (0.5, 0.8, 0.72)
PrinterNormalTextColor = (0, 0, 0)

# endregion
# 光刻机选中时的文字颜色
PhotoetchingSelectTextColor = (0.5, 0.8, 0.72)
PhotoetchingNormalTextColor = (0, 0, 0)

# endregion

# region 方块数据存储参数
# blockEntityData存储数据的key
BlockEntityDataKey = "{}_electric_entity_data".format(modConfig.ModNameSpace)
# endregion
