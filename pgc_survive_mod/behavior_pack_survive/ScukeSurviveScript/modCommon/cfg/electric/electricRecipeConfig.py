# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.defines.electricEnum import ElectricEnum


"""
电器配方表
打印机、光刻机、机械工作台
"""


# region 工作台的合成物品列表
_DollMolangDict = {
    "variable.is_enchanted": 0,
    "variable.has_trim": 0,
    "variable.working_state": 0,
    "variable.show_range":0,
    "variable.correct_pos":1
}


_WorkbenchCraftDict = {
    ElectricEnum.Photoetching: [
        {
            "item": {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
        },
        {
            "item": {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
        },
        {
            "item": {"newItemName": "scuke_survive:mat_chip_large", "count": 1},
        },
    ],
    ElectricEnum.Machinery:{
        # 维修
        "repair":{
        "scuke_survive:gun_pistol1":{
            # 显示模型
                "entity_identifier": "scuke_survive:gun_entity_pistol1",
                "rotation_axis": (1, 1, 0),
                "molang_dict": _DollMolangDict,
        },
        "scuke_survive:gun_smg1":{
                "entity_identifier": "scuke_survive:gun_entity_smg1",
                "rotation_axis": (1, 1, 0),
                "molang_dict": _DollMolangDict,
        },
        "scuke_survive:gun_shotgun1":{
                "entity_identifier": "scuke_survive:gun_entity_shotgun1",
                "rotation_axis": (1, 1, 0),
                "molang_dict": _DollMolangDict,
        },
        "scuke_survive:gun_rifle1_s1":{
                "entity_identifier": "scuke_survive:gun_entity_rifle1_s1",
                "rotation_axis": (1, 1, 0),
                "molang_dict": _DollMolangDict,
        },
        "scuke_survive:gun_bazooka1_s1":{
                "entity_identifier": "scuke_survive:gun_entity_bazooka1_s1",
                "rotation_axis": (1, 1, 0),
                "molang_dict": _DollMolangDict,
        },
        'scuke_survive:gun_lmg1_s1': {
            'entity_identifier': 'scuke_survive:gun_entity_hmg1_s1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_sniper1_s1': {
            'entity_identifier': 'scuke_survive:gun_entity_sniper1_s1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_hmg1_s1': {
            'entity_identifier': 'scuke_survive:gun_entity_hmg1_s1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_pistol1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_pistol1_s1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_smg1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_smg1_s1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_shotgun1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_shotgun1_s1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_sniper1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_sniper1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_bazooka1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_bazooka1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_lmg1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_lmg1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_rifle1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_rifle1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_hmg1_s2': {
            'entity_identifier': 'scuke_survive:gun_entity_hmg1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_pistol1_s3': {
            'entity_identifier': 'scuke_survive:gun_entity_pistol1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_smg1_s3': {
            'entity_identifier': 'scuke_survive:gun_entity_smg1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_shotgun1_s3': {
            'entity_identifier': 'scuke_survive:gun_entity_shotgun1_s2',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_bazooka1': {
            'entity_identifier': 'scuke_survive:gun_entity_bazooka1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_lmg1': {
            'entity_identifier': 'scuke_survive:gun_entity_lmg1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_rifle1': {
            'entity_identifier': 'scuke_survive:gun_entity_rifle1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_hmg1': {
            'entity_identifier': 'scuke_survive:gun_entity_hmg1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:gun_sniper1': {
            'entity_identifier': 'scuke_survive:gun_entity_sniper1',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_axe_red': {
            'entity_identifier': 'scuke_survive:axe_red_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_axe': {
            'entity_identifier': 'scuke_survive:axe_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_axe_golden': {
            'entity_identifier': 'scuke_survive:axe_golden_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_baseball_bat': {
            'entity_identifier': 'scuke_survive:baseball_bat_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_baseball_bat_m': {
            'entity_identifier': 'scuke_survive:baseball_bat_m_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_baseball_bat_golden': {
            'entity_identifier': 'scuke_survive:baseball_bat_golden_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_chainsaw_old': {
            'entity_identifier': 'scuke_survive:chainsaw_old_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_chainsaw': {
            'entity_identifier': 'scuke_survive:chainsaw_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_chainsaw_golden': {
            'entity_identifier': 'scuke_survive:chainsaw_golden_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow01_helmet': {
            'entity_identifier': 'scuke_survive:entity_snow01_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow01_chest': {
            'entity_identifier': 'scuke_survive:entity_snow01_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow01_legs': {
            'entity_identifier': 'scuke_survive:entity_snow01_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow01_boots': {
            'entity_identifier': 'scuke_survive:entity_snow01_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow02_helmet': {
            'entity_identifier': 'scuke_survive:entity_snow02_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow02_chest': {
            'entity_identifier': 'scuke_survive:entity_snow02_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow02_legs': {
            'entity_identifier': 'scuke_survive:entity_snow02_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_snow02_boots': {
            'entity_identifier': 'scuke_survive:entity_snow02_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_safety_helmet': {
            'entity_identifier': 'scuke_survive:entity_safety_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_safety_chest': {
            'entity_identifier': 'scuke_survive:entity_safety_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_safety_legs': {
            'entity_identifier': 'scuke_survive:entity_safety_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_safety_boots': {
            'entity_identifier': 'scuke_survive:entity_safety_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_red_rescue_helmet': {
            'entity_identifier': 'scuke_survive:entity_red_rescue_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_red_rescue_chest': {
            'entity_identifier': 'scuke_survive:entity_red_rescue_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_red_rescue_legs': {
            'entity_identifier': 'scuke_survive:entity_red_rescue_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_red_rescue_boots': {
            'entity_identifier': 'scuke_survive:entity_red_rescue_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_black_rescue_helmet': {
            'entity_identifier': 'scuke_survive:entity_black_rescue_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_black_rescue_chest': {
            'entity_identifier': 'scuke_survive:entity_black_rescue_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_black_rescue_legs': {
            'entity_identifier': 'scuke_survive:entity_black_rescue_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_black_rescue_boots': {
            'entity_identifier': 'scuke_survive:entity_black_rescue_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor01_helmet': {
            'entity_identifier': 'scuke_survive:entity_armor01_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor01_chest': {
            'entity_identifier': 'scuke_survive:entity_armor01_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor01_legs': {
            'entity_identifier': 'scuke_survive:entity_armor01_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor01_boots': {
            'entity_identifier': 'scuke_survive:entity_armor01_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor02_helmet': {
            'entity_identifier': 'scuke_survive:entity_armor02_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor02_chest': {
            'entity_identifier': 'scuke_survive:entity_armor02_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor02_legs': {
            'entity_identifier': 'scuke_survive:entity_armor02_legs',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_armor02_boots': {
            'entity_identifier': 'scuke_survive:entity_armor02_boots',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_soviet_tig_helmet_black': {
            'entity_identifier': 'scuke_survive:entity_soviet_tig_helmet_black',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_soviet_tig_helmet_silver': {
            'entity_identifier': 'scuke_survive:entity_soviet_tig_helmet_silver',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_soviet_tig_helmet_gold': {
            'entity_identifier': 'scuke_survive:entity_soviet_tig_helmet_gold',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_pan_copper': {
            'entity_identifier': 'scuke_survive:pan_copper_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_pan': {
            'entity_identifier': 'scuke_survive:pan_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:melee_pan_golden': {
            'entity_identifier': 'scuke_survive:pan_golden_entity',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },

        'scuke_survive:armor_green_helmet': {
            'entity_identifier': 'scuke_survive:entity_green_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_tattered_helmet': {
            'entity_identifier': 'scuke_survive:entity_tattered_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_tattered_chest': {
            'entity_identifier': 'scuke_survive:entity_tattered_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_red_mask_helmet': {
            'entity_identifier': 'scuke_survive:entity_red_mask_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_red_helmet': {
            'entity_identifier': 'scuke_survive:entity_red_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_military_helmet': {
            'entity_identifier': 'scuke_survive:entity_military_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_military_chest': {
            'entity_identifier': 'scuke_survive:entity_military_chest',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_skull_helmet': {
            'entity_identifier': 'scuke_survive:entity_skull_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_skull_mask_helmet': {
            'entity_identifier': 'scuke_survive:entity_skull_mask_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        'scuke_survive:armor_skull_hood_helmet': {
            'entity_identifier': 'scuke_survive:entity_skull_hood_helmet',
            'rotation_axis': (1,
            1,
            0),
            'molang_dict': _DollMolangDict
        },
        },
        # 强化
        "enhancement":{

        }
    },
    ElectricEnum.Printer: {
        # region 分页
        "tabs": ["gun", "bullet", "item", "melee_weapons", "armor", "carpart"],
        # endregion
        # region 枪械
        "gun": [
            {
                # 合成物品
                "item": {"newItemName": "scuke_survive:gun_pistol1", "count": 1},
                # 显示模型，不设置则显示item
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_pistol1",
			        "rotation_axis": (1, 1, 0),
                    "scale": 1.0,
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_smg1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_smg1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_shotgun1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_shotgun1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_rifle1_s1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_rifle1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_bazooka1_s1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_bazooka1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_lmg1_s1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_hmg1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_sniper1_s1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_sniper1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_hmg1_s1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_hmg1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_pistol1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_pistol1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_smg1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_smg1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_shotgun1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_shotgun1_s1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_sniper1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_sniper1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_bazooka1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_bazooka1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_lmg1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_lmg1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_rifle1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_rifle1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_hmg1_s2", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_hmg1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_pistol1_s3", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_pistol1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_smg1_s3", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_smg1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_shotgun1_s3", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_shotgun1_s2",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_bazooka1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_bazooka1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_lmg1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_lmg1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_rifle1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_rifle1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_hmg1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_hmg1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:gun_sniper1", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:gun_entity_sniper1",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
        ],
        # endregion
        # region 子弹
        "bullet": [
            {
                "item": {"newItemName": "scuke_survive:clip_normal", "count": 16},
            },
            {
                "item": {"newItemName": "scuke_survive:clip_advanced", "count": 16},
            },
            {
                "item": {"newItemName": "scuke_survive:clip_energy", "count": 16},
            },
            {
                "item": {"newItemName": "scuke_survive:clip_explosion", "count": 16},
            },
        ],
        # endregion
        # region 物品
        "item": [
            #防御工事物品
            {
                "item": {"newItemName": "scuke_survive:electric_dynamo_middle", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_dynamo_middle_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:electric_dynamo_large", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_dynamo_large_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:electric_machinery", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_machinery_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:electric_photoetching", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_photoetching_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:electric_heater_small", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_heater_small_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:electric_heater_large", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_heater_large_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:time_bomb1", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:c4_bomb1", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:c4_detonator", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:electric_spike_trap", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:electric_spike_trap_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },


            {
                "item": {"newItemName": "scuke_survive:items_barricade_wood", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_barricade_wood_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:items_trap", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_trap_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:items_landmine", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_landmine_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:car_repair", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:car_repair",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:items_wirecloth", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:items_barricade_iron", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_barricade_iron_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:items_grenade_small", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_grenade_small_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:items_grenade_middle", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_grenade_middle_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:items_grenade_large", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_grenade_large_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            # 雷达
            {
                "item": {"newItemName": "scuke_survive:items_ladar", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:items_ladar",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:build_struct", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:car_rescue", "count": 1},
            },
            #箱子
            {
                "item": {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:chest_storage_blue", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:chest_storage_orange", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:chest_storage_red", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:chest_military", "count": 1},
            },
            #汽油桶
            {
                "item": {"newItemName": "scuke_survive:items_oil_drum_small", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:items_oil_drum_large", "count": 1},
            },
        ],
        # endregion
        # region 近战武器
        "melee_weapons":[
            {
                "item": {"newItemName": "scuke_survive:melee_axe_red", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:axe_red_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_axe", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:axe_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_axe_golden", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:axe_golden_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_baseball_bat", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:baseball_bat_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_baseball_bat_m", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:baseball_bat_m_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_baseball_bat_golden", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:baseball_bat_golden_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_chainsaw_old", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:chainsaw_old_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_chainsaw", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:chainsaw_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_chainsaw_golden", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:chainsaw_golden_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_pan_copper", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:pan_copper_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_pan", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:pan_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:melee_pan_golden", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:pan_golden_entity",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:sword_lead", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:sword_lithium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:sword_rare_earth", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:sword_yttrium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:axe_lead", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:axe_lithium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:axe_rare_earth", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:axe_yttrium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:pickaxe_lead", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:pickaxe_lithium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:pickaxe_rare_earth", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:pickaxe_yttrium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:shovel_lead", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:shovel_lithium", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:shovel_rare_earth", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:shovel_yttrium", "count": 1},
            },
        ],
        # endregion
        # region盔甲
        "armor":[
            {
                "item": {"newItemName": "scuke_survive:armor_snow01_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow01_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow01_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow01_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow01_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow01_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow01_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow01_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow02_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow02_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow02_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow02_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow02_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow02_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_snow02_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_snow02_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_safety_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_safety_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_safety_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_safety_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_safety_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_safety_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_safety_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_safety_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_red_rescue_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_red_rescue_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_red_rescue_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_red_rescue_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_red_rescue_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_red_rescue_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_red_rescue_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_red_rescue_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_black_rescue_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_black_rescue_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_black_rescue_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_black_rescue_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_black_rescue_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_black_rescue_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_black_rescue_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_black_rescue_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor01_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor01_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor01_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor01_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor01_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor01_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor01_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor01_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor02_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor02_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor02_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor02_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor02_legs", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor02_legs",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_armor02_boots", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_armor02_boots",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_helmet", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_chest", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_legs", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_boots", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_lithium_helme", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_lithium_chest", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_lithium_legs", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_lithium_boots", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_rare_earth_helmet", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_rare_earth_chest", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_rare_earth_legs", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_rare_earth_boots", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_helmet", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_chest", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_legs", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_yttrium_boots", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:armor_soviet_tig_helmet_black", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_soviet_tig_helmet_black",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_soviet_tig_helmet_silver", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_soviet_tig_helmet_silver",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_soviet_tig_helmet_gold", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_soviet_tig_helmet_gold",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },

            {
                "item": {"newItemName": "scuke_survive:armor_green_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_green_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_tattered_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_tattered_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_tattered_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_tattered_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_red_mask_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_red_mask_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_red_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_red_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_military_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_military_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_military_chest", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_military_chest",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_skull_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_skull_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_skull_mask_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_skull_mask_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
            {
                "item": {"newItemName": "scuke_survive:armor_skull_hood_helmet", "count": 1},
                "view_model": {
                    "entity_identifier": "scuke_survive:entity_skull_hood_helmet",
			        "rotation_axis": (1, 1, 0),
                    "molang_dict": _DollMolangDict,
                },
            },
        ],
        # endregion
        # region 载具配件
        "carpart": [
            {
                "item": {"newItemName": "scuke_survive:carpart_old_engine", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_efficient_engine", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_red_engine", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_old_bumper", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_alloy_bumper", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_bullbar", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_safety_cage", "count": 1},
            },
            # {
            #     "item": {"newItemName": "scuke_survive:carpart_emp", "count": 1},
            # },
            {
                "item": {"newItemName": "scuke_survive:carpart_missile", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_armor_profile", "count": 1},
            },
            # {
            #     "item": {"newItemName": "scuke_survive:carpart_spike_profile", "count": 1},
            # },
            # {
            #     "item": {"newItemName": "scuke_survive:carpart_thruster", "count": 1},
            # },
            {
                "item": {"newItemName": "scuke_survive:carpart_run_water", "count": 1},
            },
            {
                "item": {"newItemName": "scuke_survive:carpart_fly", "count": 1},
            },
        ],
        # endregion
    },
}
def GetElectricWorkbenchRecipes(blockName):
    """获取工作台的所有配方数据"""
    return _WorkbenchCraftDict.get(blockName)
# endregion


# region 物品配方
_ItemRecipeDict = {
    # region 枪械武器
    "scuke_survive:gun_pistol1": {
        # 输出：合成物品
        "output": {"newItemName": "scuke_survive:gun_pistol1", "newAuxValue": 0, "count": 1, "showInHand": False},
        # 输入：材料
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
        ],
        # 合成时长
        "time": 2,
    },
    "scuke_survive:gun_smg1": {
        "output": {"newItemName": "scuke_survive:gun_smg1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_shotgun1": {
        "output": {"newItemName": "scuke_survive:gun_shotgun1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count":8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_rifle1_s1": {
        "output": {"newItemName": "scuke_survive:gun_rifle1_s1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_bazooka1_s1": {
        "output": {"newItemName": "scuke_survive:gun_bazooka1_s1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 15},
            {"newItemName": "minecraft:copper_ingot", "count": 10},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 1},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 3},
        ],
        "time": 2,
    },
    "scuke_survive:gun_lmg1_s1": {
        "output": {"newItemName": "scuke_survive:gun_lmg1_s1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 12},
            {"newItemName": "minecraft:copper_ingot", "count": 10},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_sniper1_s1": {
        "output": {"newItemName": "scuke_survive:gun_sniper1_s1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 15},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "minecraft:redstone", "count": 3},
            {"newItemName": "minecraft:blaze_rod", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_hmg1_s1": {
        "output": {"newItemName": "scuke_survive:gun_hmg1_s1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 15},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "minecraft:gunpowder", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 4},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
        ],
        "time": 4,
    },
    "scuke_survive:gun_pistol1_s2": {
        "output": {"newItemName": "scuke_survive:gun_pistol1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_smg1_s2": {
        "output": {"newItemName": "scuke_survive:gun_smg1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:gun_shotgun1_s2": {
        "output": {"newItemName": "scuke_survive:gun_shotgun1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 12},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 3,
    },
    "scuke_survive:gun_sniper1_s2": {
        "output": {"newItemName": "scuke_survive:gun_sniper1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 15},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "minecraft:redstone", "count": 3},
            {"newItemName": "minecraft:blaze_rod", "count": 3},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
        ],
        "time": 3,
    },
    "scuke_survive:gun_bazooka1_s2": {
        "output": {"newItemName": "scuke_survive:gun_bazooka1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 17},
            {"newItemName": "minecraft:copper_ingot", "count": 12},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 3},
            {"newItemName": "minecraft:gunpowder", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 3,
    },
    "scuke_survive:gun_lmg1_s2": {
        "output": {"newItemName": "scuke_survive:gun_lmg1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 12},
            {"newItemName": "minecraft:copper_ingot", "count": 10},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
        ],
        "time": 3,
    },
    "scuke_survive:gun_rifle1_s2": {
        "output": {"newItemName": "scuke_survive:gun_rifle1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
        ],
        "time": 3,
    },
    "scuke_survive:gun_hmg1_s2": {
        "output": {"newItemName": "scuke_survive:gun_hmg1_s2", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 30},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 8},
        ],
        "time": 4,
    },
    "scuke_survive:gun_pistol1_s3": {
        "output": {"newItemName": "scuke_survive:gun_pistol1_s3", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 12},
            {"newItemName": "minecraft:copper_ingot", "count": 4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 3,
    },
    "scuke_survive:gun_smg1_s3": {
        "output": {"newItemName": "scuke_survive:gun_smg1_s3", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
        ],
        "time": 3,
    },
    "scuke_survive:gun_shotgun1_s3": {
        "output": {"newItemName": "scuke_survive:gun_shotgun1_s3", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 12},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 3,
    },
    "scuke_survive:gun_bazooka1": {
        "output": {"newItemName": "scuke_survive:gun_bazooka1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 20},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 12},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "minecraft:gunpowder", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 4,
    },
    "scuke_survive:gun_lmg1": {
        "output": {"newItemName": "scuke_survive:gun_lmg1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 20},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 14},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 4,
    },
    "scuke_survive:gun_rifle1": {
        "output": {"newItemName": "scuke_survive:gun_rifle1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 30},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 5},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 8},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
        ],
        "time": 4,
    },
    "scuke_survive:gun_hmg1": {
        "output": {"newItemName": "scuke_survive:gun_hmg1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 30},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 8},
            {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
        ],
        "time": 4,
    },
    "scuke_survive:gun_sniper1": {
        "output": {"newItemName": "scuke_survive:gun_sniper1", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 15},
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
            {"newItemName": "minecraft:redstone", "count": 3},
            {"newItemName": "minecraft:blaze_rod", "count": 3},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
            {"newItemName": "scuke_survive:mat_chip_large", "count": 1},
        ],
        "time": 4,
    },
    # endregion
    # region 子弹弹匣
    "scuke_survive:clip_normal": {
        "output": {"newItemName": "scuke_survive:clip_normal", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:raw_iron", "count": 1},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:clip_advanced": {
        "output": {"newItemName": "scuke_survive:clip_advanced", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:raw_copper", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:clip_energy": {
        "output": {"newItemName": "scuke_survive:clip_energy", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:clip_explosion": {
        "output": {"newItemName": "scuke_survive:clip_explosion", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ],
        "time": 1,
    },
    # endregion
    # region 近战武器
    "scuke_survive:melee_axe_red": {
        "output": {"newItemName": "scuke_survive:melee_axe_red", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:copper_ingot", "count": 1},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:melee_baseball_bat": {
        "output": {"newItemName": "scuke_survive:melee_baseball_bat", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 1},
            {"newItemName": "minecraft:stick", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:sword_lead": {
        "output": {"newItemName": "scuke_survive:sword_lead", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:shovel_lead": {
        "output": {"newItemName": "scuke_survive:shovel_lead", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 1},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:axe_lead": {
        "output": {"newItemName": "scuke_survive:axe_lead", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:pickaxe_lead": {
        "output": {"newItemName": "scuke_survive:pickaxe_lead", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:melee_baseball_bat_m": {
        "output": {"newItemName": "scuke_survive:melee_baseball_bat_m", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:melee_axe": {
        "output": {"newItemName": "scuke_survive:melee_axe", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:melee_chainsaw_old": {
        "output": {"newItemName": "scuke_survive:melee_chainsaw_old", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:sword_lithium": {
        "output": {"newItemName": "scuke_survive:sword_lithium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:pickaxe_lithium": {
        "output": {"newItemName": "scuke_survive:pickaxe_lithium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:shovel_lithium": {
        "output": {"newItemName": "scuke_survive:shovel_lithium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:axe_lithium": {
        "output": {"newItemName": "scuke_survive:axe_lithium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:melee_chainsaw": {
        "output": {"newItemName": "scuke_survive:melee_chainsaw", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:melee_baseball_bat_golden": {
        "output": {"newItemName": "scuke_survive:melee_baseball_bat_golden", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:gold_ingot", "count": 8},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:melee_pigsaw": {
        "output": {"newItemName": "scuke_survive:melee_pigsaw", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
            {"newItemName": "minecraft:porkchop", "count": 10},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:sword_rare_earth": {
        "output": {"newItemName": "scuke_survive:sword_rare_earth", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
        ],
        "time": 2,
    },
    "scuke_survive:pickaxe_rare_earth": {
        "output": {"newItemName": "scuke_survive:pickaxe_rare_earth", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:shovel_rare_earth": {
        "output": {"newItemName": "scuke_survive:shovel_rare_earth", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:axe_rare_earth": {
        "output": {"newItemName": "scuke_survive:axe_rare_earth", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:sword_yttrium": {
        "output": {"newItemName": "scuke_survive:sword_yttrium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "minecraft:stick", "count": 1},
        ],
        "time": 2,
    },
    "scuke_survive:pickaxe_yttrium": {
        "output": {"newItemName": "scuke_survive:pickaxe_yttrium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:shovel_yttrium": {
        "output": {"newItemName": "scuke_survive:shovel_yttrium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:axe_yttrium": {
        "output": {"newItemName": "scuke_survive:axe_yttrium", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 3},
            {"newItemName": "minecraft:stick", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:melee_axe_golden": {
        "output": {"newItemName": "scuke_survive:melee_axe_golden", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "minecraft:gold_ingot", "count": 10},
            {"newItemName": "minecraft:stick", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
        ],
        "time": 2,
    },
    "scuke_survive:melee_chainsaw_golden": {
        "output": {"newItemName": "scuke_survive:melee_chainsaw_golden", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:gold_ingot", "count": 10},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "minecraft:stick", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 2,
    },
    "scuke_survive:melee_pigsaw_golden": {
        "output": {"newItemName": "scuke_survive:melee_pigsaw_golden", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:gold_ingot", "count": 10},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "minecraft:porkchop", "count": 20},
            {"newItemName": "minecraft:ghast_tear", "count": 1},
        ],
        "time": 3,
    },
    # endregion
    # region 盔甲
    "scuke_survive:armor_snow01_helmet": {
        "output": {"newItemName": "scuke_survive:armor_snow01_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 5},
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:armor_snow01_chest": {
        "output": {"newItemName": "scuke_survive:armor_snow01_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 6},
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:armor_snow01_legs": {
        "output": {"newItemName": "scuke_survive:armor_snow01_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 6},
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "scuke_survive:ingot_lead", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:armor_snow01_boots": {
        "output": {"newItemName": "scuke_survive:armor_snow01_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 4},
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "scuke_survive:ingot_lead", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:armor_snow02_helmet": {
        "output": {"newItemName": "scuke_survive:armor_snow02_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 1},
            {"newItemName": "minecraft:leather", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:armor_snow02_chest": {
        "output": {"newItemName": "scuke_survive:armor_snow02_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 1},
            {"newItemName": "minecraft:leather", "count": 8},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:armor_snow02_legs": {
        "output": {"newItemName": "scuke_survive:armor_snow02_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 1},
            {"newItemName": "minecraft:leather", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:armor_snow02_boots": {
        "output": {"newItemName": "scuke_survive:armor_snow02_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:white_wool", "count": 1},
            {"newItemName": "minecraft:leather", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:armor_safety_helmet": {
        "output": {"newItemName": "scuke_survive:armor_safety_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "scuke_survive:mat_phone1", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_safety_chest": {
        "output": {"newItemName": "scuke_survive:armor_safety_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 6},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "scuke_survive:mat_game_machine", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_safety_legs": {
        "output": {"newItemName": "scuke_survive:armor_safety_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_safety_boots": {
        "output": {"newItemName": "scuke_survive:armor_safety_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_red_rescue_helmet": {
        "output": {"newItemName": "scuke_survive:armor_red_rescue_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "scuke_survive:mat_read_machine", "count": 1},
        ],
        "time": 4,
    },
    "scuke_survive:armor_red_rescue_chest": {
        "output": {"newItemName": "scuke_survive:armor_red_rescue_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 8},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "scuke_survive:mat_phone_watch", "count": 1},
        ],
        "time": 4,
    },
    "scuke_survive:armor_red_rescue_legs": {
        "output": {"newItemName": "scuke_survive:armor_red_rescue_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 6},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ],
        "time": 4,
    },
    "scuke_survive:armor_red_rescue_boots": {
        "output": {"newItemName": "scuke_survive:armor_red_rescue_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ],
        "time": 4,
    },
    "scuke_survive:armor_black_rescue_helmet": {
        "output": {"newItemName": "scuke_survive:armor_black_rescue_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 6},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "scuke_survive:mat_phone_watch", "count": 1},
        ],
        "time": 5,
    },
    "scuke_survive:armor_black_rescue_chest": {
        "output": {"newItemName": "scuke_survive:armor_black_rescue_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
        ],
        "time": 5,
    },
    "scuke_survive:armor_black_rescue_legs": {
        "output": {"newItemName": "scuke_survive:armor_black_rescue_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 8},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 5,
    },
    "scuke_survive:armor_black_rescue_boots": {
        "output": {"newItemName": "scuke_survive:armor_black_rescue_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 6},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 5,
    },
    "scuke_survive:armor_armor01_helmet": {
        "output": {"newItemName": "scuke_survive:armor_armor01_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 8},
            {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 6,
    },
    "scuke_survive:armor_armor01_chest": {
        "output": {"newItemName": "scuke_survive:armor_armor01_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 12},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 6,
    },
    "scuke_survive:armor_armor01_legs": {
        "output": {"newItemName": "scuke_survive:armor_armor01_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "scuke_survive:mat_phone3", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 6,
    },
    "scuke_survive:armor_armor01_boots": {
        "output": {"newItemName": "scuke_survive:armor_armor01_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 8},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
        ],
        "time": 6,
    },
    "scuke_survive:armor_armor02_helmet": {
        "output": {"newItemName": "scuke_survive:armor_armor02_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 4},
        ],
        "time": 7,
    },
    "scuke_survive:armor_armor02_chest": {
        "output": {"newItemName": "scuke_survive:armor_armor02_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 14},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 4},
        ],
        "time": 7,
    },
    "scuke_survive:armor_armor02_legs": {
        "output": {"newItemName": "scuke_survive:armor_armor02_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 12},
            {"newItemName": "scuke_survive:mat_chip_large", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 7,
    },
    "scuke_survive:armor_armor02_boots": {
        "output": {"newItemName": "scuke_survive:armor_armor02_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "scuke_survive:mat_phone2", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 3},
        ],
        "time": 7,
    },

    "scuke_survive:armor_lead_boots": {
        "output": {"newItemName": "scuke_survive:armor_lead_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:armor_lead_chest": {
        "output": {"newItemName": "scuke_survive:armor_lead_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 8},
        ],
        "time": 1,
    },
    "scuke_survive:armor_lead_helme": {
        "output": {"newItemName": "scuke_survive:armor_lead_helme", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 5},
        ],
        "time": 1,
    },
    "scuke_survive:armor_lead_legs": {
        "output": {"newItemName": "scuke_survive:armor_lead_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lead", "count": 7},
        ],
        "time": 1,
    },
    "scuke_survive:armor_lithium_boots": {
        "output": {"newItemName": "scuke_survive:armor_lithium_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
        ],
        "time": 2,
    },
    "scuke_survive:armor_lithium_chest": {
        "output": {"newItemName": "scuke_survive:armor_lithium_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 8},
        ],
        "time": 2,
    },
    "scuke_survive:armor_lithium_helme": {
        "output": {"newItemName": "scuke_survive:armor_lithium_helme", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 5},
        ],
        "time": 2,
    },
    "scuke_survive:armor_lithium_legs": {
        "output": {"newItemName": "scuke_survive:armor_lithium_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 7},
        ],
        "time": 2,
    },
    "scuke_survive:armor_rare_earth_boots": {
        "output": {"newItemName": "scuke_survive:armor_rare_earth_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
        ],
        "time": 3,
    },
    "scuke_survive:armor_rare_earth_chest": {
        "output": {"newItemName": "scuke_survive:armor_rare_earth_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 8},
        ],
        "time": 3,
    },
    "scuke_survive:armor_rare_earth_helmet": {
        "output": {"newItemName": "scuke_survive:armor_rare_earth_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 5},
        ],
        "time": 3,
    },
    "scuke_survive:armor_rare_earth_legs": {
        "output": {"newItemName": "scuke_survive:armor_rare_earth_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 7},
        ],
        "time": 3,
    },
    "scuke_survive:armor_yttrium_boots": {
        "output": {"newItemName": "scuke_survive:armor_yttrium_boots", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
        ],
        "time": 4,
    },
    "scuke_survive:armor_yttrium_chest": {
        "output": {"newItemName": "scuke_survive:armor_yttrium_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 8},
        ],
        "time": 4,
    },
    "scuke_survive:armor_yttrium_helmet": {
        "output": {"newItemName": "scuke_survive:armor_yttrium_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 5},
        ],
        "time": 4,
    },
    "scuke_survive:armor_yttrium_legs": {
        "output": {"newItemName": "scuke_survive:armor_yttrium_legs", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 7},
        ],
        "time": 4,
    },
    "scuke_survive:armor_soviet_tig_helmet_black": {
        "output": {"newItemName": "scuke_survive:armor_soviet_tig_helmet_black", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:copper_ingot", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
            {"newItemName": "minecraft:glass", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:armor_soviet_tig_helmet_silver": {
        "output": {"newItemName": "scuke_survive:armor_soviet_tig_helmet_silver", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:glass", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_soviet_tig_helmet_gold": {
        "output": {"newItemName": "scuke_survive:armor_soviet_tig_helmet_gold", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:gold_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:glass", "count": 1},
        ],
        "time": 4,
    },

    "scuke_survive:armor_green_helmet": {
        "output": {"newItemName": "scuke_survive:armor_green_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "minecraft:green_wool", "count": 3},
        ],
        "time": 1,
    },
    "scuke_survive:armor_tattered_helmet": {
        "output": {"newItemName": "scuke_survive:armor_tattered_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "minecraft:green_wool", "count": 3},
        ],
        "time": 1,
    },
    "scuke_survive:armor_tattered_chest": {
        "output": {"newItemName": "scuke_survive:armor_tattered_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:leather", "count": 1},
            {"newItemName": "minecraft:green_wool", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:armor_red_mask_helmet": {
        "output": {"newItemName": "scuke_survive:armor_red_mask_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 2},
            {"newItemName": "minecraft:red_wool", "count": 4},
        ],
        "time": 2,
    },
    "scuke_survive:armor_red_helmet": {
        "output": {"newItemName": "scuke_survive:armor_red_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 2},
            {"newItemName": "minecraft:red_wool", "count": 4},
        ],
        "time": 2,
    },
    "scuke_survive:armor_military_helmet": {
        "output": {"newItemName": "scuke_survive:armor_military_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 2},
            {"newItemName": "minecraft:green_wool", "count": 5},
        ],
        "time": 3,
    },
    "scuke_survive:armor_military_chest": {
        "output": {"newItemName": "scuke_survive:armor_military_chest", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "minecraft:leather", "count": 3},
            {"newItemName": "minecraft:green_wool", "count": 6},
        ],
        "time": 3,
    },
    "scuke_survive:armor_skull_helmet": {
        "output": {"newItemName": "scuke_survive:armor_skull_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "minecraft:leather", "count": 4},
            {"newItemName": "minecraft:black_wool", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_skull_mask_helmet": {
        "output": {"newItemName": "scuke_survive:armor_skull_mask_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "minecraft:leather", "count": 4},
            {"newItemName": "minecraft:black_wool", "count": 1},
        ],
        "time": 3,
    },
    "scuke_survive:armor_skull_hood_helmet": {
        "output": {"newItemName": "scuke_survive:armor_skull_hood_helmet", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
        ],
        "time": 5,
    },

    # endregion
    # region 物品道具
    "scuke_survive:time_bomb1": {
        "output": {"newItemName": "scuke_survive:time_bomb1", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:gunpowder", "count": 1},
            {"newItemName": "scuke_survive:mat_phone1", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:c4_bomb1": {
        "output": {"newItemName": "scuke_survive:c4_bomb1", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:gunpowder", "count": 1},
            {"newItemName": "scuke_survive:mat_read_machine", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:c4_detonator": {
        "output": {"newItemName": "scuke_survive:c4_detonator", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:copper_ingot", "count": 1},
            {"newItemName": "scuke_survive:ingot_lead", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:build_struct": {
        "output": {"newItemName": "scuke_survive:build_struct", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:car_rescue": {
        "output": {"newItemName": "scuke_survive:car_rescue", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 3},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 3},
        ],
        "time": 1,
    },
    "scuke_survive:electric_heater_small": {
        "output": {"newItemName": "scuke_survive:electric_heater_small", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
            {"newItemName": "scuke_survive:mat_screw", "count": 2},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:electric_heater_large": {
        "output": {"newItemName": "scuke_survive:electric_heater_large", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 3},
            {"newItemName": "minecraft:blaze_rod", "count": 2},
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:mat_screw", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:items_barricade_wood": {
        "output": {"newItemName": "scuke_survive:items_barricade_wood", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:oak_log", "count": 9},
        ],
        "time": 1,
    },
    "scuke_survive:car_repair": {
        "output": {"newItemName": "scuke_survive:car_repair", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:items_wirecloth": {
        "output": {"newItemName": "scuke_survive:items_wirecloth", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:items_barricade_iron": {
        "output": {"newItemName": "scuke_survive:items_barricade_iron", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
        ],
        "time": 1,
    },
    "scuke_survive:items_grenade_small": {
        "output": {"newItemName": "scuke_survive:items_grenade_small", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:items_trap": {
        "output": {"newItemName": "scuke_survive:items_trap", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:items_grenade_middle": {
        "output": {"newItemName": "scuke_survive:items_grenade_middle", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:items_landmine": {
        "output": {"newItemName": "scuke_survive:items_landmine", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 4},
        ],
        "time": 2,
    },
    "scuke_survive:items_grenade_large": {
        "output": {"newItemName": "scuke_survive:items_grenade_large", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 2},
            {"newItemName": "minecraft:gunpowder", "count": 2},
            {"newItemName": "scuke_survive:raw_yttrium", "count": 2},
        ],
        "time": 2,
    },

    "scuke_survive:mat_circuit_board": {
        "output": {"newItemName": "scuke_survive:mat_circuit_board", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:raw_copper", "count":8},
            {"newItemName": "scuke_survive:raw_lithium", "count": 3},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:chest_storage_orange": {
        "output": {"newItemName": "scuke_survive:chest_storage_orange", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:raw_copper", "count":6},
            {"newItemName": "minecraft:raw_iron", "count": 6},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 9},
        ],
        "time": 1,
    },
    "scuke_survive:chest_storage_blue": {
        "output": {"newItemName": "scuke_survive:chest_storage_blue", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:raw_copper", "count":6},
            {"newItemName": "minecraft:raw_iron", "count": 6},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 9},
        ],
        "time": 1,
    },
    "scuke_survive:chest_storage_red": {
        "output": {"newItemName": "scuke_survive:chest_storage_red", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:raw_copper", "count":6},
            {"newItemName": "minecraft:raw_iron", "count": 6},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 9},
        ],
        "time": 1,
    },
    "scuke_survive:chest_military": {
        "output": {"newItemName": "scuke_survive:chest_military", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:raw_copper", "count":6},
            {"newItemName": "minecraft:raw_iron", "count": 6},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 9},
            {"newItemName": "scuke_survive:raw_rare_earth", "count": 3},
        ],
        "time": 1,
    },
    # 雷达
    "scuke_survive:items_ladar": {
        "output": {"newItemName": "scuke_survive:items_ladar", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 1},
        ],
        "time": 1,
    },

    #光刻机配方
    "scuke_survive:mat_chip_small": {
        "output": {"newItemName": "scuke_survive:mat_chip_small", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_lithium", "count":4},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 3},
            {"newItemName": "minecraft:redstone", "count": 2},
        ],
        "time": 1,
    },

    "scuke_survive:mat_chip_middle": {
        "output": {"newItemName": "scuke_survive:mat_chip_middle", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count":4},
            {"newItemName": "minecraft:emerald", "count": 2},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 4},
            {"newItemName": "minecraft:redstone", "count": 6},
        ],
        "time": 1,
    },

    "scuke_survive:mat_chip_large": {
        "output": {"newItemName": "scuke_survive:mat_chip_large", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count":6},
            {"newItemName": "minecraft:gold_ingot", "count": 4},
            {"newItemName": "minecraft:diamond", "count": 2},
            {"newItemName": "minecraft:redstone", "count":6},
        ],
        "time": 1,
    },

    "scuke_survive:electric_dynamo_middle": {
        "output": {"newItemName": "scuke_survive:electric_dynamo_middle", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:copper_ingot", "count":4},
            {"newItemName": "minecraft:gold_ingot", "count":4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
            {"newItemName": "scuke_survive:ingot_lead", "count": 4},
            {"newItemName": "scuke_survive:mat_screw", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:electric_machinery": {
        "output": {"newItemName": "scuke_survive:electric_machinery", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:redstone", "count":2},
            {"newItemName": "minecraft:gold_ingot", "count":4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 1},
            {"newItemName": "scuke_survive:mat_screw", "count": 2},
        ],
        "time": 2,
    },
    "scuke_survive:electric_dynamo_large": {
        "output": {"newItemName": "scuke_survive:electric_dynamo_large", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:redstone", "count":2},
            {"newItemName": "minecraft:gold_ingot", "count":8},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 8},
            {"newItemName": "scuke_survive:mat_circuit_board", "count": 2},
        ],
        "time": 3,
    },
    "scuke_survive:electric_photoetching": {
        "output": {"newItemName": "scuke_survive:electric_photoetching", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:redstone", "count":2},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 3},
        ],
        "time": 3,
    },
    "scuke_survive:electric_spike_trap": {
        "output": {"newItemName": "scuke_survive:electric_spike_trap", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count":4},
            {"newItemName": "minecraft:copper_ingot", "count":2},
            {"newItemName": "minecraft:redstone", "count":2},
        ],
        "time": 2,
    },
    "scuke_survive:items_oil_drum_small": {
        "output": {"newItemName": "scuke_survive:items_oil_drum_small", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count":3},
            {"newItemName": "minecraft:gunpowder", "count":2},
        ],
        "time": 2,
    },
    "scuke_survive:items_oil_drum_large": {
        "output": {"newItemName": "scuke_survive:items_oil_drum_large", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count":4},
            {"newItemName": "minecraft:gunpowder", "count":3},
        ],
        "time": 2,
    },
    # endregion
    # region 配件
    "scuke_survive:carpart_old_engine": {
        "output": {"newItemName": "scuke_survive:carpart_old_engine", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:blaze_rod", "count": 2},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 6},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_efficient_engine": {
        "output": {"newItemName": "scuke_survive:carpart_efficient_engine", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "minecraft:blaze_rod", "count": 2},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 6},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_red_engine": {
        "output": {"newItemName": "scuke_survive:carpart_red_engine", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "minecraft:blaze_rod", "count": 4},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 10},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 10},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_old_bumper": {
        "output": {"newItemName": "scuke_survive:carpart_old_bumper", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "minecraft:copper_ingot", "count": 6},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_alloy_bumper": {
        "output": {"newItemName": "scuke_survive:carpart_alloy_bumper", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_lead", "count": 3},
            {"newItemName": "scuke_survive:mat_plastic_board", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_bullbar": {
        "output": {"newItemName": "scuke_survive:carpart_bullbar", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "minecraft:iron_ingot", "count": 4},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_safety_cage": {
        "output": {"newItemName": "scuke_survive:carpart_safety_cage", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 12},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_lead", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_missile": {
        "output": {"newItemName": "scuke_survive:carpart_missile", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 10},
            {"newItemName": "scuke_survive:mat_chip_large", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_armor_profile": {
        "output": {"newItemName": "scuke_survive:carpart_armor_profile", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 8},
            {"newItemName": "minecraft:copper_ingot", "count": 5},
            {"newItemName": "minecraft:gold_ingot", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_run_water": {
        "output": {"newItemName": "scuke_survive:carpart_run_water", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:mat_chip_large", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 6},
        ],
        "time": 1,
    },
    "scuke_survive:carpart_fly": {
        "output": {"newItemName": "scuke_survive:carpart_fly", "newAuxValue": 0, "count": 1},
        "input": [
            {"newItemName": "scuke_survive:mat_chip_middle", "count": 1},
            {"newItemName": "scuke_survive:mat_chip_small", "count": 1},
            {"newItemName": "scuke_survive:mat_chip_large", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 6},
        ],
        "time": 1,
    },
    "scuke_survive:melee_pan_copper": {
        "output": {"newItemName": "scuke_survive:melee_pan_copper", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:copper_ingot", "count": 8},
            {"newItemName": "scuke_survive:ingot_lead", "count": 1},
        ],
        "time": 1,
    },
    "scuke_survive:melee_pan": {
        "output": {"newItemName": "scuke_survive:melee_pan", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:iron_ingot", "count": 20},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 4},
        ],
        "time": 1,
    },
    "scuke_survive:melee_pan_golden": {
        "output": {"newItemName": "scuke_survive:melee_pan_golden", "newAuxValue": 0, "count": 1, "showInHand": False},
        "input": [
            {"newItemName": "minecraft:gold_ingot", "count": 15},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
        ],
        "time": 1,
    },
    # endregion
}
_ItemRepairRecipeDict = {
    "scuke_survive:gun_pistol1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
        ]
    },
    "scuke_survive:gun_smg1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
        ]
    },
    "scuke_survive:gun_shotgun1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
        ]
    },
    "scuke_survive:gun_pistol1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ]
    },
    "scuke_survive:gun_smg1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ]
    },
    "scuke_survive:gun_rifle1_s1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ]
    },
    "scuke_survive:gun_bazooka1_s1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ]
    },
    "scuke_survive:gun_lmg1_s1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ]
    },
    "scuke_survive:gun_sniper1_s1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "minecraft:copper_ingot", "count": 2},
        ]
    },
    "scuke_survive:gun_pistol1_s3": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_shotgun1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_sniper1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_bazooka1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_lmg1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_smg1_s3": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_shotgun1_s3": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_rifle1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 6},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:gun_hmg1_s1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:gun_bazooka1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:gun_lmg1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:gun_hmg1_s2": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 5},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},

        ]
    },
    "scuke_survive:gun_rifle1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:gun_hmg1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:gun_sniper1": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },

    "scuke_survive:melee_axe_red": {
        "repair": [
            {"newItemName": "minecraft:stick", "count": 2},
        ]
    },
    "scuke_survive:melee_baseball_bat": {
        "repair": [
            {"newItemName": "minecraft:stick", "count": 2},
        ]
    },
    "scuke_survive:melee_pan_copper": {
        "repair": [
            {"newItemName": "minecraft:copper_ingot", "count": 4},
        ]
    },
    "scuke_survive:melee_baseball_bat_m": {
        "repair": [
            {"newItemName": "minecraft:stick", "count": 1},
            {"newItemName": "minecraft:iron_ingot", "count": 2},
        ]
    },
    "scuke_survive:melee_axe": {
        "repair": [
            {"newItemName": "minecraft:stick", "count": 1},
            {"newItemName": "minecraft:iron_ingot", "count": 2},
        ]
    },
    "scuke_survive:melee_chainsaw_old": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
            {"newItemName": "minecraft:iron_ingot", "count": 2},
        ]
    },
    "scuke_survive:melee_pan": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 10},
        ]
    },
    "scuke_survive:melee_chainsaw": {
        "repair": [
            {"newItemName": "minecraft:iron_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
        ]
    },
    "scuke_survive:melee_baseball_bat_golden": {
        "repair": [
            {"newItemName": "minecraft:stick", "count": 1},
            {"newItemName": "minecraft:gold_ingot", "count": 2},
        ]
    },
    "scuke_survive:melee_pigsaw": {
        "repair": [
            {"newItemName": "minecraft:porkchop", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
        ]
    },
    "scuke_survive:melee_pan_golden": {
        "repair": [
            {"newItemName": "minecraft:gold_ingot", "count": 8},
        ]
    },
    "scuke_survive:melee_axe_golden": {
        "repair": [
            {"newItemName": "minecraft:gold_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
        ]
    },
    "scuke_survive:melee_chainsaw_golden": {
        "repair": [
            {"newItemName": "minecraft:gold_ingot", "count": 10},
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:melee_pigsaw_golden": {
        "repair": [
            {"newItemName": "minecraft:porkchop", "count": 4},
            {"newItemName": "minecraft:gold_ingot", "count": 2},
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
        ]
    },

    "scuke_survive:armor_soviet_tig_helmet_black": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_snow01_helmet": {
        "repair": [
            {"newItemName": "minecraft:white_wool", "count": 2},
        ]
    },
    "scuke_survive:armor_snow01_chest": {
        "repair": [
            {"newItemName": "minecraft:white_wool", "count": 2},
        ]
    },
    "scuke_survive:armor_snow01_legs": {
        "repair": [
            {"newItemName": "minecraft:white_wool", "count": 2},
        ]
    },
    "scuke_survive:armor_snow01_boots": {
        "repair": [
            {"newItemName": "minecraft:white_wool", "count": 2},
        ]
    },

    "scuke_survive:armor_soviet_tig_helmet_silver": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
        ]
    },

    "scuke_survive:armor_snow02_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },
    "scuke_survive:armor_snow02_chest": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },
    "scuke_survive:armor_snow02_legs": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },
    "scuke_survive:armor_snow02_boots": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_rare_earth", "count": 1},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },

    "scuke_survive:armor_safety_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_safety_chest": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_safety_legs": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_safety_boots": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },

    "scuke_survive:armor_soviet_tig_helmet_gold": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
        ]
    },

    "scuke_survive:armor_red_rescue_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_red_rescue_chest": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_red_rescue_legs": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_red_rescue_boots": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 2},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_black_rescue_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
        ]
    },
    "scuke_survive:armor_black_rescue_chest": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_black_rescue_legs": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_black_rescue_boots": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 3},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor01_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor01_chest": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 6},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor01_legs": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 5},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor01_boots": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 4},
            {"newItemName": "scuke_survive:ore_lithium", "count": 1},
        ]
    },
    "scuke_survive:armor_armor02_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 5},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor02_chest": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 7},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor02_legs": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 6},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },
    "scuke_survive:armor_armor02_boots": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 5},
            {"newItemName": "scuke_survive:ore_lithium", "count": 2},
            {"newItemName": "minecraft:redstone", "count": 1},
        ]
    },

    
    "scuke_survive:armor_green_helmet": {
        "repair": [
            {"newItemName": "minecraft:green_wool", "count": 1},
        ]
    },
    "scuke_survive:armor_tattered_helmet": {
        "repair": [
            {"newItemName": "minecraft:green_wool", "count": 1},
        ]
    },
    "scuke_survive:armor_tattered_chest": {
        "repair": [
            {"newItemName": "minecraft:green_wool", "count": 1},
        ]
    },
    "scuke_survive:armor_red_mask_helmet": {
        "repair": [
            {"newItemName": "minecraft:red_wool", "count": 2},
        ]
    },
    "scuke_survive:armor_red_helmet": {
        "repair": [
            {"newItemName": "minecraft:red_wool", "count": 2},
        ]
    },
    "scuke_survive:armor_military_helmet": {
        "repair": [
            {"newItemName": "minecraft:green_wool", "count": 2},
        ]
    },
    "scuke_survive:armor_military_chest": {
        "repair": [
            {"newItemName": "minecraft:green_wool", "count": 3},
        ]
    },
    "scuke_survive:armor_skull_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },
    "scuke_survive:armor_skull_mask_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 1},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },
    "scuke_survive:armor_skull_hood_helmet": {
        "repair": [
            {"newItemName": "scuke_survive:ingot_yttrium", "count": 3},
            {"newItemName": "minecraft:leather", "count": 1},
        ]
    },
}
def GetElectricItemRecipe(itemName):
    """获取物品的合成配方数据"""
    return _ItemRecipeDict.get(itemName) if itemName in _ItemRecipeDict else None 

def GetElectricItemRepairRecipe(itemName):
    """获取物品的修复配方数据"""
    # 增加判断防止配方中没有该物品配方
    return _ItemRepairRecipeDict.get(itemName) if itemName in _ItemRepairRecipeDict else None 

def GetAllElectricItemRecipes():
    """
    获取所有物品的配方数据
    
    格式={itemName: {}, ...}
    """
    return _ItemRecipeDict
# endregion

