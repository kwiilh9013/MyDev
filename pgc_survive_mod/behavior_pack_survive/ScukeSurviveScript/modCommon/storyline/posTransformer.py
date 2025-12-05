# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3, Quaternion
from ScukeSurviveScript.modCommon.cfg.buildingPlaceConfig import GetMarkerConfig

class PosTransformer(object):
	def __init__(self, system, playerId, config):
		self._system = system
		self._center = None
		self._rot = 0
		self._pos = None
		tType = config['type']
		if tType == 'building':
			buildingInfo = self._system.GetBuildingInfo(playerId, config['identifier'], config['filter'])
			self._pos = buildingInfo['pos']
			self._rot = buildingInfo['rot']
			self._center = (0, 0, 0)
			markerConfig = GetMarkerConfig(config['identifier'])
			if markerConfig:
				self._center = markerConfig['center']

	def GetPos(self, pos):
		if self._pos:
			pos = MathUtils.TupleSub(pos, self._center)
			pos = MathUtils.RotByFace(pos, self._rot)
			pos = MathUtils.TupleAdd(pos, self._pos)
		return pos

	def GetRot(self, rot):
		ret = Quaternion.Euler(rot[0], rot[1], rot[2])
		angle = self._rot
		offset = Quaternion.AngleAxis(angle, Vector3.Up())
		return (offset * ret).EulerAngles().ToTuple()

	def Destroy(self):
		pass
