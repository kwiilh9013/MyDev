# -*- encoding: utf-8 -*-
GunMolangDict = {  # 传入molang变量，控制动画
                "variable.not_in_ui": 0.0,  # 标记生物是否在UI内，如果在UI内就不启动某些动画
                "variable.correct_pos": 1.0  # 是否启动控件点位修正
            }

HmgTxt = "\n这把末日废土中的重型机关枪，以其无情的火力和惊人的破坏力而闻名。枪身覆满岁月的锈迹，却仍然在废土的荒原上闪闪发光，仿佛来自末世的绝望呼啸。"
SmgTxt = "\n其流线型金属外壳散发出冰冷的光泽，能量线路如同星空中的脉络。可穿透敌人的防线，让人仿佛置身于未来战场的边缘地带。"
LmgTxt = "\n相比于传统的能量机枪，它射速极快，几乎没有后坐力，让你在激烈的战斗中仍能保持精确的射击，给你带来压倒性的战斗优势。"
SniperTxt = "\n只需短短几秒便可完成充能，发射的脉冲光波不仅具有极强的穿透力，更能在瞬间瓦解泰坦的防御，将其轰然击倒。"
ShotGunTxt = "\n每次射击可喷射出10颗子弹，覆盖广泛，火力凶猛。尽管后坐力较大，但其半自动机制使你能够快速连续射击，在短时间内对敌人造成毁灭性打击"
RifleTxt = "\n仿佛一件来自未来的科技杰作。弹匣设计在枪托旁边，极为靠后，将重心集中于肩部，增强了射击的稳定性。"
PistolTxt = "\n其独特的外观设计酷似一把加油枪，兼具美观与实用。枪身主体以黑色和白色为主色调，线条流畅，造型前卫，给人一种未来科技的感觉。"
BazookaTxt = "\n是末日战场上对抗巨型敌人的终极武器。其庞大的枪身涂装为深沉的黑色与闪耀的银色，透露出一股冰冷而致命的气息。每一个细节都精雕细琢，展现出未来科技的巅峰之作。"
AxeTxt = "\n无论面对何种险境，这把斧头都是战士们不可或缺的伙伴，象征着勇气、力量与坚韧。"
BaseBallBatTxt = "\n棍身上刻有深深的划痕，那是经历无数次战斗后的荣誉勋章。可蓄力击打，击打时能产生巨大的冲击力，一击便能打碎敌人的骨骼，甚至撕裂他们的防具。"
ChainsawTxt = "\n每一次启动，锯齿都会带着狂暴的力量，撕裂一切挡在面前的障碍。无论是单个僵尸，还是成群的尸潮，这把电锯都能在瞬间将其碾碎成碎片。"
PigSawTxt = "\n象征着野性与力量的完美结合。手握这把电锯，战士们仿佛化身为狂野的野猪，无所畏惧地冲向敌人，将毁灭与死亡带向他们的对手。"
PanTxt = "\n好用的平底锅"


ConfigList = [
    {
        "id": "scuke_survive:gun_hmg1",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_hmg1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_hmg1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5)
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": HmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_hmg1_s1",  # 标记ID
        "cardType": "red",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_hmg1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_hmg1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5)
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": HmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_hmg1_s2",  # 标记ID
        "cardType": "red",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_hmg1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_hmg1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5)
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": HmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_smg1",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_smg1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_smg1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": SmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_smg1_s2",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_smg1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_smg1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": SmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_smg1_s3",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_smg1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_smg1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": SmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_lmg1",  # 标记ID
        "cardType": "red",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_lmg1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_lmg1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": LmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_lmg1_s1",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_lmg1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_lmg1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": LmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_lmg1_s2",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_lmg1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_lmg1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": LmgTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_sniper1",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_sniper1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_sniper1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": SniperTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_sniper1_s1",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_sniper1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_sniper1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": SniperTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_sniper1_s2",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_sniper1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_sniper1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": SniperTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_shotgun1",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_shotgun1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_shotgun1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ShotGunTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_shotgun1_s2",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_shotgun1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_shotgun1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ShotGunTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_shotgun1_s3",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_shotgun1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_shotgun1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ShotGunTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_rifle1",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_rifle1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_rifle1",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RifleTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_rifle1_s1",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_rifle1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_rifle1_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RifleTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_rifle1_s2",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_rifle1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_rifle1_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": RifleTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_pistol1",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_pistol1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_pistol1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PistolTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_pistol1_s2",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_pistol1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_pistol1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PistolTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_pistol1_s3",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_pistol1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_pistol1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PistolTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_bazooka1",  # 标记ID
        "cardType": "red",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_bazooka1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_bazooka1_grain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BazookaTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_bazooka1_s1",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_bazooka1_s1",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_bazooka1_grain_02",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BazookaTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:gun_bazooka1_s2",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:gun_entity_bazooka1_s2",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "gun/gun_bazooka1_grain_03",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BazookaTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_axe",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:axe_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": AxeTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_axe_red",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:axe_red_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe_red",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": AxeTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_axe_golden",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:axe_golden_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe_golden",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": AxeTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_baseball_bat",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:baseball_bat_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/baseball_bat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BaseBallBatTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_baseball_bat_m",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:baseball_bat_m_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/baseball_bat_m",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BaseBallBatTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_baseball_bat_golden",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:baseball_bat_golden_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/baseball_bat_golden",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": BaseBallBatTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_chainsaw",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:chainsaw_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/chainsaw",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ChainsawTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_chainsaw_old",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:chainsaw_old_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/chainsaw_old",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ChainsawTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_chainsaw_golden",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:chainsaw_golden_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/chainsaw_golden",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": ChainsawTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_pigsaw",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:pigsaw_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pigsaw",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PigSawTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_pigsaw_golden",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:pigsaw_golden_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pigsaw_golden",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PigSawTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_pan_copper",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:pan_copper_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pan_copper",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PanTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_pan",  # 标记ID
        "cardType": "purple",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:pan_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pan",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PanTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:melee_pan_golden",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:pan_golden_entity",  # 实体ID
            "scale": 1.0,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": GunMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pan_golden",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": PanTxt  # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:axe_lead",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:axe_lead",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:axe_lithium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:axe_lithium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:axe_rare_earth",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:axe_rare_earth",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:axe_yttrium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:axe_yttrium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/axe_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:hoe_lead",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:hoe_lead",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/hoe_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:hoe_lithium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:hoe_lithium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/hoe_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:hoe_rare_earth",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:hoe_rare_earth",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/hoe_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:hoe_yttrium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:hoe_yttrium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/hoe_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:pickaxe_lead",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:pickaxe_lead",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pickaxe_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:pickaxe_lithium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:pickaxe_lithium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pickaxe_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:pickaxe_rare_earth",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:pickaxe_rare_earth",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pickaxe_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:pickaxe_yttrium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:pickaxe_yttrium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/pickaxe_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:shovel_lead",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:shovel_lead",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/shovel_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:shovel_lithium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:shovel_lithium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/shovel_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:shovel_rare_earth",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:shovel_rare_earth",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/shovel_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:shovel_yttrium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:shovel_yttrium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/shovel_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:sword_lead",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "green",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:sword_lead",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/sword_lead",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:sword_lithium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "blue",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:sword_lithium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/sword_lithium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:sword_rare_earth",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:sword_rare_earth",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/sword_rare_earth",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
        "id": "scuke_survive:sword_yttrium",  # 标记ID
        "chineseName": "",  # 显示的中文字
        "cardType": "purple",
        "showType": "itemRender",  # 显示类型，可选paperDoll，image，itemRender
        "itemRenderData": {  # 当showType为itemRender时启动
            "itemName": "scuke_survive:sword_yttrium",  # 物品ID
            "auxValue": 0,  # 特殊值
            "enchant": False,  # 是否附魔
            "userData": {},  # 物品数据
            "alpha": 1.0  # 不透明度
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "melee/sword_yttrium",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
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
]
