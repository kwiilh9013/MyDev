from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.ui.baseWidget import BaseWidget


class TabViewWidget(BaseWidget):

	def __init__(self, baseUI, path, tabs, pages, caller=None, index=0):
		super(TabViewWidget, self).__init__(baseUI, path)
		self._tabs = []
		self._pages = []
		self._index = -1
		self._caller = caller
		for i in range(0, len(tabs)):
			tabPath = tabs[i]
			tabCtrl = self.GetBaseUIControl(tabPath).asButton()
			tabCtrl.AddTouchEventParams({"isSwallow":True})
			def _selectFunc(index):
				return lambda (args): self.SetIndex(index)
			tabCtrl.SetButtonTouchUpCallback(_selectFunc(i))
			self._tabs.append({
				'default': tabCtrl.GetChildByName('default').asImage(),
				'selected': tabCtrl.GetChildByName('selected').asImage(),
			})
			if pages and i < len(pages):
				pagePath = pages[i]
				pathCtrl = self.GetBaseUIControl(pagePath)
				self._pages.append(pathCtrl)
		self.SetIndex(index)

	def SetIndex(self, index):
		last = self._index
		if index == last:
			return
		for i in range(0, len(self._tabs)):
			tabItem = self._tabs[i]
			active = i == index
			self._SetBtnState(tabItem, 'selected' if active else 'default')
			if i < len(self._pages):
				pathCtrl = self._pages[i]
				pathCtrl.SetVisible(active)

		self._index = index
		if self._caller:
			self._caller(last, index)

	def _SetBtnState(self, btn, state):
		for key, img in btn.iteritems():
			img.SetAlpha(1 if key == state else 0)
			img.SetVisible(key == state)