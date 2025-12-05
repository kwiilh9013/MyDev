# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.ScukeCore.client.engineApiGac import *
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
CreatingItem = compFactory.CreateItem
CreatedGame = compFactory.CreateGame(levelId)
MyPid = GetLocalPlayerId()
ContentPathPrefix = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content/"
Tab1Path = '/panel/tabPanel/tabLevel1' + ContentPathPrefix
Tab2Path = "/panel/tabPanel/tabLevel2/"
DamageShowPath = Tab2Path + 'normalSetting' + ContentPathPrefix + "stackPanel/damageShowSet/damageShowToggleMain"
NormalSetPath = Tab2Path + "normalSetting" + ContentPathPrefix + "stackPanel"
GameSetPath = Tab2Path + "gameSetting" + ContentPathPrefix + "stackPanel"
GunSetPath = Tab2Path + "gunSetting" + ContentPathPrefix + "stackPanel"
TipsMap = {
    "damageShow": "开启后，生物受到伤害时显示伤害值",

    "mobLimit": "决定该地图中能自然生成的生物数量上限的倍率，生物数量会随着天数增加提高，倍率越高，能生成的总数越多，也可能导致越严重的性能问题（低配慎重 超过1.5x）",
    "mobRefreshTimes": "决定生物刷新速度，您可以通过此自定义战斗节奏",
    "worldTimeFlow": "调整时间的流速倍率，流速越快，就越快到下一天，反之越慢",
    "eventHappenTimes": "调整事件（如陨石雨、血月）的发生概率倍率，可通过此控制战斗节奏",
    "respawnProtect": "开启后，复活后10秒内免疫大部分伤害",
    "canBreakBlocks": "控制怪物和某些方块能否破坏地形",
    "blockDestroy": "控制防御类方块（如地雷、油桶）能否破坏地形",

    "gunDamageTimes": "控制枪械伤害的倍率，不建议修改，这将影响游戏平衡",
    "infiniteAmmo": "开启后，装填弹药时无需消耗对应弹药",
    "noConsumeAmmo": "开启后，枪械射击不消耗弹药",
    "ignoreDurability": "开启后，武器（近战和枪械）具有无限的耐久，不会产生损耗",
    "gunWeight": "开启后，不同武器将会带来不同程度的重量影响",
    "breakBlocks": "开启后，枪械射出的弹药对部分方块（如玻璃、树叶）具有破坏效果",
    "hasRecoil": "开启后，枪械射击具有后坐力，镜头会向上偏移",
    "aimAssist": "开启后，在瞄准状态下具有辅助瞄准功能，视角会吸附在镜头中心附近的敌人上"
}

TipsBtnMap = [
    (DamageShowPath + "/txt/helpBtn", "damageShow"),
    (GameSetPath + "/mobLimitSet/bg/txt/helpBtn", "mobLimit"),
    (GameSetPath + "/mobRefreshTimesSet/bg/txt/helpBtn", "mobRefreshTimes"),
    (GameSetPath + "/timeFlowSet/bg/txt/helpBtn", "worldTimeFlow"),
    (GameSetPath + "/eventHappenTimesSet/bg/txt/helpBtn", "eventHappenTimes"),
    (GameSetPath + "/togglePanel1/respawnProtect/bg/txt/helpBtn", "respawnProtect"),
    (GameSetPath + "/togglePanel1/canBreakBlocks/bg/txt/helpBtn", "canBreakBlocks"),
    (GameSetPath + "/togglePanel1/blockDestroy/bg/txt/helpBtn", "blockDestroy"),
    (GunSetPath + "/gunDamageTimesSet/bg/txt/helpBtn", "gunDamageTimes"),
    (GunSetPath + "/togglePanel1/infiniteAmmo/bg/txt/helpBtn", "infiniteAmmo"),
    (GunSetPath + "/togglePanel2/noConsumeAmmo/bg/txt/helpBtn", "noConsumeAmmo"),
    (GunSetPath + "/togglePanel1/gunWeight/bg/txt/helpBtn", "gunWeight"),
    (GunSetPath + "/togglePanel1/breakBlocks/bg/txt/helpBtn", "breakBlocks"),
    (GunSetPath + "/togglePanel2/hasRecoil/bg/txt/helpBtn", "hasRecoil"),
    (GunSetPath + "/togglePanel2/aimAssist/bg/txt/helpBtn", "aimAssist"),
    (GunSetPath + "/togglePanel2/ignoreDurability/bg/txt/helpBtn", "ignoreDurability"),
]

TogglesMap = [
    (DamageShowPath + "/toggle", "damageShow"),
    (GameSetPath + "/togglePanel1/respawnProtect/bg/toggle", "respawnProtect"),
    (GameSetPath + "/togglePanel1/canBreakBlocks/bg/toggle", "canBreakBlocks"),
    (GameSetPath + "/togglePanel1/blockDestroy/bg/toggle", "blockDestroy"),
    (GunSetPath + "/togglePanel1/infiniteAmmo/bg/toggle", "infiniteAmmo"),
    (GunSetPath + "/togglePanel2/noConsumeAmmo/bg/toggle", "noConsumeAmmo"),
    (GunSetPath + "/togglePanel1/gunWeight/bg/toggle", "gunWeight"),
    (GunSetPath + "/togglePanel1/breakBlocks/bg/toggle", "breakBlocks"),
    (GunSetPath + "/togglePanel2/hasRecoil/bg/toggle", "hasRecoil"),
    (GunSetPath + "/togglePanel2/aimAssist/bg/toggle", "aimAssist"),
    (GunSetPath + "/togglePanel2/ignoreDurability/bg/toggle", "ignoreDurability"),
]

SliderMap = [
    (GameSetPath + "/mobLimitSet/bg/slider", "mobLimit", GameSetPath + "/mobLimitSet/bg/valueTxt",
     {"0.0": ["0.5x", 0.5], "1.0": ["0.75x", 0.75], "2.0": ["1.0x", 1.0], "3.0": ["1.5x", 1.5], "4.0": ["2.0x", 2.0]}),
    (GameSetPath + "/mobRefreshTimesSet/bg/slider", "mobRefreshTimes", GameSetPath + "/mobRefreshTimesSet/bg/valueTxt",
     {"0.0": ["0.0x", 0.0], "1.0": ["0.5x", 0.5], "2.0": ["1.0x", 1.0], "3.0": ["1.5x", 1.5], "4.0": ["2.0x", 2.0]}),
    (GameSetPath + "/timeFlowSet/bg/slider", "worldTimeFlow", GameSetPath + "/timeFlowSet/bg/valueTxt",
     {"0.0": ["1.0x", 1.0], "1.0": ["1.5x", 1.5], "2.0": ["2.0x", 2.0], "3.0": ["2.5x", 2.5], "4.0": ["3.0x", 3.0]}),
    (GameSetPath + "/eventHappenTimesSet/bg/slider", "eventHappenTimes", GameSetPath + "/eventHappenTimesSet/bg/valueTxt",
     {"0.0": ["0.0x", 0.0], "1.0": ["0.5x", 0.5], "2.0": ["1.0x", 1.0], "3.0": ["2.0x", 2.0], "4.0": ["3.0x", 3.0]}),
    (GunSetPath + "/gunDamageTimesSet/bg/slider", "gunDamageTimes", GunSetPath + "/gunDamageTimesSet/bg/valueTxt",
     {"0.0": ["1.0x", 1.0], "1.0": ["2.0x", 2.0], "2.0": ["4.0x", 4.0], "3.0": ["6.0x", 6.0], "4.0": ["8.0x", 8.0]}),
]

CommonBtnMap = [
    (NormalSetPath + "/btnsSet/gunBtnsSetBtn", "gunBtnSet"),
    (NormalSetPath + "/btnsSet/meleeBtnsSetBtn", "meleeBtnSet"),
    (NormalSetPath + "/btnsSet/carBtnsSetBtn", "carBtnSet"),
    (NormalSetPath + "/btnsSet/hudSetBtn", "hudSet"),
    (GameSetPath + "/togglePanel2/btn1/clearAllDropItemsBtn", "clearAllItem"),
    (GameSetPath + "/togglePanel2/btn2/clearUselessItemsBtn", "clearUselessItem"),
    (GameSetPath + "/togglePanel2/btn3/clearExpBallBtn", "clearExpBall"),
    ("/panel/confirmPanel/confirmBg/yesBtn", "yes"), ("/panel/confirmPanel/confirmBg/noBtn", "no")
]


class SettingUI(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(SettingUI, self).__init__(namespace, name, param)
        self._mTick = 0  # tick
        self._exitBtn = None
        self._tabLevel1BtnList = ['normalSetBtn', 'gameSetBtn', 'gunSetBtn']
        self._tabLevel2ScrList = ['normalSetting', 'gameSetting', 'gunSetting']
        self._normalSetBtn = None
        self._gameSetBtn = None
        self._gunSetBtn = None
        self._tipsMain = None
        self._client = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.SettingClientSystem)
        self._settingsDict = self._client._settingDict.copy()
        self._defaultSettingLen = len(self._settingsDict.keys())
        self._tab2BtnInstanceDict = {}
        self._tab2ToggleInstanceDict = {}
        self._tab2ToggleState = {}
        self._tab2SliderInstanceDict = {}
        self._confirmPanel = None
        self._hasInitialized = False
        self._confirmSelect = None
        self._isOperator = False

    def Create(self):
        super(SettingUI, self).Create()
        self.CreateBtn()

    def Update(self):
        self._mTick += 1
        if self._mTick % 5 == 0 and self._hasInitialized:
            self.GetAllToggleState()
            self.GetAllSliderValue()

    @ViewBinder.binding(ViewBinder.BF_BindInt, '#SettingUI.ReturnSliderStep')
    def ReturnSliderStep(self):
        return 5

    def CreateBtn(self):
        # 退出按钮初始化
        self._exitBtn = self.GetBaseUIControl('/panel/exitBtn').asButton()
        self._exitBtn.AddTouchEventParams({"isSwallow": True, 'type': '_exitBtn'})
        self._exitBtn.SetButtonTouchUpCallback(self.OnBtnPress)
        # 提示文字面板初始化
        self._tipsMain = self.GetBaseUIControl('/panel/tips').asLabel()
        self._tipsMain.SetVisible(False)
        # 一级面板初始化
        for x in self._tabLevel1BtnList:
            setattr(self, "_" + x, self.GetBaseUIControl(Tab1Path + x).asButton())
            getattr(self, "_" + x).AddTouchEventParams({"isSwallow": True, 'type': x})
            getattr(self, "_" + x).SetButtonTouchUpCallback(self.OnBtnPress)
            self.GetBaseUIControl(Tab1Path + x + '/selected').SetVisible(False)
        self.GetBaseUIControl(Tab1Path + 'normalSetBtn/selected').SetVisible(True)
        # 二级面板初始化
        map(lambda y: self.GetBaseUIControl(Tab2Path + self._tabLevel2ScrList[self._tabLevel1BtnList.index(y)]).SetVisible(True), self._tabLevel1BtnList)
        map(lambda y: self.GetBaseUIControl(Tab2Path + self._tabLevel2ScrList[self._tabLevel1BtnList.index(y)]).SetAlpha(0.0), self._tabLevel1BtnList)
        # 提示模块按钮注册和初始化
        for z in TipsBtnMap:
            self._tab2BtnInstanceDict.update({z[1]: self.GetBaseUIControl(z[0]).asButton()})
            self._tab2BtnInstanceDict[z[1]].AddTouchEventParams({"isSwallow": True, 'type': z[1]})
            self._tab2BtnInstanceDict[z[1]].SetButtonTouchUpCallback(self.OnBtnPress)
        # 开关注册和初始化
        map(lambda f: self._tab2ToggleInstanceDict.update({f[1]: self.GetBaseUIControl(f[0]).asSwitchToggle()}), TogglesMap)
        map(lambda f: self._tab2ToggleInstanceDict[f[1]].SetToggleState(self._settingsDict[f[1]]), TogglesMap)
        # 滑动条注册和初始化
        for t in SliderMap:
            self._tab2SliderInstanceDict.update({t[1]: self.GetBaseUIControl(t[0]).asSlider()})
            self._tab2SliderInstanceDict[t[1]].SetSliderValue(self._settingsDict.get(t[1], [4.0, 1.0])[0])
            self.GetBaseUIControl(t[2]).asLabel().SetText(t[3].get(str(self._settingsDict.get(t[1], [0.0, 1.0])[0]), ["未知", ])[0])
        # 单次按钮初始化
        map(lambda d: self.GetBaseUIControl(d[0]).asButton().AddTouchEventParams({"isSwallow": True, 'type': d[1]}), CommonBtnMap)
        map(lambda d: self.GetBaseUIControl(d[0]).asButton().SetButtonTouchUpCallback(self.OnOnceBtnPress), CommonBtnMap)

        # 再次确认界面初始化
        self._confirmPanel = self.GetBaseUIControl('/panel/confirmPanel')
        self._confirmPanel.SetVisible(False)
        # 初始化完毕
        # self._hasInitialized = True
        self.RequestLatestData()

    def OnBtnPress(self, args):
        Type = args['AddTouchEventParams']['type']
        if Type == '_exitBtn':
            self.GetAllToggleState()
            self.SetAllToggleState()
            self._client._settingDict = self._settingsDict
            self._client.CommitSettingData({'pid': MyPid, 'data': self._settingsDict})
            Instance.mUIManager.PopUI()
        if Type in self._tabLevel1BtnList:
            map(lambda x: self.GetBaseUIControl(Tab1Path + x + '/selected').SetVisible(False), self._tabLevel1BtnList)
            self.GetBaseUIControl(Tab1Path + Type + '/selected').SetVisible(True)
            self.GetBaseUIControl(Tab2Path + "maskBtn").SetVisible((Type in self._tabLevel1BtnList[1:] and not self._isOperator))
            index = self._tabLevel1BtnList.index(Type)
            map(lambda y: self.GetBaseUIControl(Tab2Path + self._tabLevel2ScrList[self._tabLevel1BtnList.index(y)]).SetVisible(False), self._tabLevel1BtnList)
            SelectPanel = self.GetBaseUIControl(Tab2Path + self._tabLevel2ScrList[index])
            Exes = [SelectPanel.SetVisible(True), SelectPanel.StopAnimation(), SelectPanel.PlayAnimation()]
        if Type in TipsMap:
            Exes = [self._tipsMain.SetVisible(True), self._tipsMain.StopAnimation(),
                    self._tipsMain.PlayAnimation(), self._tipsMain.SetText(TipsMap.get(Type, "？？？"))]

    def OnOnceBtnPress(self, args):
        def _setConfirmTxt(mType, mTxt):
            self._confirmSelect = mType
            self._confirmPanel.SetVisible(True)
            ConfirmTxt = self.GetBaseUIControl("/panel/confirmPanel/confirmBg/informTxt").asLabel()
            ConfirmTxt.SetText(mTxt)
        Type = args['AddTouchEventParams']['type']
        if Type == "clearAllItem":
            txt = "这将会清理所有掉落在地上的物品，您确定吗？"
            _setConfirmTxt(Type, txt)
        elif Type == "clearUselessItem":
            txt = "这将会清理 泥土、石头、圆石、原木、竹子、雪球、腐肉，您确定吗？"
            _setConfirmTxt(Type, txt)
        elif Type == "clearExpBall":
            txt = "这将会清理附近地面上的所有经验球，这些未获取的经验不会到您的等级中，您确定吗？"
            _setConfirmTxt(Type, txt)
        elif Type == "gunBtnSet":
            Instance.mUIManager.PushUI(UIDef.UI_GunBtnSettingUI)
        elif Type == "meleeBtnSet":
            Instance.mUIManager.PushUI(UIDef.UI_MeleeBtnSettingUI)
        elif Type == "carBtnSet":
            Instance.mUIManager.PushUI(UIDef.UI_CarBtnSettingUI)
        elif Type == "hudSet":
            txt = "继续确认，将会重置菜单hud（显示天数的可拖动面板）的位置。您确定吗？"
            _setConfirmTxt(Type, txt)
        elif Type == "yes":
            self._confirmPanel.SetVisible(False)
            if self._confirmSelect == "clearAllItem":
                self._client.ClearAllItem({"pid": MyPid})
            if self._confirmSelect == "clearUselessItem":
                self._client.ClearUselessItem({"pid": MyPid})
            if self._confirmSelect == "clearExpBall":
                self._client.ClearExpBall({"pid": MyPid})
            if self._confirmSelect == "hudSet":
                hudUi = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
                if hudUi and hudUi._ButtonMenu:
                    pos = self._client._settingDict["hudBtnData"]["Button_Menu"]['dfPos']
                    if pos != (-999, -999):
                        hudUi._ButtonMenu.SetPosition(pos)
                        self._client._settingDict["hudBtnData"]["Button_Menu"]['newPos'] = pos
        elif Type == "no":
            self._confirmPanel.SetVisible(False)

    def GetAllToggleState(self):
        if self._hasInitialized and self._tab2ToggleInstanceDict and TogglesMap:
            StateList = map(lambda x: {x[1]: self._tab2ToggleInstanceDict[x[1]].GetToggleState()}, TogglesMap)
            self._tab2ToggleState = {item.keys()[0]: item.values()[0] for item in StateList}
            self._settingsDict.update(self._tab2ToggleState)

    def SetAllToggleState(self):
        if self._hasInitialized and self._tab2ToggleInstanceDict:
            map(lambda y: self._tab2ToggleInstanceDict[y[1]].SetToggleState(self._settingsDict[y[1]]), TogglesMap)

    def GetAllSliderValue(self):
        if self._hasInitialized and self._tab2SliderInstanceDict and SliderMap:
            ValueList = map(lambda x: {x[1]: [self._tab2SliderInstanceDict[x[1]].GetSliderValue(),
                                              x[3].get(str(self._tab2SliderInstanceDict[x[1]].GetSliderValue()), [0.0, 1.0])[1]]}, SliderMap)
            ValueDict = {item.keys()[0]: item.values()[0] for item in ValueList}
            self._settingsDict.update(ValueDict)
            map(lambda t: self.GetBaseUIControl(t[2]).asLabel().SetText(t[3].get(str(self._settingsDict.get(t[1], [0.0, 1.0])[0]), ["未知", ])[0]), SliderMap)

    def SetAllSliderValue(self):
        if self._hasInitialized:
            map(lambda t: self._tab2SliderInstanceDict[t[1]].SetSliderValue(self._settingsDict.get(t[1], [4.0, 1.0])[0]), SliderMap)

    def UpdateSettingData(self, args=None):
        """接收设置数据并更新设置数据，同时更新所有UI状态"""
        Exes = [self._tipsMain.SetVisible(True), self._tipsMain.StopAnimation(), self._tipsMain.PlayAnimation()]
        if not args or args is None:
            self._tipsMain.SetText("未获取到存储数据")
            return
        if type(args) != dict:
            self._tipsMain.SetText("数据类型错误code==1，请联系开发者")
            return
        if 'data' not in args:
            self._tipsMain.SetText("数据类型错误code==2，请联系开发者")
            return
        if len(args['data'].keys()) < self._defaultSettingLen:
            self._tipsMain.SetText("数据长度异常code==3，请联系开发者")
            return
        self._settingsDict = args['data']
        self._isOperator = MyPid in args['operator']
        self._tipsMain.SetText("获取设置数据成功")
        self._hasInitialized = True
        self.SetAllToggleState()
        self.SetAllSliderValue()
        # 二级面板初始化
        map(lambda y: self.GetBaseUIControl(Tab2Path + self._tabLevel2ScrList[self._tabLevel1BtnList.index(y)]).SetVisible(False), self._tabLevel1BtnList)
        map(lambda y: self.GetBaseUIControl(Tab2Path + self._tabLevel2ScrList[self._tabLevel1BtnList.index(y)]).SetAlpha(1.0), self._tabLevel1BtnList)
        self.GetBaseUIControl(Tab2Path + "maskBtn").SetVisible(False)
        DefaultPanel = self.GetBaseUIControl(Tab2Path + 'normalSetting')
        Exes = [DefaultPanel.SetVisible(True), DefaultPanel.StopAnimation(), DefaultPanel.PlayAnimation()]

    def RequestLatestData(self):
        """请求最新数据"""
        self._client.GetSettingData({'pid': MyPid})

