# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.modClient.ui.uiDef import UIDef
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance

compFactory = clientApi.GetEngineCompFactory()

TeamPanel = "/teamManagerPanel/teamPanel"
ContentPathPrefix = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"
ContentPath = TeamPanel+'/mbGroupScrollView'+ContentPathPrefix
ModulePath = ContentPath+"/mCloneMemberSinglePanel"
NameTextPath = ModulePath+'/nameText'
GetInvitePath = TeamPanel+'/getInviteBtn'

class TableTeamMgr(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(TableTeamMgr, self).__init__(namespace, name, param)
        self.paramDict = param
        if self.paramDict:
            self._allPlayerTeam = self.paramDict['teamDic']
        else:
            # 当前玩家组队信息，通过发送事件到服务端获取
            self._allPlayerTeam = {}
        
        if self.paramDict:
            self._allPlayerName = self.paramDict['allPlayerName']
        else:
            # 所有玩家id：中文名，便于离线时候获取名字
            self._allPlayerName = {}

        # 组队状态的玩家
        self._playerInTeam = []
        # 非组队状态的玩家
        self._playerNotInTeam = []
        self._newModulePathList = []
        self._teamBtnDict = {}
        self._moreBtnPressed = False

        # 邀请他人cd
        self._inviteCD = 5 *30
        # 邀请玩家与进度条对象,字典格式：pid:barObj
        self._inviteBarObj = {}
        # 邀请玩家与邀请cd,字典格式：pid:cd(int)
        self._inviteBarCD = {}
        # 处于被邀请状态时邀请人id
        self._initrPlayerId = None

    def Destroy(self):
        super(TableTeamMgr, self).Destroy()
        # UI销毁时将储存cd状态进行储存
        self.BroadcastEvent('SaveinviteBarCD',{"pid": self.mPlayerId,'inviteBarCD':self._inviteBarCD,"inviteBarObj":self._inviteBarObj})

    def Update(self):
        for obj in self.mWidgetList:
            obj.Update()
        if self._inviteBarObj:
            for pid in list(self._inviteBarObj.keys()):
                barObj = self._inviteBarObj[pid]
                if self._inviteBarCD[pid]>0:
                    barObj.SetVisible(True)
                    barObj.SetValue(float(self._inviteBarCD[pid])/float(self._inviteCD))
                else:
                    barObj.SetVisible(False)
                    self._inviteBarObj.pop(pid)
                    self._inviteBarCD.pop(pid)
                    self.BroadcastEvent('SaveinviteBarCD',{"pid": self.mPlayerId,'inviteBarCD':self._inviteBarCD,"inviteBarObj":self._inviteBarObj})

    def Create(self):
        super(TableTeamMgr, self).Create()
        self._teamPanel = self.GetBaseUIControl(TeamPanel)
        # 关闭按钮
        self._closeBtn = self._teamPanel.GetChildByPath('/headPanel/closeBtn').asButton()
        clientApiMgr.SetBtnTouchUpCallback(self._closeBtn,self.OnClose)
        self._inviteBtn = self.GetBaseUIControl(GetInvitePath).asButton()
        self._inviteRedDot = self.GetBaseUIControl(GetInvitePath+'/redDot')
        self.InitUI()

    def InitUI(self):
        """初始化"""
        self.BroadcastEvent('GetinviteBarCD',{"pid": self.mPlayerId})
        self.BroadcastEvent('GetInvite',{'pid':self.mPlayerId})
        self.GetPlayerTeam({'teamDic':self._allPlayerTeam,'allPlayerName':self._allPlayerName})
        pass
    
    # region 按钮回调
    def OnClose(self,args):
        clientApi.PopScreen()
        pass 
    def OnInvite(self,args):
        """有邀请时邀请按钮点击回调"""
        data = args['AddTouchEventParams']
        opid = data['opid']
        self._inviteRedDot.SetVisible(False)
        name = compFactory.CreateName(opid).GetName()
        if not name:
            name = self._allPlayerName[opid]
        def AcceptInvite():
            self._inviteBtn.SetVisible(False)
            self.SendMsgToServer('TryAcceptInvite',{'opid':opid,'tpid':self.mPlayerId})
            self.BroadcastEvent('NoInvite', {'opid':opid, 'pid':self.mPlayerId})
        def RefuseInvite():
            self._inviteBtn.SetVisible(False)
            self.BroadcastEvent('NoInvite', {'opid':opid, 'pid':self.mPlayerId})
            self.BroadcastEvent("RefuseInvite", {'opid':opid, 'pid':self.mPlayerId})
        param = {
            "confirmMethod": AcceptInvite,
            "cancelMethod" : RefuseInvite,
            "headTxt": "新邀请",
            "infoTxt": "是否接受玩家 %s 的邀请？" % (name),
            "confirmTxt":"接受",
            "cancelTxt":"拒绝"
        }
        Instance.mUIManager.PushUI(UIDef.UI_TableNotice,param)

    def OnBtnPress(self,args):
        """主要操作按钮回调，需要keyType做区分"""
        data = args['AddTouchEventParams']
        keyType,keyData = data['keyType'],data['keyData']
        tpid = keyData['tpid']
        data = {
            'opid':self.mPlayerId,
            'tpid':tpid
        }
        # 邀请
        if keyType == 'inviteBtn':
            barObj = keyData['barObj']
            if tpid in self._inviteBarObj:
                self._inviteBarObj[tpid] = barObj
                return
            else:
                self._inviteBarCD[tpid] = self._inviteCD
                self._inviteBarObj[tpid] = barObj
                barObj.SetVisible(True)
                self.SendMsgToServer('TryInviteTeam', data)
                self.BroadcastEvent('TryInviteTeam', {"pid": self.mPlayerId})
                self.BroadcastEvent('SaveinviteBarCD', {"pid": self.mPlayerId, 'inviteBarCD':self._inviteBarCD, "inviteBarObj":self._inviteBarObj})
        # 离开团队
        elif keyType == 'leaveTeamBtn':
            def TryLeaveTeam():
                self.SendMsgToServer('TryLeaveTeam',data)
                self.BroadcastEvent('TryLeaveTeam',data)
            pid = tpid
            if tpid not in self._allPlayerTeam:
                pid = self.FindOwnr(tpid)
            name = compFactory.CreateName(pid).GetName()
            if not name:
                name = self._allPlayerName[pid]
            param = {
            "confirmMethod": TryLeaveTeam,
            "headTxt": "确认离开",
            "infoTxt": "是否离开 %s 的团队？" % (name),
            }
            Instance.mUIManager.PushUI(UIDef.UI_TableNotice,param)
        # 更多操作：只控制按钮显示
        elif keyType == 'moreBtn':
            kickBtnObj = self._teamBtnDict['kickBtn'+tpid]
            transferBtnObj = self._teamBtnDict['transferBtn'+tpid]
            moreFuncPanelObj = keyData['moreFuncPanelObj']
            moreFuncPanelObj.SetVisible(True)
            if self._moreBtnPressed:
                self._moreBtnPressed = not self._moreBtnPressed
                kickBtnObj.SetVisible(False)
                transferBtnObj.SetVisible(False)
            else:
                self._moreBtnPressed = not self._moreBtnPressed
                kickBtnObj.SetVisible(True)
                transferBtnObj.SetVisible(True)
        # 踢出团队
        elif keyType == 'kickBtn':
            def TryKickTeam():
                self.SendMsgToServer('TryKickTeam',{'opid':self.mPlayerId,'tpid':tpid})
            name = compFactory.CreateName(tpid).GetName()
            if not name:
                name = self._allPlayerName[tpid]
            param = {
            "confirmMethod": TryKickTeam,
            "headTxt": "确认踢出",
            "infoTxt": "是否将玩家 %s 踢出团队？" % (name),
            }
            Instance.mUIManager.PushUI(UIDef.UI_TableNotice,param)
        # 转让队长
        elif keyType == 'transferBtn':
            name = compFactory.CreateName(tpid).GetName()
            if not name:
                name = self._allPlayerName[tpid]
            def TryTransferTeam():
                self.SendMsgToServer('TryTransferTeam',data)
            param = {
            "confirmMethod": TryTransferTeam,
            "headTxt": "确认转让",
            "infoTxt": "是否将队长转让给玩家 %s ？" % (name),
            }
            Instance.mUIManager.PushUI(UIDef.UI_TableNotice,param)
        else:
            print '!!!!!=====团队按钮UI错误=====!!!!!'
    # endregion
    # region 方法
    def OnBtnPressDown(self,args):
        pass
    def RegisterBtn(self, dictPath, dictKey, keyPath, keyType, keyData):
        """注册按钮回调 包含数据信息 
        dictPath=需要储存按钮信息的字典 dictKey=字典中key keyPath=按钮的完整路径 keyType=按钮类型，需要自定义用于区分 keyData=自定义数据，在按钮回调中获取到
        """
        dictPath.update({dictKey: self.GetBaseUIControl(keyPath).asButton()})
        btnObj = dictPath[dictKey]
        btnObj.AddTouchEventParams({"isSwallow": True, 'keyType':keyType,'keyData': keyData})
        btnObj.SetButtonTouchUpCallback(self.OnBtnPress)
        btnObj.SetButtonTouchDownCallback(self.OnBtnPressDown)
        btnObj.SetVisible(True)
        return btnObj
    
    def SetPurview(self,modulePath,key):
        """设置玩家权限显示"""
        Leader = '/mbStateStackPanel/mbStateLeader'
        Member = '/mbStateStackPanel/mbStateMember'
        Other = '/mbStateStackPanel/mbStateOther'
        purViewDic = {'Leader':Leader,'Member':Member,'Other':Other}
        for purView in [Leader,Member,Other]:
            purViewObj = self.GetBaseUIControl(modulePath+purView)
            if purView == purViewDic[key]:
                purViewObj.SetVisible(True)
            else:
                purViewObj.SetVisible(False)
    def SetName(self,modulePath,name):
        """设置玩家名字"""
        # 玩家名字路径
        textPath = '/nameText'
        self.GetBaseUIControl(modulePath+textPath).asLabel().SetText(name)
    def SetBtn(self,modulePath,key):
        """设置玩家特定按钮可见"""
        inviteBarPath = '/mbFuncBtnStackPanel/invite_panel/invite_cd_bar'
        inviteBtn = '/mbFuncBtnStackPanel/invite_panel/inviteBtn'
        leaveTeamBtn = '/mbFuncBtnStackPanel/leaveTeamBtn'
        moreFuncPanelPath = '/mbFuncBtnStackPanel/moreFuncPanel'
        moreBtn = '/mbFuncBtnStackPanel/moreBtn'
        kickBtn = '/mbFuncBtnStackPanel/moreFuncPanel/kickBtn'
        transferBtn = '/mbFuncBtnStackPanel/moreFuncPanel/transferBtn'
        btnDic = {'inviteBtn':inviteBtn,'leaveTeamBtn':leaveTeamBtn,'moreBtn':moreBtn,'kickBtn':kickBtn,'transferBtn':transferBtn}
        if key:
            moreFuncPanel = self.GetBaseUIControl(modulePath+moreFuncPanelPath)
            for btnPath in [inviteBtn,leaveTeamBtn,moreBtn,kickBtn,transferBtn]:
                btnObj = self.GetBaseUIControl(modulePath+btnPath).asButton()
                if btnDic[key] == btnPath:
                    if btnPath == moreBtn:
                        moreFuncPanel.SetVisible(True)
                    btnObj.SetVisible(True)
                else:
                    btnObj.SetVisible(False)
                    moreFuncPanel.SetVisible(False)
        else:
            for btnPath in [inviteBtn,leaveTeamBtn,moreBtn,kickBtn,transferBtn]:
                btnObj = self.GetBaseUIControl(modulePath+btnPath).asButton().SetVisible(False)
    def FindOwnr(self,tpid):
        """寻找某个玩家的队长
        return 队长id opid"""
        for opid in self._allPlayerTeam:
            memberPlayerList = self._allPlayerTeam[opid]
            if memberPlayerList:
                for pid in memberPlayerList:
                    if tpid == pid:
                        return opid
        return None
    def GetNewName(self,pid):
        """获取玩家的最新名字，并存在self._allPlayerName
        return name
        """
        name = self._allPlayerName[pid]
        nowName = compFactory.CreateName(pid).GetName()
        if nowName:
            name = nowName
        if pid == self.mPlayerId:
            name+='（我）'
        return name
    # endregion

    # region 刷新UI
    def UpdateTeamView(self):
        """刷新组队UI"""
        # 初始化
        for newModulePath in self._newModulePathList:
            self.RemoveComponent(newModulePath,ContentPath)
        self._newModulePathList = []
        self.SetBtn(ModulePath,False)


        mpid = self.mPlayerId
        # 模版名称
        moduleName = 'mCloneMemberSinglePanel'
        # 原版模版路径
        ModulePath
        # 按钮路径
        inviteBtn = '/mbFuncBtnStackPanel/invite_panel/inviteBtn'
        leaveTeamBtn = '/mbFuncBtnStackPanel/leaveTeamBtn'
        moreBtn = '/mbFuncBtnStackPanel/moreBtn'
        moreFuncPanelPath = '/mbFuncBtnStackPanel/moreFuncPanel'
        kickBtn = '/mbFuncBtnStackPanel/moreFuncPanel/kickBtn'
        transferBtn = '/mbFuncBtnStackPanel/moreFuncPanel/transferBtn'
        # 邀请进度条
        inviteBar = '/mbFuncBtnStackPanel/invite_panel/invite_cd_bar'
        
        btnPathKey = {inviteBtn:'inviteBtn',leaveTeamBtn:'leaveTeamBtn',moreBtn:'moreBtn',kickBtn:'kickBtn',transferBtn:'transferBtn'}
        btnPathList = [inviteBtn,leaveTeamBtn,moreBtn,kickBtn,transferBtn]
        
        self._tabView = self.GetBaseUIControl('/teamManagerPanel/teamPanel/mbGroupScrollView').asScrollView()
        # 判断当前这个玩家是否是队长
        if mpid in self._allPlayerTeam:
            self.SetName(ModulePath,self.GetNewName(mpid))
            self.SetBtn(ModulePath,'leaveTeamBtn')
            self.RegisterBtn(self._teamBtnDict,'leaveTeamBtn'+mpid,ModulePath+leaveTeamBtn,'leaveTeamBtn',{'tpid':mpid})
            self.SetPurview(ModulePath,'Leader')
            memberPlayerList = self._allPlayerTeam[mpid]
            # 是否有成员
            if memberPlayerList:
                self.SetBtn(ModulePath,'leaveTeamBtn')
                for tpid in memberPlayerList:
                    newModuleName = moduleName+tpid
                    newModulePath = ContentPath+'/'+newModuleName
                    # 克隆成员面板
                    if self.Clone(ModulePath,ContentPath,newModuleName,False,False):
                        self._newModulePathList.append(newModulePath)
                    # 设置成员名字
                    tname = self.GetNewName(tpid)
                    self.SetName(newModulePath,tname)
                    self.SetPurview(newModulePath,'Member')
                    # 成员绑定对应按钮回调
                    for btnPath in btnPathList:
                        btnKey = btnPathKey[btnPath]
                        data = {'tpid':tpid}
                        if btnPath == moreBtn:
                            data = {'tpid':tpid,'moreFuncPanelObj':self.GetBaseUIControl(newModulePath+moreFuncPanelPath)}
                        self.RegisterBtn(self._teamBtnDict,btnKey+tpid,newModulePath+btnPath,btnKey,data)
                    self.SetBtn(newModulePath,'moreBtn')
            else:
                self.SetBtn(ModulePath,False)

            # 将没有组队玩家罗列出来并初始化邀请按钮
            if self._playerNotInTeam:
                for opid in self._playerNotInTeam:
                    if opid == self.mPlayerId:
                        continue
                    newModuleName = moduleName+opid
                    newModulePath = ContentPath+'/'+newModuleName
                    if self.Clone(ModulePath,ContentPath,newModuleName,False,False):
                        self._newModulePathList.append(newModulePath)
                    # 设置名字
                    oName = tname = self.GetNewName(opid)
                    self.SetName(newModulePath,oName)
                    self.SetPurview(newModulePath,'Other')
                    data = {'tpid':opid}
                    for btnPath in btnPathList:
                        btnKey = btnPathKey[btnPath]
                        # 邀请按钮时将邀请cd显示的进度条obj传入data
                        if btnKey == 'inviteBtn':
                            data = {'tpid':opid,'barObj':self.GetBaseUIControl(newModulePath+inviteBar).asProgressBar()}
                        self.RegisterBtn(self._teamBtnDict,btnKey+opid,newModulePath+btnPath,btnKey,data)
                    self.SetBtn(newModulePath,'inviteBtn')
        # 是否是某个玩家的成员
        elif mpid in self._playerInTeam:
            # 队长id
            opid = None
            opid = self.FindOwnr(mpid)
            tList = self._allPlayerTeam[opid]
            # 设置队长信息
            oPlayerName = compFactory.CreateName(opid).GetName()
            if not oPlayerName:
                oPlayerName = self._allPlayerName[opid]
            self.SetName(ModulePath,oPlayerName)
            self.SetPurview(ModulePath,'Leader')
            # 将成员罗列出来
            for tpid in tList:
                newModuleName = moduleName+tpid
                newModulePath = ContentPath+'/'+newModuleName
                if self.Clone(ModulePath,ContentPath,newModuleName,False,False):
                    self._newModulePathList.append(newModulePath)
                tname = self.GetNewName(tpid)
                self.SetName(newModulePath,tname)
                self.SetPurview(newModulePath,'Member')
                for btnPath in btnPathList:
                    btnKey = btnPathKey[btnPath]
                    self.RegisterBtn(self._teamBtnDict,btnKey+tpid,newModulePath+btnPath,btnKey,{'tpid':tpid})
                if tpid == mpid:
                    self.SetBtn(newModulePath,'leaveTeamBtn')
                else:
                    self.SetBtn(newModulePath,False)
                
        self.UpdateScreen(True)
    # endregion 
    # region 同端（客服端）事件
    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.TableTeamClient)
    def InviteTeamUI(self,args):
        """被邀请事件"""
        if args['pid'] == self.mPlayerId:
            opid = args.get('opid',None)
            self._initrPlayerId = opid
            if opid:
                # 有邀请人时
                self._inviteBtn.SetVisible(True)
                self._inviteRedDot.SetVisible(True)
                # 邀请玩家名称
                clientApiMgr.SetBtnTouchUpCallback(self._inviteBtn,self.OnInvite,{'opid':opid})
            else:
                self._inviteBtn.SetVisible(False)
                
    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.TableTeamClient)
    def GetinviteBarCDUI(self,args):
        if args['pid'] == self.mPlayerId:
            self._inviteBarCD = args['inviteBarCD']
            self._inviteBarObj = args['inviteBarObj']
    # endregion 
    # region 服务端事件
    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def InviteTeamBarUI(self,args):
        """隐藏队员的CD显示与CD重置"""
        if args['pid'] == self.mPlayerId:
            mpid = self.mPlayerId
            if mpid in self._allPlayerTeam:
                tlist = self._allPlayerTeam[mpid]
                if tlist:
                    for pid in tlist:
                        if pid in self._inviteBarObj:
                            inviteBarObj = self._inviteBarObj[pid]
                            inviteBarObj.SetVisible(False)
                            self._inviteBarObj.pop(pid)
                            self._inviteBarCD.pop(pid)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def GetPlayerTeam(self,args):
        """获取到当前组队信息"""
        mpid = self.mPlayerId
        allOnlinePid = clientApi.GetPlayerList()
        self._allPlayerTeam = args["teamDic"]
        self._allPlayerName = args["allPlayerName"]
        self._playerInTeam = []
        self._playerNotInTeam = []
        if self._allPlayerTeam:
            for opid in self._allPlayerTeam:
                tpidList = self._allPlayerTeam[opid]
                if tpidList:
                    self._playerInTeam.append(opid)
                    for tpid in tpidList:
                        if tpid in self._playerInTeam:
                            print '错误，有重复组队'
                        else:
                            self._playerInTeam.append(tpid)
                else:
                    if opid in allOnlinePid:
                        self._playerNotInTeam.append(opid)
        self.UpdateTeamView()


    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def HasAcceptInvite(self,args):
        pass
        
    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def PlayerLeaveGame(self,args):
        """玩家离开时，如果离开人是邀请人，则隐藏邀请"""
        pid = args['pid']
        if pid == self._initrPlayerId:
            self._inviteBtn.SetVisible(False)
    # endregion 
