# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.ScukeCore.common.api import commonApiMgr


class TableTiming(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableTiming, self).__init__(namespace, name, param)
        self.paramDict = param.get("data", {})
        self._btnDict = {}
        self.timeSetPath = "/timingPanel/timeSetPanel"
        self.timePanelPath = self.timeSetPath + "/timeSetStackPanel"
        self.rgBtnDict = {
            "closeBtn": self.timeSetPath + "/headPanel/closeBtn",
        }
        self.timeSellText = None
        self.timeBuyText = None
        self.timeSellToggle = None
        self.timeBuyToggle = None
        self.timeSellSlider = None
        self.timeBuySlider = None
        self.maxTime = 600.0
        self.timeSellSliderValue = self.paramDict.get("sellTimingSec", 0.0) / self.maxTime
        self.timeBuySliderValue = self.paramDict.get("buyTimingSec", 0.0) / self.maxTime
        self.timeSellToggleState = self.paramDict.get("toggleSellState", False)
        self.timeBuyToggleState = self.paramDict.get("toggleBuyState", False)
        self.timeBuySec = 0
        self.timeSellSec = 0
        self.prefixTxt = "定时时间："
        # 最大定时时间（秒），最小为10秒
        self.hasCreate = False

    def Destroy(self):
        self.GetAllCtrlStateAndExe()
        super(TableTiming, self).Destroy()

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()
        if not self.hasCreate: return
        # 定时时间计算
        if self.timeBuySlider is not None:
            buyValue = self.timeBuySlider.GetSliderValue()
            if buyValue != self.timeBuySliderValue:
                self.timeBuySliderValue = buyValue
                self.SetBuyText()
        if self.timeSellSlider is not None:
            sellValue = self.timeSellSlider.GetSliderValue()
            if sellValue != self.timeSellSliderValue:
                self.timeSellSliderValue = sellValue
                self.SetSellText()
        # 开关互斥
        if self.timeBuyToggle is not None:
            stateBuy = self.timeBuyToggle.GetToggleState()
            if stateBuy != self.timeBuyToggleState:
                self.timeBuyToggleState = stateBuy
                if stateBuy:
                    self.timeSellToggle.SetToggleState(False)
        if self.timeSellToggle is not None:
            stateSell = self.timeSellToggle.GetToggleState()
            if stateSell != self.timeSellToggleState:
                self.timeSellToggleState = stateSell
                if stateSell:
                    self.timeBuyToggle.SetToggleState(False)

    def Create(self):
        super(TableTiming, self).Create()
        for key, path in self.rgBtnDict.items():
            uiUtils.UICreateBtn(self, self._btnDict, key, path, None, self.OnCommonBtnPressUp)
        sellPath = self.timePanelPath + "/timeSellPanel"
        self.timeSellText = self.GetBaseUIControl(sellPath + "/timeTxt").asLabel()
        self.timeSellSlider = self.GetBaseUIControl(sellPath + "/slider").asSlider()
        self.timeSellToggle = self.GetBaseUIControl(sellPath + "/toggle").asSwitchToggle()
        buyPath = self.timePanelPath + "/timeBuyPanel"
        self.timeBuyText = self.GetBaseUIControl(buyPath + "/timeTxt").asLabel()
        self.timeBuySlider = self.GetBaseUIControl(buyPath + "/slider").asSlider()
        self.timeBuyToggle = self.GetBaseUIControl(buyPath + "/toggle").asSwitchToggle()
        self.timeBuyToggle.SetToggleState(self.timeBuyToggleState)
        self.timeSellToggle.SetToggleState(self.timeSellToggleState)
        self.timeBuySlider.SetSliderValue(self.timeBuySliderValue)
        self.timeSellSlider.SetSliderValue(self.timeSellSliderValue)
        self.SetBuyText()
        self.SetSellText()
        self.hasCreate = True

    def SetBuyText(self):
        buySec = max(self.maxTime * self.timeBuySliderValue, 10)
        self.timeBuyText.SetText(self.prefixTxt + commonApiMgr.FormatSeconds(buySec))
        self.timeBuySec = buySec

    def SetSellText(self):
        sellSec = max(self.maxTime * self.timeSellSliderValue, 10)
        self.timeSellText.SetText(self.prefixTxt + commonApiMgr.FormatSeconds(sellSec))
        self.timeSellSec = sellSec

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        if clickType == "closeBtn":
            clientApi.PopScreen()

    def GetAllCtrlStateAndExe(self):
        # 获取控件状态，并决定是否执行定时或取消定时
        param = {
            "toggleBuyState": self.timeBuyToggleState,
            "toggleSellState": self.timeSellToggleState,
            "buyTimingSec": round(self.timeBuySec, 2),
            "sellTimingSec": round(self.timeSellSec, 2)
        }
        self.SendMsgToServer("UpdateTimingData", {"pid": self.mPlayerId, "data": param})
        self.BroadcastEvent("UpdateClientTimingData", {"pid": self.mPlayerId, "data": param})
        self.BroadcastEvent("RefreshTimingInfoPanel", {"data": None})
