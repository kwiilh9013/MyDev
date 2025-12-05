# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.modClient.ui.widget.corePanel import CorePanel
from ScukeConvertTableScript.modClient.ui.widget.tableEyePanel import TableEyePanel
from ScukeConvertTableScript.modClient.ui.widget.exchangePanel import ExchangePanel
from ScukeConvertTableScript.modClient.ui.widget.tipInfoPanel import TipInfoPanel
from ScukeConvertTableScript.modClient.ui.widget.autoExchangePanel import AutoExchangePanel
from ScukeConvertTableScript.modClient.ui.uiAnimator import Animator
ViewBinder = clientApi.GetViewBinderCls()


class TableMain(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableMain, self).__init__(namespace, name, param)
        self.paramDict = param
        self.basePath = "tablePanel"
        self.rootPanel = None
        self.corePanel = None
        self.corePanelPath = self.basePath + "/mainScreenPanel/mainStackPanel/corePanel"
        self.tableEyePanel = None
        self.tableEyePanelPath = self.basePath + "/mainScreenPanel/mainStackPanel/tableEyePanel"
        self.exchangePanel = None
        self.exchangePanelPath = self.basePath + "/exchangePanel"
        self.tipInfoPanel = None
        self.tipInfoPanelPath = self.basePath + "/tipInfoPanel"
        self.autoExchangePanel = None
        self.autoExchangePanelPath = self.basePath + "/mainScreenPanel/autoExchangePanel"
        self.hasInit = False
        self.animator = None

    def Destroy(self):
        del self.animator
        super(TableMain, self).Destroy()

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()

    def Create(self):
        super(TableMain, self).Create()
        self.rootPanel = self.GetBaseUIControl(self.basePath)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#main.scuke_convert_table_render_tick")
    def OnRenderTick(self):
        # 每渲染帧执行一次
        self._mTick0 += 1
        if not self.hasInit and self._mTick0 % 1 == 0:
            if self.corePanel is None:
                self.corePanel = CorePanel(self, self._clientSystem, self.corePanelPath, self.paramDict)
                return
            if self.tableEyePanel is None:
                self.tableEyePanel = TableEyePanel(self, self._clientSystem, self.tableEyePanelPath, self.paramDict)
                return
            if self.exchangePanel is None:
                self.exchangePanel = ExchangePanel(self, self._clientSystem, self.exchangePanelPath, self.paramDict)
                return
            if self.tipInfoPanel is None:
                self.tipInfoPanel = TipInfoPanel(self, self._clientSystem, self.tipInfoPanelPath, self.paramDict)
                return
            if self.autoExchangePanel is None:
                self.autoExchangePanel = AutoExchangePanel(self, self._clientSystem, self.autoExchangePanelPath, self.paramDict)
                self.animator = Animator(self)
                self.hasInit = True
                return
        if self.corePanel and self.corePanel.startFlyAnim:
            self.corePanel.SetItemFlying()
        if self.autoExchangePanel and self.autoExchangePanel.startFlyAnim:
            self.autoExchangePanel.SetItemFlyAnim()
