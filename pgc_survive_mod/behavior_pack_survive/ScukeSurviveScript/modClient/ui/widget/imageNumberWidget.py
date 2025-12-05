# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget


class ImageNumberWidget(PoolableWidget):

	def __init__(self, baseUI, path, itemPath, numberTextures):
		super(ImageNumberWidget, self).__init__(baseUI, path, '', itemPath)
		self._contentContainer = self.GetBaseUIControl('')
		self._itemContainer = self.GetBaseUIControl(itemPath)
		self._numberTextures = numberTextures
		self.SetNumber(0)

	def SetNumber(self, value):
		_base = 10
		_cur = int(value)
		index = 0
		numbers = []
		count = len(self._itemCtrlActive)
		while _cur > 0 or index == 0:
			b = _cur % _base
			a = int((_cur - b)/_base)
			item = self._GetActiveItemCtrl(index)
			if not item:
				item = self.AddItemCtrl()
				item['index'] = index
				count += 1
			numbers.append(b)
			_cur = a
			index += 1
		index = 0
		n = len(numbers)
		while index < n:
			item = self._GetActiveItemCtrl(index)
			ctrl = item['ctrl']
			v = numbers[n-1-index]
			ctrl.asImage().SetSprite(self._numberTextures[v])
			ctrl.SetVisible(True)
			index += 1
		while index < count:
			item = self._itemCtrlActive[index]
			ctrl = item['ctrl']
			ctrl.SetVisible(False)
			index += 1
		self._itemContainer.SetVisible(False)

	def SetTexture(self, path):
		"""设置贴图"""
		item = self._GetActiveItemCtrl(0)
		ctrl = item['ctrl']
		ctrl.asImage().SetSprite(path)
		if ctrl.GetVisible() is not True:
			ctrl.SetVisible(True)
		pass

	def SetColor(self, color):
		"""设置颜色"""
		item = self._GetActiveItemCtrl(0)
		ctrl = item['ctrl']
		ctrl.asImage().SetSpriteColor(color)
		pass
