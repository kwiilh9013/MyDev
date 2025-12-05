# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon.cfg.illustration import illustrateMergeCfg
from ScukeSurviveScript.ScukeCore.client.engineApiGac import *
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.modCommon import modConfig

ViewBinder = clientApi.GetViewBinderCls()
CreatingItem = compFactory.CreateItem
CreatedGame = compFactory.CreateGame(levelId)
MyPid = GetLocalPlayerId()
GridScrollPath = "bg/scroll_view/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"
ContentPathPrefix = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content/"
ContentPathPrefix2 = "/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content/"
ScrollViewPath = "scroll_view/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"
CardTypeMap = {
    "green": 0,
    "blue": 1,
    "yellow": 2,
    "purple": 3,
    "red": 4,
    "gold": 5
}


class IllustrateUI(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(IllustrateUI, self).__init__(namespace, name, param)
        self._mTick = 0  # tick
        self._selectType = 'mob'  # 图鉴类型
        # 按钮映射数据配置表键值
        self._btnDict = {'mobBtn': "mob", 'rebelBtn': "rebel", 'weaponBtn': "weapon", 'equipBtn': "equipment", 'itemBtn': "item",
                         'blockBtn': "block", 'eventBtn': "event", 'buildingBtn': "building", 'vehicleBtn': "vehicle"}
        self._closeBtn = None  # 关闭按钮实例
        self._contentList = []      # 内容列表
        self._contentGrid = None  # 内容网格
        self._showNum = 1  # 可显示的内容数量
        self._hasCallbackContent = {}  # 已注册回调的内容
        self._contentObjTouchPos = (0, 0)  # 内容按钮点击位置
        self._contentCardPanel = None
        self._scheduleSum = 0
        self._scheduleNum = 0
        self._gridScrollView = None
        self._gridContentPath = ""
        self._client = None

    def Create(self):
        super(IllustrateUI, self).Create()
        for i in illustrateMergeCfg.__illustrationCfgDict__.values():
            self._scheduleSum += len(i)
        # NowText.SetText('{}'.format(self._scheduleSum))
        self.CreateBtn()
        self.CreateContentCardCallBack()
        self._gridScrollView = self.GetBaseUIControl("bg/scroll_view").asScrollView()
        self._gridContentPath = self._gridScrollView.GetScrollViewContentPath()
        grid = self.GetBaseUIControl(self._gridContentPath).asGrid()
        if grid is None:
            grid = self.GetBaseUIControl(GridScrollPath).asGrid()
        grid.SetGridDimension((0, 0))
        grid.SetVisible(False)
        self.GetBaseUIControl('/showContentCard').SetVisible(False)
        AddTimer(0.03, self.CreateContentGrid, 'mob')
        self._client = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.IllustrateClientSystem)
        NowText = self.GetBaseUIControl('/bg/processTxt').asLabel()
        self._scheduleNum = len(self._client.hasUnlockList)
        self._scheduleSum = len(self._client._memoryList)
        NowText.SetText('总进度 {}/{}'.format(self._scheduleNum, self._scheduleSum))
        NowText.SetVisible(True)

    # 注册按钮回调
    def CreateBtn(self):
        self._closeBtn = self.GetBaseUIControl('/bg/closeBtn').asButton()
        self._closeBtn.AddTouchEventParams({"isSwallow": True, 'type': '_closeBtn'})
        self._closeBtn.SetButtonTouchUpCallback(self.OnBtnPress)
        for i in self._btnDict.keys():
            self.GetBaseUIControl('/bg/divide/stackPanel/{}'.format(i)).asButton().AddTouchEventParams({"isSwallow": True, 'type': i})
            self.GetBaseUIControl('/bg/divide/stackPanel/{}'.format(i)).asButton().SetButtonTouchUpCallback(self.OnBtnPress)
        self.SetOneBtnHighlight('mobBtn')

    # 创建内容网格
    def CreateContentGrid(self, contentType):
        self._gridContentPath = self._gridScrollView.GetScrollViewContentPath()
        self.GetBaseUIControl(self._gridContentPath).SetVisible(True)
        self._contentGrid = self.GetBaseUIControl(self._gridContentPath).asGrid()
        self._contentList = illustrateMergeCfg.GetData(contentType)
        if all(i == {} for i in self._contentList):
            self._contentList = []
        self._showNum = len(self._contentList)
        GridRow = self._showNum // 5 + 1
        GridColumn = self._showNum if self._showNum < 6 else 5
        self._contentGrid.SetGridDimension((5, GridRow))
        AddTimer(0.03, self.CreateContentObj)
        self.GetBaseUIControl('/showContentCard/inputPanel').asInputPanel().SetIsModal(False)

    # 创建网格中的内容
    def CreateContentObj(self, shouldUpdate=False):
        if self._gridScrollView is None: return
        self._gridContentPath = self._gridScrollView.GetScrollViewContentPath()
        if not self._gridContentPath:return
        ChildPaths = self.GetAllChildrenPath(self._gridContentPath)
        for i in range(1, self._showNum + 1):
            Content = 'contentObj%s' % i
            if (ContentPathPrefix + Content) in ChildPaths or (ContentPathPrefix2 + Content) in ChildPaths:
                Path = self._gridContentPath + "/" + Content
                Index = Path.split(self._gridContentPath + '/contentObj')[1]
                try:
                    Index = int(Index) - 1
                except ValueError:
                    continue
                if Index > len(self._contentList) - 1: continue
                Data = self._contentList[Index]
                if not Data:
                    self.GetBaseUIControl(Path + '/objPaperDoll').SetVisible(False)
                    self.GetBaseUIControl(Path + '/objImage').SetVisible(False)
                    self.GetBaseUIControl(Path + '/objItemRender').SetVisible(False)
                    self.GetBaseUIControl(Path + '/unlockTxt').SetVisible(False)
                    continue
                if Content not in self._hasCallbackContent:
                    self._hasCallbackContent[Content] = self.GetBaseUIControl(self._gridContentPath + "/" + Content + "/Btn").asButton()
                    self._hasCallbackContent[Content].AddTouchEventParams({"isSwallow": True, 'type': 100 + i})
                    self._hasCallbackContent[Content].SetButtonTouchUpCallback(self.OnBtnPress)
                    self._hasCallbackContent[Content].SetButtonTouchDownCallback(self.OnContentObjClick)
                    self.SetOneContent(Data, Path)
                if shouldUpdate:
                    self.SetOneContent(Data, Path)

    # 设置网格中某个内容组中的内容
    def SetOneContent(self, data, path):
        showType = data['showType']
        showTypeMap = {'paperDoll': 'objPaperDoll', 'image': 'objImage', 'itemRender': 'objItemRender'}
        for p in showTypeMap.values():
            self.GetBaseUIControl(path + '/%s' % p).SetVisible(False)
        self.GetBaseUIControl(path + '/objPaperDoll').asNeteasePaperDoll().SetVisible(showType == 'paperDoll')
        targetPath = path + '/%s' % showTypeMap[showType]
        self.GetBaseUIControl(targetPath).SetVisible(True)
        if 'cardType' not in data:
            commonData = illustrateMergeCfg.CardTypeList[0]
        else:
            commonData = illustrateMergeCfg.CardTypeList[CardTypeMap.get(data['cardType'], 0)]
        rPosX, rPosY = commonData['showPosition'][0], commonData['showPosition'][1]
        sizeX, sizeY = commonData['showSize'][0], commonData['showSize'][1]
        CN_Name = data['chineseName'] if data['chineseName'] else CreatingItem(levelId).GetItemHoverName(data['id'], 0)
        if not CN_Name:
            CN_Name = CreatedGame.GetChinese('entity.{}.name'.format(data['id']))
        unlockTxt = self.GetBaseUIControl(path + '/unlockTxt').asLabel()
        unlockTxt.SetText(CN_Name)
        unlockTxt.SetTextColor(commonData['nameColor'])
        unlockTxt.SetAlpha(commonData['nameAlpha'])
        unlockTxt.SetVisible(True)
        lockCover = self.GetBaseUIControl(path + '/lockCover').asImage()
        lockCover.SetVisible(data['id'] not in self._client.hasUnlockList)
        lockTxt = self.GetBaseUIControl(path + '/lockCover/lockTxt').asLabel()
        lockTxt.SetText(CN_Name)
        lockTxt.SetTextColor(commonData['lockNameColor'])
        lockTxt.SetAlpha(commonData['nameAlpha'])
        lockTxt.SetVisible(True)
        selectImage = self.GetBaseUIControl(path + '/selectImage').asImage().SetVisible(False)
        if showType == 'paperDoll':
            Doll = self.GetBaseUIControl(targetPath).asNeteasePaperDoll()
            Doll.SetVisible(True)
            Doll.RenderEntity(data['paperDollData'])
        elif showType == 'image':
            Image = self.GetBaseUIControl(targetPath).asImage()
            Image.SetSprite(data['imageData']['path'])
            Image.SetSpriteColor(commonData['imageDataColor'])
            Image.SetAlpha(commonData['imageDataAlpha'])
        elif showType == 'itemRender':
            itemRender = self.GetBaseUIControl(targetPath).asItemRenderer()
            renderData = data['itemRenderData']
            itemName, aux, ench = renderData['itemName'], renderData['auxValue'], renderData['enchant']
            userData, alpha = renderData['userData'], renderData['alpha']
            itemRender.SetUiItem(itemName, aux, ench, userData)
            itemRender.SetAlpha(alpha)

    # 绑定显示
    @ViewBinder.binding_collection(ViewBinder.BF_BindBool, "contentGrid", "#CtObj.visible")
    def ContentGridItemVisible(self, index):
        return index < self._showNum and self._contentGrid.GetVisible()

    def OnBtnPress(self, args):
        Type = args['AddTouchEventParams']['type']
        if Type == '_closeBtn':
            Instance.mUIManager.PopUI()
        elif Type in self._btnDict:
            self._selectType = self._btnDict[Type]
            self.SetOneBtnHighlight(Type)
            self._hasCallbackContent.clear()
            self.CreateContentGrid(self._selectType)
            self._gridScrollView.SetScrollViewPercentValue(0)
        # 内容按钮松开触发
        elif type(Type) == int and Type > 100:
            # 判定是否在滑动，如果在滑动，就不执行回调
            if abs(args['TouchPosY'] - self._contentObjTouchPos[1]) > 1:
                return
            Path = args['ButtonPath']
            self._gridContentPath = self._gridScrollView.GetScrollViewContentPath()
            Index = Path.split(self._gridContentPath + '/contentObj')[1].split('/')[0]
            try:
                Index = int(Index)-1
            except ValueError:
                pass
            if Index > len(self._contentList) - 1: return
            Data = self._contentList[Index]
            Path2 = Path.split('/Btn')[0]
            if not Data:
                self.GetBaseUIControl(Path2 + '/objPaperDoll').SetVisible(False)
                self.GetBaseUIControl(Path2 + '/objImage').SetVisible(False)
                self.GetBaseUIControl(Path2 + '/objItemRender').SetVisible(False)
                self.GetBaseUIControl(Path2 + '/unlockTxt').SetVisible(False)
                return
            self.SetContentCard(Data)

    # 获取内容按钮按下位置
    def OnContentObjClick(self, args):
        self._contentObjTouchPos = (args['TouchPosX'], args['TouchPosY'])

    def SetContentCard(self, data):
        if data['id'] not in self._client.hasUnlockList:
            pass
            return
        _path = '/showContentCard'
        _illusPath = 'textures/ui/scuke_survive/illustration/'
        self._gridContentPath = self._gridScrollView.GetScrollViewContentPath()
        self.GetBaseUIControl(self._gridContentPath).SetTouchEnable(False)
        self._contentCardPanel.SetVisible(True)
        self.GetBaseUIControl('/showContentCard/inputPanel').asInputPanel().SetIsModal(True)
        if 'cardType' not in data:
            commonData = illustrateMergeCfg.CardTypeList[0]
        else:
            commonData = illustrateMergeCfg.CardTypeList[CardTypeMap.get(data['cardType'], 0)]
        cardData = data['detailCardData']
        N1, N2, N3, N4 = cardData['baseData'][0:4]
        VisibleBool = all((N1, N2, N3, N4))
        CN_Name = data['chineseName'] if data['chineseName'] else CreatingItem(levelId).GetItemHoverName(data['id'], 0)
        if not CN_Name:
            CN_Name = CreatedGame.GetChinese('entity.{}.name'.format(data['id']))
        Image = self.GetBaseUIControl(_path + '/imageBg/image').asImage()
        Image.SetSprite(_illusPath + cardData['imagePath'])
        ImageBg = self.GetBaseUIControl(_path + '/imageBg').asImage()
        ImageBg.SetSpriteColor(commonData['cardImageBg2Color'])
        ImageBg0 = self.GetBaseUIControl(_path).asImage()
        ImageBg0.SetSpriteColor(commonData['cardImageBg0Color'])
        ImageBg1 = self.GetBaseUIControl(_path + '/bg').asImage()
        ImageBg1.SetSprite(_illusPath + commonData['cardImageBg1Path'])
        ImageBg2 = self.GetBaseUIControl(_path + '/imageBg/bg').asImage()
        ImageBg2.SetSpriteColor(commonData['cardImageBg2Color'])
        NameTxt = self.GetBaseUIControl(_path + '/imageBg/nameBg/nameTxt').asLabel()
        NameTxt.SetText(CN_Name)
        NameTxt.SetTextColor(commonData['cardImageTextAndIconColor'])
        NameImg1 = self.GetBaseUIControl(_path + '/imageBg/nameBg').asImage()
        NameImg1.SetSpriteColor(commonData['cardImageBg2Color'])
        NameImg2 = self.GetBaseUIControl(_path + '/imageBg/nameBg/bg').asImage()
        NameImg2.SetSpriteColor(commonData['cardImageBg2Color'])
        HealthTxt = self.GetBaseUIControl(_path + '/imageBg/healthTxt').asLabel()
        HealthTxt.SetText("HP " + cardData['baseData'][3])
        HealthTxt.SetVisible(VisibleBool)
        Len = len(self._contentList)
        Index = self._contentList.index(data) + 1
        Len = str(Len) if Len > 10 else "0" + str(Len)
        Index = str(Index) if Index > 10 else "0" + str(Index)
        RareCount = cardData['baseData'][4]
        if type(RareCount) != int:RareCount = 1
        NumberTxt = self.GetBaseUIControl(_path + '/imageBg/numberTxt').asLabel()
        NumberTxt.SetText('No.{} {} HT:{} WT:{}'.format(Index + Len, N1, N2, N3))
        NumberTxt.SetTextColor(commonData['cardImageTextAndIconColor'])
        NumTxt = self.GetBaseUIControl(_path + '/numberBg/numberTxt').asLabel()
        NumTxt.SetText(Index + "/" + Len)
        for ra1 in range(1, 6):
            self.GetBaseUIControl(_path + '/rarePanel/star%s' % ra1).asImage().SetAlpha(0.3)
        for ra2 in range(1, RareCount + 1):
            self.GetBaseUIControl(_path + '/rarePanel/star%s' % ra2).asImage().SetAlpha(1.0)
        contentBg = self.GetBaseUIControl(_path + '/inputPanel/contentBg').asImage()
        contentBg.SetSpriteColor(commonData['cardContentBgColor'])
        contentBg.SetAlpha(commonData['cardContentBgAlpha'])
        for ct in range(1, 6):
            self.GetBaseUIControl(_path + '/inputPanel/contentBg/' + ScrollViewPath + '/content%s' % ct).SetVisible(False)
        CtData = cardData['content']
        if not VisibleBool:
            NumberTxt.SetText('No.%s' % (Index + Len))
        for index, ct2 in enumerate(CtData):
            _thisPath = _path + '/inputPanel/contentBg/' + ScrollViewPath + '/content%s' % (index+1)
            self.GetBaseUIControl(_thisPath).SetVisible(True)
            MainTxt = self.GetBaseUIControl(_thisPath + '/context').asLabel()
            MainTxt.SetText(("\n" if not VisibleBool else "") + (ct2['mainText']) if ct2['mainText'] else "\n" + CN_Name)
            MainTxt.SetTextColor(commonData['cardContentTextColor'])
            HeadTxt = self.GetBaseUIControl(_thisPath + '/headTxt').asLabel()
            HeadTxt.SetText(ct2['headText'])
            HeadTxt.SetTextColor(commonData['cardContentTextColor'])
            HeadTxt.SetVisible(VisibleBool)
            DamTxt = self.GetBaseUIControl(_thisPath + '/damageTxt').asLabel()
            DamTxt.SetText(ct2['damageText'])
            DamTxt.SetTextColor(commonData['cardContentTextColor'])
            DamTxt.SetVisible(VisibleBool)
            Icon1 = self.GetBaseUIControl(_thisPath + '/icon1').asImage()
            Icon1.SetSpriteColor(commonData['cardImageBg2Color'])
            Icon1.SetVisible(VisibleBool)
            Icon = self.GetBaseUIControl(_thisPath + '/icon1/icon').asImage()
            Icon.SetSprite(_illusPath + ct2['iconPath'])
            Icon.SetSpriteColor(commonData['cardImageTextAndIconColor'])

    def CreateContentCardCallBack(self):
        self._contentCardPanel = self.GetBaseUIControl('/showContentCard').asImage()
        btnList = [('closeBtn', '/inputPanel/closeBtn'), ('bgBtn', '/bgBtn')]
        for btn in btnList:
            BtnN = self.GetBaseUIControl('/showContentCard' + btn[1]).asButton()
            BtnN.AddTouchEventParams({"isSwallow": True, 'type': btn[0]})
            BtnN.SetButtonTouchUpCallback(self.ContentCardBtnPress)

    def ContentCardBtnPress(self, args):
        Type = args['AddTouchEventParams']['type']
        if Type == 'closeBtn':
            self._gridContentPath = self._gridScrollView.GetScrollViewContentPath()
            self.GetBaseUIControl(self._gridContentPath).SetTouchEnable(True)
            self.GetBaseUIControl('/showContentCard/inputPanel').asInputPanel().SetIsModal(False)
            self._contentCardPanel.SetVisible(False)
        elif Type == 'bgBtn':
            pass

    # 设置tab栏显示
    def SetOneBtnHighlight(self, btnName):
        for btn in self._btnDict.keys():
            self.GetBaseUIControl('/bg/divide/stackPanel/{}/default'.format(btn)).asImage().SetAlpha(0.0)
            self.GetBaseUIControl('/bg/divide/stackPanel/{}/default'.format(btn)).asImage().SetVisible(False)
            self.GetBaseUIControl('/bg/divide/stackPanel/{}/txt'.format(btn)).asLabel().SetTextColor((203.0 / 255.0, 203.0 / 255.0, 203.0 / 255.0))
            self.GetBaseUIControl('/bg/divide/stackPanel/{}/div'.format(btn)).asImage().SetVisible(False)
        self.GetBaseUIControl('/bg/divide/stackPanel/{}/default'.format(btnName)).asImage().SetAlpha(1.0)
        self.GetBaseUIControl('/bg/divide/stackPanel/{}/default'.format(btnName)).asImage().SetSprite('textures/ui/scuke_survive/common/btn03')
        self.GetBaseUIControl('/bg/divide/stackPanel/{}/default'.format(btnName)).asImage().SetVisible(True)
        self.GetBaseUIControl('/bg/divide/stackPanel/{}/txt'.format(btnName)).asLabel().SetTextColor((178.0 / 255.0, 255.0 / 255.0, 232.0 / 255.0))
        self.GetBaseUIControl('/bg/divide/stackPanel/{}/div'.format(btnName)).asImage().SetVisible(True)

    def Update(self):
        self._mTick += 1
        if self._mTick % 2 == 0:
            self.CreateContentObj(True)
