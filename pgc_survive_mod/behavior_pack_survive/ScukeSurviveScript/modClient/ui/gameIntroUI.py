# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
ViewBinder = clientApi.GetViewBinderCls()


class GameIntroUI(ModBaseUI):
	"""一键建造 建造操作UI"""
	def __init__(self, namespace, name, param):
		super(GameIntroUI, self).__init__(namespace, name, param)
		self._entryBtn = None

	def Destroy(self):
		# Instance.mEventMgr.UnRegisterEvent(eventConfig.BuildStructUIEvent, self.BuildStructUISubscribeEvent)
		pass

	def Create(self):
		self._entryBtn = self.GetBaseUIControl("/panel_item/btn_open").asButton()
		self._entryBtn.AddTouchEventParams({"isSwallow": True, 'type': '_entryBtn'})
		self._entryBtn.SetButtonTouchUpCallback(self.OnBtnPress)
		self.SetScreenVisible(False)

	def OnBtnPress(self, args):
		Type = args['AddTouchEventParams']['type']
		Instance.mUIManager.PushUI(UIDef.UI_HelpUI, {"isGameIntro": True})
