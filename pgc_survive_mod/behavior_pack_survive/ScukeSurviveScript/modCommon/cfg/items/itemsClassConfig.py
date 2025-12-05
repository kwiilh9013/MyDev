# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modServer.blocks.blockLandmine import BlockLandmine
from ScukeSurviveScript.modServer.blocks.blockBarricade import BlockBarricade
from ScukeSurviveScript.modServer.blocks.blockTombStone import BlockTombStone
from ScukeSurviveScript.modServer.blocks.blockTrap import BlockTrap
from ScukeSurviveScript.modServer.blocks.blockTimeBomb import BlockTimeBomb
from ScukeSurviveScript.modServer.blocks.blockC4Bomb import BlockC4Bomb


"""
物品方块 对象映射表
为避免循环引用，单独一个表
"""


ItemsNameEnum = itemsConfig.ItemsNameEnum

_ItemsClassDict = {
    # 地雷
    ItemsNameEnum.Landmine: BlockLandmine,
    ItemsNameEnum.BarricadeWood: BlockBarricade,
    ItemsNameEnum.BarricadeIron: BlockBarricade,
    ItemsNameEnum.Trap: BlockTrap,
    ItemsNameEnum.TimeBomb1: BlockTimeBomb,
    ItemsNameEnum.TimeBomb2: BlockTimeBomb,
    ItemsNameEnum.TimeBomb3: BlockTimeBomb,
    ItemsNameEnum.C4Bomb1: BlockC4Bomb,
    ItemsNameEnum.C4Bomb2: BlockC4Bomb,
    ItemsNameEnum.C4Bomb3: BlockC4Bomb,
    ItemsNameEnum.TombStone: BlockTombStone,
}


def GetItemsClass(itemName):
    """获取物品方块类"""
    return _ItemsClassDict.get(itemName)
