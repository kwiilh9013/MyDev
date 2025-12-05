# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.cfg.struct import structConfig


"""
一键建造配置表
"""


# region 参数

# 范围实体id
BuildRangeEngineTypeStr = "scuke_survive:build_entity"
# 建造特效实体
BuildingEffectEngineTypeStr = "scuke_survive:build_effect_entity"

# 建造道具id
BuildItemName = "scuke_survive:build_struct"

# 生成建筑的频率，默认0.05秒
BuildStructTimerCD = 0.05
# 一次生成的方块数量，默认1秒
OnceBuildBlockCount = 3

# 旧方块处理方式：0=直接替换，1=旧方块掉落
OldBlockHandling = 0

# 区块不加载时，tick逻辑停止的时长，秒
WaitingChunkTime = 5

# 同时建造的数量上限
BuildingLogicMaxCount = 3

# 获取准星位置的timer更新频率，默认0.5/秒
GetCrossPosTime = 0.5
# 准星位置最大距离，使用曼哈顿距离来判断（这里不需要精准的距离判断）
GetCrossMaxDistance = 48
GetCrossMaxDistanceManhattan = GetCrossMaxDistance * 2

# 特效id
BuildEffects = {
    "scuke_survive:build_struct_boom": {"delay_time": 2,},
}
# 音效
BuildSound = "dig.stone"

# 需给玩家挂上的动画
AddAnimations = {
    "animKey": "buildgun_in_hand_idle",
    "animName": "animation.scuke_survive_player.third_hand_up",
    "condition": "!variable.is_first_person && query.get_equipped_item_name == '{}'".format(BuildItemName.split(":")[1]),
}
# endregion


# region 提示信息
# 提示显示的时长，秒
TipsShowTime = 4

_TipsDict = {
    1: "建造材料不够，请收集足够材料后放在背包里。",
    11: "解锁",
    12: "锁定",
    13: "确定",
    14: "预览",

    51: "同时建造的建筑已达到上限，请等待其他建筑建造完成！",
}
def GetTips(tipId):
    return _TipsDict.get(tipId, "")

# endregion


# region 建筑数据
class StructEnum:
    """建筑id枚举"""

    # FortressHight = "fortress_hight"
    # """高碉堡"""
    # FortressBase = "fortress_base"
    # """碉堡底座"""
    FortressTower = "fortress_tower"
    """塔楼"""

    WallLine = "wall_line"
    """直线围墙"""
    WallSlant = "wall_slant"
    """斜线围墙"""

    RoadLine = "road_line"
    """直线道路"""
    Road90 = "road_90"
    """90度道路"""
    # RoadU = "road_u"
    # """U型道路"""
    RoadUphill = "road_uphill"
    """上坡道路"""

    TentSmall = "tent_small"
    """小帐篷"""
    TentLarge = "tent_large"
    """大帐篷"""

    # Refuge = "refuge"
    # """避难所"""
    # RepairStation = "repair_station"
    # """维修站"""
    
    

# 建筑的调色板字典数据
# volume = 体积（长宽高，以x+为正方向）,即坐标关系是(z,x,y)
_StructPaletteDicts = {
    # 碉堡
    # StructEnum.FortressHight: structConfig.FortressHight,
    # StructEnum.FortressBase: structConfig.FortressBase,
    StructEnum.FortressTower: structConfig.FortressTower,
    # 围墙
    StructEnum.WallLine: structConfig.WallLine,
    StructEnum.WallSlant: structConfig.WallSlant,
    # 道路
    StructEnum.RoadLine: structConfig.RoadLine,
    StructEnum.Road90: structConfig.Road90,
    # StructEnum.RoadU: structConfig.RoadU,
    StructEnum.RoadUphill: structConfig.RoadUphill,
    # 帐篷
    StructEnum.TentSmall: structConfig.TentSmall,
    StructEnum.TentLarge: structConfig.TentLarge,
    # 避难所
    # StructEnum.Refuge: structConfig.Refuge,
    # StructEnum.RepairStation: structConfig.RepairStation,
}
def GetStructPaletteDict(structId):
    """获取建筑的调色板数据"""
    return _StructPaletteDicts.get(structId)

def GetBlockGeoKey(structId):
    """获取方块几何体的key"""
    return "scuke_servive_build_struct_geo_{}".format(structId)

# endregion


# region 需旋转的方块数据
# val填写的是aux变化的顺序，之后根据转向幅度直接获取值
_aux0213 = (0, 2, 1, 3,  4, 6, 5, 7,  8, 10, 9, 11,)
_aux0123 = (0, 1, 2, 3,)
_aux4253 = (4, 2, 5, 3,)
_aux12 = (1, 2,)
_RotateBlockAuxDict = {
    # 楼梯：0 2 1 3顺序
    'minecraft:mangrove_stairs': _aux0213, 'minecraft:oak_stairs': _aux0213, 'minecraft:stone_stairs': _aux0213, 
    'minecraft:smooth_sandstone_stairs': _aux0213, 'minecraft:mossy_stone_brick_stairs': _aux0213, 'minecraft:sandstone_stairs': _aux0213, 
    'minecraft:spruce_stairs': _aux0213, 'minecraft:birch_stairs': _aux0213, 'minecraft:bamboo_stairs': _aux0213, 
    'minecraft:red_sandstone_stairs': _aux0213, 'minecraft:mossy_cobblestone_stairs': _aux0213, 'minecraft:stone_brick_stairs': _aux0213, 
    'minecraft:jungle_stairs': _aux0213, 'minecraft:dark_oak_stairs': _aux0213, 'minecraft:normal_stone_stairs': _aux0213, 
    'minecraft:acacia_stairs': _aux0213, 'minecraft:cherry_stairs': _aux0213, 'minecraft:smooth_red_sandstone_stairs': _aux0213, 
    'minecraft:bamboo_mosaic_stairs': _aux0213, 'minecraft:prismarine_stairs': _aux0213, 'minecraft:diorite_stairs': _aux0213, 
    'minecraft:deepslate_brick_stairs': _aux0213, 'minecraft:polished_granite_stairs': _aux0213, 'minecraft:polished_andesite_stairs': _aux0213, 
    'minecraft:weathered_cut_copper_stairs': _aux0213, 'minecraft:mud_brick_stairs': _aux0213, 'minecraft:quartz_stairs': _aux0213, 
    'minecraft:nether_brick_stairs': _aux0213, 'minecraft:waxed_exposed_cut_copper_stairs': _aux0213, 'minecraft:blackstone_stairs': _aux0213, 
    'minecraft:red_nether_brick_stairs': _aux0213, 'minecraft:exposed_cut_copper_stairs': _aux0213, 'minecraft:end_brick_stairs': _aux0213, 
    'minecraft:polished_blackstone_brick_stairs': _aux0213, 'minecraft:smooth_quartz_stairs': _aux0213, 'minecraft:deepslate_tile_stairs': _aux0213, 
    'minecraft:cut_copper_stairs': _aux0213, 'minecraft:warped_stairs': _aux0213, 'minecraft:brick_stairs': _aux0213, 
    'minecraft:prismarine_bricks_stairs': _aux0213, 'minecraft:andesite_stairs': _aux0213, 'minecraft:dark_prismarine_stairs': _aux0213, 
    'minecraft:cobbled_deepslate_stairs': _aux0213, 'minecraft:granite_stairs': _aux0213, 'minecraft:polished_deepslate_stairs': _aux0213, 
    'minecraft:polished_diorite_stairs': _aux0213, 'minecraft:polished_blackstone_stairs': _aux0213, 'minecraft:purpur_stairs': _aux0213, 
    'minecraft:waxed_weathered_cut_copper_stairs': _aux0213, 'minecraft:crimson_stairs': _aux0213, 'minecraft:oxidized_cut_copper_stairs': _aux0213, 
    'minecraft:waxed_cut_copper_stairs': _aux0213, 'minecraft:waxed_oxidized_cut_copper_stairs': _aux0213,
    # 活板门：0 2 1 3顺序
    'minecraft:dark_oak_trapdoor': _aux0213, 'minecraft:jungle_trapdoor': _aux0213, 'minecraft:iron_trapdoor': _aux0213, 
    'minecraft:acacia_trapdoor': _aux0213, 'minecraft:crimson_trapdoor': _aux0213, 'minecraft:bamboo_trapdoor': _aux0213, 
    'minecraft:birch_trapdoor': _aux0213, 'minecraft:mangrove_trapdoor': _aux0213, 'minecraft:warped_trapdoor': _aux0213, 
    'minecraft:trapdoor': _aux0213, 'minecraft:cherry_trapdoor': _aux0213, 'minecraft:spruce_trapdoor': _aux0213,
    # 门: 0 1 2 3顺序
    'minecraft:dark_oak_door': _aux0123, 'minecraft:bamboo_door': _aux0123, 'minecraft:spruce_door': _aux0123, 
    'minecraft:mangrove_door': _aux0123, 'minecraft:jungle_door': _aux0123, 'minecraft:cherry_door': _aux0123, 
    'minecraft:warped_door': _aux0123, 'minecraft:acacia_door': _aux0123, 'minecraft:birch_door': _aux0123, 
    'minecraft:wooden_door': _aux0123, 'minecraft:crimson_door': _aux0123, 'minecraft:iron_door': _aux0123,
    # 栅栏门: 0 1 2 3顺序
    'minecraft:crimson_fence_gate': _aux0123, 'minecraft:spruce_fence_gate': _aux0123, 'minecraft:dark_oak_fence_gate': _aux0123, 
    'minecraft:birch_fence_gate': _aux0123, 'minecraft:acacia_fence_gate': _aux0123, 'minecraft:jungle_fence_gate': _aux0123, 
    'minecraft:fence_gate': _aux0123, 'minecraft:cherry_fence_gate': _aux0123, 'minecraft:bamboo_fence_gate': _aux0123, 
    'minecraft:warped_fence_gate': _aux0123, 'minecraft:mangrove_fence_gate': _aux0123,
    # 梯子、末地烛、画
    'minecraft:ladder': _aux4253, 'minecraft:end_rod': _aux4253, 'minecraft:frame': _aux4253,
    # 墙上告示牌
    'minecraft:wall_sign': _aux4253, 'minecraft:spruce_wall_sign': _aux4253, 'minecraft:birch_wall_sign': _aux4253,
    'minecraft:acacia_wall_sign': _aux4253, 'minecraft:darkoak_wall_sign': _aux4253, 'minecraft:cherry_wall_sign': _aux4253,
    'minecraft:bamboo_wall_sign': _aux4253, 'minecraft:crimson_wall_sign': _aux4253, 'minecraft:warped_wall_sign': _aux4253, 
    'minecraft:jungle_wall_sign': _aux4253, 'minecraft:mangrove_wall_sign': _aux4253, 
    'minecraft:oak_hanging_sign': _aux4253, 'minecraft:bamboo_hanging_sign': _aux4253, 
    'minecraft:spruce_hanging_sign': _aux4253, 'minecraft:birch_hanging_sign': _aux4253, 'minecraft:jungle_hanging_sign': _aux4253,
    'minecraft:acacia_hanging_sign': _aux4253, 'minecraft:dark_oak_hanging_sign': _aux4253, 'minecraft:mangrove_hanging_sign': _aux4253,
    'minecraft:cherry_hanging_sign': _aux4253, 'minecraft:crimson_hanging_sign': _aux4253, 'minecraft:warped_hanging_sign': _aux4253,
    # 熔炉、箱子
    'minecraft:blast_furnace': _aux4253, 'minecraft:smoker': _aux4253, 'minecraft:furnace': _aux4253, 
    'minecraft:lit_blast_furnace': _aux4253, 'minecraft:lit_smoker': _aux4253, 'minecraft:lit_furnace': _aux4253, 
    'minecraft:chest': _aux4253, 'minecraft:trapped_chest': _aux4253, 'minecraft:ender_chest': _aux4253, 
    # 原木
    'minecraft:mangrove_log': _aux12, 'minecraft:stripped_mangrove_log': _aux12, 'minecraft:cherry_log': _aux12, 
    'minecraft:stripped_spruce_log': _aux12, 'minecraft:warped_stem': _aux12, 'minecraft:stripped_dark_oak_log': _aux12, 
    'minecraft:stripped_acacia_log': _aux12, 'minecraft:spruce_log': _aux12, 'minecraft:jungle_log': _aux12, 
    'minecraft:stripped_oak_log': _aux12, 'minecraft:acacia_log': _aux12, 'minecraft:crimson_stem': _aux12, 
    'minecraft:stripped_crimson_stem': _aux12, 'minecraft:stripped_birch_log': _aux12, 'minecraft:birch_log': _aux12, 
    'minecraft:oak_log': _aux12, 'minecraft:stripped_warped_stem': _aux12, 'minecraft:dark_oak_log': _aux12, 
    'minecraft:stripped_jungle_log': _aux12, 'minecraft:stripped_cherry_log': _aux12, 

    # 蜂箱、南瓜灯
    'minecraft:beehive': _aux0123, 'minecraft:lit_pumpkin': _aux0123, 'minecraft:bee_nest': _aux0123, 'minecraft:carved_pumpkin': _aux0123,
    # 书架、讲台、铁砧、砂轮
    'minecraft:grindstone': _aux0123, 'minecraft:chiseled_bookshelf': _aux0123, 'minecraft:anvil': _aux0123, 'minecraft:lectern': _aux0123,
}

def GetBlockRotateAux(blockName, aux, rot):
    """获取方块的旋转后的aux"""
    if rot == 0:
        return aux
    rotNum = rot // 90
    auxList = _RotateBlockAuxDict.get(blockName)
    if auxList:
        # 在列表里抽取
        if aux in auxList:
            lens = len(auxList)
            index = auxList.index(aux)
            # 对4以上的特殊处理，限制在[4,7] 或 [8,11]之间，轮询切换
            if index > 3:
                num = index // 4
                index += rotNum
                index = index % 4 + num * 4
                aux = auxList[index]
            else:
                aux = auxList[(index + rotNum) % 4]
    return aux
# endregion


# region 需最后生成的方块：墙上旗帜、墙上火把、墙上按钮等

# endregion


# region UI轮盘数据
WheelMaxCount = 6
# 建筑类型、每个类型对应的建筑数量，都是最多6个，可留空
# 以索引对应显示位置
StructTypeWheelCfg = [
    None,   # 表示该索引的位置没有数据
    {
        "id": "road",
        "name": "道路",     # 类型名字
        # 该类型下的所有建筑id
        "wheel_structs": {
            # 格式: 建筑id: 轮盘索引
            StructEnum.RoadLine: 1,
            StructEnum.Road90: 2,
            # StructEnum.RoadU: 3,
            StructEnum.RoadUphill: 4,
        },
    },
    {
        "id": "campsite",
        "name": "营地",
        "wheel_structs": {
            # StructEnum.RepairStation: 1,
            StructEnum.TentSmall: 2,
            StructEnum.TentLarge: 3,
        },
    },
    {
        "id": "fortress",
        "name": "碉堡",
        "wheel_structs": {
            # StructEnum.Refuge: 1,
            # StructEnum.FortressHight: 2,
            StructEnum.FortressTower: 3,
            # StructEnum.FortressBase: 4,
        },
    },
    {
        "id": "fortress",
        "name": "围墙",
        "wheel_structs": {
            StructEnum.WallLine: 1,
            StructEnum.WallSlant: 2,
        },
    },
]
"""建筑的轮盘类型数据"""
# 不足6个的部分，补上None
for i in xrange(len(StructTypeWheelCfg), WheelMaxCount):
    StructTypeWheelCfg.append(None)

StructIdCfg = {
    # StructEnum.FortressHight: {
    #     "name": "高碉堡",
    #     "ui_scale": 0.0025,    # ui模型的缩放-预览时
    #     "ui_wheel_scale": 0.003,    # ui模型的缩放-轮盘时
    #     # 建造所需材料
    #     "materials": [
    #         ("minecraft:diamond_block", 3),
    #         ("minecraft:iron_ingot", 7),
    #         ("minecraft:diamond", 5),
    #     ],
    #     # 建造耗时
    #     "time": 1,
    # },
    StructEnum.FortressTower: {
        "name": "塔楼",
        "ui_scale": 0.004,
        "ui_wheel_scale": 0.005, 
        "materials": [
            ("minecraft:iron_ingot", 5),
            ("scuke_survive:ingot_lithium", 2),
            ("scuke_survive:ingot_lead", 2),
        ],
    },
    # StructEnum.FortressBase: {
    #     "name": "碉堡底座",
    #     "ui_scale": 0.003,
    #     "ui_wheel_scale": 0.003, 
    #     "materials": [
    #         ("minecraft:diamond", 5),
    #     ],
    # },

    StructEnum.WallLine: {
        "name": "直线围墙",
        "ui_scale": 0.008,
        "ui_wheel_scale": 0.008, 
        "materials": [
            ("minecraft:iron_ingot", 2),
            ("scuke_survive:ingot_lithium", 2),
            ("scuke_survive:ingot_lead", 2),
        ],
    },
    StructEnum.WallSlant: {
        "name": "斜线围墙",
        "ui_scale": 0.006,
        "ui_wheel_scale": 0.006, 
        "materials": [
            ("minecraft:iron_ingot", 3),
            ("scuke_survive:ingot_lithium", 2),
            ("scuke_survive:ingot_lead", 2),
        ],
    },
    StructEnum.RoadLine: {
        "name": "直线道路",
        "ui_scale": 0.003,
        "ui_wheel_scale": 0.003, 
        "materials": [
            ("minecraft:iron_ingot", 2),
            ("minecraft:copper_ingot", 2),
            ("scuke_survive:ingot_lead", 2),
        ],
    },
    StructEnum.Road90: {
        "name": "90度道路",
        "ui_scale": 0.005,
        "ui_wheel_scale": 0.005, 
        "materials": [
            ("minecraft:iron_ingot", 2),
            ("minecraft:copper_ingot", 2),
            ("scuke_survive:ingot_lead", 1),
        ],
    },
    # StructEnum.RoadU: {
    #     "name": "U型道路",
    #     "ui_scale": 0.001,
    #     "ui_wheel_scale": 0.0015, 
    #     "materials": [
    #         ("minecraft:diamond", 5),
    #     ],
    # },
    StructEnum.RoadUphill: {
        "name": "上坡道路",
        "ui_scale": 0.002,
        "ui_wheel_scale": 0.002, 
        "materials": [
            ("minecraft:iron_ingot", 3),
            ("minecraft:copper_ingot", 2),
            ("scuke_survive:ingot_lead", 2),
        ],
    },
    StructEnum.TentSmall: {
        "name": "小帐篷",
        "ui_scale": 0.01,
        "ui_wheel_scale": 0.018, 
        "materials": [
            ("minecraft:iron_ingot", 2),
            ("minecraft:oak_log", 6),
        ],
    },
    StructEnum.TentLarge: {
        "name": "大帐篷",
        "ui_scale": 0.01,
        "ui_wheel_scale": 0.02, 
        "materials": [
            ("minecraft:iron_ingot", 2),
            ("minecraft:copper_ingot", 2),
            ("minecraft:oak_log", 10),
        ],
    },
    # StructEnum.Refuge: {
    #     "name": "避难所",
    #     "ui_scale": 0.003,
    #     "ui_wheel_scale": 0.003, 
    #     "materials": [
    #         ("minecraft:diamond", 5),
    #     ],
    # },
    # StructEnum.RepairStation: {
    #     "name": "维修站",
    #     "ui_scale": 0.004,
    #     "ui_wheel_scale": 0.004, 
    #     "materials": [
    #         ("minecraft:diamond", 5),
    #     ],
    # },
}
"""具体建筑的轮盘数据"""

# 计算建造时间
def CalcBuildingTime(structId):
    """计算建筑建造时间"""
    t = 1
    palette = GetStructPaletteDict(structId)
    if palette:
        blockCount = palette.get("block_count", 1)
        t = blockCount // OnceBuildBlockCount + 1
    return t * BuildStructTimerCD

for structId, structCfg in StructIdCfg.iteritems():
    structCfg["time"] = CalcBuildingTime(structId)
# endregion
