# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget


class ImageMultiNumberWidget(PoolableWidget):
	"""多个数字贴图，不进行克隆"""
	def __init__(self, baseUI, path, itemPathList, numberTextures):
		"""
		itemPathList: 每位数字的控件路径，从右到左排列
		"""
		super(ImageMultiNumberWidget, self).__init__(baseUI, path, '', '')
		self._contentContainer = self.GetBaseUIControl('')
		self._itemList = []
		for path in itemPathList:
			item = self.GetBaseUIControl(path)
			self._itemList.append(item)
		self._numberTextures = numberTextures
		self.SetNumber(0)

	def SetNumber(self, value):
		_base = 10
		_cur = int(value)
		index = 0
		count = len(self._itemList)
		while index < count:
			b = _cur % _base
			a = int((_cur - b)/_base)
			item = self._itemList[index]
			# 设置UI
			item.asImage().SetSprite(self._numberTextures[b])
			_cur = a
			index += 1
			if index >= count:
				break
		pass
