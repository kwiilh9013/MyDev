# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler


class BannerViewWidget(PoolableWidget):

	def __init__(self, baseUI, path, itemPath, onActiveCall, onChangeCall, direct=2):
		super(BannerViewWidget, self).__init__(baseUI, path, '', itemPath)
		self._direct = direct
		self._container = self.GetBaseUIControl('')
		self._contentContainer = self._container
		self._itemContainer = self.GetBaseUIControl(itemPath)
		self._itemSize = (0, 0)
		self._data = []
		self._onActiveCall = onActiveCall
		self._onChangeCall = onChangeCall
		self._index = -1
		self._bannerIndex = 0
		self._tweenHandler = None
		self._movingDir = 0
		while len(self._itemCtrlActive) < 3:
			self.AddItemCtrl()

	def UpdateData(self, data):
		self._data = data

	def SetCurrent(self, index):
		self._index = index
		self._bannerIndex = 0
		self._BannerChange(True)
		self._tweenHandler = None

	def _BannerChange(self, force=False):
		size = self._contentContainer.GetSize()
		i = 0
		n = len(self._itemCtrlActive)
		while i < n:
			item = self._itemCtrlActive[i]
			ctrl = item['ctrl']
			offsetIndex = ((i + self._bannerIndex) % n) - 1
			pos = MathUtils.TupleMul(size, offsetIndex)
			if self._direct == 1:
				pos = (0, pos[1])
			if self._direct == 2:
				pos = (pos[0], 0)
			ctrl.SetVisible(True)
			ctrl.SetPosition(pos)
			ctrl.SetSize(size, True)
			dataIndex = (self._index + offsetIndex) % len(self._data)
			item['index'] = dataIndex
			if self._onActiveCall:
				if force or dataIndex != self._index:
					self._onActiveCall(item['path'], ctrl, dataIndex, self._data[dataIndex])
			i += 1
		self._itemSize = size
		self._itemContainer.SetPosition(self._itemSize)
		self._itemContainer.SetVisible(True)

	def Update(self):
		size = self._contentContainer.GetSize()
		if size[0] != self._itemSize[0] or size[1] != self._itemSize[1]:
			self._BannerChange()
		if self._tweenHandler:
			self._tweenHandler.Update()

	def Prev(self):
		self._Move(-1)

	def Next(self):
		self._Move(1)

	def Move(self, dir):
		if self._tweenHandler:
			return
		target = 0
		if self._direct == 1:
			target = self._itemSize[1]
		if self._direct == 2:
			target = self._itemSize[0]
		self._movingDir = dir
		self.DoTweenScroll(0, -dir * target)

	def DoTweenScroll(self, fromPos, toPos):
		self._tweenHandler = TweenHandler('easeOutQuad', 0.3, fromPos, toPos, self.TweenScrollUpdate, self.TweenScrollEnd)

	def TweenScrollUpdate(self, value):
		size = self._itemSize
		i = 0
		n = len(self._itemCtrlActive)
		while i < n:
			item = self._itemCtrlActive[i]
			ctrl = item['ctrl']
			offsetIndex = ((i + self._bannerIndex) % n) - 1
			pos = MathUtils.TupleMul(size, offsetIndex)
			if self._direct == 1:
				pos = (0, pos[1]+value)
			if self._direct == 2:
				pos = (pos[0]+value, 0)
			ctrl.SetPosition(pos)
			i += 1

	def TweenScrollEnd(self):
		self._index = (self._index + self._movingDir) % len(self._data)
		self._bannerIndex -= self._movingDir
		self._tweenHandler = None
		self._movingDir = 0
		self._BannerChange()
		ctrl = self._GetActiveItemCtrl(self._index)
		if self._onChangeCall:
			self._onChangeCall(ctrl['path'], ctrl['ctrl'], self._index, self._data[self._index])
