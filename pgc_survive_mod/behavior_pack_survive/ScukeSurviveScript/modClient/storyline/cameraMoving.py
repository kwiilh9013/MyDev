# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLine

import mod.client.extraClientApi as clientApi

CompFactory = clientApi.GetEngineCompFactory()

class CameraMovingLine(StoryLine):
	__env__ = StoryLineEnvEnum.Client

	def __init__(self, system, playerId, config, data):
		super(CameraMovingLine, self).__init__(system, playerId, config, data)
		self._playerId = clientApi.GetLocalPlayerId()
		self._cameraComp = CompFactory.CreateCamera(self._playerId)

		self._pos = self.GetConfigValue('pos')
		self._rot = self.GetConfigValue('rot')
		self._posTotal, self._posSplinesDis = MathUtils.CubicSplinePrepare(self._pos, MathUtils.CubicPosTupleDis)

		self._curFov = self._cameraComp.GetFov()
		self._curAnchor = self._cameraComp.GetCameraAnchor()
		self._curOffset = self._cameraComp.GetCameraOffset()
		self._curRot = self._cameraComp.GetCameraRotation()
		self._fov = config.get('fov', self._curFov)
		stayTime = self.GetConfigValue('stayTime') * 1000
		if stayTime is not None:
			self._endTime += stayTime

	def GetCameraPos(self, t):
		ret = MathUtils.CubicSplineInterpolation(self._pos, t, self._posTotal, self._posSplinesDis)
		if self.mPosTransformer:
			ret = self.mPosTransformer.GetPos(ret)
		return ret

	def GetCameraRot(self, t):
		ret = MathUtils.CubicSplineInterpolation(self._rot, t, self._posTotal, self._posSplinesDis)
		if self.mPosTransformer:
			ret = self.mPosTransformer.GetRot(ret)
		return ret

	def OnBegin(self):
		self._cameraComp.SetFov(self._fov)

	def OnUpdate(self, curTime, percent):
		pos = self.GetCameraPos(percent)
		rot = self.GetCameraRot(percent)
		self._cameraComp.LockCamera(pos, (rot[0], rot[1]))

	def OnEnd(self):
		self._cameraComp.UnLockCamera()
		self._cameraComp.SetFov(self._curFov)
		self._cameraComp.SetCameraAnchor(self._curAnchor)
		self._cameraComp.SetCameraOffset(self._curOffset)
		self._cameraComp.SetCameraRotation(self._curRot)

