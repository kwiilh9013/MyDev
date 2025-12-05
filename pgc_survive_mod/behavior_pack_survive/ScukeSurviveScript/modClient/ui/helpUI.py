# -*- coding: utf-8 -*-
import random
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.ScukeCore.client.engineApiGac import *
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.helpConfig import *
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()

ContentPathPrefix = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content/"
Tab1Path = '/mainPanel/tab1ScrollView' + ContentPathPrefix
Tab2Path = '/mainPanel/tab2ScrollView' + ContentPathPrefix
Tab2DefaultCtl = ("mLeftTxt", "mMiddleTxt", "mRightTxt", "mPict", "mPictSmall")


class HelpUI(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(HelpUI, self).__init__(namespace, name, param)
        self._openType = "help" if not param else "gameIntro"
        self._quitBtn = None
        self._selectIndex = 0
        self._BgToggleShow = False
        self._touchPos = (0, 0)
        self._tab1TitleBtnDict = {}
        self._tab1ContentBtnDict = {}
        self._tab2PanelDict = {}
        self._tab2View = None

    def Create(self):
        super(HelpUI, self).Create()
        self.CreateBtn()
        self.OnActive()

    def SetCtlVisible(self, path, vis=True):
        self.GetBaseUIControl(path).SetVisible(vis)

    def RegisterBtn(self, dictPath, dictKey, keyPath, keyType):
        dictPath.update({dictKey: self.GetBaseUIControl(keyPath).asButton()})
        dictPath[dictKey].AddTouchEventParams({"isSwallow": True, 'type': keyType})
        dictPath[dictKey].SetButtonTouchUpCallback(self.OnBtnPress)
        dictPath[dictKey].SetButtonTouchDownCallback(self.OnBtnPressDown)
        dictPath[dictKey].SetVisible(True)

    def CreateBtn(self):
        self._quitBtn = self.GetBaseUIControl("/mainPanel/exitBtn").asButton()
        self._quitBtn.AddTouchEventParams({"isSwallow": True, 'type': "quit"})
        self._quitBtn.SetButtonTouchUpCallback(self.OnBtnPress)
        pathList = [Tab1Path + "mCloneTitleBtn", Tab1Path + "mCloneContentBtn", Tab2Path + "mClonePanel"]
        self._tab2View = self.GetBaseUIControl('/mainPanel/tab2ScrollView').asScrollView()
        for s in pathList:
            self.SetCtlVisible(s, False)
        dataSource = AllInfoConfig if self._openType == "help" else GameIntroConfig
        self.GetBaseUIControl("/mainPanel/exitBtn/txtImage").asImage().SetVisible(self._openType == "help")
        self.GetBaseUIControl("/mainPanel/exitBtn/txtImage2").asImage().SetVisible(self._openType != "help")
        for i, k in enumerate(dataSource):
            key = k['module']
            self.Clone(Tab1Path + "mCloneTitleBtn", Tab1Path[:-1], key + "TitleBtn", False, False)
            self.RegisterBtn(self._tab1TitleBtnDict, key, Tab1Path + key + "TitleBtn", "title_" + key)
            self.GetBaseUIControl(Tab1Path + key + "TitleBtn/txt").asLabel().SetText(k['moduleName'])
            for a, b in enumerate(k['content']):
                self.Clone(Tab1Path + "mCloneContentBtn", Tab1Path[:-1], key + "%s_ContentBtn" % a, False, False)
                btnKey = key + str(a)
                self.RegisterBtn(self._tab1ContentBtnDict, btnKey, Tab1Path + key + "%s_ContentBtn" % a, "content_" + btnKey)
                self.GetBaseUIControl(Tab1Path + key + "%s_ContentBtn/txt" % a).asLabel().SetText(b['title'])
                self.SetCtlVisible(Tab1Path + key + "%s_ContentBtn/selected" % a, a == 0 and i == 0)
                # 克隆tab2
                self.Clone(Tab2Path + "mClonePanel", Tab2Path[:-1], btnKey + "Panel", False, False)
                tab2PanelPath = Tab2Path + btnKey + "Panel"
                self._tab2PanelDict.update({btnKey: self.GetBaseUIControl(tab2PanelPath).asStackPanel()})
                self._tab2PanelDict[btnKey].SetVisible(True)
                defaultTxtList = [("titleTxt", "title", 1.3), ("emailTxt", "emailMan", 1.1)]
                for g in defaultTxtList:
                    if b[g[1]] and self._openType == "help":
                        self.Clone(tab2PanelPath + "/mLeftTxt", tab2PanelPath, g[0], False, False)
                        titleTxt = self.GetBaseUIControl(tab2PanelPath + "/%s/txt" % g[0]).asLabel()
                        titleTxt.SetText(b[g[1]] + "\n ")
                        titleTxt.SetTextFontSize(g[2])
                cloneMap = {"<leftTxt>": "mLeftTxt", "<middleTxt>": "mMiddleTxt", "<rightTxt>": "mRightTxt"}
                for c, p in enumerate(b['richText']):
                    if not p.startswith("<"):continue
                    if p.startswith("<image>"):
                        self.Clone(tab2PanelPath + "/mPict", tab2PanelPath, "cloneImage%s" % c, False, False)
                        image = self.GetBaseUIControl(tab2PanelPath + "/cloneImage%s/mPicture" % c).asImage()
                        image.SetSprite("textures/ui/scuke_survive/help/" + p.split(">")[1])
                    elif p.startswith("<imageSmall>"):
                        self.Clone(tab2PanelPath + "/mPictSmall", tab2PanelPath, "cloneImageSmall%s" % c, False, False)
                        image = self.GetBaseUIControl(tab2PanelPath + "/cloneImageSmall%s/mPicture" % c).asImage()
                        image.SetSprite("textures/ui/scuke_survive/help/" + p.split(">")[1])
                    elif p.startswith("<imageSquare>"):
                        self.Clone(tab2PanelPath + "/mPictSquare", tab2PanelPath, "cloneImageSquare%s" % c, False, False)
                        image = self.GetBaseUIControl(tab2PanelPath + "/cloneImageSquare%s/mPicture" % c).asImage()
                        image.SetSprite("textures/ui/scuke_survive/help/" + p.split(">")[1])
                    else:
                        cloneType = cloneMap.get(p.split(">")[0] + ">", "mLeftTxt")
                        showTxt = p.split(">")[1]
                        self.Clone(tab2PanelPath + "/" + cloneType, tab2PanelPath, "cloneTxt%s" % c, False, False)
                        self.GetBaseUIControl(tab2PanelPath + "/cloneTxt%s/txt" % c).asLabel().SetText(showTxt)
                shouldHideList = ["/mLeftTxt", "/mMiddleTxt", "/mRightTxt", "/mPict", "/mPictSmall", "/mPictSquare"]
                for v in shouldHideList:
                    self.SetCtlVisible(tab2PanelPath + v, False)
                self.SetCtlVisible(tab2PanelPath, a == 0 and i == 0)
        self.UpdateScreen(True)

    def OnBtnPress(self, args):
        Type = args['AddTouchEventParams']['type']
        if Type == "quit":
            clientApi.PopScreen()
        if args['TouchPosX'] - self._touchPos[0] > 3 or args['TouchPosY'] - self._touchPos[1] > 3:
            return
        if Type.startswith("title_"):
            child = Type.split("title_")[1]
            for key, value in self._tab1ContentBtnDict.items():
                if child in key:
                    self._tab1ContentBtnDict[key].SetVisible(not self._tab1ContentBtnDict[key].GetVisible())
        if Type.startswith("content_"):
            instance = Type.split("content_")[1]
            for key, value in self._tab1ContentBtnDict.items():
                selectImage = self._tab1ContentBtnDict[key].GetChildByPath("/selected")
                selectImage.SetVisible(False)
            for key2, value2 in self._tab2PanelDict.items():
                self._tab2PanelDict[key2].SetVisible(False)
            self._tab1ContentBtnDict[instance].GetChildByPath("/selected").SetVisible(True)
            self._tab2PanelDict[instance].SetVisible(True)
            self._tab2View.SetScrollViewPercentValue(0)

    def OnBtnPressDown(self, args):
        self._touchPos = (args['TouchPosX'], args['TouchPosY'])

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged, "#HelpUI.BgToggleChange")
    def BgToggleChange(self, args):
        self._BgToggleShow = args["state"]
        self.GetBaseUIControl("/mainPanel/bg").asImage().SetAlpha(0.5 if self._BgToggleShow else 1.0)
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindBool, "#HelpUI.BgToggleState")
    def BgToggleState(self):
        return self._BgToggleShow

