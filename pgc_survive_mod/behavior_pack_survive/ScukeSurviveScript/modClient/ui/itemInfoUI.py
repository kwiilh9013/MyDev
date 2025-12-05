# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()
from ScukeSurviveScript.modClient.ui.widget.safeAreaWidget import SafeAreaWidget

class ItemInfoUI(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(ItemInfoUI, self).__init__(namespace, name, param)
		self._identifier = param['identifier']
		self._pos = param['touchPos']

	def Create(self):
		super(ItemInfoUI, self).Create()
		self._closeBtn = self.GetBaseUIControl('/button').asButton()
		self._closeBtn.AddTouchEventParams({"isSwallow": True})
		self._closeBtn.SetButtonTouchUpCallback(self.Close)
		self._label = self.GetBaseUIControl('/button/panel/bg/label').asLabel()
		comp = clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLevelId())
		info = comp.GetItemFormattedHoverText(self._identifier)
		self._label.SetText(info)
		self._ItemInfoSafeAreaWidget = SafeAreaWidget(self, '/button/panel', '/bg')
		self._ItemInfoSafeAreaWidget.UpdatePos(self._pos)
		engineApiGac.AddTimer(0, self.DelayUpdate)

	def DelayUpdate(self):
		self._ItemInfoSafeAreaWidget.UpdatePos(self._pos)

	def Close(self, args):
		Instance.mUIManager.PopUI()
