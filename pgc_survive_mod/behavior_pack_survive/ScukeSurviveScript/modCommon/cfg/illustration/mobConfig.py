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
        "id": "scuke_survive:zombie_normal",    # 标记ID
        "cardType": "green",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_normal",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 180,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "imageData": {      # 当showType为image时启动
            "path": "textures/ui/scuke_survive/task/img_p_earth",       # 自定义贴图路径
        },
        "itemRenderData":{      # 当showType为itemRender时启动
            "itemName": "minecraft:apple",      # 物品ID
            "auxValue": 0,      # 特殊值
            "enchant": False,   # 是否附魔
            "userData": {},      # 物品数据
            "alpha": 1.0        # 不透明度
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/zombie_normal",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "10", 1],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "啃咬",      # 技能大字
                    "damageText": "2",      # 伤害文字
                    "mainText": "长时间的加班使得它们身体脆弱不堪。虽然伤害像挠痒痒一样，但是在庞大的数量面前也不要掉以轻心。"        # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_baby",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_baby",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_baby",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['small', "1.0", "0.3", "6", 1],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "嗷嗷待哺",  # 技能大字
                    "damageText": "1",  # 伤害文字
                    "mainText": "小小的也很可爱，可别被这小巧玲珑的体型所蒙蔽，脖子上被狠狠咬上一口就知道它的厉害了！"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_gangs",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_gangs",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_gangs",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "22", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "啃咬",  # 技能大字
                    "damageText": "3",  # 伤害文字
                    "mainText": "长时间混迹街头显然对于变成僵尸之后是很有效果的：不仅皮糙肉厚，丰富的格斗经验也是很大的威胁。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_chick",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_chick",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_chick",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1", "20", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "啃咬",  # 技能大字
                    "damageText": "5",  # 伤害文字
                    "mainText": "别看她们身材娇小火辣，啃起幸存者的速度来可丝毫不落于其他僵尸！伤害更是有过之而无不及。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_guard",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_guard",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_guard",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "20", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "电机疗法",  # 技能大字
                    "damageText": "4",  # 伤害文字
                    "mainText": "我是一名保安，保卫一方平安。对待曾经的业主，保安们可不会丝毫的手软！小心他们的电击枪！"
                    # 详细描述文字
                },
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "擒拿",  # 技能大字
                    "damageText": "1",  # 伤害文字
                    "mainText": "大概天天躲在岗亭里睡大觉，虽然每天早上练习的擒拿拳都绵软无力，但遇到歹徒跑得比谁都快。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_dog",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_dog",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_dog",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['small', "1.5", "0.6", "16", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "撕咬",  # 技能大字
                    "damageText": "9",  # 伤害文字
                    "mainText": "曾经在主人怀里撒娇打滚的小狗如今已经变得凶残无比，请用砍刀和猎枪招呼，而不是关心和爱。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_explosive",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_explosive",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_explosive",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.2", "1.0", "20", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "boom",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "轰轰爆破",  # 技能大字
                    "damageText": "0",  # 伤害文字
                    "mainText": "叮叮叮叮叮叮，什么声音？幸存者以为是叫幸存者起床的闹铃响吗？别再沉浸在美梦当中了！要爆炸了快跑！"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_fat",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_fat",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_fat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.2", "1.8", "22", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "横冲直撞",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "脂肪不会随着变成僵尸而逐渐消失，而是腐烂膨胀。小心别被他碰到，不然身上的腥臭味一周也散不尽。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_grandpa",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_grandpa",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_grandpa",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.0", "1.0", "16", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "倚老卖老",  # 技能大字
                    "damageText": "9",  # 伤害文字
                    "mainText": "闪烁的老花镜，老北京比基尼，可不要以为是邻居家的老大爷。当幸存者把它的报纸不小心碰掉就会知道什么叫老当益壮。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_otaku",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_otaku",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_otaku",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.5", "1.8", "40", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "爱的拥抱",  # 技能大字
                    "damageText": "3",  # 伤害文字
                    "mainText": "变成僵尸的肥宅对世界充满了幻想，只不过表达爱意的力度不太好掌握。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "爱的守护",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "衷情的肥宅对于幸存者的侵犯很不满意！为了守护住最美好的幻想而咆哮！"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_venom",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_venom",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_venom",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.2", "1.0", "20", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "腐蚀毒液",  # 技能大字
                    "damageText": "4",  # 伤害文字
                    "mainText": "通过变异，这种身上长满脓包的怪物掌握了远程喷吐毒液的技能。不光看着恶心，并且有着剧毒。"
                    # 详细描述文字
                },
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "毒牙攻击",  # 技能大字
                    "damageText": "1",  # 伤害文字
                    "mainText": "没有人想挨上这怪物的一口，虽然伤口并不致命，但恶心的感觉会持续很长时间。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_jocker",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_jocker",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_jocker",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.2", "1.0", "12", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "boom",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "海盗桶",  # 技能大字
                    "damageText": "6",  # 伤害文字
                    "mainText": "在马戏团滑稽的小丑，变成僵尸后笑的格外瘆人。蹦蹦跳跳的海盗桶滚向幸存者时，并不是游戏而是爆炸。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "危险拥抱",  # 技能大字
                    "damageText": "15",  # 伤害文字
                    "mainText": "当看到小丑僵尸举着手向幸存者走来时，绝对不是想和幸存者进行拥抱，而是向幸存者发起攻击！"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_giant",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_giant",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_giant",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['large', "5", "3.5", "32", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "巨力践踏",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "为了守护它同样变成僵尸的孩子，任何侵犯它领地的幸存者都会遭到无情的追杀。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "舐犊情深",  # 技能大字
                    "damageText": "0",  # 伤害文字
                    "mainText": "在迫不得已的情况时会将身上的幼年僵尸抛出，而它也将会战斗到最后一刻。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_sarcoma",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_sarcoma",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_sarcoma",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['large', "5.0", "5.0", "44", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "波涛汹涌",  # 技能大字
                    "damageText": "6",  # 伤害文字
                    "mainText": "当一团肉瘤向幸存者涌来时，就好像无情的泥沼想要吞噬着一切。只有远离才是最好的生存方式。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "投尸车",  # 技能大字
                    "damageText": "0",  # 伤害文字
                    "mainText": "肉瘤就像是一个巨大的弹簧一样，能够将被吞噬的僵尸高高的抛出。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_flyinglava",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_flyinglava",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_flyinglava",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "3.0", "1.5", "300", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "从天而降",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "火球并不能让人感受到温暖，当它向幸存者发射火球时，更能体验到的是从头到脚的寒意。"
                    # 详细描述文字
                }
            ]
        }
    },
    # 变种僵尸↓↓↓
    {
        "id": "scuke_survive:zombie_captain",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_captain",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_captain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "22", 2],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "愤怒啃咬",  # 技能大字
                    "damageText": "3",  # 伤害文字
                    "mainText": "中年失业大叔的威力可不容小觑，将房贷和车贷还不上的愤怒化成的攻击力，幸存者敢接下这一拳吗？"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_gangs_captain",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_gangs_captain",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_gangs_captain",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.2", "1.2", "16", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "黑手袭击",  # 技能大字
                    "damageText": "9",  # 伤害文字
                    "mainText": "大金链子小手表，曾经的帮派头目虽然没有街头混混的皮糙肉厚，但是下起手来是绝对的心狠手辣。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_spicy_chick",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_spicy_chick",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_spicy_chick",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.1", "1.1", "20", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "鬼魅啃咬",  # 技能大字
                    "damageText": "6",  # 伤害文字
                    "mainText": "火红的短发显得格外显眼，蓝色皮肤却又在雪地里隐藏的极好。夜里仿佛一团红色的火焰来夺走幸存者的生命。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_special_guard",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_special_guard",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_guard_leader",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.1", "1.1", "16", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "格斗术",  # 技能大字
                    "damageText": "5",  # 伤害文字
                    "mainText": "退伍老兵的加持使其打出的拳法格外孔武有力。这可不是那些普通的保安僵尸所能比拟的。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_supertnt",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_supertnt",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_explosive_sup",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.3", "1.1", "24", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "boom",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "爆炸盛宴",  # 技能大字
                    "damageText": "0",  # 伤害文字
                    "mainText": "叮叮叮叮叮叮，又是自爆僵尸？快揉揉眼睛，胸口怎么有辐射标志！？看起来威力可比自爆僵尸大多了。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_tons_king",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_tons_king",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_fat_sup",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.2", "1.8", "26", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "天旋地转",  # 技能大字
                    "damageText": "9",  # 伤害文字
                    "mainText": "不光是被碰到后带来的腥臭味挥之不去，被他撞击后仿佛五脏六腑都在翻腾，丝毫不亚于一辆全险半挂。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_hypertension_grandpa",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_hypertension_grandpa",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_grandpa_high",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.0", "1.0", "23", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "投资需谨慎",  # 技能大字
                    "damageText": "3",  # 伤害文字
                    "mainText": "幸存者的脸怎么红了？精神焕发！显然大爷的脸红并不是气色好，手中报纸狂跌的股价或许就是答案。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_otaku_black",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_otaku_black",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_otaku_black",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "3.0", "2.16", "20", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "腹黑冲击",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "千万可不要被它看到，否则会不顾一切的想要占有每一个所见到幸存者。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "病娇嘶吼",  # 技能大字
                    "damageText": "12",  # 伤害文字
                    "mainText": "越是得不到的就越想要，它会将心中的不甘发泄在无能的咆哮当中！"
                    # 详细描述文字
                },
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_flame_venom",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_flame_venom",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_venom_fire",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.64", "1.2", "20", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "烈焰灼烧",  # 技能大字
                    "damageText": "4",  # 伤害文字
                    "mainText": "这种恶心的喷吐物在火焰的加持下味道更加刺鼻，恶心的同时还有一股焦臭的味道。小心不要被击中。"
                    # 详细描述文字
                },
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "怒火撕咬",  # 技能大字
                    "damageText": "6",  # 伤害文字
                    "mainText": "被这怪物啃上一口，可不光是咬伤，还有烧伤！"
                    # 详细描述文字
                },
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_big",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_big",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_normal_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['large', "5.4", "3.0", "50", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "狂暴重拳",  # 技能大字
                    "damageText": "10",  # 伤害文字
                    "mainText": "一个绿色的巨人向幸存者挥拳，可不要以为浑身的肌肉是中看不中用的花架子，只有挨上了才知道是什么滋味。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_golden_chick",  # 标记ID
        "cardType": "green",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_golden_chick",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_chick_gold",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.16", "1.2", "24", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "金光闪耀",  # 技能大字
                    "damageText": "13",  # 伤害文字
                    "mainText": "闪闪发光的黄金辣妹打到身上的攻击仿佛也有一股金钱的香气。虽然很痛，但也是多少猪灵的梦中情人。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_big_dog",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_big_dog",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_dog_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.25", "0.9", "40", 3],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "地狱撕咬",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "白蓝色的皮肤是在雪地中最好的伪装，擦亮眼睛，当它发起进攻时往往已经是最后的绝杀。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_jocker_king",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_jocker_king",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_jocker_dc",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.64", "1.2", "26", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "boom",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "混乱之桶",  # 技能大字
                    "damageText": "6",  # 伤害文字
                    "mainText": "患有狂笑症的小丑僵尸无时无刻不在咯咯的笑个不停。从他手中抛出的桶可绝不可能是什么好东西。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "小丑病毒",  # 技能大字
                    "damageText": "36",  # 伤害文字
                    "mainText": "当看到小丑僵尸咯咯笑着向幸存者走来时，绝对不是想和幸存者进行拥抱，而是向幸存者发起攻击！"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_big_giant",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_big_giant",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_normal_titan",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['large', "9.0", "5.0", "100", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "重拳轰击",  # 技能大字
                    "damageText": "50",  # 伤害文字
                    "mainText": "那一天，人类回想起了，在它们支配之下的恐怖，还有那被囚禁于鸟笼中的那份耻辱。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_black_venom",  # 标记ID
        "cardType": "blue",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_black_venom",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_venom_marvel",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "4.4", "2.0", "80", 4],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "毒牙撕咬",  # 技能大字
                    "damageText": "3",  # 伤害文字
                    "mainText": "任何一名幸存者都不想被这满嘴的尖牙咬上一口。看到它的嘴身上就已经开始疼了。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "毒液狂潮",  # 技能大字
                    "damageText": "12",  # 伤害文字
                    "mainText": "被这团黑色的毒液沾上可不会让你变成埃迪·布洛克，而是被腐蚀成一团肉泥。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_giant_king",  # 标记ID
        "cardType": "gold",
        "chineseName": "",  # 显示的中文字
        "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
        "paperDollData": {  # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_giant_king",  # 实体ID
            "scale": 0.95,  # 模型渲染大小
            "render_depth": -1000,  # 渲染深度
            "init_rot_y": 180,  # 默认旋转角度y
            "init_rot_x": 0,  # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData": {  # 卡片数据 绿卡
            "imagePath": "entity/zombie_giant_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['large', "10.0", "7.0", "600", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content": [  # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "踏地震天",  # 技能大字
                    "damageText": "8",  # 伤害文字
                    "mainText": "为了守护它同样变成僵尸的孩子，任何侵犯它领地的幸存者都会遭到无情的追杀。"
                    # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "舐犊情深",  # 技能大字
                    "damageText": "0",  # 伤害文字
                    "mainText": "在迫不得已的情况时会将身上的幼年僵尸抛出，而它也将会战斗到最后一刻。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_giant_sarcoma",    # 标记ID
        "cardType": "gold",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_giant_sarcoma",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 180,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/zombie_sarcoma_large",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['large', "10.0", "10.0", "500", 5],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "汹涌澎湃",      # 技能大字
                    "damageText": "10",      # 伤害文字
                    "mainText": "拥有适应严寒的深蓝色皮肤，运动起来时像是大海的波浪一样波涛起伏。但幸存者绝不想这团波浪向幸存者涌来。"        # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "投尸车",      # 技能大字
                    "damageText": "0",      # 伤害文字
                    "mainText": "肉瘤就像是一个巨大的弹簧一样，能够将被吞噬的僵尸高高的抛出。小心点，可千万别被砸中！"        # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_witch_normal",    # 标记ID
        "cardType": "blue",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_witch_normal",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 180,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/zombie_witch_normal",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "20", 3],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "惊扰突袭",  # 技能大字
                    "damageText": "5",  # 伤害文字
                    "mainText": "原地发出低沉而悠长的哭泣声。千万不要惊扰她。"  # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "怨念召唤",  # 技能大字
                    "damageText": "",  # 伤害文字
                    "mainText": "惊扰并发起攻击的同时，借助怨念之力，从周围的迷雾中召唤出其他怪物，与它一同对目标发起进攻。"
                    # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_witch",    # 标记ID
        "cardType": "gold",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_witch",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 180,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/zombie_witch",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "1.8", "1.0", "100", 4],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "惊扰突袭",      # 技能大字
                    "damageText": "30",      # 伤害文字
                    "mainText": "原地发出低沉而悠长的哭泣声。千万不要惊扰尖叫者。"        # 详细描述文字
                },
                {
                    "iconPath": "remote_attack",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "怨念召唤",      # 技能大字
                    "damageText": "",      # 伤害文字
                    "mainText": "惊扰并发起攻击的同时，借助怨念之力，从周围的迷雾中召唤出其他怪物，与它一同对目标发起进攻。"        # 详细描述文字
                }
            ]
        }
    },
    {
        "id": "scuke_survive:zombie_snap_killer",    # 标记ID
        "cardType": "gold",
        "chineseName": "",      # 显示的中文字
        "showType": "paperDoll",    # 显示类型，可选paperDoll，image，itemRender
        "paperDollData":{           # 当showType为paperDoll时启动
            "entity_identifier": "scuke_survive:zombie_snap_killer",     # 实体ID
            "scale": 0.95,   # 模型渲染大小
            "render_depth": -1000,   # 渲染深度
            "init_rot_y": 180,    # 默认旋转角度y
            "init_rot_x": 0,    # 默认旋转角度x
            "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
            "molang_dict": MobMolangDict
        },
        "detailCardData":{      # 卡片数据 绿卡
            "imagePath": "entity/zombie_snap_killer",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
            "baseData": ['medium', "2.0", "1.0", "500", 5],   # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
            "content":[         # 详情描述，字典作为富文本
                {
                    "iconPath": "combat",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "利爪斩击",      # 技能大字
                    "damageText": "30",      # 伤害文字
                    "mainText": "扑杀者挥动强力的爪子，对前方的目标发起一次迅猛的攻击。试图撕开目标的防御。"        # 详细描述文字
                },
                {
                    "iconPath": "combat",   # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
                    "headText": "跃击突袭",      # 技能大字
                    "damageText": "10",      # 伤害文字
                    "mainText": "扑杀者用力一跃，向目标快速扑去。用爪子和力量将目标击倒。"        # 详细描述文字
                },
            ]
        }
    },
    # {
    #     "id": "scuke_survive:camel_electric",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:camel_electric",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_iron_golem",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_iron_golem",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_moss",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_moss",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_robot",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_robot",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_scientist",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_scientist",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_golden_creeper",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_golden_creeper",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_igniter",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_igniter",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_trader",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_trader",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
    # {
    #     "id": "scuke_survive:npc_wheelchair_man",  # 标记ID
    #     "cardType": "gold",
    #     "chineseName": "",  # 显示的中文字
    #     "showType": "paperDoll",  # 显示类型，可选paperDoll，image，itemRender
    #     "paperDollData": {  # 当showType为paperDoll时启动
    #         "entity_identifier": "scuke_survive:npc_wheelchair_man",  # 实体ID
    #         "scale": 0.95,  # 模型渲染大小
    #         "render_depth": -1000,  # 渲染深度
    #         "init_rot_y": 180,  # 默认旋转角度y
    #         "init_rot_x": 0,  # 默认旋转角度x
    #         "rotation_axis": (0, 0, 0),  # 控制绕什么轴旋转
    #         "molang_dict": MobMolangDict
    #     },
    #     "detailCardData": {  # 卡片数据 绿卡
    #         "imagePath": "entity/zombie_sarcoma_large",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #         "baseData": ['', "", "", "", 5],  # 基本数据，依次为：体型（small-medium-large）、高度、宽度、血量、稀有度（1-5）
    #         "content": [  # 详情描述，字典作为富文本
    #             {
    #                 "iconPath": "icon_bg",  # 贴图路径，需要放在res/textures/ui/scuke_survive/illustration/ 下
    #                 "headText": "",  # 技能大字
    #                 "damageText": "",  # 伤害文字
    #                 "mainText": "【NPC生物】"
    #                 # 详细描述文字
    #             }
    #         ]
    #     }
    # },
]
