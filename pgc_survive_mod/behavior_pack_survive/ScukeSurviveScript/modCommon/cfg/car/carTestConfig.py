# -*- coding: UTF-8 -*-
from ScukeSurviveScript.modCommon.cfg.car import carConfig


"""
载具配置表
"""

def GetTestConfig(carObj):
    # 载具配置数据
    BaseCarConfig = {
        # 最大时速，用于计算行为包设置的速度、显示UI
        "maxSpeedKmh": 100.0,

        # 最大加速度
        "maxASpeed": 0.5,
        # 刹车最大加速度
        "cutASpeed": 0.75,
        # 前进摩擦力（用来控制不踩油门时能滑多久）
        "frictionSpeed": 1.0,
        # 倒退的摩擦力（倒退时能滑距离更短，所以需要单独设置）
        "cutFrictionSpeed": 1.2,

        # 山地速度倍率(山地速度=陆地速度)，默认0.5
        "mountainSpeed": 0.35,
        # 水上速度倍率(水速度*0.5=陆地速度)，默认0.25
        "waterSpeed": 0.4,
        # 岩浆上速度倍率(岩浆速度=陆地速度)，默认0.5
        "lavaSpeed": 0.5,

        # 转向速度/秒
        "turnSpeed": 160,
        
        # 撞到实体后，速度倍率，默认为当前速度的95%
        "knockEntitySpeed": 0.95,
        # 破坏方块后，速度倍率，默认为当前速度的90%
        "breakBlockSpeed": 0.9,
        # 破坏方块后，速度倍率，默认为当前速度的90%
        "crashBlockSpeed": 0.5,
    }

    for k, v in BaseCarConfig.items():
        carConfig.BaseCarConfig[k] = v
    carObj._carConfig = carConfig.BaseCarConfig