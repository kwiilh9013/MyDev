# -*- coding: utf-8 -*-
import random

from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.ScukeCore.client.engineApiGac import *
from ScukeSurviveScript.modCommon import modConfig


class SurviveMenu(ModBaseUI):
    def __init__(self, namespace, name, param):
        super(SurviveMenu, self).__init__(namespace, name, param)
        self._closeBtn = None
        self._taskBtn = None
        self._illustrateBtn = None
        self._settingBtn = None
        self._helpBtn = None
        self._phaseClientSystem = None
        self._starTxt = None
        self._leftDaysTxt = None

    def Create(self):
        super(SurviveMenu, self).Create()
        self.CreateBtn()
        self.OnActive()
        self._phaseClientSystem = clientApi.GetSystem(modConfig.ModNameSpace,
                                                      modConfig.ClientSystemEnum.PhaseClientSystem)
        if self._phaseClientSystem:
            phaseInfo = self._phaseClientSystem.PhaseInfo
            phaseTag = phaseInfo['phase']['tag']
            if phaseInfo['keyPointPhase']:
                phaseTag = phaseInfo['keyPointPhase']['tag']
            LeftDays = phaseInfo['leftDays']
            Days = phaseInfo['days']
            NameMap = {
                "mars": "火星", "earth": "地球",
                "asteroid_belt": "小行星带",
                "jupiter": "木星", "saturn": "土星",
                "uranus": "天王星", "neptune": "海王星"
            }
            self._starTxt = self.GetBaseUIControl("/panel/bg/emojiBg/positionTxt").asLabel()
            self._leftDaysTxt = self.GetBaseUIControl("/panel/bg/emojiBg/dayTxt").asLabel()
            if LeftDays > 0:
                self._starTxt.SetText("流浪总天数： {}天".format(str(Days)))
                self._leftDaysTxt.SetText("距离{}撞击： {}天".format(NameMap.get(phaseTag, "???"), LeftDays))
            else:
                self._starTxt.SetText("流浪总天数： {}天".format(str(Days)))
                self._leftDaysTxt.SetText("地球已漂流： {}天".format(Days))

    def CreateBtn(self):
        BtnList = [('_closeBtn', 'clsBtn'), ('_taskBtn', 'taskModel/iconBtn'),
                   ('_illustrateBtn', 'illustrateModel/iconBtn'), ('_settingBtn', 'settingModel/iconBtn'),
                   ('_helpBtn', 'helpModel/iconBtn')]
        for btn in BtnList:
            setattr(self, btn[0], self.GetBaseUIControl('/panel/bg/' + btn[1]).asButton())
            getattr(self, btn[0]).AddTouchEventParams({"isSwallow": True, 'type': btn[0]})
            getattr(self, btn[0]).SetButtonTouchUpCallback(self.OnMenuBtnPress)

    def OnMenuBtnPress(self, args):
        Type = args['AddTouchEventParams']['type']
        if Type == '_closeBtn':
            Instance.mUIManager.PopUI()
        elif Type == '_taskBtn':
            Instance.mUIManager.PushUI(UIDef.UI_TasksUI)
        elif Type == '_illustrateBtn':
            Instance.mUIManager.PushUI(UIDef.UI_IllustrateUI)
        elif Type == '_settingBtn':
            Instance.mUIManager.PushUI(UIDef.UI_SettingUI)
        elif Type == '_helpBtn':
            Instance.mUIManager.PushUI(UIDef.UI_HelpUI)

    def OnActive(self):
        Image = self.GetBaseUIControl('/panel/bg/emojiBg/emoji').asImage()
        Image.StopAnimation()
        AddTimer(0.5, Image.PlayAnimation)
        AddTimer(random.uniform(0.53, 1.5), Image.StopAnimation)

    def Destroy(self):
        pass
