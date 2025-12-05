# -*- coding: utf-8 -*-
import random

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()

class BindHud(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(BindHud, self).__init__(namespace, name, param)
		self._updateCallback = None

	def Create(self):
		super(BindHud, self).Create()
		self._anchor = self.GetBaseUIControl('/anchor')
		self._anchorPoint = self.GetBaseUIControl('/anchor/point')
		self._delayFrame = 0

	def GetBindSize(self):
		return self._anchor.GetSize()

	def GetBindAnchorPos(self):
		return self._anchorPoint.GetGlobalPosition()

	def Update(self):
		if self._delayFrame < 5:
			self._delayFrame += 1
			return
		if self._updateCallback:
			self._updateCallback(self._anchorPoint.GetGlobalPosition(), self._anchor.GetSize())

	def SetUpdateCallback(self, callback):
		self._updateCallback = callback