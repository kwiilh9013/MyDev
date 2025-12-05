# -*- encoding: utf-8 -*-
from blockConfig import ConfigList as BlocksCfg
from buildingConfig import ConfigList as BuildingsCfg
from equipmentConfig import ConfigList as EquipCfg
from eventConfig import ConfigList as EventCfg
from itemConfig import ConfigList as ItemCfg
from mobConfig import ConfigList as MobCfg
from rebelConfig import ConfigList as RebelCfg
from vehicleConfig import ConfigList as VehicleCfg
from weaponConfig import ConfigList as WeaponCfg

__illustrationCfgDict__ = {
    'block': BlocksCfg,
    'building': BuildingsCfg,
    'equipment': EquipCfg,
    'event': EventCfg,
    'item': ItemCfg,
    'mob': MobCfg,
    'rebel': RebelCfg,
    'vehicle': VehicleCfg,
    'weapon': WeaponCfg
}


def GetData(illustrateType):
    if illustrateType in __illustrationCfgDict__:
        return __illustrationCfgDict__[illustrateType]
    return None


def GetAllData():
    return __illustrationCfgDict__


# 不同类型卡片配置
CardTypeList = [
    {
        "type": "green",        # 卡片类型
        "nameAlpha": 1.0,       # 中文字不透明度
        "nameColor": (255.0/255.0, 255.0/255.0, 255.0/255.0),       # 网格预览：未锁定文字颜色
        "lockNameColor": (178.0/255.0, 255.0/255.0, 232.0/255.0),   # 网格预览： 锁定文字颜色
        "showPosition": (0.0, 0.0),     # 纸娃娃相对父控件坐标
        "showSize": (2.0, 2.0),     # 纸娃娃相对父控件大小
        "imageDataColor": (255.0/255.0, 255.0/255.0, 255.0/255.0),      # 贴图显示模式颜色蒙版
        "imageDataAlpha": 1.0,      # 贴图显示模式不透明度
        "cardImageBg0Color": (161.0/255.0, 255.0/255.0, 38.0/255.0),        # 卡片：最底层颜色
        "cardImageBg1Path": "bg_green",     # 卡片：纹理路径
        "cardImageBg2Color": (255.0/255.0, 255.0/255.0, 255.0/255.0),       # 卡片：指定图片背景颜色
        "cardImageTextAndIconColor": (0.0/255.0, 0.0/255.0, 0.0/255.0),     # 卡片：指定图片背景上文字颜色和详情描述icon背景色
        "cardContentBgAlpha": 0.2,      # 卡片：详情内容背景不透明度
        "cardContentBgColor": (0.0/255.0, 255.0/255.0, 0.0/255.0),      # 详情内容背景颜色
        "cardContentTextColor": (0.0/255.0, 0.0/255.0, 0.0/255.0)       # 详情内容文字颜色
    },
    {
        "type": "blue",        # 卡片类型
        "nameAlpha": 1.0,  # 中文字不透明度
        "nameColor": (255.0/255.0, 255.0/255.0, 255.0/255.0),       # 网格预览：未锁定文字颜色
        "lockNameColor": (178.0/255.0, 255.0/255.0, 232.0/255.0),   # 网格预览： 锁定文字颜色
        "showPosition": (0.0, 0.0),     # 纸娃娃相对父控件坐标
        "showSize": (2.0, 2.0),     # 纸娃娃相对父控件大小
        "imageDataColor": (255.0/255.0, 255.0/255.0, 255.0/255.0),      # 贴图显示模式颜色蒙版
        "imageDataAlpha": 1.0,      # 贴图显示模式不透明度
        "cardImageBg0Color": (120.0 / 255.0, 253.0 / 255.0, 255.0 / 255.0),        # 卡片：最底层颜色
        "cardImageBg1Path": "bg_blue",     # 卡片：纹理路径
        "cardImageBg2Color": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),       # 卡片：指定图片背景颜色
        "cardImageTextAndIconColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0),     # 卡片：指定图片背景上文字颜色和详情描述icon背景色
        "cardContentBgAlpha": 0.2,      # 卡片：详情内容背景不透明度
        "cardContentBgColor": (190.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),      # 详情内容背景颜色
        "cardContentTextColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0)       # 详情内容文字颜色
    },
    {
        "type": "yellow",  # 卡片类型
        "nameAlpha": 1.0,  # 中文字不透明度
        "nameColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 网格预览：未锁定文字颜色
        "lockNameColor": (178.0 / 255.0, 255.0 / 255.0, 232.0 / 255.0),  # 网格预览： 锁定文字颜色
        "showPosition": (0.0, 0.0),  # 纸娃娃相对父控件坐标
        "showSize": (2.0, 2.0),  # 纸娃娃相对父控件大小
        "imageDataColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 贴图显示模式颜色蒙版
        "imageDataAlpha": 1.0,  # 贴图显示模式不透明度
        "cardImageBg0Color":  (255.0 / 255.0, 222.0 / 255.0, 0.0 / 255.0),  # 卡片：最底层颜色
        "cardImageBg1Path": "bg_yellow",  # 卡片：纹理路径
        "cardImageBg2Color": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 卡片：指定图片背景颜色
        "cardImageTextAndIconColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0),  # 卡片：指定图片背景上文字颜色和详情描述icon背景色
        "cardContentBgAlpha": 0.2,  # 卡片：详情内容背景不透明度
        "cardContentBgColor": (255.0 / 255.0, 243.0 / 255.0, 165.0 / 255.0),  # 详情内容背景颜色
        "cardContentTextColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0)  # 详情内容文字颜色
    },
    {
        "type": "purple",  # 卡片类型
        "nameAlpha": 1.0,  # 中文字不透明度
        "nameColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 网格预览：未锁定文字颜色
        "lockNameColor": (178.0 / 255.0, 255.0 / 255.0, 232.0 / 255.0),  # 网格预览： 锁定文字颜色
        "showPosition": (0.0, 0.0),  # 纸娃娃相对父控件坐标
        "showSize": (2.0, 2.0),  # 纸娃娃相对父控件大小
        "imageDataColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 贴图显示模式颜色蒙版
        "imageDataAlpha": 1.0,  # 贴图显示模式不透明度
        "cardImageBg0Color": (241.0 / 255.0, 173.0 / 255.0, 255.0 / 255.0),  # 卡片：最底层颜色
        "cardImageBg1Path": "bg_purple",  # 卡片：纹理路径
        "cardImageBg2Color": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 卡片：指定图片背景颜色
        "cardImageTextAndIconColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0),  # 卡片：指定图片背景上文字颜色和详情描述icon背景色
        "cardContentBgAlpha": 0.2,  # 卡片：详情内容背景不透明度
        "cardContentBgColor": (255.0 / 255.0, 155.0 / 255.0, 249.0 / 255.0),  # 详情内容背景颜色
        "cardContentTextColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0)  # 详情内容文字颜色
    },
    {
        "type": "red",  # 卡片类型
        "nameAlpha": 1.0,  # 中文字不透明度
        "nameColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 网格预览：未锁定文字颜色
        "lockNameColor": (178.0 / 255.0, 255.0 / 255.0, 232.0 / 255.0),  # 网格预览： 锁定文字颜色
        "showPosition": (0.0, 0.0),  # 纸娃娃相对父控件坐标
        "showSize": (2.0, 2.0),  # 纸娃娃相对父控件大小
        "imageDataColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 贴图显示模式颜色蒙版
        "imageDataAlpha": 1.0,  # 贴图显示模式不透明度
        "cardImageBg0Color": (255.0 / 255.0, 199.0 / 255.0, 199.0 / 255.0),  # 卡片：最底层颜色
        "cardImageBg1Path": "bg_red",  # 卡片：纹理路径
        "cardImageBg2Color": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 卡片：指定图片背景颜色
        "cardImageTextAndIconColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0),  # 卡片：指定图片背景上文字颜色和详情描述icon背景色
        "cardContentBgAlpha": 0.2,  # 卡片：详情内容背景不透明度
        "cardContentBgColor": (255.0 / 255.0, 91.0 / 255.0, 91.0 / 255.0),  # 详情内容背景颜色
        "cardContentTextColor": (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0)  # 详情内容文字颜色
    },
    {
        "type": "gold",  # 卡片类型
        "nameAlpha": 1.0,  # 中文字不透明度
        "nameColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 网格预览：未锁定文字颜色
        "lockNameColor": (178.0 / 255.0, 255.0 / 255.0, 232.0 / 255.0),  # 网格预览： 锁定文字颜色
        "showPosition": (0.0, 0.0),  # 纸娃娃相对父控件坐标
        "showSize": (2.0, 2.0),  # 纸娃娃相对父控件大小
        "imageDataColor": (255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),  # 贴图显示模式颜色蒙版
        "imageDataAlpha": 1.0,  # 贴图显示模式不透明度
        "cardImageBg0Color": (255.0/255.0, 252.0/255.0, 83.0/255.0),  # 卡片：最底层颜色
        "cardImageBg1Path": "bg_gold",  # 卡片：纹理路径
        "cardImageBg2Color": (0.0/255.0, 0.0/255.0, 0.0/255.0),  # 卡片：指定图片背景颜色
        "cardImageTextAndIconColor": (255.0/255.0, 252.0/255.0, 83.0/255.0),  # 卡片：指定图片背景上文字颜色和详情描述icon背景色
        "cardContentBgAlpha": 0.2,  # 卡片：详情内容背景不透明度
        "cardContentBgColor": (255.0/255.0, 252.0/255.0, 83.0/255.0),  # 详情内容背景颜色
        "cardContentTextColor": (0.0/255.0, 0.0/255.0, 0.0/255.0)  # 详情内容文字颜色
    },
]
