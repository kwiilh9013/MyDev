# -*- coding: utf-8 -*-
import math
import time
import random
from ..ScukeCore.client.system.BaseClientSystem import BaseClientSystem
import mod.client.extraClientApi as clientApi
from ..ScukeCore.utils.mathUtils import MathUtils
from ..modCommon.handler.tweenHandler import TweenHandler

PI = math.pi

class CameraEffectAnchor(object):
	def __init__(self, cameraHandler, obj):
		self.mCameraHandler = cameraHandler
		self._obj = obj
		self.mDeltaAnchor = (0.0, 0.0, 0.0)

	def OnUpdate(self):
		pass

	@property
	def Completed(self):
		return True

	@property
	def Obj(self):
		return self._obj

class CameraShakingAnchor(CameraEffectAnchor):
	def __init__(self, cameraHandler, obj, amplitude, duration):
		super(CameraShakingAnchor, self).__init__(cameraHandler, obj)
		dt = 2 * PI
		n0 = int(duration * 5)
		n1 = int(n0 * 1.5)
		xK = (random.randint(n0, n1), random.randint(0, 2))
		yK = (random.randint(n0, n1), random.randint(0, 2))
		zK = (random.randint(n0, n1), random.randint(0, 2))

		self._amplitude = amplitude
		def _updater_(ctx, xK, yK, zK):
			def _update_(value):
				x = math.sin(xK[0] * (value * dt) + xK[1] * PI)
				y = math.sin(yK[0] * (value * dt) + yK[1] * PI)
				z = math.sin(zK[0] * (value * dt) + zK[1] * PI)
				k = 1.0 - value
				cur = MathUtils.TupleMul((x,y,z), k*k*k*amplitude)
				delta = MathUtils.TupleSub(cur, ctx.mDeltaAnchor)
				ctx.mCameraHandler.ApplyDeltaAnchor(delta)
				ctx.mDeltaAnchor = cur
			return _update_
		self._tween = TweenHandler('easeOutQuad', duration, 0.0, 1.0, _updater_(self, xK, yK, zK))

	def OnUpdate(self):
		self._tween.Update()

	@property
	def Completed(self):
		return self._tween.Completed


class CameraEffectClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(CameraEffectClientSystem, self).__init__(namespace, systemName)
		self._cameraFrameShakingAmplitude = 0
		self._cameraShakingAmplitude = 0
		self._cameraShakingStart = 0.0
		self._cameraShaking = (0.0, 0.0, 0.0)

		self._cameraEffectAnchor = (0.0, 0.0, 0.0)
		self._cameraEffects = []

		self._cameraModifiedAnchor = (0.0, 0.0, 0.0)
		self._cameraAnchor = (0.0, 0.0, 0.0)

		n0 = int(1.0 * 5)
		n1 = int(n0 * 1.5)
		self._shakingXK = (random.randint(n0, n1), random.randint(0, 2))
		self._shakingYK = (random.randint(n0, n1), random.randint(0, 2))
		self._shakingZK = (random.randint(n0, n1), random.randint(0, 2))

		self._cameraComp = clientApi.GetEngineCompFactory().CreateCamera(self.mPlayerId)
		self._viewComp = clientApi.GetEngineCompFactory().CreatePlayerView(self.mPlayerId)

		self._anchorContext = []

	def Destroy(self):
		return super(CameraEffectClientSystem, self).Destroy()

	def SetCameraShaking(self, amplitude):
		self._cameraFrameShakingAmplitude += amplitude

	def EmitCameraShaking(self, obj, amplitude, duration):
		self._cameraEffects.append(CameraShakingAnchor(self, obj, amplitude, duration))

	def StopEmitedCameraShaking(self, obj):
		ret = None
		for item in self._cameraEffects:
			if item.Obj == obj:
				ret = item
				break
		if ret is None:
			return
		self._cameraEffects.remove(ret)
		self.RevertAnchor(ret.mDeltaAnchor)

	def UpdateCameraEffect(self):
		curAnchor = self._cameraComp.GetCameraAnchor()
		anchorChanged = MathUtils.TupleSub(curAnchor, self._cameraAnchor)
		if MathUtils.TupleLength(anchorChanged) > 0.01:
			# 被其他地方修改过了，清空累计值
			self._cameraModifiedAnchor = (0.0, 0.0, 0.0)
		# Global Shaking
		curAmplitude = self._cameraShakingAmplitude
		last = self._cameraShaking
		if curAmplitude > 0 or last[0] > 0 or last[1] > 0 or last[2] > 0:
			dt = 2 * PI
			xK = self._shakingXK
			yK = self._shakingYK
			zK = self._shakingZK

			deltaTime = time.time() - self._cameraShakingStart
			x = math.sin(xK[0] * (deltaTime * dt) + xK[1] * PI)
			y = math.sin(yK[0] * (deltaTime * dt) + yK[1] * PI)
			z = math.sin(zK[0] * (deltaTime * dt) + zK[1] * PI)
			self._cameraShaking = MathUtils.TupleMul((x, y, z), curAmplitude)
		cur = self._cameraShaking
		deltaShaking = MathUtils.TupleSub(cur, last)
		# Effect
		self._cameraEffectAnchor = (0.0, 0.0, 0.0)
		i = 0
		while i < len(self._cameraEffects):
			effect = self._cameraEffects[i]
			effect.OnUpdate()
			if effect.Completed:
				self.ApplyDeltaAnchor(MathUtils.TupleMul(effect.mDeltaAnchor, -1.0))
				self._cameraEffects.pop(i)
			else:
				i += 1
		deltaEffectAnchor = self._cameraEffectAnchor

		deltaAnchor = MathUtils.TupleAdd(deltaShaking, deltaEffectAnchor)
		if deltaAnchor[0] != 0 or deltaAnchor[1] != 0 or deltaAnchor[2] != 0:
			self._cameraModifiedAnchor = MathUtils.TupleAdd(self._cameraModifiedAnchor, deltaAnchor)
			curAnchor = self._cameraComp.GetCameraAnchor()
			curAnchor = MathUtils.TupleAdd(curAnchor, deltaAnchor)
			self._cameraComp.SetCameraAnchor(curAnchor)
		self._cameraAnchor = self._cameraComp.GetCameraAnchor()


	def Update(self):
		if self._cameraShakingAmplitude * self._cameraFrameShakingAmplitude == 0:
			self._cameraShakingStart = time.time()
			leftShaking = self._cameraModifiedAnchor
			if leftShaking[0] != 0 or leftShaking[1] != 0 or leftShaking[2] != 0:
				curAnchor = self._cameraComp.GetCameraAnchor()
				curAnchor = MathUtils.TupleSub(curAnchor, leftShaking)
				self._cameraComp.SetCameraAnchor(curAnchor)
				self._cameraModifiedAnchor = (0.0, 0.0, 0.0)
		self._cameraShakingAmplitude = self._cameraFrameShakingAmplitude
		self._cameraFrameShakingAmplitude = 0

		self.UpdateCameraEffect()

	def ApplyDeltaAnchor(self, deltaAnchor):
		self._cameraEffectAnchor = MathUtils.TupleAdd(self._cameraEffectAnchor, deltaAnchor)

	def RevertAnchor(self, deltaAnchor):
		self._cameraModifiedAnchor = MathUtils.TupleSub(self._cameraModifiedAnchor, deltaAnchor)
		curAnchor = MathUtils.TupleSub(self._cameraComp.GetCameraAnchor(), deltaAnchor)
		ret = self._cameraComp.SetCameraAnchor(curAnchor)
		self._cameraAnchor = self._cameraComp.GetCameraAnchor()

	def PushCameraAnchorContext(self, context):
		if context is None:
			return
		self._anchorContext.append(context)

	def PopCameraAnchorContext(self, context):
		if context is None:
			return
		self._anchorContext.remove(context)

	def SetCameraAnchor(self, anchor, context=None):
		curContext = None if len(self._anchorContext) == 0 else self._anchorContext[-1]
		if curContext != context:
			return False
		curAnchor = MathUtils.TupleSub(anchor, self._cameraModifiedAnchor)
		ret = self._cameraComp.SetCameraAnchor(curAnchor)
		self._cameraAnchor = self._cameraComp.GetCameraAnchor()
		return ret

	def GetCameraAnchor(self):
		curAnchor = self._cameraComp.GetCameraAnchor()
		return MathUtils.TupleSub(curAnchor, self._cameraModifiedAnchor)

	def SetCameraOffset(self, offset):
		return self._cameraComp.SetCameraOffset(offset)

	def GetCameraOffset(self):
		return self._cameraComp.GetCameraOffset()

