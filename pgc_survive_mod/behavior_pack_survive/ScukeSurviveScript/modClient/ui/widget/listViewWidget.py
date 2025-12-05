# -*- coding: utf-8 -*-
import math
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget


class ListViewWidget(PoolableWidget):

	def __init__(self, baseUI, path, contentPath, itemPath, onActiveCall, onItemClickCall, scrollView, spacing=0):
		"""
		baseUI = UI界面对象, path = 控件完整路径, contentPath = 内容控件路径(从滚动框开始), itemPath = 控件内容的路径(从滚动框开始), 
		onActiveCall = 设置控件内容的回调, onItemClickCall = 点击选项的回调, scrollView = 滚动框控件对象, spacing = 单个控件的间隔
		"""
		super(ListViewWidget, self).__init__(baseUI, path, contentPath, itemPath)
		self._direct = scrollView.Direct
		self._container = self.GetBaseUIControl('')
		self._contentContainer = self.GetBaseUIControl(contentPath)
		self._itemContainer = self.GetBaseUIControl(itemPath)
		self._scrollView = scrollView
		self._itemSize = (0, 0)
		self._data = []
		self._preloadCount = 2
		self._ranges = (0, -1)
		self._size = (0, 0)
		self._onActiveCall = onActiveCall
		self._onItemClickCall = onItemClickCall
		self._spacing = spacing

	def UpdateData(self, data):
		"""
		更新数据
		:param data: 数据 [{}, ...]
		"""
		self._data = data
		self.ScrollTo(0, 0)
		ranges = (0, -1)
		self.UpdateItem(ranges)
		self._ranges = (0, -1)

	def UpdateView(self):
		ranges = self._ranges
		self._ranges = (0, -1)
		self.UpdateItem(ranges)
		self._ranges = ranges

	def UpdateSize(self):
		sizeChanged = None
		if MathUtils:
			data = self._data
			curSize = self._contentContainer.GetSize()
			# 内容控件大小固定的
			itemSize = self.GetItemSize()
			itemSize = MathUtils.TupleAdd(itemSize, (self._spacing, self._spacing))
			if self._direct == 1:
				curSize = (curSize[0], len(data) * itemSize[1])
			if self._direct == 2:
				curSize = (len(data) * itemSize[0], curSize[1])
			sizeChanged = itemSize[0] != self._itemSize[0] or itemSize[1] != self._itemSize[1]
			if curSize[0] != self._size[0] or curSize[1] != self._size[1] or sizeChanged:
				self._itemContainer.SetPosition(curSize)
				if curSize[0] > 0 and curSize[1] > 0:
					self._contentContainer.SetSize(curSize, True)
					self._size = curSize
			self._itemSize = itemSize
		return sizeChanged

	def Update(self):
		if not self._scrollView or not self._container:
			return

		self._scrollView.Update()
		if self.UpdateSize():
			self._ranges = (0, -1)
		ranges = self.GetIndexRanges()
		if not ranges:
			return
		
		self.UpdateItem(ranges)
		self._ranges = ranges
		clickInfo = self._scrollView.FlushClickInfo()
		if clickInfo and self._onItemClickCall:
			pos = clickInfo['pos']
			dir = 1  # left/top
			index = -1
			itemRealSize = MathUtils.TupleSub(self._itemSize, (self._spacing, self._spacing))
			if self._direct == 1 and self._itemSize[1] > 0:
				d = dir * pos[1]
				index = int(d / self._itemSize[1])
				offset = pos[1] - index * self._itemSize[1]
				if offset > itemRealSize[1]:
					index = -1
				else:
					pos = (pos[0], offset)
			if self._direct == 2 and self._itemSize[0] > 0:
				d = dir * pos[0]
				index = int(d / self._itemSize[0])
				offset = pos[0] - index * self._itemSize[0]
				if offset > itemRealSize[0]:
					index = -1
				else:
					pos = (offset, pos[1])
			if index > -1:
				itemCtrl = self._GetActiveItemCtrl(index)
				if itemCtrl and index < len(self._data):
					self._onItemClickCall(itemCtrl['path'], itemCtrl['ctrl'], index, self._data[index], {
						'pos': pos,
						'touchPos': clickInfo['touchPos'],
					})

	def GetIndexRanges(self):
		curPos = self._scrollView.Position
		if not curPos:
			return None
		
		ranges = (0, 0)
		contentSize = self._container.GetSize()
		dataCount = len(self._data)
		dir = -1  # left/top
		if self._direct == 1 and self._itemSize[1] > 0:
			d = dir * curPos[1]
			ranges = (int(math.ceil(d / self._itemSize[1])), int(math.ceil((d + contentSize[1]) / self._itemSize[1])))
		if self._direct == 2 and self._itemSize[0] > 0:
			d = dir * curPos[0]
			ranges = (int(math.ceil(d / self._itemSize[0])), int(math.ceil((d + contentSize[0]) / self._itemSize[0])))
		ranges = (max(ranges[0] - self._preloadCount, 0), min(ranges[1] + self._preloadCount, dataCount - 1))
		return ranges

	def UpdateItem(self, ranges):
		range1 = self._ranges
		range2 = ranges
		start1 = range1[0]
		start2 = range2[0]
		end1 = start1 + max(0, range1[1] - range1[0] + 1)
		end2 = start2 + max(0, range2[1] - range2[0] + 1)
		if start1 == start2 and end1 == end2:
			return
		if start2 < start1:
			s = start1
			start1 = start2
			start2 = s
			s = end1
			end1 = end2
			end2 = s
		dirty = []
		if end1 <= start2:
			dirty.append((start1, end1))
			dirty.append((start2, end2))
		else:
			if start1 < start2:
				dirty.append((start1, start2))
			else:
				dirty.append((start2, start1))
			if end1 < end2:
				dirty.append((end1, end2))
			else:
				dirty.append((end2, end1))
		posDir = (0, 0)
		if self._direct == 1:
			posDir = (0, self._itemSize[1])
		if self._direct == 2:
			posDir = (self._itemSize[0], 0)

		#curCount = max(0, self._ranges[1] - self._ranges[0] + 1)
		#newCount = max(0, ranges[1] - ranges[0] + 1)
		for dirtyRange in dirty:
			i = dirtyRange[0]
			e = dirtyRange[1]
			while i < e:
				active = i >= ranges[0] and i <= ranges[1]
				itemCtrl = self.GetActiveItemCtrl(i)
				if itemCtrl is None:
					itemCtrl = self.AddItemCtrl()
				if itemCtrl:
					if active:
						itemCtrl['index'] = i
						itemCtrl['ctrl'].SetPosition(MathUtils.TupleMul(posDir, i))
					else:
						itemCtrl['index'] = -1
					if self._onActiveCall and active:
						self._onActiveCall(itemCtrl['path'], itemCtrl['ctrl'], i, self._data[i])
					itemCtrl['ctrl'].SetVisible(active)
				else:
					self.logger.error('Not found ItemCtrl of %d' % i)
				i += 1


	def ScrollTo(self, index, duration=0.1):
		pos = MathUtils.TupleMul(self._itemSize, -index)
		self._scrollView.ScrollTo(pos, duration)

	def GetDataFromIndex(self, index):
		if index < 0:
			return None
		if index >= len(self._data):
			return None
		return self._data[index]

