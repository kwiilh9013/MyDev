# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import gunConfig as GunConfig
import mod.server.extraServerApi as serverApi

LEVEL_ID = serverApi.GetLevelId()
CMD = serverApi.GetEngineCompFactory().CreateCommand(LEVEL_ID).SetCommand
WORLD = serverApi.GetEngineCompFactory().CreateGame(LEVEL_ID)
MOB_TYPE = serverApi.GetEngineCompFactory().CreateEngineType
CreatingItem = serverApi.GetEngineCompFactory().CreateItem
CreatingExtraData = serverApi.GetEngineCompFactory().CreateExtraData
DefaultMeleeData = {
    "Button_Attack": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
}

DefaultGunData = {
    "Button_Fire": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "Button_Aim": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "Button_Fire_Left": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "Button_Reload": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "Button_Kick": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    }
}

DefaultCarData = {
    "btn_geton": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "btn_energy": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "btn_cut": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "btn_up": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "btn_turn_left": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    },
    "btn_turn_right": {
        "relaPos": [0, 0],
        "relaSize": 0.0,
        "alpha": 1.0
    }
}

DefaultServerData = {
    "mobLimit": [2.0, 1.0],
    "mobRefreshTimes": [2.0, 1.0],
    "worldTimeFlow": [0.0, 1.0],
    "eventHappenTimes": [2.0, 1.0],
    "respawnProtect": True,
    "mobDestroy": True,
    "blockDestroy": True,
    "canBreakBlocks": True,

    "gunDamageTimes": [0.0, 1.0],
    "infiniteAmmo": False,
    "noConsumeAmmo": False,
    "ignoreDurability": False,
    "gunWeight": True,
    "breakBlocks": True,
    "hasRecoil": True,
    "aimAssist": True
}

ClearItemList = [
    "minecraft:snowball", "minecraft:dirt", "minecraft:cobblestone",
    "minecraft:stone", "minecraft:log", "minecraft:bamboo", "minecraft:log2",
    "minecraft:cherry_log", "minecraft:mangrove_log", "minecraft:spruce_log", "minecraft:birch_log",
    "minecraft:jungle_log", "minecraft:dark_oak_log", "minecraft:oak_log", "minecraft:acacia_log"]


class SettingServerSystem(BaseServerSystem):
    def __init__(self, namespace, systemName):
        super(SettingServerSystem, self).__init__(namespace, systemName)
        self._operators = []
        self.serverData = {}
        self.weaponWeight = True

    def Update(self):
        pass

    @EngineEvent()
    def LoadServerAddonScriptsAfter(self, args=None):
        """加载服务端脚本完成事件"""
        # 读取一次设置数据，否则此时获取不到设置
        self.serverData = CreatingExtraData(LEVEL_ID).GetExtraData('scukeSurviveSettingServerData')
        if self.serverData is None:
            self.serverData = DefaultServerData
        self.SendSettingDataToOtherSystem()

    def SendSettingDataToOtherSystem(self):
        bulletServer = serverApi.GetSystem(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
        if bulletServer:
            bulletServer._S_damageCoef = self.serverData.get("gunDamageTimes", [0.0, 1.0])[1]
            bulletServer._S_blockBreaking = self.serverData.get("breakBlocks", True)
        phaseServer = serverApi.GetSystem(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
        if phaseServer:
            phaseServer._S_spawnerLimitCoef = self.serverData.get("mobLimit", [2.0, 1.0])[1]
            phaseServer._S_spawnerTimerCoef = self.serverData.get("mobRefreshTimes", [2.0, 1.0])[1]
            phaseServer._S_eventPlaceCoef = self.serverData.get("eventHappenTimes", [2.0, 1.0])[1]
            phaseServer._S_daySpeedCoef = self.serverData.get("worldTimeFlow", [2.0, 1.0])[1]
        gunServer = serverApi.GetSystem(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
        if gunServer:
            gunServer._S_infiniteClip = self.serverData.get("infiniteAmmo", False)
            gunServer._S_ignoreDurability = self.serverData.get("ignoreDurability", False)
            state = self.serverData.get("gunWeight", True)
            gunServer._S_enableModifyAttr = state
            if self.weaponWeight != state:
                gunServer.ModifyAllPlayersCarryAttr(state)
        meleeServer = serverApi.GetSystem(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
        if meleeServer:
            state = self.serverData.get("gunWeight", True)
            meleeServer._S_enableModifyAttr = state
            meleeServer._S_ignoreDurability = self.serverData.get("ignoreDurability", False)
            if self.weaponWeight != state:
                self.weaponWeight = state
                meleeServer.ModifyAllPlayersCarryAttr(state)
        WORLD.SetGameRulesInfoServer({"cheat_info": {"mob_griefing": self.serverData.get("canBreakBlocks", True)}})

    @AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
    def ClearItems(self, args):
        Type = args['type']
        pid = args['pid']
        self.DetectPower(args)
        if pid not in self._operators:
            return
        if Type == 'all':
            CMD('kill @e[type=item]', pid)
        elif Type == 'useless':
            EntList = WORLD.GetEntitiesAround(pid, 200, {"subject": "other", "test": "is_family", "value": "player",
                                                         "operator": "!="})
            for i in EntList:
                if MOB_TYPE(i).GetEngineTypeStr() == "minecraft:item":
                    name = CreatingItem(LEVEL_ID).GetDroppedItem(i)['itemName']
                    if name in ClearItemList:
                        self.DestroyEntity(i)
        elif Type == "expBall":
            EntList = WORLD.GetEntitiesAround(pid, 200, {"subject": "other", "test": "is_family", "value": "player",
                                                         "operator": "!="})
            for i in EntList:
                if MOB_TYPE(i).GetEngineTypeStr() == "minecraft:xp_orb":
                    self.DestroyEntity(i)

    @AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
    def GetSettingDataFromServer(self, args):
        MyClientData = CreatingExtraData(args['pid']).GetExtraData('scukeSurviveSettingClientData')
        self.serverData = CreatingExtraData(LEVEL_ID).GetExtraData('scukeSurviveSettingServerData')
        self.DetectPower(args)
        self.NotifyToClient(args['pid'], 'HasGetSettingData', {
            'pid': args['pid'],
            'operators': self._operators,
            "clientData": MyClientData,
            "serverData": self.serverData
        })

    def DetectPower(self, args):
        operation = serverApi.GetEngineCompFactory().CreatePlayer(args['pid']).GetPlayerAbilities()
        if operation['op'] and args['pid'] not in self._operators:
            self._operators.append(args['pid'])
        if not operation['op'] and args['pid'] in self._operators:
            self._operators.remove(args['pid'])

    @AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
    def CommitSetData(self, args):
        pid = args['pid']
        Data = args['data']
        ClientData = {
            "damageShow": Data.get('damageShow', True),
            "gunBtnData": Data.get("gunBtnData", DefaultGunData),
            "carBtnData": Data.get("carBtnData", DefaultCarData),
            "meleeBtnData": Data.get("meleeBtnData", DefaultMeleeData),
            "hudBtnData": Data.get("hudBtnData", {"Button_Menu": {"newPos": (-999, -999), "dfPos": (-999, -999)}})
        }
        self.serverData = Data.copy()
        if 'gunBtnData' in self.serverData:
            del self.serverData['gunBtnData']
        if "carBtnData" in self.serverData:
            del self.serverData['carBtnData']
        if "meleeBtnData" in self.serverData:
            del self.serverData['meleeBtnData']
        if "damageShow" in self.serverData:
            del self.serverData['damageShow']
        if "hudBtnData" in self.serverData:
            del self.serverData['hudBtnData']
        CreatingExtraData(pid).SetExtraData("scukeSurviveSettingClientData", ClientData)
        if pid in self._operators:
            CreatingExtraData(LEVEL_ID).SetExtraData("scukeSurviveSettingServerData", self.serverData)
            CreatingExtraData(LEVEL_ID).SaveExtraData()
            self.SendSettingDataToOtherSystem()
        CreatingExtraData(pid).SaveExtraData()

    @EngineEvent()
    def PlayerJoinMessageEvent(self, args):
        if len(self._operators) < 1:
            if args['id'] not in self._operators:
                self._operators.append(args['id'])
        self.GetSettingDataFromServer({'pid': args['id']})

    @EngineEvent()
    def PlayerLeftMessageServerEvent(self, args):
        if args['id'] in self._operators:
            self._operators.remove(args['id'])
            if len(self._operators) < 1 and serverApi.GetPlayerList():
                self._operators.append(serverApi.GetPlayerList()[0])

    # region api
    def IsRespawnProtect(self):
        """是否拥有重生保护"""
        if not self.serverData:
            return True
        return self.serverData.get("respawnProtect", True)
# endregion
