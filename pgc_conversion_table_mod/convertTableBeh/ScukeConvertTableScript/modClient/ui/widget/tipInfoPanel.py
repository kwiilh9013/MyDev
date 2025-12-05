# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.widget.uiBaseWidget import *


class TipInfoPanel(UiBaseWidget):
    def __init__(self, uiInst, sysInst, path, param):
        UiBaseWidget.__init__(self, uiInst, sysInst, path)
        self.rootPanel = self.GetBaseUiControl("")
        self.scroll = None
        self.scrollContentPath = ""
        self.text = None
        self.timer = None
        self.Create()

    def Create(self):
        self.rootPanel.SetVisible(False)
        self.scroll = self.rootPanel.GetChildByPath("/infoBg/scrollView").asScrollView()
        self.scrollContentPath = self.scroll.GetScrollViewContentPath()
        self.text = self.uiInst.GetBaseUIControl(self.scrollContentPath).asLabel()

    def Update(self):
        pass

    def SetTipsShow(self, referPanelInst, txt, itemDict=None, t=3.0, atTop=False):
        # 设置位置到参照控件实例附近，并做出安全区判定
        self.rootPanel.SetVisible(True)
        self.text.SetText(txt)
        lt = len(txt)
        if lt > 80: t = min(math.sqrt(lt / 2.0), 10)
        sx, sy = self.text.GetSize()
        safeSize = (min(max(sx + 3, 25), 100), min(max(sy + 3, 12), 120))
        self.scroll.SetSize(safeSize, True)
        self.scroll.SetScrollViewPercentValue(0)
        globalPos1 = referPanelInst.GetGlobalPosition()
        rpSizeX, rpSizeY = referPanelInst.GetSize()
        pos1 = MathUtils.TupleAdd(globalPos1, (rpSizeX / 2.0, -rpSizeY / 2.0))
        globalPos2 = self.rootPanel.GetGlobalPosition()
        rtSizeX, rtSizeY = self.rootPanel.GetSize()
        pos2 = MathUtils.TupleAdd(globalPos2, (rtSizeX / 2.0, rtSizeY / (1.0 if atTop else 2.0)))
        deltaPos = MathUtils.TupleSub(pos1, pos2)
        oriRelatePos = self.rootPanel.GetPosition()
        newRelatePos = MathUtils.TupleAdd(oriRelatePos, deltaPos)
        # 设置安全位置
        basePanel = self.uiInst.GetBaseUIControl("/tablePanel")
        basePosX, basePosY = basePanel.GetPosition()
        bSizeX, bSizeY = basePanel.GetSize()
        safeX = max(min(newRelatePos[0], bSizeX - rtSizeX + basePosX), 1 + basePosX)
        safeY = max(min(newRelatePos[1], bSizeY - rtSizeY + basePosY), 1 + basePosY)
        self.rootPanel.SetPosition((safeX, safeY))
        engineApiGac.CancelTimer(self.timer)
        self.timer = engineApiGac.AddTimer(t, self.EndTipsShow)
        self.uiInst.UpdateScreen(True)

    def EndTipsShow(self):
        self.rootPanel.SetVisible(False)
        pass
