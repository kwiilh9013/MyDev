# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.widget.uiBaseWidget import *
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance
from ScukeConvertTableScript.modClient.ui.uiDef import UIDef

ViewBinder = clientApi.GetViewBinderCls()


class CorePanel(UiBaseWidget):
    def __init__(self, uiInst, sysInst, path, param):
        UiBaseWidget.__init__(self, uiInst, sysInst, path)
        self.param = param
        self.gameComp = engineApiGac.compFactory.CreateGame(engineApiGac.levelId)
        self.emcPanel = None
        self.settingsData = self.param.get("globalSetting", {})
        self.emcValue = self.param.get("emcValue", 0)
        self.hasPower = self.param.get("hasPower", False)
        self.emcText = None
        self.rootPanel = self.GetBaseUiControl("")
        # 一键整理
        self._sortCD = 1
        self._sortCDTimer = None
        self._sortType = None
        self._isCanSort = True

        self.stackPanelPath = "/infoStackPanel"
        self.btnGroupPanel = None
        self.btnGroupPath = self.stackPanelPath + "/btnGroupPanel"
        self.invStackPath = self.stackPanelPath + "/inventoryStackPanel"
        self.invItemStackPath = self.invStackPath + "/itemStackPanel"
        self.registerBtnDict = {
            "verticalSortBtn": self.stackPanelPath + "/sortPanel/verticalSortBtn",
            "horizontalSortBtn": self.stackPanelPath + "/sortPanel/horizontalSortBtn",
            "settingBtn": self.btnGroupPath + "/settingBtn",
            "teamBtn": self.btnGroupPath + "/teamBtn",
            "autoExchangeBtn": self.btnGroupPath + "/autoExchangeBtn",
            "sellBtn": self.btnGroupPath + "/sellBtn",
            "visibleBtn": "/visibleBtn"
        }
        # 根据背包槽位映射
        self.cellInstList = []
        self.newSelectIndex = None
        self.lastSelectIndex = None
        self.highlightSelecting = False
        self.invBtnClickTime = 0
        self.canMoveItem = False
        self.flyItemArray = []
        self.startFlyAnim = False
        self.itemGroupingRecord = set()
        self.iGRLen = 0
        self.selectItemCache = {}
        self.invItemCache = {}
        # 用于处理异常分堆的暂存变量
        self.igStartGrouping = False
        self.Create()

    def Create(self):
        uiUtils.UICreateBtn(self.uiInst, self._btnDict, "closeBtn", self.path + "/closeBtn", None, self.OnClose)
        for key, path in self.registerBtnDict.iteritems():
            uiUtils.UICreateBtn(self.uiInst, self._btnDict, key, self.path + path, None, self.OnCommonBtnPressUp)
        self.emcPanel = self.GetBaseUiControl(self.stackPanelPath + "/emcPanel")
        self.emcText = self.emcPanel.GetChildByPath("/emcValue").asLabel()
        self.emcText.SetText("EMC: " + str(self.param["emcValue"]))
        self.CreateInv()

    def CreateInv(self):
        # 注册背包
        for i in range(0, 36):
            n = i // 9
            m = i % 9
            cellPath = self.invItemStackPath + "%s/itemPanel%s/item" % (n, m)
            self.cellInstList.append((self.GetBaseUiControl(cellPath), self.path + cellPath))
        # 背包按钮、物品显示
        self.invItemCache = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
        for index, content in enumerate(self.cellInstList):
            btnPath = content[1] + "/ctrlBtn"
            uiUtils.UICreateBtn(self.uiInst, self._btnDict, "cell_%s" % index, btnPath, None, self.OnInvCellBtnPressUp)
            # 注册分堆功能回调
            self._btnDict["cell_%s" % index].SetButtonTouchDownCallback(self.OnInvCellBtnPressDown)
            self._btnDict["cell_%s" % index].SetButtonTouchMoveInCallback(self.OnInvCellBtnMoveIn)
            self._btnDict["cell_%s" % index].SetButtonTouchMoveOutCallback(self.OnInvCellBtnMoveOut)
            self._btnDict["cell_%s" % index].SetButtonTouchCancelCallback(self.OnInvCellBtnCancel)
            self.RefreshOneCellInst(self.invItemCache, index)

    def RefreshOneCellInst(self, invItems, index):
        # 刷新某个格子实例的内容，需要从self.cellInstList中获取实例
        def itemStateSet(obj, state, count=1):
            obj.GetChildByPath("/bg/cell_highlight").SetVisible(state)
            obj.GetChildByPath("/bg/cell_normal").SetVisible(not state)
            countTxt = obj.GetChildByPath("/countTxt").asLabel()
            if countTxt:
                countTxt.SetVisible(state and count > 1)
                countTxt.SetText(str(count))
        inst = self.cellInstList[index][0]
        renderPanel = inst.GetChildByPath("/renderPanel")
        renderPanelFly = inst.GetChildByPath("/renderPanelFlying")
        renderPanelFly.SetVisible(False)
        item = invItems[index]
        inst.GetChildByPath("/bg/cell_select").SetVisible(False)
        if not item:
            renderPanel.SetVisible(False)
            itemStateSet(inst, False)
        else:
            c = item["count"]
            renderPanel.SetVisible(True)
            itemStateSet(inst, True, c)
            itemName, itemAux = item["newItemName"], item["newAuxValue"]
            userData = item["userData"]
            enchant = False if userData is None else "ench" in userData
            itemRender = renderPanel.GetChildByPath("/item").asItemRenderer()
            itemRender.SetUiItem(itemName, itemAux, enchant, userData)
            itemRenderFly = renderPanelFly.GetChildByPath("/item").asItemRenderer()
            itemRenderFly.SetUiItem(itemName, itemAux, enchant, userData)

    def Destroy(self):
        hud = clientApi.GetUI(modConfig.ModNameSpace, "ScukeConvertTableHud")
        if hud: hud.isInMainScreen = False
        UiBaseWidget.Destroy(self)

    def Update(self):
        pass

    def CheckItemGroupingChange(self):
        # 检测是否产生了新指定的分堆槽位，需要超过两个额外槽位，且槽位数量不大于选中物品数量
        if not self.selectItemCache: return False
        l = len(self.itemGroupingRecord)
        return self.iGRLen < l <= self.selectItemCache["count"] and l >= 2

    def GetClickSlotIndex(self, args):
        clickType = args['AddTouchEventParams']['type']
        try:
            slotIndex = int(clickType.split("_")[1])
        except ValueError:
            return None
        return slotIndex

    def CanItemGrouping(self, index):
        # 物品是否可分堆到指定槽位，返回(bool, slot)
        if not self.invItemCache: return False, index
        if self.invItemCache[index] is not None: return False, index
        return self.lastSelectIndex is not None and self.highlightSelecting and self.canMoveItem and index != self.lastSelectIndex, self.lastSelectIndex

    def OnInvCellBtnPressDown(self, args):
        # 分堆过程开始
        slotIndex = self.GetClickSlotIndex(args)
        if slotIndex is None: return
        self.igStartGrouping = True
        if self.uiInst.exchangePanel:
            if self.uiInst.exchangePanel.presentMode == "sell":
                self.uiInst.exchangePanel.SetRootPanelVisible(False)

    def OnInvCellBtnMoveIn(self, args):
        # 记录分堆槽位
        slotIndex = self.GetClickSlotIndex(args)
        if slotIndex is None: return
        if self.CanItemGrouping(slotIndex)[0]:
            self.itemGroupingRecord.add(slotIndex)
            # 异常的分堆触发方式，则不做处理
            if not self.igStartGrouping and len(self.itemGroupingRecord) >= 2:
                self.CancelHighlightAndEndGrouping()
                if self.uiInst.exchangePanel.presentMode == "sell":
                    self.uiInst.exchangePanel.SetRootPanelVisible(False)
                return
            # 如果产生了新的分堆槽位，则通知服务端更新最新物品数据
            if self.CheckItemGroupingChange():
                self.iGRLen = len(self.itemGroupingRecord)
                data = {
                    "fromSlot": self.lastSelectIndex,
                    "cacheItem": self.selectItemCache,
                    "toSlots": list(self.itemGroupingRecord),
                    "pid": self.mPlayerId
                }
                self.sys.NotifyToServer("OnItemGrouping", data)
            else:
                self.RefreshOneCellInst(self.invItemCache, self.lastSelectIndex)

    def OnInvCellBtnMoveOut(self, args):
        # 按钮移出触发，用于取消分堆记录
        slotIndex = self.GetClickSlotIndex(args)
        if slotIndex is None: return
        if len(self.itemGroupingRecord) == 0:
            self.igStartGrouping = False

    def OnInvCellBtnCancel(self, args):
        # 按住滑动过多个按钮，之后最后松手后会触发，触发时的传入参数默认为第一个按下的按钮的参数
        slotIndex = self.GetClickSlotIndex(args)
        if slotIndex is None: return
        # 此时也需要取消高亮选择
        self.CancelHighlightAndEndGrouping()

    def CancelHighlightAndEndGrouping(self):
        self.invItemCache = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
        self.SelectCellToHighlight(0, 0, None, None, self.invItemCache)
        self.EndItemGrouping()

    def EndItemGrouping(self):
        # 分堆过程结束
        self.canMoveItem = False
        self.newSelectIndex = None
        self.lastSelectIndex = None
        self.itemGroupingRecord.clear()
        self.iGRLen = 0
        self.selectItemCache = {}

    def OnInvCellBtnPressUp(self, args):
        slotIndex = self.GetClickSlotIndex(args)
        if slotIndex is None: return
        self.invItemCache = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
        self.newSelectIndex = slotIndex
        item = self.invItemCache[self.newSelectIndex]
        t = time.time()
        # 选择高亮某个槽位的外框，并缓存选中槽位的物品
        if self.SelectCellToHighlight(t, self.invBtnClickTime, self.newSelectIndex, self.lastSelectIndex, self.invItemCache):
            self.canMoveItem = True
            self.selectItemCache = DeepCopy(item)
        # 操作为合堆
        if self.CheckIsTryingStackTogether(t, self.invBtnClickTime, self.newSelectIndex, self.lastSelectIndex, self.invItemCache):
            ret = self.StackOneItemExe(self.invItemCache, self.newSelectIndex)
            self.NotifyServerTryExchangeItems(ret, True)
            self.invBtnClickTime = t
            self.lastSelectIndex = slotIndex
            self.canMoveItem = False
            self.selectItemCache = {}
            return
        # 如果前后两次槽位的物品slot不一样，且没有进行分堆操作，则进一步判定
        bool1 = self.lastSelectIndex is not None and not self.highlightSelecting and self.canMoveItem
        if bool1 and len(self.itemGroupingRecord) <= 1:
            self.canMoveItem = False
            self.selectItemCache = {}
            ret = self.MarkItemStackData(self.invItemCache, self.lastSelectIndex, self.newSelectIndex)
            if ret:
                self.NotifyServerTryExchangeItems(ret)
                self.EndItemGrouping()
        self.invBtnClickTime = t
        self.lastSelectIndex = slotIndex
        # 设置物品购买、出售面板显示
        if self.uiInst.autoExchangePanel:
            autoV = self.uiInst.autoExchangePanel.rootPanel.GetVisible()
            self.uiInst.exchangePanel.SetRootPanelVisible(self.canMoveItem and not autoV)
        if self.canMoveItem:
            self.sys.BroadcastEvent("ShowExchangeItemData", {"item": self.selectItemCache, "mode": "sell"})

    def StackOneItemExe(self, invItems, itemIndex):
        # 对背包中的某个槽位的物品进行合堆尝试
        targetItem = invItems[itemIndex]
        if not targetItem: return []
        itemName = targetItem["newItemName"]
        aux = targetItem["newAuxValue"]
        nowCount = targetItem["count"]
        maxStack = itemApi.GetItemMaxStackSize(engineApiGac.compFactory, engineApiGac.levelId, itemName, aux)
        if nowCount == maxStack: return []
        # 需要吸附的物品数量
        needCount = maxStack - nowCount
        markToStackItemList = []
        for index, i in enumerate(invItems):
            # 搜寻出背包内其他这类物品
            if index != itemIndex and itemApi.IsSameItem(targetItem, i):
                markToStackItemList.append([index, i])
        if markToStackItemList:
            # 优先吸附数量少的和距离这个槽位最近的其他槽位
            markToStackItemList.sort(key=lambda x: (x[1]["count"] if x[1]["count"] != maxStack else 999) * abs(itemIndex - x[0]))
        # 已吸附物品数量
        hasCount = 0
        afterStackMarkItemList = []
        for value in markToStackItemList:
            slot = value[0]
            if slot == itemIndex: continue
            iDict = value[1]
            count = iDict["count"]
            if hasCount >= needCount:
                break
            reFatherPos, fromTargetPos, toTargetPos = self.GetItemFlyInitPos(invItems, slot, itemIndex)
            if count + hasCount > needCount:
                afterStackMarkItemList.append([reFatherPos, fromTargetPos, iDict, slot, itemIndex, (needCount - hasCount), targetItem, False])
                break
            hasCount += count
            afterStackMarkItemList.append([reFatherPos, fromTargetPos, iDict, slot, itemIndex, count, targetItem, True])
        return afterStackMarkItemList

    def MarkItemStackData(self, invItems, fromSlotIndex, toSlotIndex):
        # 标记物品合堆数据
        ret = self.GetItemFlyInitPos(invItems, fromSlotIndex, toSlotIndex)
        if ret:
            reFatherPos, fromTargetPos, toTargetPos = ret
            # 点击槽位不一样，开始判定是否需要移动、合堆
            if fromTargetPos != toTargetPos:
                moveOldItem = invItems[fromSlotIndex]
                moveNewItem = invItems[toSlotIndex]
                moveCount = moveOldItem["count"]
                hasMoveAll = True
                # 如果旧槽位的数量加上新槽位的数量大于可堆叠最大数量，则仅移动部分过去
                if itemApi.IsSameItem(DeepCopy(moveOldItem), DeepCopy(moveNewItem)):
                    maxStack = itemApi.GetItemMaxStackSize(engineApiGac.compFactory, engineApiGac.levelId, moveNewItem["newItemName"], moveOldItem["newAuxValue"])
                    if 1 < maxStack < moveOldItem["count"] + moveNewItem["count"]:
                        moveCount = maxStack - moveNewItem["count"]
                        hasMoveAll = False if moveCount > 0 else True
                moveAnimArray = [(reFatherPos, fromTargetPos, moveOldItem, fromSlotIndex, toSlotIndex, moveCount, moveNewItem, hasMoveAll)]
                # 如果前后两次槽位的物品slot不一样，则进一步判定
                if not itemApi.IsTwoItemSame(moveNewItem, moveOldItem, engineApiGac.compFactory, engineApiGac.levelId) and hasMoveAll:
                    moveAnimArray.append((reFatherPos, toTargetPos, moveNewItem, toSlotIndex, fromSlotIndex, moveNewItem["count"], moveOldItem, hasMoveAll))
                return moveAnimArray
        return []

    def GetItemFlyInitPos(self, invItems, fromIndex, toIndex):
        # 获取物品栏中某个槽位需要前往的目标槽位的位置数据
        if invItems[fromIndex]:
            # 获取前后两次点击的槽位的位置
            fromCellFlyInst = self.cellInstList[fromIndex][0].GetChildByPath("/renderPanelFlying")
            toCellFlyInst = self.cellInstList[toIndex][0].GetChildByPath("/renderPanelFlying")
            fromCellPos = fromCellFlyInst.GetGlobalPosition()
            toCellPos = toCellFlyInst.GetGlobalPosition()
            # 计算相对移动的坐标
            reFatherPos = fromCellFlyInst.GetPosition()
            dtPos = MathUtils.TupleSub(toCellPos, fromCellPos)
            fromTargetPos = MathUtils.TupleAdd(reFatherPos, dtPos)
            toTargetPos = MathUtils.TupleSub(reFatherPos, dtPos)
            return reFatherPos, fromTargetPos, toTargetPos
        return None

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def UpdateSettingData(self, args):
        self.settingsData = args["data"]

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def PushTableTeamUI(self, args):
        param = {
            'teamDic':args['teamDic'],
            'allPlayerName':args['allPlayerName']
            }
        Instance.mUIManager.PushUI(UIDef.UI_TableTeamManager,param)

    def OnCommonBtnPressUp(self, args):
        clickType = args['AddTouchEventParams']['type']
        def sortTime():
            self._isCanSort = True
        if clickType == "verticalSortBtn":
            if self._sortType == 'vertical':
                if self._isCanSort:
                    if self._sortCDTimer:
                        engineApiGac.CancelTimer(self._sortCDTimer)
                    self._sortCDTimer = engineApiGac.AddTimer(self._sortCD,sortTime)
                    self.sys.NotifyToServer("SortPlayInventory", {"isVerticalkey": True, "playerId": self.mPlayerId})
                    self._isCanSort = False
            else:
                self._sortType = 'vertical'
                if self._sortCDTimer:
                    engineApiGac.CancelTimer(self._sortCDTimer)
                self._sortCDTimer = engineApiGac.AddTimer(self._sortCD,sortTime)
                self.sys.NotifyToServer("SortPlayInventory", {"isVerticalkey": True, "playerId": self.mPlayerId})
        elif clickType == "horizontalSortBtn":
            if self._sortType == 'horizontal':
                if self._isCanSort:
                    if self._sortCDTimer:
                        engineApiGac.CancelTimer(self._sortCDTimer)
                    self._sortCDTimer = engineApiGac.AddTimer(self._sortCD,sortTime)
                    self.sys.NotifyToServer("SortPlayInventory", {"isVerticalkey": False, "playerId": self.mPlayerId})
                    self._isCanSort = False
            else:
                self._sortType = 'horizontal'
                if self._sortCDTimer:
                    engineApiGac.CancelTimer(self._sortCDTimer)
                self._sortCDTimer = engineApiGac.AddTimer(self._sortCD,sortTime)
                self.sys.NotifyToServer("SortPlayInventory", {"isVerticalkey": False, "playerId": self.mPlayerId})
        elif clickType == "settingBtn":
            if not self.hasPower:
                inst = self._btnDict["settingBtn"]
                txt = "§c§l你不是房主，无法进行设置操作"
                self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
                self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
                return
            # 推出设置UI
            param = {
                "settingData": self.settingsData
            }
            clientApi.PushScreen(modConfig.ModNameSpace, "ScukeConvertTable_Setting", param)
        elif clickType == "teamBtn":
            self.SendMsgToServer('TryPushTableTeamUI',{"pid": self.mPlayerId})
        elif clickType == "autoExchangeBtn":
            v = self.uiInst.autoExchangePanel.rootPanel.GetVisible()
            self.uiInst.autoExchangePanel.SetPanelState(not v)
            self.uiInst.exchangePanel.SetRootPanelVisible(False)
        elif clickType == "sellBtn":
            self.invItemCache = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
            if self.invItemCache.count(None) == 36:
                inst = self._btnDict["sellBtn"]
                txt = "§c§l背包里没有物品"
                self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
                self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
                return
            # 推出提示UI
            param = {
                "confirmMethod": self.OnSellInvAllItems,
                "headTxt": "出售操作",
                "infoTxt": "是否要将背包中的所有物品出售？"
            }
            clientApi.PushScreen(modConfig.ModNameSpace, "ScukeConvertTable_Notice", param)
        elif clickType == "visibleBtn":
            v = self.uiInst.tableEyePanel.rootPanel.GetVisible()
            self.uiInst.tableEyePanel.SetRootPanelVisible(not v)

    def OnSellInvAllItems(self):
        # 卖出背包所有物品
        self.SendMsgToServer("TrySellInvAllItems", {"pid": self.mPlayerId})
        self.BroadcastEvent("TrySellInvAllItems", {"pid": self.mPlayerId})

    def OnClose(self, args):
        clientApi.PopScreen()

    def CheckIsTryingStackTogether(self, t1, t2, newIndex, lastIndex, invItemList):
        # 检测是否尝试对某个槽位的物品进行合堆
        dt = t1 - t2
        if 0 < dt < 0.2:
            if newIndex == lastIndex:
                if invItemList[newIndex] is not None:
                    return True
        return False

    def SelectCellToHighlight(self, t1, t2, newIndex, lastIndex, invItemsList):
        # 选中一个槽位高亮外框，或取消高亮
        if newIndex is None and lastIndex is None:
            self.highlightSelecting = False
            self.RefreshInventoryUI()
            return self.highlightSelecting
        if lastIndex is None: lastIndex = newIndex
        lastCellInst = self.cellInstList[lastIndex][0]
        newCellInst = self.cellInstList[newIndex][0]
        lastCellInst.GetChildByPath("/bg/cell_select").SetVisible(False)
        newItem = invItemsList[newIndex]
        oldItem = invItemsList[lastIndex]
        if oldItem == newItem and lastIndex == newIndex:
            self.highlightSelecting = not self.highlightSelecting
        if lastIndex != newIndex:
            self.highlightSelecting = not self.highlightSelecting
        if newItem is None:
            self.highlightSelecting = False
        newCellInst.GetChildByPath("/bg/cell_select").SetVisible(self.highlightSelecting)
        return self.highlightSelecting

    def NotifyServerTryExchangeItems(self, arrayList, isStacking=False):
        self.sys.NotifyToServer("TryExchangeSlotItem", {"data": arrayList, "pid": self.mPlayerId, "isStacking": isStacking})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def StartItemFlyingAnim(self, args):
        # 接收服务端消息，开始物品飞行动画
        animList = args["data"]
        for index, value in enumerate(animList):
            inst = self.cellInstList[value[2]][0]
            visible = value[4]
            inst.GetChildByPath("/renderPanel").SetVisible(not visible)
            inst.GetChildByPath("/bg/cell_highlight").SetVisible(not visible)
            inst.GetChildByPath("/bg/cell_normal").SetVisible(visible)
            inst.GetChildByPath("/countTxt").SetVisible(not visible and inst.GetChildByPath("/countTxt").GetVisible())
            self.BuildItemFlyingData(value, 0.14)
        self.startFlyAnim = True

    def BuildItemFlyingData(self, value, flySec=0.14):
        # 物品飞行时间，单位秒
        # flySec = 0.14
        # 生成物品飞行数据
        nowFPS = int(self.gameComp.GetFps())
        fromPos, toPos = value[0], value[1]
        x1, y1 = fromPos
        x2, y2 = toPos
        inst = self.cellInstList[value[2]][0]
        flyItemInst = inst.GetChildByPath("/renderPanelFlying")
        lerpData = [
            [0.0, x1, y1, 0],
            [0.01, x1, y1, 0],
            [flySec, x2, y2, 0],
            [flySec + 0.01, x2, y2, 0]
        ]
        lerpResult = MathUtils.TimeLinearInterpolation(lerpData, nowFPS)
        finalPosList = [(i[1], i[2]) for i in lerpResult]
        finalPosList.append(fromPos)
        self.flyItemArray.append([flyItemInst, finalPosList])
        flyItemInst.SetVisible(True)

    def SetItemFlying(self):
        # 设置物品飞行
        for value in self.flyItemArray:
            posList = value[1]
            lenList = len(posList)
            if lenList == 0:
                self.flyItemArray.remove(value)
                continue
            posX, posY = posList[0]
            if lenList == 1:
                value[0].SetVisible(False)
            sizeX, sizeY = value[0].GetSize()
            value[0].SetPosition((posX - sizeX / 2.0, posY - sizeY / 2.0))
            posList.pop(0)
        if not self.flyItemArray:
            self.startFlyAnim = False
            self.RefreshInventoryUI()

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def UpdateEMCValue(self, args):
        self.emcValue = args["value"]

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def RefreshInventoryUI(self, args=None):
        self.invItemCache = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
        for i in range(0, 36):
            # 刷新背包对应槽位显示
            self.RefreshOneCellInst(self.invItemCache, i)
        if args and "emcValue" in args:
            self.emcText.SetText("EMC: " + str(args["emcValue"]))
        if args and "endSelecting" in args:
            self.CancelHighlightAndEndGrouping()
        if args and "flyData" in args:
            # 购买物品，做出物品飞行动画
            d = args["flyData"]
            toSlots, fromSlot = d["toSlots"], d["fromSlot"]
            toInst = self.uiInst.tableEyePanel.GetItemPanelData(fromSlot)[0]
            if not toInst: return
            hasData = False
            for index in toSlots:
                fromInst = self.cellInstList[index][0]
                if fromInst:
                    hasData = True
                    self.uiInst.autoExchangePanel.BuildItemFlyData(fromInst, toInst, 0.14, True)
            if hasData:
                self.uiInst.autoExchangePanel.startFlyAnim = True

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PlayInventorySystem)
    def RefreshInventory(self, args):
        self.RefreshInventoryUI()
    
    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
    def RefreshEMCTextUI(self, args):
        """刷新EMC值显示"""
        self.emcText.SetText("EMC: " + str(args["emcValue"]))
