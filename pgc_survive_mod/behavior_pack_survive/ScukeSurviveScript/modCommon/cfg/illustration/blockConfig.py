# -*- encoding: utf-8 -*-

ConfigList = [
    {
        "id": "scuke_survive:metal_block_lead",  # 标记ID
        "chineseName": "铅块",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 0.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/metal_block_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:metal_block_lithium",  # 标记ID
        "chineseName": "锂块",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 1.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/metal_block_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:metal_block_rare_earth",  # 标记ID
        "chineseName": "稀土块",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 2.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/metal_block_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:metal_block_yttrium",  # 标记ID
        "chineseName": "钇金陨石块",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 3.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/metal_block_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_lead",  # 标记ID
        "chineseName": "铅矿",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 4.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_lithium",  # 标记ID
        "chineseName": "锂矿",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 5.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_rare_earth",  # 标记ID
        "chineseName": "稀土矿",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 6.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_yttrium",  # 标记ID
        "chineseName": "钇金陨石矿",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 7.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_lead_deepslate",  # 标记ID
        "chineseName": "深层铅矿",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 8.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_lead_deepslate",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_lithium_deepslate",  # 标记ID
        "chineseName": "深层锂矿",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 9.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_lithium_deepslate",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:ore_rare_earth_deepslate",  # 标记ID
        "chineseName": "深层稀土矿",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:block_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.block_index": 10.0
            }
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/ore_rare_earth_deepslate",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_oil_drum_small",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_oil_drum_small",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_oil_drum_small",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_oil_drum_large",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "red",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_oil_drum_large",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_oil_drum_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_landmine",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_landmine",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_landmine",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_barricade_wood",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_barricade_wood",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_barricade_wood",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_barricade_iron",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_barricade_iron",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_barricade_iron",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_wirecloth",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_wirecloth",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_barbed_wire",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:items_trap",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:items_trap",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/items_trap",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:chest_paper",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:chest_paper",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/chest_paper_icon",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:chest_paper_tag",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:chest_paper_tag",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/chest_paper_tag_icon",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:chest_storage_orange",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:chest_storage_orange",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/chest_storage_orange_icon",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:chest_storage_blue",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:chest_storage_blue",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/chest_storage_blue_icon",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:chest_storage_red",  # 标记ID
        "chineseName": "",  # 显示的中文
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:chest_storage_red",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/chest_storage_red_icon",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:chest_military",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:chest_military",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/chest_military",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_dynamo_small",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_dynamo_small",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_dynamo_small",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_dynamo_middle",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "red",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_dynamo_middle",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_dynamo_middle",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_dynamo_large",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_dynamo_large",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_dynamo_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_heater_small",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_heater_small",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_heater_small",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_heater_large",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_heater_large",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_heater_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    # {
    #     "id": "scuke_survive:electric_refrigeration_small",  # 标记ID
    #     "chineseName": "",  # 显示的中文字
    #     "cardType": "blue",
    #     "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
    #     "itemRenderData": {  # 当showType为itemRender时启动
    #         "itemName": "scuke_survive:electric_refrigeration_small",  # 物品ID
    #         "auxValue": 0,  # 特殊值
    #         "enchant": False,  # 是否附魔
    #         "userData": {},  # 物品数据
    #         "alpha": 1.0  # 不透明度
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "blocks/electric_refrigeration_small",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": ""  # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:electric_refrigeration_large",  # 标记ID
    #     "chineseName": "",  # 显示的中文字
    #     "cardType": "red",
    #     "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
    #     "itemRenderData": {  # 当showType为itemRender时启动
    #         "itemName": "scuke_survive:electric_refrigeration_large",  # 物品ID
    #         "auxValue": 0,  # 特殊值
    #         "enchant": False,  # 是否附魔
    #         "userData": {},  # 物品数据
    #         "alpha": 1.0  # 不透明度
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "blocks/electric_refrigeration_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": ""  # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    {
        "id": "scuke_survive:electric_printer",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_printer",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_printer",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_photoetching",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_photoetching",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_photoetching",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_machinery",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_machinery",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_machinery",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:electric_spike_trap",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:electric_spike_trap",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/electric_spike_trap",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:car_remold",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:car_remold",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/car_remold",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:time_bomb1",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:time_bomb1",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/time_bomb",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:c4_bomb1",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:c4_bomb1",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "blocks/c4_bomb",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ""  # 详细描述文字
                }
            ]
        }
    },
]
