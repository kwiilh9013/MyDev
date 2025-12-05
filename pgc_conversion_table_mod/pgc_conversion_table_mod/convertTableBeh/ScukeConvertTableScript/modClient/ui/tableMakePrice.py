# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr


class TableMakePrice(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableMakePrice, self).__init__(namespace, name, param)
        self.paramDict = param
        self.pricePanelPath = "/makePricePanel/pricePanel"
        self.itemPanelPath = self.pricePanelPath + "/itemPanel"
        self.rgBtnDict = {
            "closeBtn": self.pricePanelPath + "/headPanel/closeBtn",
            "confirmBtn": self.pricePanelPath + "/confirmBtn"
        }
        self._btnDict = {}
        self.itemDict = self.paramDict.get("itemDict", {})
        self.editBox = None
        self.editBoxValue = None
        # [(itemName, aux), [cnName, emcValue]]
        self.emcData = self.paramDict.get("emcData", None)
        self.itemInst = None
        self.itemText = None
        self.headText = None
        self.timer = None

    def Destroy(self):
        engineApiGac.CancelTimer(self.timer)
        super(TableMakePrice, self).Destroy()

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()

    def Create(self):
        super(TableMakePrice, self).Create()
        self.headText = self.GetBaseUIControl(self.pricePanelPath + "/headPanel/headTxt").asLabel()
        for key, path in self.rgBtnDict.items():
            uiUtils.UICreateBtn(self, self._btnDict, key, path, None, self.OnCommonBtnPressUp)
        self.editBox = self.GetBaseUIControl(self.itemPanelPath + "/emcEditBox").asTextEditBox()
        if self.emcData is not None:
            v = self.emcData[1][1]
            self.editBoxValue = v
            self.editBox.SetEditText(str(v))
        self.GetBaseUIControl(self.itemPanelPath + "/item/renderPanel").SetVisible(True)
        self.itemInst = self.GetBaseUIControl(self.itemPanelPath + "/item/renderPanel/item").asItemRenderer()
        self.itemText = self.GetBaseUIControl(self.itemPanelPath + "/itemNameTxt").asLabel()
        if not self.itemDict: return
        itemDict = self.itemDict
        name, aux = itemDict["newItemName"], itemDict["newAuxValue"]
        enchant = "userData" in itemDict and itemDict["userData"] is not None and "ench" in itemDict["userData"]
        itemInfo = self.GetItemInfo(self.mPlayerId, name, aux, enchant)
        cnName = itemInfo["itemName"]
        text = "%s aux: %s" % (cnName, aux)
        self.itemText.SetText(text)
        self.itemInst.SetUiItem(name, aux, enchant, itemDict.get("userData", None))
        self.itemInst.SetVisible(True)

    def GetItemInfo(self, pid, itemName, aux, enchant=False):
        comp = engineApiGac.compFactory.CreateItem(pid)
        return comp.GetItemBasicInfo(itemName, aux, enchant)

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        if clickType == "closeBtn":
            clientApi.PopScreen()
        elif clickType == "confirmBtn":
            self.CheckAndReadEditBoxData()

    def CheckAndReadEditBoxData(self):
        # 获取玩家输入框数据，如果异常就清除
        if self.emcData is None: return
        text = self.editBox.GetEditText()
        try:
            v = int(text)
            if v <= 0:
                self.ErrorReturn()
                return
            # 超过亿级别的单位无法作为int存储
            v = min(v, 999999999)
            # 数值正常，更新数值通知服务端
            self.emcData[1][1] = v
            updateEmcDict = {self.emcData[0]: self.emcData[1]}
            # 通知服务端改价
            self.SendMsgToServer("OnMakePrice", {"pid": self.mPlayerId, "data": updateEmcDict})
            clientApi.PopScreen()
        except ValueError:
            self.ErrorReturn()
            return

    def ErrorReturn(self):
        lastValue = self.emcData[1][1]
        self.editBox.SetEditText(str(lastValue))
        self.SetWarning()

    def SetWarning(self):
        engineApiGac.CancelTimer(self.timer)
        self.headText.SetText("§c请输入正整数！")
        self.timer = engineApiGac.AddTimer(2.0, self.headText.SetText, "定价")
