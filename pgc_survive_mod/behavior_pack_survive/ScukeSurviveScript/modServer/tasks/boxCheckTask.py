# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils

def _BuildBoxedPosList(s):
	map = []
	r = range(-s, s + 1)
	for i in r:
		for j in r:
			for k in r:
				pos = (i, j, k)
				layer = max(abs(i), abs(j), abs(k))
				while len(map) <= layer:
					map.append([])
				map[layer].append(pos)
	return map


BoxedPosListMap = _BuildBoxedPosList(8)


class BoxCheckTask(object):
	def __init__(self, eid, filterCall, completedCall):
		self._boxCheckPoint = (0, 0, 0)
		self._boxCheckStep = 0
		self._boxCheckResult = []
		self._boxCheckCallInstance = None
		self._boxCheckCenter = (0, 0, 0)
		self._boxCheckDim = 0
		self._eid = eid
		self._boxCheckFilter = filterCall
		self._boxCheckCompleted = completedCall

	def Start(self, dim, pos, radius, step):
		total = 0
		i = 0
		while i <= radius:
			total += len(BoxedPosListMap[i])
			i += 1
		self._boxCheckPoint = (0, 0, total)
		self._boxCheckStep = step
		self._boxCheckResult = []
		self._boxCheckCenter = MathUtils.TupleFloor2Int(pos)
		self._boxCheckDim = dim

	def Tick(self):
		l = self._boxCheckPoint[0]
		start = self._boxCheckPoint[1]
		remain = self._boxCheckPoint[2]
		if remain <= 0:
			return
		checkRemain = min(self._boxCheckStep, remain)
		checkTotal = checkRemain
		filterCall = self._boxCheckFilter
		completedCall = self._boxCheckCompleted
		for i in range(l, len(BoxedPosListMap)):
			l = i
			layer = BoxedPosListMap[i]
			for j in range(start, len(layer)):
				p = layer[j]
				pos = (self._boxCheckCenter[0]+p[0], self._boxCheckCenter[1]+p[1], self._boxCheckCenter[2]+p[2])
				block = engineApiGas.GetBlock(pos, self._boxCheckDim)
				if block['name'] != 'minecraft:air' and filterCall(pos, block):
					self._boxCheckResult.append({
						'pos': pos,
						'block': block
					})
				checkRemain -= 1
				if checkRemain == 0:
					total = remain - checkTotal
					self._boxCheckPoint = (l, j, total)
					if total == 0:
						completedCall(self._eid, self._boxCheckResult)
					return
			start = 0
			self._boxCheckPoint = (l, start, remain - checkTotal)
