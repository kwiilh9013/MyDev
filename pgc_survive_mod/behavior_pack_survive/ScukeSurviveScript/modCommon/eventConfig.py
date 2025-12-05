# -*- coding: utf-8 -*-

"""
存放事件id、订阅id
"""

# region 订阅id

# 客户端渲染tick
GameTickSubscribeEvent = "GameTickSubscribeEvent"

# 载具 订阅事件
CarSubscribeEvent = "CarSubscribeEvent"

# 显示道具UI
ShowItemUseUIEvent = "ShowItemUseUIEvent"
# 点击道具按钮
ItemUseBtnClickedEvent = "ItemUseBtnClickedEvent"

# 全屏UI
FullScreenUIEvent = "FullScreenUIEvent"

# 一键建造UI
BuildStructUIEvent = "BuildStructUIEvent"

# 引爆方块
DetonateExplodeBlockEvent = "DetonateExplodeBlockEvent"

# 电器的订阅事件
ElectricSubscriptEvent = "ElectricSubscriptEvent"
# 电器的UI订阅事件
ElectricUISubscriptEvent = "ElectricUISubscriptEvent"
# 电器的逻辑订阅事件，用于电力的数据沟通
ElectricLogicSubscriptEvent = "ElectricLogicSubscriptEvent"

# 获得奖励的弹窗显示订阅
GetRewardsPopupEvent = "GetRewardsPopupEvent"

# hud显示、隐藏的订阅
HudShowSubscriptEvent = "HudShowSubscriptEvent"

# 天气事件的订阅
WeatherSubscribeEvent = "WeatherSubscribeEvent"

# 设置界面订阅
SettingDataSubscribtEvent = "SettingDataSubscribtEvent"

# 电磁事件，用于载具、电器被瘫痪的逻辑
ElectromagnetismSubscribeEvent = "ElectromagnetismSubscribeEvent"

# 实体数据订阅，用于其他模块将数据传递给实体对象
EntityDataSubscribeEvent = "EntityDataSubscribeEvent"

# 镜头晃动订阅，用于其他模块实现晃动效果
CameraShakingSubscribeEvent = "CameraShakingSubscribeEvent"
# endregion


# region 服务端客户端消息id
# 载具控制消息事件
CarCtrlEvent = "CarCtrlEvent"
# 载具技能消息事件
CarSkillsEvent = "CarSkillsEvent"

# 使用物品事件
ItemUsedEvent = "ItemUsedEvent"

# molang表达式事件
MolangUpdateEvent = "MolangUpdateEvent"

# 一键建造事件
BuildStructEvent = "BuildStructEvent"

# 雷达相关事件
LadarEvent = "LadarEvent"

# 使用物品事件
UseItemEvent = "UseItemEvent"

# 电器相关事件
ElectricEvent = "ElectricEvent"

# 特效相关事件
EffectPlayEvent = "EffectPlayEvent"

# 电器设备合成物品的广播事件
ElectricCraftingItemsEvent = "ElectricCraftingItemsEvent"

# 实体客户端效果事件
EntityEffectEvent = "EntityEffectEvent"

# 打开定时炸弹界面
OpenTimeBombScreenEvent = "OpenTimeBombScreenEvent"
# 设置炸弹时间事件
TimeBombSetTimeEvent = "TimeBombSetTimeEvent"
# 同步炸弹状态事件
TimeBombSyncStatusEvent = "TimeBombSyncStatusEvent"

# C4引爆事件
C4BombIgniteEvent = "C4BombIgniteEvent"
# C4放置初始化事件
C4BombPlaceEvent = "C4BombPlaceEvent"
# C4移除事件
C4BombRemoveEvent = "C4BombRemoveEvent"

# endregion
