# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modServer.electric.electricDynamo import ElectricDynamo
from ScukeSurviveScript.modServer.electric.electricPrinter import ElectricPrinter
from ScukeSurviveScript.modServer.electric.electricSpikeTrap import ElectricSpikeTrap
from ScukeSurviveScript.modServer.electric.electicPhotoetching import ElectricPhotoetching
from ScukeSurviveScript.modServer.electric.electricMachinery import ElectricMachinery
from ScukeSurviveScript.modServer.electric.electricHeaterSmall import ElectricHeaterSmall
from ScukeSurviveScript.modServer.electric.electricHeaterLarge import ElectricHeaterLarge
from ScukeSurviveScript.modCommon.defines import electricEnum


"""
物品方块 对象映射表
为避免循环引用，单独一个表
"""


ElectricEnum = electricEnum.ElectricEnum
_ElectricClassDict = {
    ElectricEnum.DynamoSmall: ElectricDynamo,
    ElectricEnum.DynamoMiddle: ElectricDynamo,
    ElectricEnum.DynamoLarge: ElectricDynamo,
    ElectricEnum.Printer: ElectricPrinter,
    ElectricEnum.Photoetching: ElectricPhotoetching,
    ElectricEnum.SpikeTrap: ElectricSpikeTrap,
    ElectricEnum.Machinery: ElectricMachinery,
    ElectricEnum.HeaterSmall: ElectricHeaterSmall,
    ElectricEnum.HeaterLarge: ElectricHeaterLarge,
}
def GetElectricClass(itemName):
    """获取物品方块类"""
    return _ElectricClassDict.get(itemName)