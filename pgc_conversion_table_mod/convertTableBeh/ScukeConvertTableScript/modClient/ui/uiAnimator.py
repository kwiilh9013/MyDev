# -*- coding: utf-8 -*-

class Animator(object):
    def __init__(self, uiInst):
        self.ui = uiInst
        # 原色
        self.colorDefault = {
            "dark1": (18.0, 18.0, 38.0),
            "txt1": (190.0, 200.0, 255.0),
            "txt2": (115.0, 123.0, 171.0),
            "txt3": (27.0, 27.0, 59.0),
            "lightBg": (170.0, 179.0, 227.0),
            "darkBg1": (19.0, 19.0, 45.0),
            "darkBg2": (18.0, 18.0, 38.0),
            "darkBg3": (31.0, 32.0, 46.0),
            "cellColor": (55.0, 58.0, 88.0),
            "autoBg": (7.0, 7.0, 35.0),
            "autoTabDf": (77.0, 81.0, 114.0)
        }
        # 愤怒色
        self.colorAngry = {
            "dark1": (28.0, 4.0, 4.0),
            "txt1": (255.0, 194.0, 143.0),
            "txt2": (255.0, 96.0, 63.0),
            "txt3": (85.0, 1.0, 0.0),
            "lightBg": (254.0, 94.0, 63.0),
            "darkBg1": (48.0, 7.0, 7.0),
            "darkBg2": (28.0, 5.0, 5.0),
            "darkBg3": (46.0, 18.0, 18.0),
            "cellColor": (142.0, 1.0, 0.0),
            "autoBg": (57.0, 0.0, 0.0),
            "autoTabDf": (114.0, 68.0, 68.0)
        }
        self.texPrefix = "textures/ui/scuke_ct/"
        self.texPathDefault = {
            "outline1": self.texPrefix + "ui_grid_01",
            "outline2": self.texPrefix + "ui_grid_02",
            "garbage": self.texPrefix + "icon_garbage",
            "makePrice": self.texPrefix + "icon_tag",
            "btnDark01": self.texPrefix + "button_dark01",
            "btnDark01P": self.texPrefix + "button_dark01_press",
            "btn02": self.texPrefix + "button_02",
            "btn02P": self.texPrefix + "button_02_press",
            "btnHint02": self.texPrefix + "button_hint_02",
            "btnHint02Up": self.texPrefix + "button_hint_02_up",
            "iconUp": self.texPrefix + "icon_up",
            "btn01": self.texPrefix + "button_01",
            "btn01P": self.texPrefix + "button_01_press",
            "setup": self.texPrefix + "icon_setup",
            "pageLeft": self.texPrefix + "button_01_left",
            "pageLeftP": self.texPrefix + "button_01_left_press",
            "pageRight": self.texPrefix + "button_01_right",
            "pageRightP": self.texPrefix + "button_01_right_press",
            "eyeBg": self.texPrefix + "ui_backboard",
            "eyeBg2": self.texPrefix + "ui_board_01",
            "eyeCore": self.texPrefix + "ui_eye_04",
            "eyeBall1": self.texPrefix + "ui_eye_03",
            "eyeBall2": self.texPrefix + "ui_eye_02",
            "timing": self.texPrefix + "icon_clock",
            "record": self.texPrefix + "icon_note"
        }
        self.texPathAngry = {
            "outline1": self.texPrefix + "ui_grid_red",
            "outline2": self.texPrefix + "ui_grid_03",
            "garbage": self.texPrefix + "icon_garbage_red",
            "makePrice": self.texPrefix + "icon_tag_red",
            "btnDark01": self.texPrefix + "button_red_01",
            "btnDark01P": self.texPrefix + "button_red_01_press",
            "btn02": self.texPrefix + "button_03",
            "btn02P": self.texPrefix + "button_03_press",
            "btnHint02": self.texPrefix + "button_hint_03",
            "btnHint02Up": self.texPrefix + "button_hint_03_up",
            "iconUp": self.texPrefix + "icon_up_red",
            "btn01": self.texPrefix + "button_dark02",
            "btn01P": self.texPrefix + "button_dark02_press",
            "setup": self.texPrefix + "icon_setup_red",
            "pageLeft": self.texPrefix + "button_02_left",
            "pageLeftP": self.texPrefix + "button_02_left_press",
            "pageRight": self.texPrefix + "button_02_right",
            "pageRightP": self.texPrefix + "button_02_right_press",
            "eyeBg": self.texPrefix + "ui_backboard_red",
            "eyeBg2": self.texPrefix + "ui_board_red",
            "eyeCore": self.texPrefix + "ui_redeye_04",
            "eyeBall1": self.texPrefix + "ui_redeye_03",
            "eyeBall2": self.texPrefix + "ui_redeye_02",
            "timing": self.texPrefix + "icon_clock_red",
            "record": self.texPrefix + "icon_note_red"
        }

    @staticmethod
    def GetRGBColor(vec3):
        r, g, b = vec3
        return r / 255.0, g / 255.0, b / 255.0

    def SetEyeBallPos(self, pos):
        # 眼球转动动效，pos需要是和clickpos一致的vec2数据
        self.SetEyeBallAnimState(True)
        self.ui.tableEyePanel.EyeAnimation(pos)

    def SetEyeBallAnimState(self, state):
        self.ui.tableEyePanel.eyeBallAnim = state

    # region TODO 单个控件的设置
    @staticmethod
    def SetInvCell(inst, texList, color):
        inst.GetChildByPath("/bg/cell_normal").asImage().SetSprite(texList[0])
        inst.GetChildByPath("/bg/cell_normal/normal_bg").asImage().SetSpriteColor(color)
        inst.GetChildByPath("/bg/cell_highlight").asImage().SetSprite(texList[1])

    def SetSortBtn(self, inst, texPathList, color):
        self.SetButtonImage(inst, texPathList)
        inst.GetChildByPath("/sortImage").asImage().SetSpriteColor(color)
        inst.GetChildByPath("/arrow").asImage().SetSpriteColor(color)

    def SetComBtn(self, inst, texList=None, txtColor=None, iconPath=None, iconColor=None):
        if txtColor:
            txt = inst.GetChildByPath("/label").asLabel()
            txt.SetTextColor(txtColor)
        if texList:
            self.SetButtonImage(inst, texList)
        if iconColor:
            icon = inst.GetChildByPath("/icon").asImage()
            icon.SetSpriteColor(iconColor)
        if iconPath:
            inst.GetChildByPath("/icon").asImage().SetSprite(iconPath)

    def SetEmptyBtn(self, inst, texPathList):
        self.SetButtonImage(inst, texPathList)

    @staticmethod
    def SetButtonImage(inst, texPathList):
        inst.GetChildByPath("/default").asImage().SetSprite(texPathList[0])
        inst.GetChildByPath("/hover").asImage().SetSprite(texPathList[1])
        inst.GetChildByPath("/pressed").asImage().SetSprite(texPathList[1])

    @staticmethod
    def SetCirclePanelCell(inst, state="default"):
        redV = state == "angry"
        inst.GetChildByPath("/bg/cell_normal/red").SetVisible(redV)
        inst.GetChildByPath("/bg/cell_highlight/red").SetVisible(redV)

    def SetPageBtn(self, inst, texList):
        self.SetButtonImage(inst, texList)

    def SetSearchPanel(self, inst):
        pass

    @staticmethod
    def SetSingleImage(inst, texPath=None, color=None):
        if texPath is not None:
            inst.SetSprite(texPath)
        if color is not None:
            inst.SetSpriteColor(color)

    @staticmethod
    def SetSingleTxt(inst, color):
        inst.SetTextColor(color)

    def SetExchangeTabBtn(self, inst, state="default"):
        source = self.colorAngry if state == "angry" else self.colorDefault
        color = self.GetRGBColor(source["txt1"])
        color2 = self.GetRGBColor(source["autoTabDf"])
        inst.GetChildByPath("/txt").asLabel().SetTextColor(color)
        inst.GetChildByPath("/default").asImage().SetSpriteColor(color2)
        inst.GetChildByPath("/selected").asImage().SetSpriteColor(color)

    def SetEditBox(self, inst):
        pass

    def SetTipsPanel(self, inst, state="default"):
        source = self.texPathAngry if state == "angry" else self.texPathDefault
        b1, b2 = source["btnHint02"], source["btnHint02Up"]
        inst.GetChildByPath("/infoBg").asImage().SetSprite(b1)
        inst.GetChildByPath("/triangle").asImage().SetSprite(b2)

    @staticmethod
    def SetFuncBtn(inst, iconPath=None, color=None):
        if color is not None:
            txt = inst.GetChildByPath("/label").asLabel()
            txt.SetTextColor(color)
        if iconPath is not None:
            img = inst.GetChildByPath("/icon").asImage()
            img.SetSprite(iconPath)
    # endregion

    def GetMethod(self, state):
        colorSource = self.colorDefault
        texPathSource = self.texPathDefault
        # 区别于普通状态
        if state == "angry":
            colorSource = self.colorAngry
            texPathSource = self.texPathAngry
        return colorSource, texPathSource

    # region TODO 面板整体的设置
    def SetCorePanelState(self, state):
        rootPanel = self.ui.corePanel.rootPanel
        childGet = rootPanel.GetChildByPath
        colorSource, texPathSource = self.GetMethod(state)
        lightBgColor = self.GetRGBColor(colorSource["lightBg"])
        txt1Color = self.GetRGBColor(colorSource["txt1"])
        txt3Color = self.GetRGBColor(colorSource["txt3"])
        visibleBtn = childGet("/visibleBtn").asButton()
        vsTexPathList = [texPathSource["iconUp"], texPathSource["iconUp"]]
        self.SetEmptyBtn(visibleBtn, vsTexPathList)
        closeBtn = childGet("/closeBtn").asButton()
        self.SetComBtn(closeBtn, iconColor=lightBgColor)
        emcTxt = childGet("/infoStackPanel/emcPanel/emcValue").asLabel()
        self.SetSingleTxt(emcTxt, txt1Color)
        dvdImg = childGet("/infoStackPanel/emcPanel/divide").asImage()
        self.SetSingleImage(dvdImg, color=lightBgColor)
        vtSortBtn = childGet("/infoStackPanel/sortPanel/verticalSortBtn").asButton()
        vtTexList = [texPathSource["btnDark01"], texPathSource["btnDark01P"]]
        self.SetSortBtn(vtSortBtn, vtTexList, color=txt1Color)
        hzSortBtn = childGet("/infoStackPanel/sortPanel/horizontalSortBtn").asButton()
        self.SetSortBtn(hzSortBtn, vtTexList, txt1Color)
        headTxt = childGet("/infoStackPanel/sortPanel/headTxt").asLabel()
        self.SetSingleTxt(headTxt, txt1Color)
        dvd2Img = childGet("/infoStackPanel/inventoryStackPanel/dividePanel/divide").asImage()
        self.SetSingleImage(dvd2Img, color=lightBgColor)
        cellTexList = [texPathSource["outline1"], texPathSource["outline2"]]
        cellCenterColor = self.GetRGBColor(colorSource["cellColor"])
        for i in range(36):
            invCellInst = self.ui.corePanel.cellInstList[i][0]
            self.SetInvCell(invCellInst, cellTexList, cellCenterColor)
        setBtn = childGet("/infoStackPanel/btnGroupPanel/settingBtn").asButton()
        teamBtn = childGet("/infoStackPanel/btnGroupPanel/teamBtn").asButton()
        autoBtn = childGet("/infoStackPanel/btnGroupPanel/autoExchangeBtn").asButton()
        sellBtn = childGet("/infoStackPanel/btnGroupPanel/sellBtn").asButton()
        kTexList1 = [texPathSource["btn01"], texPathSource["btn01P"]]
        kTexList2 = [texPathSource["btn02"], texPathSource["btn02P"]]
        setTexPath = texPathSource["setup"]
        self.SetComBtn(setBtn, kTexList1, iconPath=setTexPath)
        self.SetComBtn(teamBtn, kTexList1, txt1Color)
        self.SetComBtn(autoBtn, kTexList1, txt1Color)
        self.SetComBtn(sellBtn, kTexList2, txt3Color)

    def SetExchangePanelState(self, state="default"):
        rootPanel = self.ui.exchangePanel.rootPanel
        childGet = rootPanel.GetChildByPath
        colorSource, texPathSource = self.GetMethod(state)
        outlineImg = childGet("/bgPanel/outline").asImage()
        olTexPath = texPathSource["outline2"]
        self.SetSingleImage(outlineImg, texPath=olTexPath)
        bgImg = childGet("/bgPanel/bg").asImage()
        bgColor = self.GetRGBColor(colorSource["dark1"])
        self.SetSingleImage(bgImg, color=bgColor)
        titleTxt = childGet("/selectItemPanel/infoPanel/titleTxt").asLabel()
        tlColor = self.GetRGBColor(colorSource["txt1"])
        self.SetSingleTxt(titleTxt, tlColor)
        subTitleTxt = childGet("/selectItemPanel/infoPanel/subTitleTxt").asLabel()
        subColor = self.GetRGBColor(colorSource["txt2"])
        self.SetSingleTxt(subTitleTxt, subColor)
        detailBtn = childGet("/selectItemPanel/infoPanel/titleTxt/detailBtn").asButton()
        self.SetComBtn(detailBtn, txtColor=subColor)
        forgetBtn = childGet("/funcStackPanel/funcBtnPanel/forgetBtn").asButton()
        fgTexPath = texPathSource["garbage"]
        self.SetFuncBtn(forgetBtn, fgTexPath, tlColor)
        mkPriceBtn = childGet("/funcStackPanel/funcBtnPanel/makePriceBtn").asButton()
        mkTexPath = texPathSource["makePrice"]
        self.SetFuncBtn(mkPriceBtn, mkTexPath, tlColor)
        sliderBg = childGet("/countSliderMovePanel/sliderBg").asImage()
        sliderPath = texPathSource["btnDark01"]
        self.SetSingleImage(sliderBg, sliderPath)
        sliderOt = childGet("/countSliderMovePanel/sliderBg/outline").asImage()
        sliderOtPath = texPathSource["outline2"]
        self.SetSingleImage(sliderOt, sliderOtPath)
        # sliderBg2 = childGet("/countSliderMovePanel/sliderBg2").asImage()
        lightBgColor = self.GetRGBColor(colorSource["lightBg"])
        # self.SetSingleImage(sliderBg2, color=lightBgColor)
        ctTxt = childGet("/countSliderMovePanel/countTxt").asLabel()
        self.SetSingleTxt(ctTxt, tlColor)
        # slBg = childGet("/countSliderMovePanel/bg").asImage()
        # self.SetSingleImage(slBg, color=lightBgColor)
        sellBuyBtn = childGet("/funcStackPanel/sellAndBuyPanel/btn").asButton()
        darkTxtColor = self.GetRGBColor(colorSource["dark1"])
        sellBuyTxtList = [texPathSource["btn02"], texPathSource["btn02P"]]
        self.SetComBtn(sellBuyBtn, sellBuyTxtList, darkTxtColor)
        priceInfo = childGet("/funcStackPanel/sellAndBuyPanel/emcPriceInfo")
        self.SetTipsPanel(priceInfo, state)
        closeBtn = childGet("/funcStackPanel/exitPanel/closeBtn").asButton()
        self.SetComBtn(closeBtn, iconColor=lightBgColor)

    def SetEyePanelState(self, state):
        rootPanel = self.ui.tableEyePanel.rootPanel
        childGet = rootPanel.GetChildByPath("/eyePanel").GetChildByPath
        colorSource, texPathSource = self.GetMethod(state)
        lightBgColor = self.GetRGBColor(colorSource["lightBg"])
        darkBg1Color = self.GetRGBColor(colorSource["darkBg1"])
        txt1Color = self.GetRGBColor(colorSource["txt1"])
        lastBtn = childGet("/lastPageBtn").asButton()
        nextBtn = childGet("/nextPageBtn").asButton()
        lastTexList = [texPathSource["pageLeft"], texPathSource["pageLeftP"]]
        nextTexList = [texPathSource["pageRight"], texPathSource["pageRightP"]]
        self.SetPageBtn(lastBtn, lastTexList)
        self.SetPageBtn(nextBtn, nextTexList)
        searchIcon = childGet("/searchPanel/searchIcon").asImage()
        self.SetSingleImage(searchIcon, color=lightBgColor)
        searchTxt = childGet("/searchPanel/searchEditBox/centering_panel/clipper_panel/visibility_panel/place_holder_control").asLabel()
        self.SetSingleTxt(searchTxt, txt1Color)
        clearBtn = childGet("/searchPanel/clearBtn").asButton()
        self.SetComBtn(clearBtn, iconColor=lightBgColor)
        searchBg1 = childGet("/searchPanel/searchBg").asImage()
        self.SetSingleImage(searchBg1, color=darkBg1Color)
        searchBg2 = childGet('/searchPanel/searchBg/bg').asImage()
        self.SetSingleImage(searchBg2, color=lightBgColor)
        pageTxt = childGet("/pageTxt").asLabel()
        self.SetSingleTxt(pageTxt, txt1Color)
        eyeBg = childGet("/bg/eyeBg").asImage()
        eyeBg2 = childGet("/bg/eyeBg2").asImage()
        self.SetSingleImage(eyeBg, texPathSource["eyeBg"])
        self.SetSingleImage(eyeBg2, texPathSource["eyeBg2"])
        eyeCoreOut = childGet("/bg/eyeCore").asImage()
        self.SetSingleImage(eyeCoreOut, texPathSource["eyeCore"])
        eyeBall1 = childGet("/bg/eyeCore/eyeBall1").asImage()
        self.SetSingleImage(eyeBall1, texPathSource["eyeBall1"])
        eyeBall2 = childGet("/bg/eyeCore/eyeBall1/eyeBall2/eyeBallRed").SetVisible(state == "angry")
        for i in range(12):
            inst = self.ui.tableEyePanel.GetItemPanelData(i)[0]
            self.SetCirclePanelCell(inst, state)

    def SetAutoPanelState(self, state):
        rootPanel = self.ui.autoExchangePanel.rootPanel
        childGet = rootPanel.GetChildByPath
        colorSource, texPathSource = self.GetMethod(state)
        bgColor = self.GetRGBColor(colorSource["autoBg"])
        lightBgColor = self.GetRGBColor(colorSource["lightBg"])
        txt1Color = self.GetRGBColor(colorSource["txt1"])
        txt3Color = self.GetRGBColor(colorSource["txt3"])
        bgImg = childGet("/bg").asImage()
        bgLeft = childGet("/bg/leftGradient").asImage()
        bgRight = childGet("/bg/rightGradient").asImage()
        for inst in [bgImg, bgLeft, bgRight]:
            self.SetSingleImage(inst, color=bgColor)
        closeBtn = childGet("/closeBtn").asButton()
        self.SetComBtn(closeBtn, iconColor=lightBgColor)
        sellBtn = childGet("/exchangeStackPanel/btnStackPanel/sellBtn").asButton()
        buyBtn = childGet("/exchangeStackPanel/btnStackPanel/buyBtn").asButton()
        self.SetExchangeTabBtn(sellBtn, state)
        self.SetExchangeTabBtn(buyBtn, state)
        countTxt = childGet("/exchangeStackPanel/countSetPanel/countTxt").asLabel()
        self.SetSingleTxt(countTxt, txt1Color)
        editBox = childGet("/exchangeStackPanel/countSetPanel/countEditBox").asTextEditBox()
        editTexList = [texPathSource["outline2"], texPathSource["outline2"]]
        self.SetButtonImage(editBox, editTexList)
        searchTxt = childGet("/exchangeStackPanel/countSetPanel/countEditBox/centering_panel/clipper_panel/visibility_panel/place_holder_control").asLabel()
        self.SetSingleTxt(searchTxt, txt1Color)
        cellTexList = [texPathSource["outline1"], texPathSource["outline2"]]
        cellCenterColor = self.GetRGBColor(colorSource["cellColor"])
        for i in range(60):
            r, c = i // 6, i % 6
            itemInst = self.ui.autoExchangePanel.GetItemInst(r, c)
            self.SetInvCell(itemInst, cellTexList, cellCenterColor)
        timingBtn = childGet("/exchangeStackPanel/funcBtnPanel/timingBtn").asButton()
        recordBtn = childGet("/exchangeStackPanel/funcBtnPanel/recordBtn").asButton()
        exeBtn = childGet("/exchangeStackPanel/funcBtnPanel/exeBtn").asButton()
        timingIconPath = texPathSource["timing"]
        recordIconPath = texPathSource["record"]
        kTexList1 = [texPathSource["btn01"], texPathSource["btn01P"]]
        kTexList2 = [texPathSource["btn02"], texPathSource["btn02P"]]
        self.SetComBtn(timingBtn, kTexList1, iconPath=timingIconPath)
        self.SetComBtn(recordBtn, kTexList1, iconPath=recordIconPath)
        self.SetComBtn(exeBtn, kTexList2, txtColor=txt3Color)
        infoPanel = childGet("/exchangeStackPanel/funcBtnPanel/timingInfoPanel")
        self.SetTipsPanel(infoPanel, state)

    def SetBaseBackgroundState(self, state):
        rootPanel = self.ui.rootPanel
        childGet = rootPanel.GetChildByPath
        colorSource, texPathSource = self.GetMethod(state)
        dark2BgColor = self.GetRGBColor(colorSource["darkBg2"])
        dark3BgColor = self.GetRGBColor(colorSource["darkBg3"])
        bg2Img = childGet("/bg2").asImage()
        self.SetSingleImage(bg2Img, texPathSource["btn01"])
        mainScrBg = childGet("/mainScreenPanel/mainScreenBg").asImage()
        self.SetSingleImage(mainScrBg, color=dark2BgColor)
        maskBg = childGet("/mainScreenPanel/mainScreenBg/maskBg").asImage()
        self.SetSingleImage(maskBg, color=dark3BgColor)
        infoPanel = childGet("/tipInfoPanel")
        self.SetTipsPanel(infoPanel, state)

    def SetAllState(self, state):
        # str: default, angry
        self.SetCorePanelState(state)
        self.SetExchangePanelState(state)
        self.SetEyePanelState(state)
        self.SetBaseBackgroundState(state)
        self.SetAutoPanelState(state)
    # endregion
