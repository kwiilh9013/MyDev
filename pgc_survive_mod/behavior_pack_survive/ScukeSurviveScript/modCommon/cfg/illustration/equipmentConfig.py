# -*- encoding: utf-8 -*-
MolangDict = {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0,  # 是否启动控件点位修正
                "variable.has_trim": 0.0,
                "variable.is_enchanted": 0.0,
                "variable.mutilated_blood": 0.0
            }

RedRescueTxt = "\n材料轻质且极其坚韧，具备卓越的耐高温和抗辐射性能，能够有效抵御火星表面的极端温差和强烈的宇宙辐射，确保穿戴者始终处于舒适状态。"
BlackRescueTxt = "\n采用了从月球表面采集的特殊材料，呈现出神秘的银灰色光泽，仿佛月夜下的冷辉，既优雅又充满力量。这种独特的材料不仅轻盈坚韧，还具备极强的反射与吸收光能的能力."
Armor01Txt = "\n灰黑色的盔甲表面覆盖了一层反光涂层，在不同光线下呈现出微妙的色彩变化，胸甲和四肢护甲的设计线条流畅，贴合人体的同时确保了极高的机动性，每一块护甲板都精密连接，形成密不透风的防护网络。"
Armor02Txt = "\n采用了高级记忆泡沫和智能纤维材料，能够根据战士的体型和战斗强度自动调整，提供最佳的舒适性和防护效果。智能散热系统和空气循环系统使战士在高强度战斗中依然保持体温和体力的稳定。"


ConfigList = [
    {
        "id": "scuke_survive:armor_snow01_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow01_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow01_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装A",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温。帽子覆盖面广，能遮盖头部和大部分面部，只有双眼露出，提供了极高的防护效果。面部区域设计有高透气性的网状结构，不仅保证了良好的视野，还有效防止呼吸时的水汽凝结。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow01_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow01_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow01_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装A",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow01_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow01_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow01_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装A",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow01_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow01_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow01_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装A",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow02_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow02_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow02_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装B",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温，还可以在雪地中伪装。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow02_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow02_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow02_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装B",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温，还可以在雪地中伪装。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow02_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow02_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow02_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装B",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温，还可以在雪地中伪装。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_snow02_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_snow02_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/snow02_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装B",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n内衬配有柔软的保暖层，确保在极低温环境下依然能保持体温，还可以在雪地中伪装。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_safety_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_safety_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/safety_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装C",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n采用了取自金星表面的特殊材料，展现出无与伦比的科技与工艺水平。套装整体呈现出深邃的金属光泽，如同金星表面独有的金黄色反射，闪烁着淡淡的冷光，令人不禁感叹于它的未来感与力量感。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_safety_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_safety_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/safety_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装C",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n采用了取自金星表面的特殊材料，展现出无与伦比的科技与工艺水平。套装整体呈现出深邃的金属光泽，如同金星表面独有的金黄色反射，闪烁着淡淡的冷光，令人不禁感叹于它的未来感与力量感。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_safety_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_safety_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/safety_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装C",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n采用了取自金星表面的特殊材料，展现出无与伦比的科技与工艺水平。套装整体呈现出深邃的金属光泽，如同金星表面独有的金黄色反射，闪烁着淡淡的冷光，令人不禁感叹于它的未来感与力量感。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_safety_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_safety_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/safety_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装C",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n采用了取自金星表面的特殊材料，展现出无与伦比的科技与工艺水平。套装整体呈现出深邃的金属光泽，如同金星表面独有的金黄色反射，闪烁着淡淡的冷光，令人不禁感叹于它的未来感与力量感。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_red_rescue_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_red_rescue_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/red_rescue_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装D",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RedRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_red_rescue_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_red_rescue_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/red_rescue_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装D",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RedRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_red_rescue_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_red_rescue_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/red_rescue_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装D",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RedRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_red_rescue_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_red_rescue_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/red_rescue_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装D",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RedRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_black_rescue_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "red",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_black_rescue_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/black_rescue_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装E",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BlackRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_black_rescue_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "red",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_black_rescue_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/black_rescue_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装E",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BlackRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_black_rescue_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "red",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_black_rescue_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/black_rescue_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装E",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BlackRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_black_rescue_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "red",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_black_rescue_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/black_rescue_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装E",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BlackRescueTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor01_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor01_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor01_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装F",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor01Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor01_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor01_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor01_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装F",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor01Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor01_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor01_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor01_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装F",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor01Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor01_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor01_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor01_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装F",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor01Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor02_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor02_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor02_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装G",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor02Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor02_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor02_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor02_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装G",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor02Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor02_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor02_legs",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor02_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装G",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor02Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_armor02_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_armor02_boots",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor02_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "套装G",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": Armor02Txt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_soviet_tig_helmet_black",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_soviet_tig_helmet_black",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/soviet_tig_helmet_black",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
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
        "id": "scuke_survive:armor_soviet_tig_helmet_silver",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_soviet_tig_helmet_silver",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/soviet_tig_helmet_silver",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
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
        "id": "scuke_survive:armor_soviet_tig_helmet_gold",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_soviet_tig_helmet_gold",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/soviet_tig_helmet_gold",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
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
        "id": "scuke_survive:armor_lead_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lead_boots",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lead_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lead_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lead_chest",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lead_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lead_helme",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lead_helme",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lead_helme",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lead_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lead_legs",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lead_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lithium_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lithium_boots",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lithium_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lithium_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lithium_chest",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lithium_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lithium_helme",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lithium_helme",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lithium_helme",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_lithium_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_lithium_legs",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_lithium_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_rare_earth_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_rare_earth_boots",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_rare_earth_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_rare_earth_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_rare_earth_chest",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_rare_earth_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_rare_earth_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_rare_earth_helmet",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_rare_earth_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_rare_earth_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_rare_earth_legs",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_rare_earth_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_yttrium_boots",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_yttrium_boots",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_yttrium_boots",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_yttrium_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_yttrium_chest",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_yttrium_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_yttrium_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_yttrium_helmet",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_yttrium_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_yttrium_legs",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:armor_yttrium_legs",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_yttrium_legs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:armor_green_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_green_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_green_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这顶绿色的帽子，仿佛在诉说着一个故事。也许曾经见证过一段刻骨铭心的爱情，也或许经历过一次伤痛的背叛。它承载着主人的喜怒哀乐，见证着主人的成长与蜕变。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_tattered_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_tattered_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_tattered_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这顶帽子虽然已经褪色，但依然散发着一种独特的光芒。它承载着历史的厚重，也见证着时代的变迁。好在其做工的扎实以至于虽然打满补丁但仍旧能抵御寒冷。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_tattered_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_tattered_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_tattered_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这件大衣虽然已经褪色，但依然散发着一种独特的光芒。它承载着历史的厚重，也见证着时代的变迁。好在其做工的扎实以至于虽然打满补丁但仍旧能抵御寒冷。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_red_mask_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_red_mask_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_red_mask_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\nY~M~C~A~戴上这一个面罩就让人情不自禁的哼出这段强劲的音乐。这个面罩，也许代表着一种对“我的世界”的热爱和期盼。也可能代表着一种对现状的不满。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_red_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_red_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_red_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\nY~M~C~A~戴上这一顶帽子就让人情不自禁的哼出这段强劲的音乐。这顶帽子，也许代表着一种对“我的世界”的热爱和期盼。也可能代表着一种对现状的不满。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_military_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_military_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_military_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这顶帽子朴实无华却散发着一种独特的光芒。它材质柔软，做工精良，可以抵御寒风和雨雪。它也象征着奉献，象征着爱。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_military_chest",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_military_chest",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_military_chest",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这件军绿色军大衣，朴实无华，却散发着一种独特的魅力。材质厚实，做工精良，可以抵御寒风和雨雪。它承载着历史的厚重，也见证着时代的变迁。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_skull_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_skull_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_skull_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这是反叛军的专属帽子，上面的骷髅图案代表着死亡，也代表着反抗。它象征着“反叛军”视死如归的决心，也象征着他们对于心目中压迫和不公的反抗。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_skull_mask_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "yellow",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_skull_mask_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_skull_mask_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这是反叛军的专属面罩，上面的骷髅图案代表着死亡，也代表着反抗。它象征着“反叛军”视死如归的决心，也象征着他们对于心目中压迫和不公的反抗。"  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:armor_skull_hood_helmet",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "gold",
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:entity_skull_hood_helmet",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "armor/armor_skull_hood_helmet",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ["", "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "\n这是反叛军的专属面罩，上面的骷髅图案代表着死亡，也代表着反抗。一般只有大人物才会佩戴。它象征着“反叛军”视死如归的决心，也象征着他们对于心目中压迫和不公的反抗。"  # 详细描述文字
                }
            ]
        }
    },
]
