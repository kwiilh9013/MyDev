# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.electric.electricRecipeConfig import GetAllElectricItemRecipes


"""
拆解台配方 配置
"""


# region 仅拆解配方
_DisassembleRecipes = {
	"scuke_survive:mat_clothes": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:mat_clothes"},
		"key": {
			"A": { "item": "minecraft:white_wool","count":2},
		}
	},
	"scuke_survive:mat_sand_hammer": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:mat_sand_hammer"},
		"key": {
			"A": { "item": "scuke_survive:mat_plastic_board","count":4},
		}
	},
	"scuke_survive:mat_carrot_knife": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:mat_carrot_knife"},
		"key": {
			"A": { "item": "scuke_survive:mat_plastic_board","count":4},
		}
	},
	"scuke_survive:mat_duck": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:mat_duck"},
		"key": {
			"A": { "item": "scuke_survive:mat_plastic_board","count":9},
		}
	},
	"scuke_survive:ore_lead": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_lead"},
		"key": {
			"A": { "item": "scuke_survive:raw_lead","count":1},
		}
	},
	"scuke_survive:ore_lead_deepslate": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_lead"},
		"key": {
			"A": { "item": "scuke_survive:raw_lead","count":1},
		}
	},
	"scuke_survive:metal_block_lead": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:metal_block_lead"},
		"key": {
			"A": { "item": "scuke_survive:ingot_lead","count":9},
		}
	},
	"scuke_survive:mat_can": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:mat_can"},
		"key": {
			"A": { "item": "minecraft:raw_iron","count":6},
		}
	},
	"scuke_survive:mat_drink_can": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:mat_drink_can"},
		"key": {
			"A": { "item": "minecraft:raw_iron","count":9},
		}
	},
	"scuke_survive:mat_frog": {
		"pattern": ["AB"],
		"result": {"item": "scuke_survive:mat_frog"},
		"key": {
			"A": { "item": "minecraft:raw_iron","count":4},
			"B":{"item": "scuke_survive:raw_lead","count":6},
		}
	},
	"scuke_survive:mat_spinning_top": {
		"pattern": ["ABC"],
		"result": {"item": "scuke_survive:mat_spinning_top"},
		"key": {
			"A": { "item": "minecraft:raw_iron","count":4},
			"B":{"item": "scuke_survive:raw_lead","count":6},
			"C":{"item": "scuke_survive:mat_plastic_board","count":2},
		}
	},
	"scuke_survive:ore_lithium": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_lithium"},
		"key": {
			"A": { "item": "scuke_survive:raw_lithium","count":1},
		}
	},
	"scuke_survive:ore_lithium_deepslate": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_lithium"},
		"key": {
			"A": { "item": "scuke_survive:raw_lithium","count":1},
		}
	},
	"scuke_survive:metal_block_lithium": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:metal_block_lithium"},
		"key": {
			"A": { "item": "scuke_survive:ingot_lithium","count":9},
		}
	},
	"scuke_survive:mat_phone1": {
		"pattern": ["ABC","DE"],
		"result": {"item": "scuke_survive:mat_phone1"},
		"key": {
			"A": { "item": "minecraft:raw_copper","count":4},
			"B": { "item": "scuke_survive:raw_lithium","count":5},
			"C": { "item": "scuke_survive:mat_plastic_board","count":4},
			"D": { "item": "minecraft:raw_iron","count":2},
			"E": { "item": "minecraft:redstone","count":1},
		}
	},
	"scuke_survive:mat_game_machine": {
		"pattern": ["ABC","D"],
		"result": {"item": "scuke_survive:mat_game_machine"},
		"key": {
			"A": { "item": "minecraft:raw_copper","count":6},
			"B": { "item": "scuke_survive:raw_lithium","count":6},
			"C": { "item": "scuke_survive:mat_plastic_board","count":4},
			"D": { "item": "minecraft:redstone","count":1},
		}
	},
	"scuke_survive:mat_read_machine": {
		"pattern": ["ABC","D"],
		"result": {"item": "scuke_survive:mat_read_machine"},
		"key": {
			"A": { "item": "minecraft:raw_copper","count":6},
			"B": { "item": "scuke_survive:raw_lithium","count":4},
			"C": { "item": "scuke_survive:mat_plastic_board","count":9},
			"D": { "item": "minecraft:redstone","count":1},
		}
	},
	"scuke_survive:ore_rare_earth": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_rare_earth"},
		"key": {
			"A": { "item": "scuke_survive:raw_rare_earth","count":1},
		}
	},
	"scuke_survive:ore_rare_earth_deepslate": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_rare_earth"},
		"key": {
			"A": { "item": "scuke_survive:raw_rare_earth","count":1},
		}
	},
	"scuke_survive:metal_block_rare_earth": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:metal_block_rare_earth"},
		"key": {
			"A": { "item": "scuke_survive:ingot_rare_earth","count":9},
		}
	},
	"scuke_survive:mat_phone_watch": {
		"pattern": ["ABC","DE"],
		"result": {"item": "scuke_survive:mat_phone_watch"},
		"key": {
			"A": { "item": "minecraft:raw_copper","count":6},
			"B": { "item": "scuke_survive:raw_lithium","count":4},
			"C": { "item": "scuke_survive:mat_plastic_board","count":9},
			"D": { "item": "scuke_survive:raw_rare_earth","count":2},
			"E": { "item": "minecraft:redstone","count":1},
		}
	},
	"scuke_survive:ore_yttrium": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:ore_yttrium"},
		"key": {
			"A": { "item": "scuke_survive:raw_yttrium","count":1},
		}
	},
	"scuke_survive:metal_block_yttrium": {
		"pattern": ["A"],
		"result": {"item": "scuke_survive:metal_block_yttrium"},
		"key": {
			"A": { "item": "scuke_survive:ingot_yttrium","count":9},
		}
	},
	"scuke_survive:mat_phone3": {
		"pattern": ["ABC","DEF"],
		"result": {"item": "scuke_survive:mat_phone3"},
		"key": {
			"A": { "item": "minecraft:raw_copper","count":6},
			"B": { "item": "scuke_survive:raw_lithium","count":4},
			"C": { "item": "scuke_survive:mat_plastic_board","count":9},
			"D": { "item": "scuke_survive:raw_rare_earth","count":2},
			"E": { "item": "scuke_survive:raw_yttrium","count":2},
			"F": { "item": "minecraft:redstone","count":1},
		}
	},
	"scuke_survive:mat_phone2": {
		"pattern": ["ABC","DEF","G"],
		"result": {"item": "scuke_survive:mat_phone2"},
		"key": {
			"A": { "item": "minecraft:raw_copper","count":6},
			"B": { "item": "scuke_survive:raw_lithium","count":4},
			"C": { "item": "scuke_survive:mat_plastic_board","count":9},
			"D": { "item": "scuke_survive:raw_rare_earth","count":2},
			"E": { "item": "scuke_survive:raw_yttrium","count":2},
			"F": { "item": "minecraft:raw_iron","count":2},
			"G": { "item": "minecraft:redstone","count":1},
		}
	},
}
# endregion


# region 所有配方


def GetDisassembleRecipes():
	"""
	获取所有拆解配方
	
	格式={ itemName: {recipe1}, {recipe2}, ... }
	"""
	# 打印机、光刻机的配方
	DisassembleRecipes = {}
	DisassembleRecipesList = ['A','B','C','D','E','F','G','H','I']
	DisassembleRecipesDic = {1:['A'],2:['AB'],3:['ABC'],4:['ABC','D'],5:['ABC','DE'],6:['ABC','DEF'],7:['ABC','DEF','G'],8:['ABC','DEF','GH'],9:['ABC','DEF','GHI']}
	electricRecipes = GetAllElectricItemRecipes()
	for itemName in electricRecipes:
		# 每一个配方字典进行一次循环
		key = {}
		pattern = []
		result = [{"item": itemName}]
		recipeInputList = electricRecipes[itemName]['input']
		RecipesInputListCount = len(recipeInputList)
		# "input": [
        #     {"newItemName": "minecraft:iron_ingot", "count": 10},
        # ]
		#判断是否配方种类数量是否为0到9
		if RecipesInputListCount in DisassembleRecipesDic:
			pattern = DisassembleRecipesDic[RecipesInputListCount]
		else:
			print itemName+'物品配方种类数量有误'
		# 对于配方中input每一个物品字典进行处理
		i = 0
		for keyValue in DisassembleRecipesList[:RecipesInputListCount]:
			itemDic = recipeInputList[i]
			key[keyValue] = {"item":itemDic['newItemName'],"count":itemDic['count']}
			i+=1
		DisassembleRecipes[itemName] = {
			"pattern": pattern,
			"result": result,
			"key": key
		}
		# 合并打印机与仅拆解的物品字典
		DisassembleRecipes.update(_DisassembleRecipes)
		# recipeList = [{
		# 		"pattern": ["ABA"],
		# 		"result": [{"item": "scuke_survive:mat_phone1"],
		# 		"key": {
		# 			"A": { "item": "scuke_survive:mat_chip_small" },
		# 			"B": { "item": "scuke_survive:mat_plastic_board" },
		# 		}
		# 	}]
	return DisassembleRecipes
# endregion