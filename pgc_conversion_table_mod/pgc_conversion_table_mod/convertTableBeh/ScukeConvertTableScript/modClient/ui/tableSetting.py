# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
ScrollViewPath = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"


class TableSetting(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableSetting, self).__init__(namespace, name, param)
        self.settingData = param["settingData"]
        self._btnDict = {}
        self.setPanelPath = "/settingPanel/setPanel"
        self.hasCreate = False
        self.svFatherPath = self.setPanelPath + "/settingScrollView" + ScrollViewPath
        self.togglePaths = {
            "itemEmcIsGlobal": self.svFatherPath + "/slot1GroupStackPanel/setSinglePanel0/toggle",
            "otherCanMakePrice": self.svFatherPath + "/slot1GroupStackPanel/setSinglePanel1/toggle",
            "teamMemorySharing": self.svFatherPath + "/slot2GroupStackPanel/setSinglePanel0/toggle",
            "teamEmcSharing": self.svFatherPath + "/slot2GroupStackPanel/setSinglePanel1/toggle",
            "metaVisualUI": self.svFatherPath + "/slot3GroupStackPanel/setSinglePanel0/toggle"
        }
        self.toggleDict = {}

    def Destroy(self):
        self.UpdateSettingData()
        super(TableSetting, self).Destroy()

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()

    def Create(self):
        super(TableSetting, self).Create()
        uiUtils.UICreateBtn(self, self._btnDict, "closeBtn", self.setPanelPath + "/headPanel/closeBtn", None, self.OnCommonBtnPressUp)
        for key, value in self.settingData.items():
            self.toggleDict[key] = self.GetBaseUIControl(self.togglePaths[key]).asSwitchToggle()
            self.toggleDict[key].SetToggleState(value)
        self.hasCreate = True

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        if clickType == "closeBtn":
            clientApi.PopScreen()

    def UpdateSettingData(self):
        # 更新设置数据
        for key, inst in self.toggleDict.items():
            self.settingData[key] = inst.GetToggleState()
        self.SendMsgToServer("UpdateGlobalSettingData", {"data": self.settingData})
