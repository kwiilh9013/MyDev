# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
ScrollViewPath = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"


class TableExchangeRecord(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableExchangeRecord, self).__init__(namespace, name, param)
        self.paramDict = param
        self.recordPanelPath = "/exchangeRecordPanel/recordPanel"
        self._btnDict = {}
        self.rgBtnDict = {
            "closeBtn": self.recordPanelPath + "/headPanel/closeBtn"
        }
        self.recordDataList = self.paramDict.get("data", [])[:]
        self.recordDataList.reverse()

    def Destroy(self):
        super(TableExchangeRecord, self).Destroy()

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()

    def Create(self):
        super(TableExchangeRecord, self).Create()
        for key, path in self.rgBtnDict.items():
            uiUtils.UICreateBtn(self, self._btnDict, key, path, None, self.OnCommonBtnPressUp)
        fatherPath = self.recordPanelPath + "/recordTextScrollView" + ScrollViewPath
        cInst = self.GetBaseUIControl(fatherPath + '/mCloneTextPanel')
        if not self.recordDataList:
            cInst.GetChildByPath("/text").asLabel().SetText("暂无任何定时买卖记录")
            return
        cInst.SetVisible(True)
        for index, text in enumerate(self.recordDataList):
            unitPath = "recordTextPanel%s" % index
            unitRealPath = fatherPath + "/%s" % unitPath
            self.Clone(fatherPath + "/mCloneTextPanel", fatherPath, unitPath, False, False)
            unitInst = self.GetBaseUIControl(unitRealPath)
            unitInst.GetChildByPath("/text").asLabel().SetText(text)
        cInst.SetVisible(False)
        self.UpdateScreen(True)

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        if clickType == "closeBtn":
            clientApi.PopScreen()
