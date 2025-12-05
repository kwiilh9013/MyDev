# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler


class SurviveLoading(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(SurviveLoading, self).__init__(namespace, name, param)

	def Create(self):
		super(SurviveLoading, self).Create()
		self._panel = self.GetBaseUIControl('/panel')

	def SetActive(self, active):
		self._panel.SetVisible(active)
