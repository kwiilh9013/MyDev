# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import time
from ScukeConvertTableScript.ScukeCore.common.api.commonApiMgr import *
from ScukeConvertTableScript.ScukeCore.client import engineApiGac
from ScukeConvertTableScript.ScukeCore.common.api import itemApi
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.ScukeCore.client.ui.utils import uiUtils
from ScukeConvertTableScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeConvertTableScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.modCommon.cfg import ItemEMCConfig


class UiBaseWidget(CommonEventRegister):
    def __init__(self, uiInst, sysInst, path):
        CommonEventRegister.__init__(self, sysInst)
        self._mTick0 = 0
        self.sys = sysInst
        self.uiInst = uiInst
        self.path = path
        self._btnDict = {}
        self.mPlayerId = clientApi.GetLocalPlayerId()
        self.uiInst.AddWidgetObj(self)

    def Create(self):
        pass

    def Update(self):
        pass

    def Destroy(self):
        CommonEventRegister.OnDestroy(self)
        del self

    def GetBaseUiControl(self, path):
        return self.uiInst.GetBaseUIControl(self.path + path)
