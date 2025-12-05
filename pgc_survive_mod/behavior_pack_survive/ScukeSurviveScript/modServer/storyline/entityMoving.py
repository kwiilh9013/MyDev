# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLine
import mod.server.extraServerApi as serverApi

class EntityMovingLine(StoryLine):
	__env__ = StoryLineEnvEnum.Server

	def __init__(self, system, playerId, config, data):
		super(EntityMovingLine, self).__init__(system, playerId, config, data)
		self._targets = self.GetConfigValue('targets')
		self._pos = self.GetConfigValue('pos')
		self._posTotal, self._posSplinesDis = MathUtils.CubicSplinePrepare(self._pos, MathUtils.CubicPosTupleDis)

		self._rot = self.GetConfigValue('rot')
		self._entityComps = {}
		for eid in self._targets:
			item = {
				'posComp': serverApi.GetEngineCompFactory().CreatePos(eid),
				'rotComp': serverApi.GetEngineCompFactory().CreateRot(eid),
			}
			self._entityComps[eid] = item

	def OnUpdate(self, curTime, percent):
		pos = self.GetEntityPos(percent)
		rot = self.GetEntityRot(percent)
		for item in self._entityComps.itervalues():
			item['posComp'].SetPos(pos)
			item['rotComp'].SetRot((rot[0], rot[1]))

	def GetEntityPos(self, t):
		ret = MathUtils.CubicSplineInterpolation(self._pos, t, self._posTotal, self._posSplinesDis)
		if self.mPosTransformer:
			ret = self.mPosTransformer.GetPos(ret)
		return ret

	def GetEntityRot(self, t):
		ret = MathUtils.CubicSplineInterpolation(self._rot, t, self._posTotal, self._posSplinesDis)
		if self.mPosTransformer:
			ret = self.mPosTransformer.GetRot(ret)
		return ret
