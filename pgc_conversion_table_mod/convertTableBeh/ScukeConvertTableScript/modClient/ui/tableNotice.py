# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr


class TableNotice(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableNotice, self).__init__(namespace, name, param)
        self.paramDict = param
        self.rootPath = "/infoNoticePanel"
        self.noticePanelPath = self.rootPath + "/noticePanel"
        self._btnDict = {}
        self.rgBtnDict = {
            "closeBtn": self.noticePanelPath + "/headPanel/closeBtn",
            "confirmBtn": self.noticePanelPath + "/confirmBtn",
            "cancelBtn": self.noticePanelPath + "/cancelBtn"
        }
        self.headText = None
        self.detailText = None
        self.confirmText = None
        self.cancelText = None
        self.tempInst = None
        self.confirmFunc = self.paramDict.get("confirmMethod", None)
        self.cancelFunc = self.paramDict.get("cancelMethod", None)

    def Destroy(self):
        super(TableNotice, self).Destroy()

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()

    def Create(self):
        super(TableNotice, self).Create()
        for key, path in self.rgBtnDict.items():
            uiUtils.UICreateBtn(self, self._btnDict, key, path, None, self.OnCommonBtnPressUp)
        self.headText = self.GetBaseUIControl(self.noticePanelPath + "/headPanel/headTxt").asLabel()
        self.detailText = self.GetBaseUIControl(self.noticePanelPath + "/infoTxt").asLabel()
        self.confirmText = self.GetBaseUIControl(self.noticePanelPath + "/confirmBtn/label").asLabel()
        self.cancelText = self.GetBaseUIControl(self.noticePanelPath + "/cancelBtn/label").asLabel()
        headTxt = self.paramDict.get("headTxt", "提示")
        infoTxt = self.paramDict.get("infoTxt", "是否要继续？")
        confirmTxt = self.paramDict.get("confirmTxt", "确认")
        cancelTxt = self.paramDict.get("cancelTxt", "取消")
        self.headText.SetText(headTxt)
        self.detailText.SetText(infoTxt)
        self.confirmText.SetText(confirmTxt)
        self.cancelText.SetText(cancelTxt)

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        if clickType == "closeBtn":
            clientApi.PopScreen()
        elif clickType == "confirmBtn":
            if self.confirmFunc is not None:
                self.confirmFunc()
                clientApi.PopScreen()
        elif clickType == "cancelBtn":
            if self.cancelFunc is not None:
                self.cancelFunc()
            clientApi.PopScreen()