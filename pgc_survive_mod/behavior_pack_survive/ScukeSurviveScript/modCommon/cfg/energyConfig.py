# -*- encoding: utf-8 -*-
"""
能源燃料配置表
"""


# 可增加能源的物品数据
_AddEnergyItems = {
	"minecraft:coal": 5,
	"minecraft:rotten_flesh": 5,
	"minecraft:raw_iron": 10,
	"minecraft:lapis_lazuli": 10,
	"minecraft:iron_ingot": 12,
	"minecraft:raw_copper": 10,
	"minecraft:copper_ingot": 12,
	"scuke_survive:raw_lead": 10,
	"scuke_survive:ingot_lead": 12,
	"scuke_survive:raw_lithium": 15,
	"scuke_survive:ingot_lithium": 17,
	"minecraft:raw_gold": 15,
	"minecraft:gold_ingot": 17,
	"scuke_survive:raw_rare_earth": 20,
	"scuke_survive:ingot_rare_earth": 22,
	"minecraft:blaze_rod": 22,
	"minecraft:redstone": 20,
	"scuke_survive:raw_yttrium": 25,
	"scuke_survive:ingot_yttrium": 27,
	"minecraft:oak_log": 5,
	"minecraft:spruce_log": 5,
	"minecraft:birch_log": 5,
	"minecraft:jungle_log": 5,
	"minecraft:acacia_log": 5,
	"minecraft:dark_oak_log": 5,
	"minecraft:mangrove_log": 5,
	"minecraft:cherry_log": 5,
	"minecraft:crimson_stem": 5,
	"minecraft:warped_stem": 5,
	"minecraft:stripped_spruce_log": 5,
	"minecraft:stripped_birch_log": 5,
	"minecraft:stripped_jungle_log": 5,
	"minecraft:stripped_acacia_log": 5,
	"minecraft:stripped_dark_oak_log": 5,
	"minecraft:stripped_oak_log": 5,
	"minecraft:stripped_mangrove_log": 5,
	"minecraft:stripped_cherry_log": 5,
	"minecraft:stripped_crimson_stem": 5,
	"minecraft:stripped_warped_stem": 5,
	"minecraft:bamboo_block": 5,
	"minecraft:stripped_bamboo_block": 5,
	"minecraft:white_wool": 5,
	"minecraft:light_gray_wool": 5,
	"minecraft:gray_wool": 5,
	"minecraft:black_wool": 5,
	"minecraft:brown_wool": 5,
	"minecraft:red_wool": 5,
	"minecraft:orange_wool": 5,
	"minecraft:yellow_wool": 5,
	"minecraft:lime_wool": 5,
	"minecraft:green_wool": 5,
	"minecraft:cyan_wool": 5,
	"minecraft:light_blue_wool": 5,
	"minecraft:blue_wool": 5,
	"minecraft:purple_wool": 5,
	"minecraft:magenta_wool": 5,
	"minecraft:pink_wool": 5,
}
_uiItemsColor = {
	"materialTextColor": (0.698, 1.0, 0.91),
	"materialNotPlayerTextColor": (0.8, 0.8, 0.8),
	"materialSpriteColor": (0.23, 0.448, 0.409),
	"materialNotPlayerSpriteColor": (0.109, 0.124, 0.121),
}
def GetAddEnergyMaterialNum(itemName):
	"""获取材料增加的能源值"""
	return _AddEnergyItems.get(itemName, 0)

