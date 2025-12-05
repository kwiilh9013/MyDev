# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client.ui.baseWidget import BaseWidget


class PoolableWidget(BaseWidget):
	def __init__(self, baseUI, path, contentPath, itemPath):
		super(PoolableWidget, self).__init__(baseUI, path)
		self._contentPath = contentPath
		self._itemPath = itemPath
		# 未使用的控件
		self._itemCtrlPool = []
		# 当前正使用的控件
		self._itemCtrlActive = []
		self._uid = 0
		# 内容控件的大小
		self._baseItemSize = (0, 0)

	def GetItemSize(self):
		if self._baseItemSize == (0, 0):
			# 如果UI是关闭状态，只会获取到(0,0)
			itemCtrl = self.GetBaseUIControl(self._itemPath)
			if itemCtrl:
				self._baseItemSize = itemCtrl.GetSize()
				if self._baseItemSize != (0, 0):
					# 如果此时获取到大小，则隐藏该UI
					self.SetUIVisible(itemCtrl, False)
		return self._baseItemSize

	def GetActiveItemCtrl(self, index):
		return self._GetActiveItemCtrl(index)

	def _GetActiveItemCtrl(self, index):
		ret = None
		for item in self._itemCtrlActive:
			_index = item['index']
			if _index == index:
				return item
			if _index == -1:
				ret = item
		return ret

	def AddItemCtrl(self):
		item = self.GetItemCtrl()
		ctrl = item['ctrl']
		ctrl.SetVisible(False)
		self._itemCtrlActive.append(item)
		return item

	def RemoveItemCtrl(self, itemCtrl=None):
		if itemCtrl:
			ctrl = itemCtrl['ctrl']
			ctrl.SetVisible(False)
			self._itemCtrlActive.remove(itemCtrl)
		else:
			activeCtrlCount = len(self._itemCtrlActive)
			if activeCtrlCount > 0:
				i = 0
				while i < activeCtrlCount:
					item = self._itemCtrlActive[i]
					if item['index'] == -1:
						itemCtrl = self._itemCtrlActive.pop(i)
						break
					i += 1
				if itemCtrl:
					ctrl = itemCtrl['ctrl']
					ctrl.SetVisible(False)
				else:
					self.logger.error('Not found ItemCtrl to remove')
		if itemCtrl:
			self.PutItemCtrl(itemCtrl)

	def RemoveAllItemCtrl(self):
		i = 0
		while i < len(self._itemCtrlActive):
			self.RemoveItemCtrl(self._itemCtrlActive[i])

	def GetItemCtrl(self):
		ret = None
		if len(self._itemCtrlPool) > 0:
			ret = self._itemCtrlPool.pop()
		else:
			total = len(self._itemCtrlPool) + len(self._itemCtrlActive)
			if total > 30:
				print 'Warning! PoolableItems count: %d, %s' % (total, self._basePath)
			ctrlName = '_item' + str(self._uid)
			if self.Clone(self._itemPath, self._contentPath, ctrlName):
				ctrlPath = self._contentPath + '/' + ctrlName
				ctrl = self.GetBaseUIControl(ctrlPath)
				if ctrl:
					ret = {
						'path': self._basePath + ctrlPath,
						'ctrl': ctrl,
						'index': -1,
					}
					self._uid += 1
		ret['index'] = -1
		return ret

	def PutItemCtrl(self, itemCtrl):
		self._itemCtrlPool.append(itemCtrl)
