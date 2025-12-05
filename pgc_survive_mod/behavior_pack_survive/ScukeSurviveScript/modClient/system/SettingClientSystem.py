# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modCommon import eventConfig

WORLD = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())


class SettingClientSystem(BaseClientSystem):
    def __init__(self, namespace, systemName):
        super(SettingClientSystem, self).__init__(namespace, systemName)
        self._settingDict = {
            # client
            "damageShow": False,
            "hudBtnData":{
                "Button_Menu": {
                    "dfPos": (-999, -999),
                    "newPos": (-999, -999)
                },
            },
            "meleeBtnData":{
                "Button_Attack": {
                    "relaPos": [0, 0],
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
            },
            "gunBtnData":{
                "Button_Fire":{
                    "relaPos": [0, 0],
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "Button_Aim":{
                    "relaPos": [0, 0],
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "Button_Fire_Left":{
                    "relaPos": [0, 0],
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "Button_Reload":{
                    "relaPos": [0, 0],
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "Button_Kick":{
                    "relaPos": [0, 0],
                    "relaSize": 0.0,
                    "alpha": 1.0
                }
            },
            "carBtnData":{
                "btn_geton":{
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "btn_energy":{
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "btn_cut":{
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "btn_up":{
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "btn_turn_left":{
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
                },
                "btn_turn_right":{
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
                }
            },
            # client

            # server
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
            # server
        }
        self._settingUI = None

        # 初始化状态，用于修改按钮位置的判断
        self._init = False

    @EngineEvent()
    def UiInitFinished(self, args=None):
        self._init = False
        self.GetSettingData({'pid': clientApi.GetLocalPlayerId()})

    def ClearAllItem(self, args):
        self.NotifyToServer('ClearItems', {
            'pid': args['pid'],
            'type': 'all'
        })

    def ClearUselessItem(self, args):
        self.NotifyToServer('ClearItems', {
            'pid': args['pid'],
            'type': 'useless'
        })

    def ClearExpBall(self, args):
        self.NotifyToServer('ClearItems', {
            'pid': args['pid'],
            'type': 'expBall'
        })

    def CommitSettingData(self, args):
        self.NotifyToServer("CommitSetData", args)
        show = args['data'].get("damageShow", False)
        self.SendDataToOtherSystem(show)

    def GetSettingData(self, args):
        self.NotifyToServer('GetSettingDataFromServer', {
            'pid': args['pid'],
        })

    def SendDataToOtherSystem(self, show=None):
        # 更新伤害显示系统
        damageClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.DamageIndicatorClientSystem)
        if damageClient:
            damageClient._S_showDamage = self._settingDict['damageShow'] if show is None else show
        gunClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
        if gunClient:
            gunClient._S_infiniteClip = self._settingDict['infiniteAmmo']
            # gunClient._initBtn = False
        meleeClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
        if meleeClient:
            # meleeClient._initBtn = False
            pass

    @AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.SettingServerSystem)
    def HasGetSettingData(self, args):
        self._settingUI = clientApi.GetUI(modConfig.ModName, UIDef.UI_SettingUI['ui_key'])
        if args['serverData']:
            for key, value in args['serverData'].items():
                if key in self._settingDict:
                    self._settingDict.update({key: value})
        if args['clientData']:
            for key2, value2 in args['clientData'].items():
                if key2 in self._settingDict:
                    self._settingDict.update({key2: value2})
        self.SendDataToOtherSystem()
        if self._settingUI:
            self._settingUI.UpdateSettingData({"data": self._settingDict, "operator": args['operators']})
        # 更新hudUI位置
        hudUi = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
        if hudUi and hudUi._ButtonMenu:
            if self._settingDict["hudBtnData"]["Button_Menu"]['dfPos'] == (-999, -999):
                self._settingDict["hudBtnData"]["Button_Menu"]['dfPos'] = hudUi._ButtonMenu.GetPosition()
            if self._settingDict["hudBtnData"]["Button_Menu"]['newPos'] != (-999, -999):
                hudUi._ButtonMenu.SetPosition(self._settingDict["hudBtnData"]["Button_Menu"]['newPos'])
        # 初始化设置按钮位置
        if self._init is False:
            self.UpdateBtnPos("car", self._settingDict.get("carBtnData"))
        self._init = True

    # region api
    def UpdateBtnPos(self, stage, posData):
        """
        更新按钮位置
        
        stage="car" || "gun" || "melee", posData={}
        """
        info = {
            "stage": stage,
            "posData": posData,
        }
        Instance.mEventMgr.NotifyEvent(eventConfig.SettingDataSubscribtEvent, info)
        pass
    # endregion
