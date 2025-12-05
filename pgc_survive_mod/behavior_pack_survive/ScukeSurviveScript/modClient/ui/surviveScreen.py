# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler

BlendTimeStep = 0.03

class SurviveScreen(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(SurviveScreen, self).__init__(namespace, name, param)
		self._screenTextureTween = None
		# 记录控件和动画的关系，用于避免重复设置
		self._uiObjAnimDict = {}
		pass

	def Destroy(self):
		super(SurviveScreen, self).Destroy()
		# 取消订阅
		Instance.mEventMgr.UnRegisterEvent(eventConfig.FullScreenUIEvent, self.FullScreenUIEvent)

	def Update(self):
		if not self.Inited:
			return
		if self._screenTextureTween:
			self._screenTextureTween.Update()

	def Create(self):
		super(SurviveScreen, self).Create()
		self._Texture = self.GetBaseUIControl('/Texture').asImage()
		self._Texture.SetSprite('')
		self._Texture.SetAlpha(0)
		self._Texture.SetVisible(True)
		self._curTexture = None
		self._curAlpha = 0.0

		# 黑屏UI
		self._blackImg = self.GetBaseUIControl("/img_black").asImage()

		# 全屏按钮，用于遮挡自定义UI的按钮响应
		self._screenTopBtn = self.GetBaseUIControl("/btn_top")

		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.FullScreenUIEvent, self.FullScreenUIEvent)


	def SetTexture(self, texture, alpha, blendTime=0):
		if blendTime > 0:
			if len(texture) > 0:
				self._Texture.SetSprite(texture)
			self._screenTextureTween = TweenHandler('linear', blendTime, self._curAlpha, alpha, self._BlendAlpha, self._BlendAlphaEnd)
		else:
			self._Texture.SetSprite(texture)
			self._curAlpha = alpha
			self._screenTextureTween = None
		self._Texture.SetAlpha(self._curAlpha)

	def _BlendAlpha(self, value):
		self._curAlpha = value
		self._Texture.SetAlpha(self._curAlpha)

	def _BlendAlphaEnd(self):
		self._screenTextureTween = None

	def FullScreenUIEvent(self, args):
		"""订阅 全屏UI事件"""
		stage = args.get("stage")
		if stage == "black":
			# 黑屏UI
			self._SetFullBlackUI(args)
		elif stage == "ui_response":
			self._SetUIResponse(args)
		pass

	def _SetFullBlackUI(self, args):
		"""设置全屏黑色UI"""
		# 黑屏UI
		clientApiMgr.SetUIVisible(self._blackImg, True)
		# 播放动画
		animList = self._uiObjAnimDict.get(self._blackImg, [])
		if not animList or args.get("animName") not in animList:
			self._blackImg.SetAnimation(args.get("propertyName"), args.get("namespace"), args.get("animName"), args.get("autoPlay", True))
			animList.append(args.get("animName"))
			self._uiObjAnimDict[self._blackImg] = animList
		else:
			# 动画播放完、再次播放前，需要停止一次，否则不会从头开始播放
			self._blackImg.StopAnimation(args.get("propertyName"))
			self._blackImg.PlayAnimation(args.get("propertyName"))
		pass

	def _SetUIResponse(self, args):
		"""设置自定义UI是否响应, 默认响应"""
		state = args.get("state", True)
		self._screenTopBtn.SetVisible(state)
		pass
