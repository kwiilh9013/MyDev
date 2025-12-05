# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()

class RewardsUI(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(RewardsUI, self).__init__(namespace, name, param)
		self._rewardsData = param['data']

	def Create(self):
		super(RewardsUI, self).Create()
		self._closeBtn = self.GetBaseUIControl('/button').asButton()
		self._closeBtn.AddTouchEventParams({"isSwallow": True})
		self._closeBtn.SetButtonTouchUpCallback(self.Close)

		rewardsPath = '/button/rewards'
		self._rewardsPathScrollView = ScrollViewWidget(self, rewardsPath, '/scroll_content', 2)
		self._rewardsPathListView = ListViewWidget(self, rewardsPath, '/scroll_content/rewards', '/scroll_content/rewards/item', self.OnRewardsItemActive, self.OnRewardItemClick, self._rewardsPathScrollView, 2)
		self._rewardsPathListView.UpdateData(self._rewardsData)

	@ViewBinder.binding(ViewBinder.BF_BindString, "#main.gametick")
	def OnGameTick(self):
		if self.Inited:
			self._rewardsPathListView.Update()

	def OnRewardsItemActive(self, path, ctrl, index, data):
		identifier = data['identifier']
		count = data['count']
		aux = 0
		ctrl.GetChildByPath('/count').asLabel().SetText('x%d' % count)
		ctrl.GetChildByPath('/icon').asItemRenderer().SetUiItem(identifier, aux)

	def OnRewardItemClick(self, path, ctrl, index, data, args):
		Instance.mUIManager.PushUI(UIDef.UI_ItemInfoUI, {
			'identifier': data['identifier'],
			'touchPos': args['touchPos']
		})

	def Close(self, args):
		Instance.mUIManager.PopUI()
