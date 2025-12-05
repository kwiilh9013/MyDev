# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.widget.uiBaseWidget import *


class AutoExchangePanel(UiBaseWidget):
    def __init__(self, uiInst, sysInst, path, param):
        UiBaseWidget.__init__(self, uiInst, sysInst, path)
        self.rootPanel = self.GetBaseUiControl("")
        self.param = param
        self.gameComp = engineApiGac.compFactory.CreateGame(engineApiGac.levelId)
        self.eStackPanelPath = "/exchangeStackPanel"
        self.rgBtnDict = {
            "closeBtn": "/closeBtn",
            "sellBtn": self.eStackPanelPath + "/btnStackPanel/sellBtn",
            "buyBtn": self.eStackPanelPath + "/btnStackPanel/buyBtn",
            "timingBtn": self.eStackPanelPath + "/funcBtnPanel/timingBtn",
            "recordBtn": self.eStackPanelPath + "/funcBtnPanel/recordBtn",
            "exeBtn": self.eStackPanelPath + "/funcBtnPanel/exeBtn"
        }
        self.countText = None
        self.countEditBox = None
        # 创建面板时，需要再次从云端传来的param获取出售列表、购买列表的上限值
        self.countContent = "63"
        self.redColor = (255.0 / 255.0, 65.0 / 255.0, 65.0 / 255.0)
        self.greenColor = (43.0 / 255.0, 168.0 / 255.0, 17.0 / 255.0)
        # 买卖输入框的值
        self.sellValue = self.param.get("autoSellValue", 63)
        self.buyValue = self.param.get("autoBuyValue", 63)
        # 批量出售、批量购买
        self.mode = "sell"
        self.itemScrollView = None
        self.itemScrollViewPath = self.eStackPanelPath + "/itemScrollView"
        self.itemScrollContentPath = self.itemScrollViewPath + uiUtils.TouchScrollViewPath
        self.itemPanelDict = {}
        self.itemPanelBtnDict = {}
        self.itemPanelBtnPressPos = (0, 0)
        self.lastSelectItemInst = None
        # 智能买卖数据，会暂存在服务端，不会上传到地图数据中保存
        self.itemSellCacheList = self.param.get("autoItemSellCacheList", [])
        self.itemBuyCacheList = self.param.get("autoItemBuyCacheList", [])
        self.lastClickTime = 0
        # [(cellInst, [(rePosX, rePosY), (x2, y2), ...])]
        self.flyItemDataArray = []
        self.startFlyAnim = False
        self.tipsInfoCount = 8
        self.Create()

    def Create(self):
        self.rootPanel.SetVisible(False)
        for key, path in self.rgBtnDict.items():
            uiUtils.UICreateBtn(self.uiInst, self._btnDict, key, self.path + path, None, self.OnCommonBtnPressUp)
        self.countText = self.GetBaseUiControl(self.eStackPanelPath + "/countSetPanel/countTxt").asLabel()
        self.countEditBox = self.GetBaseUiControl(self.eStackPanelPath + "/countSetPanel/countEditBox").asTextEditBox()
        self.itemScrollView = self.GetBaseUiControl(self.itemScrollViewPath).asScrollView()
        self.SwitchMode("sell")
        self.CreateItemPanel()
        self.RefreshItemPanel()
        # 定时信息显示
        self.RefreshTimingInfoPanel()

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def RefreshTimingInfoPanel(self, args=None):
        def SetColor(color):
            panel.GetChildByPath("/infoBg").asImage().SetSpriteColor(color)
            panel.GetChildByPath("/triangle").asImage().SetSpriteColor(color)
        # 刷新定时信息显示
        panel = self.GetBaseUiControl(self.eStackPanelPath + "/funcBtnPanel/timingInfoPanel")
        view = panel.GetChildByPath("/infoBg/scrollView").asScrollView()
        txtPath = view.GetScrollViewContentPath()
        textInst = self.uiInst.GetBaseUIControl(txtPath).asLabel()
        data = self.sys.timingData
        isBuy, isSell = data.get("toggleBuyState", False), data.get("toggleSellState", False)
        if not isBuy and not isSell:
            panel.SetVisible(False)
            return
        else:
            panel.SetVisible(True)
        timeStr = "00:00"
        if isBuy:
            # SetColor(self.redColor)
            timeStr = "买入：" + FormatSeconds(data.get("buyTimingSec", 10))
        elif isSell:
            # SetColor(self.greenColor)
            timeStr = "卖出：" + FormatSeconds(data.get("sellTimingSec", 10))
        textInst.SetText("定时%s" % timeStr)

    def Update(self):
        txt = self.countEditBox.GetEditText()
        if txt != self.countContent and txt != "":
            self.countContent = txt
            self.SetModeValue()
            self.UpdateItemListToServer()

    def SetPanelState(self, state):
        self.rootPanel.SetVisible(state)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def UpdateTimingRecord(self, args):
        self.param["timingRecordData"] = args["data"]

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        if clickType in ["sellBtn", "buyBtn"] and self.tipsInfoCount > 0:
            inst = self._btnDict[clickType]
            txt = "双击槽位的物品将其从槽位删除"
            self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
            self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
            self.tipsInfoCount -= 1
        if clickType == "closeBtn":
            self.SetPanelState(False)
        elif clickType == "sellBtn":
            self.SwitchMode("sell")
        elif clickType == "buyBtn":
            self.SwitchMode("buy")
        elif clickType == "timingBtn":
            param = {
                "data": self.sys.timingData,
            }
            clientApi.PushScreen(modConfig.ModNameSpace, "ScukeConvertTable_Timing", param)
        elif clickType == "recordBtn":
            param = {
                "data": self.param.get("timingRecordData", [])
            }
            clientApi.PushScreen(modConfig.ModNameSpace, "ScukeConvertTable_ExchangeRecord", param)
        elif clickType == "exeBtn":
            if self.mode == "sell":
                if self.itemSellCacheList.count(None) == 60:
                    self.OnTipSend("§c没有物品用于批量出售")
                    return
                self.ExeSellListItem()
            elif self.mode == "buy":
                if self.itemBuyCacheList.count(None) == 60:
                    self.OnTipSend("§c没有物品用于批量购买")
                    return
                self.ExeBuyListItem()

    def OnTipSend(self, text):
        referPanel = self._btnDict["exeBtn"]
        self.uiInst.tipInfoPanel.SetTipsShow(referPanel, text, None)
        self.uiInst.tipInfoPanel.SetTipsShow(referPanel, text, None)

    def SwitchMode(self, mode):
        def modeSet(state, text1, text2, text3):
            self._btnDict["sellBtn"].GetChildByPath("/selected").SetVisible(state)
            self._btnDict["buyBtn"].GetChildByPath("/selected").SetVisible(not state)
            self.countEditBox.SetEditText(text1)
            self.countText.SetText(text2)
            self._btnDict["exeBtn"].GetChildByPath("/label").asLabel().SetText(text3)
        self.mode = mode
        self.itemScrollView.SetScrollViewPercentValue(0)
        if self.mode == "sell":
            modeSet(True, str(self.sellValue), "保留上限", "出售")
            self.RefreshItemPanel(self.itemSellCacheList)
        elif self.mode == "buy":
            modeSet(False, str(self.buyValue), "上限数量", "购买")
            self.RefreshItemPanel(self.itemBuyCacheList)

    def CheckDoubleClick(self, t1, t2, index):
        # t1 为self属性，t2为新的时间，如果点击的槽位没有物品，也返回false
        self.lastClickTime = t2
        hasItem = False
        if self.mode == "buy":
            hasItem = self.itemBuyCacheList[index] is not None
        elif self.mode == "sell":
            hasItem = self.itemSellCacheList[index] is not None
        if t2 - t1 < 0.2 and hasItem:
            return True
        return False

    def CreateItemPanel(self):
        # 保存物品面板按钮回调、物品面板实例
        # 一共60个
        initBuyList = True
        if not self.itemBuyCacheList:
            initBuyList = False
        initSellList = True
        if not self.itemSellCacheList:
            initSellList = False
        viewObj = self.GetBaseUiControl(self.itemScrollViewPath)
        pathPrefix = uiUtils.GetScrollViewChildPath(viewObj)
        for i in range(0, 60):
            row = i // 6
            column = i % 6
            key = "itemPanel_%s_%s" % (row, column)
            path = self.itemScrollViewPath + pathPrefix + "/itemLineStackPanel%s/itemPanel%s" % (row, column)
            realPath = self.path + path
            itemPath = path + "/item"
            btnPath = realPath + "/item/ctrlBtn"
            self.itemPanelDict[key] = self.GetBaseUiControl(itemPath)
            param = {"isSwallow": True, "type": [row, column]}
            uiUtils.UICreateBtn(self.uiInst, self.itemPanelBtnDict, key, btnPath, param, self.OnItemBtnPressUp, self.OnItemBtnPressDown)
            if not initSellList:
                self.itemSellCacheList.append(None)
            if not initBuyList:
                self.itemBuyCacheList.append(None)

    def OnItemBtnPressUp(self, args):
        def UserDataReturn(t):
            inst = self.GetItemInst(r, c)
            self.uiInst.tipInfoPanel.SetTipsShow(inst, t, None)
            self.uiInst.tipInfoPanel.SetTipsShow(inst, t, None)
            self.ResetOtherPanelData()
        clickType = args['AddTouchEventParams']['type']
        posX, posY = args["TouchPosX"], args["TouchPosY"]
        x, y = self.itemPanelBtnPressPos
        if abs(posX - x) > 3 or abs(posY - y) > 3: return
        r, c = clickType
        index = r * 6 + c
        targetList = self.itemSellCacheList if self.mode == "sell" else self.itemBuyCacheList
        self.lastSelectItemInst = self.GetItemInst(r, c)
        # 将选中的物品加入买卖列表中操作
        lastItem = self.GetExchangePanelItemDict()
        # 如果双击槽位，槽位有物品，则删除该物品
        isDoubleClick = self.CheckDoubleClick(self.lastClickTime, time.time(), index)
        if isDoubleClick:
            self.DelItemDictFromList(lastItem, index)
            self.RefreshItemPanel(targetList)
            return
        if not lastItem: return
        # 如果是带有物品的容器物品或带有附魔属性的道具，则无法使用批量买卖功能
        ud = lastItem.get("userData", None)
        if ud is not None and type(ud) == dict:
            if "Items" in ud:
                txt = "带有物品的潜影盒无法放入"
                UserDataReturn(txt)
                return
            if "ench" in ud:
                txt = "带有附魔属性的道具无法放入"
                UserDataReturn(txt)
                return
        ret = self.CheckIsInList(lastItem, index)
        if ret[0] is None and ret[1] is None: return
        # 先给物品添加飞行动画，再刷新面板显示
        prMode = self.uiInst.exchangePanel.presentMode
        invLastIndex = self.uiInst.corePanel.lastSelectIndex
        eyeData = self.uiInst.tableEyePanel.lastSelectData
        self.ResetOtherPanelData()
        if prMode == "sell":
            if invLastIndex is None:
                invLastIndex = 0
            fromInst = self.uiInst.corePanel.cellInstList[invLastIndex][0]
        else:
            fromInst = self.uiInst.tableEyePanel.GetItemPanelData(eyeData[0])[0]
        toInst = self.lastSelectItemInst
        # 开始飞行动画
        self.BuildItemFlyData(fromInst, toInst)
        self.startFlyAnim = True
        if ret[0]:
            self.DelItemDictFromList(lastItem, ret[1])
        self.AddItemDictToList(lastItem, index)

    def EndFlyAnimRefresh(self):
        targetList = self.itemSellCacheList if self.mode == "sell" else self.itemBuyCacheList
        self.RefreshItemPanel(targetList)

    def OnItemBtnPressDown(self, args):
        clickType = args['AddTouchEventParams']['type']
        posX, posY = args["TouchPosX"], args["TouchPosY"]
        self.itemPanelBtnPressPos = (posX, posY)

    def GetItemInst(self, row, column):
        key = "itemPanel_%s_%s" % (row, column)
        if key not in self.itemPanelDict: return None
        return self.itemPanelDict[key]

    def SetModeValue(self):
        ret = self.GetValidEditValue()
        setattr(self, self.mode + "Value", ret)

    def GetValidEditValue(self):
        # 获取输入框的值
        if not self.countEditBox: return 0
        if self.countContent is None: return 0
        valueMap = {
            "buy": self.buyValue,
            "sell": self.sellValue
        }
        value = valueMap.get(self.mode, 0)
        try:
            newValue = int(self.countContent)
            if newValue < 0 or newValue == 64:
                self.countEditBox.SetEditText(str(value))
                return value
            newValue = min(newValue, 999)
            self.countEditBox.SetEditText(str(newValue))
            return newValue
        except ValueError:
            self.countEditBox.SetEditText(str(value))
            return value

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def UpdateSellAndBuyData(self, args):
        # 更新智能买卖的列表数据
        self.itemSellCacheList = args["sellList"]
        self.itemBuyCacheList = args["buyList"]

    def CheckIsInList(self, itemDict, i):
        # 查询是否在对应缓存列表内，返回真假和索引值，如果点击的槽位有其他物品，则返回假
        index = None
        if self.mode == "buy":
            if self.itemBuyCacheList[i] is not None:
                return None, None
            if itemDict in self.itemBuyCacheList:
                index = self.itemBuyCacheList.index(itemDict)
            return itemDict in self.itemBuyCacheList, index
        elif self.mode == "sell":
            if self.itemSellCacheList[i] is not None:
                return None, None
            if itemDict in self.itemSellCacheList:
                index = self.itemSellCacheList.index(itemDict)
            return itemDict in self.itemSellCacheList, index

    def AddItemDictToList(self, itemDict, index):
        # 将物品字典加进指定列表内
        itemDict = itemApi.FormatItemInfo(itemDict)
        if self.mode == "buy":
            self.itemBuyCacheList[index] = itemDict
        elif self.mode == "sell":
            self.itemSellCacheList[index] = itemDict
        self.UpdateItemListToServer()

    def DelItemDictFromList(self, itemDict, index):
        def DelTips():
            r, c = index // 6, index % 6
            inst = self.GetItemInst(r, c)
            txt = "已移除"
            self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None, 0.5)
            self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None, 0.5)
        # 从指定列表中删除物品字典
        if self.mode == "buy":
            if itemDict in self.itemBuyCacheList:
                self.itemBuyCacheList[index] = None
                DelTips()
        elif self.mode == "sell":
            if itemDict in self.itemSellCacheList:
                self.itemSellCacheList[index] = None
                DelTips()
        self.UpdateItemListToServer()

    def UpdateItemListToServer(self):
        # 将购买、出售列表数据更新至服务端
        param = {
            "pid": self.mPlayerId,
            "sell": self.itemSellCacheList,
            "sellValue": self.sellValue,
            "buy": self.itemBuyCacheList,
            "buyValue": self.buyValue
        }
        self.SendMsgToServer("UpdateAutoItemList", param)
        self.BroadcastEvent("UpdateClientSysAutoItemData", param)

    def GetExchangePanelItemDict(self):
        # 获取最后一次选中的物品的itemDict
        item = self.uiInst.exchangePanel.itemCache
        if not item: return None
        # 数量归一
        newItem = DeepCopy(itemApi.FormatItemInfo(item))
        newItem["count"] = 1
        return newItem

    def ResetOtherPanelData(self):
        # 重置其他面板的数据
        self.uiInst.exchangePanel.SetRootPanelVisible(False)
        self.uiInst.exchangePanel.itemCache = None
        self.uiInst.corePanel.CancelHighlightAndEndGrouping()
        self.uiInst.tableEyePanel.RefreshItemPanelSelectState(False)
        self.uiInst.tableEyePanel.lastSelectData = [None, None]

    def RefreshItemPanel(self, targetList=None):
        # 根据列表，刷新物品渲染实例
        if targetList is None:
            targetList = self.itemSellCacheList
        for index, itemDict in enumerate(targetList):
            row = index // 6
            column = index % 6
            inst = self.GetItemInst(row, column)
            if inst is None: continue
            self.RefreshItemInst(inst, itemDict)

    def RefreshItemInst(self, inst, itemDict):
        # 对某个物品面板根据物品字典进行刷新
        canSeeBool = itemDict is not None
        renderPanel = inst.GetChildByPath("/renderPanel")
        renderPanelFly = inst.GetChildByPath("/renderPanelFlying")
        renderItem = renderPanel.GetChildByPath("/item").asItemRenderer()
        renderFlyItem = renderPanelFly.GetChildByPath("/item").asItemRenderer()
        inst.GetChildByPath("/bg/cell_highlight").SetVisible(canSeeBool)
        if not canSeeBool:
            renderPanel.SetVisible(False)
            renderPanelFly.SetVisible(False)
        if canSeeBool:
            renderPanel.SetVisible(True)
            name, aux = itemDict["newItemName"], itemDict["newAuxValue"]
            enchant = "userData" in itemDict and itemDict["userData"] is not None and "ench" in itemDict["userData"]
            renderItem.SetUiItem(name, aux, enchant)
            renderFlyItem.SetUiItem(name, aux, enchant)

    def BuildItemFlyData(self, fromCellInst, toCellInst, flySec=0.14, reverse=False):
        # 构建物品飞行数据，传入物品格子实例，自动计算相关数据，仅播放from→to的飞行动画
        # flySec = 3.0
        # 获取前后两次点击的槽位的位置
        fromCellFlyInst = fromCellInst.GetChildByPath("/renderPanelFlying")
        toCellQInst = toCellInst.GetChildByPath("/renderPanelFlying")
        fromCellPos = fromCellFlyInst.GetGlobalPosition()
        toCellPos = toCellQInst.GetGlobalPosition()
        # 计算相对移动的坐标，算出初始坐标和终点坐标
        reFPos = fromCellFlyInst.GetPosition()
        dtPos = MathUtils.TupleSub(toCellPos, fromCellPos)
        reFTargetPos = MathUtils.TupleAdd(reFPos, dtPos)
        # 线性插值
        nowFPS = int(self.gameComp.GetFps())
        fromX, fromY = reFPos
        toX, toY = reFTargetPos
        lerpData = [
            [0.0, fromX, fromY, 0],
            [0.01, fromX, fromY, 0],
            [flySec, toX, toY, 0],
            [flySec + 0.01, toX, toY, 0]
        ]
        lerpResult = MathUtils.TimeLinearInterpolation(lerpData, nowFPS)
        finalPosList = [(i[1], i[2]) for i in lerpResult]
        if reverse:
            finalPosList.reverse()
        finalPosList.append(reFPos)
        self.flyItemDataArray.append([fromCellFlyInst, finalPosList])
        fromCellFlyInst.SetVisible(True)

    def SetItemFlyAnim(self):
        # 设置物品飞行
        for value in self.flyItemDataArray:
            posList = value[1]
            lenList = len(posList)
            if lenList == 0:
                self.flyItemDataArray.remove(value)
                continue
            posX, posY = posList[0]
            if lenList == 1:
                value[0].SetVisible(False)
            sizeX, sizeY = value[0].GetSize()
            value[0].SetPosition((posX - sizeX / 2.0, posY - sizeY / 2.0))
            posList.pop(0)
        if not self.flyItemDataArray:
            self.startFlyAnim = False
            self.EndFlyAnimRefresh()

    def ExeSellListItem(self):
        # 执行出售列表中的物品，需要背包拥有这些物品
        # 客户端物品校验
        invItem = self.uiInst.corePanel.invItemCache
        if invItem.count(None) == 36: return
        param = {"pid": self.mPlayerId, "data": self.itemSellCacheList, "limitCount": self.sellValue}
        self.SendMsgToServer("PlayerExeSellListItems", param)

    def ExeBuyListItem(self):
        # 执行购买列表中的物品
        invItem = self.uiInst.corePanel.invItemCache
        if invItem.count(None) == 0: return
        param = {"pid": self.mPlayerId, "data": self.itemBuyCacheList, "limitCount": self.buyValue}
        self.SendMsgToServer("PlayerExeBuyListItems", param)
