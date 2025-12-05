# -*- encoding: utf-8 -*-
MobMolangDict = {        # 传入molang变量，控制动画
                "variable.doll_rotate": 0.0,        # 纸娃娃旋转变量，暂时没用
                "variable.hurt_effect": 0.0,        # 对应生物的这个变量，防止报错
                "variable.swim_amount": 0.0,        # 同上
                "variable.attack_time": 0.0,        # 同上
                "variable.gliding_speed_value": 0.0,    # 同上
                "variable.damage_nearby_mobs": 0.0,     # 同上
                "variable.ischarging": 0.0,             # 同上
                "variable.is_brandishing_spear": 0.0,   # 同上
                "variable.is_holding_spyglass": 0.0,    # 同上
                "variable.not_in_ui": 0.0,       # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0         # 是否启动控件点位修正
            }

ConfigList = [
    {
        "id": "scuke_survive:rebel_ragman",    # 标记ID
        "cardType": "green",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:rebel_ragman",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 0,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/rebel_ragman",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "20", 1],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "pistol",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "传记",      # 技能大字
                    "damageText": "",      # 伤害文字
                    "mainText": "自从妻子神秘失踪后，他日夜搜寻未果。最终决定加入反叛军，这不仅是为了对抗不公，更是希望通过组织的行动网络，获取更多关于妻子下落的线索。每次外出执行任务，他都格外留意可能的相关信息，将寻妻的希望寄托在每一次行动中。"        # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:rebel_vagrant",    # 标记ID
        "cardType": "blue",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:rebel_vagrant",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 0,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/rebel_vagrant",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "20", 3],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "pistol",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "传记",      # 技能大字
                    "damageText": "",      # 伤害文字
                    "mainText": "在反叛军中，流浪者的身份始终成谜。她虽是女性，却拥有惊人的战斗力，每一次出击都令人震撼。她极少言语，神情冷峻，仿佛与世隔绝，令人感到深不可测。"
                }
            ]
        }
    },
    {
        "id": "scuke_survive:rebel_soldier",
        "cardType": "blue",
        "chineseName": "",
        "showType": "paperDoll",
        "paperDollData":{
            "entity_identifier": "scuke_survive:rebel_soldier",
            "scale": 0.95,
            "render_depth": -1000,
            "init_rot_y": 0,
            "init_rot_x": 0,
            "rotation_axis": (0, 0, 0),
            "molang_dict": MobMolangDict
        },
        "detailCardData":{
            "imagePath": "entity/rebel_soldier",
            "baseData": ['medium', "1.8", "1.0", "30", 3],
            "content":[
                {
                    "iconPath": "pistol",
                    "headText": "传记",
                    "damageText": "",
                    "mainText": "铁蛋脸上的刀疤足有十公分长，皮肉外翻，在昏暗的灯光下泛着暗红。这个反叛军老兵每次咧嘴笑时，疤痕都会随之扭曲，仿佛一张咧开的第二张嘴。那是在地下实验室突围时，为救同伴被僵尸抓伤的印记，也是他距离死亡最近的一次。"
                }
            ]
        }
    },
    {
        "id": "scuke_survive:rebel_leader",
        "cardType": "gold",
        "chineseName": "",
        "showType": "paperDoll",
        "paperDollData":{
            "entity_identifier": "scuke_survive:rebel_leader",
            "scale": 0.95,
            "render_depth": -1000,
            "init_rot_y": 0,
            "init_rot_x": 0,
            "rotation_axis": (0, 0, 0),
            "molang_dict": MobMolangDict
        },
        "detailCardData":{
            "imagePath": "entity/rebel_leader",
            "baseData": ['medium', "1.8", "1.0", "70", 4],
            "content":[
                {
                    "iconPath": "pistol",
                    "headText": "传记",
                    "damageText": "",
                    "mainText": "炯大帅因其炯炯有神的大眼睛而得名，那双眼睛仿佛能洞察一切。作为反叛军领袖，他总能在危机前嗅到危险，带领队伍化险为夷。无论是突袭还是埋伏，他总能凭借敏锐的直觉提前做出精准判断。他的眼睛不仅是标志，更是领导力的象征，令部下充满信任与敬畏。"
                }
            ]
        }
    },
]
