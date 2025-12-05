# -*- coding: utf-8 -*-
import math
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget


class GridViewWidget(PoolableWidget):

	def __init__(self, baseUI, path, contentPath, itemPath, onActiveCall, onItemClickCall, scrollView, spacing=0):
		super(GridViewWidget, self).__init__(baseUI, path, contentPath, itemPath)
		self._direct = scrollView.Direct
		self._container = self.GetBaseUIControl('')
		self._contentContainer = self.GetBaseUIControl(contentPath)
		self._itemContainer = self.GetBaseUIControl(itemPath)
		self._scrollView = scrollView
		self._itemSize = (0, 0)
		self._gridCount = 1
		self._data = []
		self._preloadCount = 3
		self._ranges = (0, -1)
		self._size = (0, 0)
		self._onActiveCall = onActiveCall
		self._onItemClickCall = onItemClickCall
		self._spacing = spacing

	def UpdateData(self, data):
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
			itemSize = self._itemContainer.GetSize()
			spacingSize = (self._spacing, self._spacing)
			itemSize = MathUtils.TupleAdd(itemSize, spacingSize)
			if self._direct == 1:
				self._gridCount = int((curSize[0]+spacingSize[0]+0.1) / itemSize[0] if itemSize[0] > 0 else 1)
				curSize = (curSize[0], math.ceil(float(len(data))/self._gridCount) * itemSize[1])
			if self._direct == 2:
				self._gridCount = int((curSize[1]+spacingSize[1]+0.1) / itemSize[1] if itemSize[1] > 0 else 1)
				curSize = (math.ceil(float(len(data))/self._gridCount) * itemSize[0], curSize[1])
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
		self.UpdateItem(ranges)
		self._ranges = ranges
		clickInfo = self._scrollView.FlushClickInfo()
		if clickInfo and self._onItemClickCall:
			pos = clickInfo['pos']
			dir = 1  # left/top
			index = -1
			subIndex = -1
			itemRealSize = MathUtils.TupleSub(self._itemSize, (self._spacing, self._spacing))
			if self._direct == 1 and self._itemSize[1] > 0:
				d = dir * pos[1]
				s_d = dir * pos[0]
				index = int(d / self._itemSize[1])
				subIndex = int(s_d / self._itemSize[0])
				offset = pos[1] - index * self._itemSize[1]
				s_offset = pos[0] - subIndex * self._itemSize[0]
				if offset > itemRealSize[1] or s_offset > itemRealSize[0]:
					index = -1
				else:
					pos = (s_offset, offset)
			if self._direct == 2 and self._itemSize[0] > 0:
				d = dir * pos[0]
				s_d = dir * pos[1]
				index = int(d / self._itemSize[0])
				subIndex = int(s_d / self._itemSize[1])
				offset = pos[0] - index * self._itemSize[0]
				s_offset = pos[1] - subIndex * self._itemSize[1]
				if offset > itemRealSize[0] or s_offset > itemRealSize[1]:
					index = -1
				else:
					pos = (offset, s_offset)
			if index > -1 and subIndex > -1:
				realIndex = index*self._gridCount + subIndex
				itemCtrl = self._GetActiveItemCtrl(realIndex)
				if itemCtrl and realIndex < len(self._data):
					self._onItemClickCall(itemCtrl['path'], itemCtrl['ctrl'], realIndex, self._data[realIndex], {
						'pos': pos,
						'touchPos': clickInfo['touchPos'],
					})

	def GetIndexRanges(self):
		curPos = self._scrollView.Position
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
		posDir = self._itemSize
		curCount = max(0, self._ranges[1] - self._ranges[0] + 1) * self._gridCount
		newCount = max(0, ranges[1] - ranges[0] + 1) * self._gridCount
		dynamicCount = newCount + curCount  # Easy way
		while dynamicCount - curCount > 0:
			self.AddItemCtrl()
			curCount += 1
		for dirtyRange in dirty:
			i = dirtyRange[0]
			e = dirtyRange[1]
			while i < e:
				active = i >= ranges[0] and i <= ranges[1]
				for k in range(0, self._gridCount):
					l = i * self._gridCount + k
					itemCtrl = self._GetActiveItemCtrl(l)
					if itemCtrl:
						active = active and l < len(self._data)
						if active:
							itemCtrl['index'] = l
							pos = MathUtils.TupleMul(posDir, i)
							if self._direct == 1:
								pos = (posDir[0]*k, posDir[1]*i)
							elif self._direct == 2:
								pos = (posDir[0]*i, posDir[1]*k)
							itemCtrl['ctrl'].SetPosition(pos)
						else:
							itemCtrl['index'] = -1
						if self._onActiveCall and active:
							self._onActiveCall(itemCtrl['path'], itemCtrl['ctrl'], l, self._data[l])
						itemCtrl['ctrl'].SetVisible(active)
					else:
						self.logger.error('Not found ItemCtrl of %d' % l)
				i += 1
		while dynamicCount - newCount > 0:
			self.RemoveItemCtrl()
			newCount += 1


	def ScrollTo(self, index, duration=0.1):
		pos = MathUtils.TupleMul(self._itemSize, -index)
		self._scrollView.ScrollTo(pos, duration)

	def GetDataFromIndex(self, index):
		if index < 0:
			return None
		if index >= len(self._data):
			return None
		return self._data[index]

