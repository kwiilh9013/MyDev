# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_planet_booster import Config as Scuke_planetBooster
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_old_booster import Config as Scuke_oldBooster
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_house1 import Config as Scuke_house1
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_shipwrecks import Config as Scuke_shipwrecks
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_offices import Config as Scuke_offices
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_railwaystation import Config as Scuke_railwaystation
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_airplane_top import Config as Scuke_airplane_top
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_airplane_center import Config as Scuke_airplane_center
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_airplane_bottom import Config as Scuke_airplane_bottom
from ScukeSurviveScript.modCommon.cfg.buildings.markers.repair_station import Config as Repair_station
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_signal_tower import Config as Signal_tower
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_community01 import Config as Community01
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_ship_shelter import Config as Ship_shelter
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_train_workshop import Config as Train_workshop
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_city_broken import Config as CityBroken
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_city_new import Config as CityNew

# 所有需刷实体的建筑marker
__MarkerConfig = {
    Scuke_planetBooster['structure_name_base']: Scuke_planetBooster,
    Scuke_oldBooster['structure_name_base']: Scuke_oldBooster,
    Scuke_house1['structure_name_base']: Scuke_house1,
    Scuke_shipwrecks['structure_name_base']: Scuke_shipwrecks,
    Scuke_offices['structure_name_base']: Scuke_offices,
    Scuke_railwaystation['structure_name_base']: Scuke_railwaystation,
    Scuke_airplane_top['structure_name_base']: Scuke_airplane_top,
    Scuke_airplane_center['structure_name_base']: Scuke_airplane_center,
    Scuke_airplane_bottom['structure_name_base']: Scuke_airplane_bottom,
    Repair_station['structure_name_base']: Repair_station,
    Signal_tower['structure_name_base']: Signal_tower,
    Community01['structure_name_base']: Community01,
    Ship_shelter['structure_name_base']: Ship_shelter,
    Train_workshop['structure_name_base']: Train_workshop,
    CityNew["structure_name_base"]: CityNew,
    CityBroken["structure_name_base"]: CityBroken
}

Config = {
    'planetBoosterGroup': {
        'name': 'planetBooster',
        'mode': 'distance',
        'distance': 5000,
        'pools': {
            Scuke_planetBooster['structure_name_base']: {
                'mode': 'limit_count',
                # 限制建筑生成的数量
                # 'limit_count': 3,
                # 会执行cancel逻辑
                # 'try_cancel': True,
                'size': Scuke_planetBooster['size'],
                'y': 61,
            },
            Scuke_oldBooster['structure_name_base']: {
                'mode': 'singleton',
                'size': Scuke_oldBooster['size'],
                'y': 61,
            },
        }
    },
    'buildingGroup': {
        'name': 'buildings',
        'mode': 'distance',
        'distance': 80,
        'planetBooster_distance': 500,
        'pools': {
            Scuke_house1['structure_name_base']: {
                'mode': 'outter',
            },
            Scuke_shipwrecks['structure_name_base']: {
                'mode': 'outter',
            },
            Scuke_offices['structure_name_base']: {
                'mode': 'outter',
            },
            Scuke_railwaystation['structure_name_base']: {
                'mode': 'outter',
            },
            Scuke_airplane_top['structure_name_base']: {
                'mode': 'outter',
            },
            Scuke_airplane_center['structure_name_base']: {
                'mode': 'outter',
            },
            Scuke_airplane_bottom['structure_name_base']: {
                'mode': 'outter',
            },
            Repair_station['structure_name_base']: {
                'mode': 'outter',
            },
            Signal_tower['structure_name_base']: {
                'mode': 'outter',
            },
            Community01['structure_name_base']: {
                'mode': 'outter',
            },
            Ship_shelter['structure_name_base']: {
                'mode': 'outter',
            },
            Train_workshop['structure_name_base']: {
                'mode': 'outter',
            },
            CityNew["structure_name_base"]: {
                "mode": "outter",
            },
            CityBroken["structure_name_base"]: {
                "mode": "outter"
            },
        }
    }
}


def GetStructNameBase(identifier):
    """获取建筑的结构名称基类"""
    structNameBase = identifier.rsplit('_', 2)[0]
    return structNameBase


def GetMarkerConfig(identifier):
    """获取建筑的config数据"""
    cfg = __MarkerConfig.get(identifier)
    if cfg is None:
        cfg = __MarkerConfig.get(GetStructNameBase(identifier))
    return cfg


def TransMarkerPos(buildingPos, rot, center, marker):
    pos = marker['pos']
    face = marker['face']
    face = (int(rot / 90) + face) % 4
    pos = MathUtils.TupleSub(pos, center)
    pos = MathUtils.RotByFace(pos, rot)
    pos = MathUtils.TupleAdd(pos, buildingPos)
    return pos, face


def GetMarkerPos(identifier, buildingPos, rot, markerId):
    config = GetMarkerConfig(identifier)
    if not config:
        return buildingPos, 0
    markers = config['posMarkers']
    center = config['center']
    for marker in markers:
        id = marker['id']
        if id != markerId:
            continue
        return TransMarkerPos(buildingPos, rot, center, marker)
    return buildingPos, 0


def InverseMarkerPos(markerPos, markerFace, identifier, markerId):
    config = GetMarkerConfig(identifier)
    if not config:
        return markerPos, markerFace * 90
    markers = config['posMarkers']
    center = config['center']
    for marker in markers:
        id = marker['id']
        if id != markerId:
            continue
        pos = marker['pos']
        face = marker['face']
        rot = (markerFace - face + 4) % 4 * 90
        pos = MathUtils.RotByFace(pos, rot)
        center = MathUtils.RotByFace(center, rot)
        pos = MathUtils.TupleSub(markerPos, pos)
        pos = MathUtils.TupleAdd(pos, center)
        return pos, rot
    return markerPos, markerFace * 90
