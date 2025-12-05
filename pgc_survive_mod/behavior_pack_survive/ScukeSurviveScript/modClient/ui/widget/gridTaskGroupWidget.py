# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget


class GridTaskGroupWidget(PoolableWidget):
	@staticmethod
	def SplitGridMapData(data, filterFunc):
		ret = []
		sizeMap = {
			1: [],
			4: []
		}
		groupData = {}
		for item in data:
			big, levelGroup = filterFunc(item)
			size = 4 if big else 1
			if levelGroup not in groupData:
				groupData[levelGroup] = []
			groupData[levelGroup].append({
				'size': size,
				'data': item
			})
		groupKeys = groupData.keys()
		groupKeys.sort()
		gridMap = []
		for key in groupKeys:
			items = groupData[key]
			map = []
			curSize = 0
			for item in items:
				size = item['size']
				if curSize + size <= 16:
					map.append(item)
					curSize += size
				else:
					gridMap.append(map)
					map = []
					map.append(item)
					curSize = size
			if len(map) > 0:
				gridMap.append(map)
		for group in gridMap:
			GridTaskGroupWidget.__PlaceGroupItems(sizeMap, ret, group)
		while len(sizeMap[1])+len(sizeMap[4]) > 0:
			GridTaskGroupWidget.__PlaceGroupItems(sizeMap, ret, None)
		return ret

	@staticmethod
	def __PlaceGroupItems(sizeMap, ret, group):
		sequence = [4, 1, 4]
		sequenceSize = [50, 25, 50]
		startSize = -1
		startSeqIndex = 0
		gridPlaceData = []
		if group is not None:
			for item in group:
				if startSize < 0:
					startSize = item['size']
					startSeqIndex = sequence.index(startSize)
				sizeMap[item['size']].append(item)
		i = 0
		n = 4
		placeGridIndex = 0
		while i < n:
			if len(sizeMap[1]) + len(sizeMap[4]) <= 0 or placeGridIndex > 3:
				break
			_index = (startSeqIndex + i) % len(sequence)
			targetSize = sequence[_index]
			curBase = sequenceSize[_index]
			count = 4 / targetSize
			gridRet = []
			while len(sizeMap[targetSize]) > 0 and count > 0:
				gridRet.append(sizeMap[targetSize].pop(0))
				count -= 1
			if count > 0:
				if count == 4 / targetSize:
					n += 1
					while len(gridRet) > 0:
						sizeMap[targetSize].insert(0, gridRet.pop())
			if len(gridRet) > 0:
				xOffset = placeGridIndex % 2
				yOffset = placeGridIndex / 2
				j = 0
				while j < len(gridRet):
					item = gridRet[j]
					x = j % 2
					y = j / 2
					px = x * curBase + xOffset * 50
					py = y * curBase + yOffset * 50
					gridPlaceData.append({
						'x': px,
						'y': py,
						'size': curBase,
						'data': item['data']
					})
					j += 1
				placeGridIndex += 1
			i += 1
		if len(gridPlaceData) > 0:
			ret.append(gridPlaceData)

	def __init__(self, baseUI, path, contentPath, itemPath, onActiveCall, onItemClickCall):
		super(GridTaskGroupWidget, self).__init__(baseUI, path, contentPath, itemPath)
		self._container = self.GetBaseUIControl('')
		self._contentContainer = self.GetBaseUIControl(contentPath)
		self._itemContainer = self.GetBaseUIControl(itemPath)
		self._data = []
		self._onActiveCall = onActiveCall
		self._onItemClickCall = onItemClickCall

	def UpdateData(self, data):
		self._data = data
		while len(self._itemCtrlActive) > 0:
			itemCtrl = self._itemCtrlActive.pop()
			ctrl = itemCtrl['ctrl']
			ctrl.SetVisible(False)
			self.PutItemCtrl(itemCtrl)
		i = 0
		while i < len(self._data):
			gridBox = self._data[i]
			itemCtrl = self.AddItemCtrl()
			ctrl = itemCtrl['ctrl']
			ctrl.SetVisible(True)
			x = gridBox['x']
			y = gridBox['y']
			size = gridBox['size'] - 0.0 # spacing
			sizeDic = {'followType': 'parent', 'relativeValue': size / 100.0}
			ctrl.SetFullSize('x', sizeDic)
			ctrl.SetFullSize('y', sizeDic)
			ctrl.SetFullPosition('x', {'followType': 'parent', 'relativeValue': x / 100.0})
			ctrl.SetFullPosition('y', {'followType': 'parent', 'relativeValue': y / 100.0})
			itemCtrl['index'] = i
			if self._onActiveCall:
				self._onActiveCall(itemCtrl['path'], ctrl, i, gridBox['data'])
			i += 1
		self._itemContainer.SetSize((0, 0), True)
		self._itemContainer.SetVisible(False)

	def OnClick(self, path, ctrl, index, data, args):
		if self._onItemClickCall is None:
			return
		for activeCtrl in self._itemCtrlActive:
			ctrl = activeCtrl['ctrl']
			size = ctrl.GetSize()
			minPos = ctrl.GetGlobalPosition()
			maxPos = MathUtils.TupleAdd(minPos, size)
			touchPos = args['touchPos']
			if minPos[0] <= touchPos[0] <= maxPos[0] and minPos[1] <= touchPos[1] <= maxPos[1]:
				path = activeCtrl['path']
				index = activeCtrl['index']
				data = self._data[index]['data']
				pos = MathUtils.TupleSub(touchPos, minPos)
				self._onItemClickCall(path, ctrl, index, data, {
					'pos': pos,
					'touchPos': touchPos
				})
				return
