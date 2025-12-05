# -*- coding: utf-8 -*-
import math
import time
import random
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.eventConfig import CameraShakingSubscribeEvent
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler
from ScukeSurviveScript.cameraEffect import cameraEffectConfig

class CameraClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(CameraClientSystem, self).__init__(namespace, systemName)
		self._cameraEffectSys = clientApi.GetSystem(cameraEffectConfig.SystemNameSpace, cameraEffectConfig.SystemName)

		Instance.mEventMgr.RegisterEvent(CameraShakingSubscribeEvent, self.CameraShakingSubscribeEvent)

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(CameraShakingSubscribeEvent, self.CameraShakingSubscribeEvent)
		return super(CameraClientSystem, self).Destroy()

	def SetCameraShaking(self, amplitude):
		if self._cameraEffectSys is None:
			return
		self._cameraEffectSys.SetCameraShaking(amplitude)

	def EmitCameraShaking(self, amplitude, duration):
		if self._cameraEffectSys is None:
			return
		self._cameraEffectSys.EmitCameraShaking(self, amplitude, duration)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def ChangeCameraAnchor(self, args):
		applyAnchor = args['anchor']
		if self._cameraEffectSys is None:
			return
		self._cameraEffectSys.SetCameraAnchor(applyAnchor)

	def CameraShakingSubscribeEvent(self, args):
		"""订阅 镜头抖动事件"""
		self.EmitCameraShaking(args['amplitude'], args['duration'])
		pass
