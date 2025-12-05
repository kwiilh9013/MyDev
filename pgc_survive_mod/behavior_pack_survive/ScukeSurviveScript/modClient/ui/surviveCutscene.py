# -*- coding: utf-8 -*-
import time
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.widget.cutsceneWordsWidget import CutsceneWordsWidget
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler, TweenList
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()


class SurviveCutscene(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(SurviveCutscene, self).__init__(namespace, name, param)
		self._cutsceneConfig = param
		self._wakeUpTween = None
		self._movieScaleTween = None
		self._movieMoveYTween = None
		self._movieMoveXTween = None
		self._movieFadeTween = None
		self._cutsceneCompleted = False
		self._cutsceneQueen = []
		self._completedCallback = None
		self._playedMusic = None
		self._playedSounds = []
		self._audioComp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())
		# 长按跳过按钮时间计时器ID
		self._skipBtnStateTimer = None
		# 检测是否长按时间
		self._skipBtnPressTime = 3.0
		# 自动切换下一章timer，用于跳过时取消，放置画面连续跳转
		self._autoInNextMovieCutsceneTimer = None
		# 记录上一个场景的音频文字timer列表，用于跳过进入下一个场景时候取消计时器
		self._lastTimer = None
		# 跳过按钮被长按时为True
		self._isPressSkipBtn = False
		self._updateTime = 0

	def Create(self):
		super(SurviveCutscene, self).Create()
		self._cutsceneItems = {
			'movie': {'ctrl': self.GetBaseUIControl('/movie'), 'init': self.SetMovie},
			'words': {'ctrl': self.GetBaseUIControl('/words'), 'init': self.SetWords},
			'wakeup': {'ctrl': self.GetBaseUIControl('/wakeup'), 'init': self.SetWakeup},
		}
		self._wakeUp0 = self.GetBaseUIControl('/wakeup/up')
		self._wakeUp1 = self.GetBaseUIControl('/wakeup/down')
		self._movieText = self.GetBaseUIControl('/movie/text/movieText').asLabel()
		self._movieText2 = self.GetBaseUIControl('/movie/text/movieText2').asLabel()
		self._movieImage = self.GetBaseUIControl('/movie/content/movieImage').asImage()
		self._movieLogo = self.GetBaseUIControl('/movie/content/logo').asImage()
		self._skipProgressBar = self.GetBaseUIControl('/movie/skip_progress_bar').asProgressBar()

		# 剧情跳过按钮
		self._skipBtn = self.GetBaseUIControl('/movie/skip_btn').asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._skipBtn, self.OnSkipButtonDown,self.OnSkipButtonUp)

		self._storyStageSystem = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.StoryStageClientSystem)

		self.InitCutscenes()


	def PushCutscene(self, config):
		self._cutsceneQueen.append(config)

	def InitCutscenes(self):
		engineApiGac.AddTimer(2,clientApiMgr.SetUIVisible(self._skipBtn,True))
		self._cutsceneCompleted = False
		cType = self._cutsceneConfig['type']
		for key, item in self._cutsceneItems.iteritems():
			panel = item['ctrl']
			active = key == cType
			panel.SetVisible(active)
			if active:
				if 'playMusic' in self._cutsceneConfig:
					self.SetMusic(self._cutsceneConfig['playMusic'])
				item['init'](item)
		if self._storyStageSystem:
			self._storyStageSystem.NotifyToServer('PlayerInCutscene', {'playerId': clientApi.GetLocalPlayerId()})

	def SetMusic(self, musicName):
		if self._playedMusic is not None:
			self._audioComp.StopCustomMusicById(self._playedMusic, 0.5)
		if musicName is not None:
			self._audioComp.DisableOriginMusic(True)
			self._playedMusic = self._audioComp.PlayCustomMusic(musicName, entityId=clientApi.GetLocalPlayerId())
		else:
			self._audioComp.DisableOriginMusic(False)
			self._playedMusic = None

	def PlaySound(self, soundName):
		mid = self._audioComp.PlayCustomMusic(soundName, entityId=clientApi.GetLocalPlayerId())
		self._playedSounds.append(mid)

	def SetMovie(self, item):
		texture = self._cutsceneConfig.get('texture', '')
		self._movieImage.SetSprite(texture)
		self._movieText.SetText('')
		self._movieText2.SetText('')
		self._movieLogo.SetVisible(False)
		scale = self._cutsceneConfig.get('scale', 100)
		sizeY = self._cutsceneConfig.get('sizeY', 47)
		self._movieImage.SetFullSize('y', {'followType': 'x', 'relativeValue': sizeY / 100.0})
		moveY = self._cutsceneConfig.get('moveY', 0)
		moveX = self._cutsceneConfig.get('moveX', 0)
		if type(scale) is tuple:
			self._UpdateMovieTexture(scale[0])
		else:
			self._UpdateMovieTexture(scale)
		if type(moveY) is tuple:
			self._UpdateMovieTextureMoveY(moveY[0])
		else:
			self._UpdateMovieTextureMoveY(moveY)
		if type(moveX) is tuple:
			self._UpdateMovieTextureMoveX(moveX[0])
		else:
			self._UpdateMovieTextureMoveX(moveX)
		delay = self._cutsceneConfig.get('fadein', 0)
		engineApiGac.AddTimer(delay, self.__SetMovie, item)
		self._movieFadeTween = TweenHandler('linear', delay, 0, 1, self._UpdateMovieFade)

	def __SetMovie(self, item):
		duration = self._cutsceneConfig.get('duration', 0.5)
		scale = self._cutsceneConfig.get('scale', 100)
		moveY = self._cutsceneConfig.get('moveY', 0)
		moveX = self._cutsceneConfig.get('moveX', 0)
		textData = self._cutsceneConfig.get('text', [])
		soundsData = self._cutsceneConfig.get('sounds', [])
		# 清除上一个场景的音频文字timer
		if self._lastTimer:
			for timerId in self._lastTimer:
				engineApiGac.CancelTimer(timerId)
		timers = []
		for item in textData:
			offset = item['offset']
			text = item.get('text', '')
			text2 = item.get('text2', '')
			t = engineApiGac.AddTimer(offset, self._UpdateMovieText, text, text2)
			timers.append(t)
			if item.get('showLogo', False):
				t = engineApiGac.AddTimer(offset, self._ShowMovieLogo)
				timers.append(t)
		for item in soundsData:
			offset = item['offset']
			name = item['name']
			t = engineApiGac.AddTimer(offset, self.PlaySound, name)
			timers.append(t)
		if type(scale) is tuple:
			self._movieScaleTween = TweenHandler('linear', duration, scale[0], scale[1], self._UpdateMovieTexture)
		else:
			self._UpdateMovieTexture(scale)
		if type(moveY) is tuple:
			self._movieMoveYTween = TweenHandler('linear', duration, moveY[0], moveY[1], self._UpdateMovieTextureMoveY)
		else:
			self._UpdateMovieTextureMoveY(moveY)
		if type(moveX) is tuple:
			self._movieMoveXTween = TweenHandler('linear', duration, moveX[0], moveX[1], self._UpdateMovieTextureMoveX)
		else:
			self._UpdateMovieTextureMoveX(moveX)
		# 清除已有跳转下一章的timer，防止跳过章节后再次执行导致顺序错乱
		if self._autoInNextMovieCutsceneTimer:
			engineApiGac.CancelTimer(self._autoInNextMovieCutsceneTimer)
			self._autoInNextMovieCutsceneTimer = None
		self._autoInNextMovieCutsceneTimer = engineApiGac.AddTimer(duration, self.OnMovieCutsceneCompleted)
		item['timers'] = timers
		self._lastTimer = timers

	def OnMovieCutsceneCompleted(self):
		delay = self._cutsceneConfig.get('fadeout', 0)
		self._movieFadeTween = TweenHandler('linear', delay, 1, 0, self._UpdateMovieFade, self._OnRealCutsceneCompleted)

	def _UpdateMovieTexture(self, value):
		self._movieImage.SetFullSize('x', {'followType': 'parent', 'relativeValue': value / 100.0})

	def _UpdateMovieTextureMoveY(self, value):
		self._movieImage.SetFullPosition('y', {'absoluteValue': 0, 'followType': 'parent', 'relativeValue': value/100.0})

	def _UpdateMovieTextureMoveX(self, value):
		self._movieImage.SetFullPosition('x', {'absoluteValue': 0, 'followType': 'parent', 'relativeValue': value/100.0})

	def _UpdateMovieText(self, text, text2):
		self._movieText.SetText(text)
		self._movieText2.SetText(text2)

	def _ShowMovieLogo(self):
		self._movieLogo.SetVisible(True)
		self._movieLogo.StopAnimation()
		self._movieLogo.PlayAnimation()

	def _UpdateMovieFade(self, value):
		self._movieLogo.SetAlpha(value)
		self._movieImage.SetAlpha(value)
		self._movieText.SetAlpha(value)
		self._movieText2.SetAlpha(value)

	def SetWords(self, item):
		wordsWidget = CutsceneWordsWidget(self, '/words/lines', '/label', self.OnCutsceneCompleted)
		item['widget'] = wordsWidget
		wordsWidget.SetWordsConfig(self._cutsceneConfig)
		wordsWidget.Restart()

	def SetWakeup(self, item):
		tweens = [
			TweenHandler('easeInOutQuad', 0.8, 0, 20, self._UpdateWakeup),
			TweenHandler('easeInOutQuad', 0.3, 20, 0, self._UpdateWakeup),
			TweenHandler('easeInOutQuad', 1.5, 0, 50, self._UpdateWakeup),
		]
		item['tween'] = TweenList(tweens, self.OnCutsceneCompleted)
		comp = clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLocalPlayerId())
		comp.SetPerspective(0)
		self._wakeUpTween = item['tween']

	def _UpdateWakeup(self, value):
		self._wakeUp0.SetFullPosition('y', {'followType': 'parent', 'relativeValue': -value / 100.0})
		self._wakeUp1.SetFullPosition('y', {'followType': 'parent', 'relativeValue': value / 100.0})

	def OnCutsceneCompleted(self):
		engineApiGac.AddTimer(self._cutsceneConfig.get('duration', 0.5), self._OnRealCutsceneCompleted)

	def _OnRealCutsceneCompleted(self):
		self._movieLogo.SetVisible(False)
		if self._cutsceneConfig['type'] == 'wakeup':
			comp = clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLocalPlayerId())
			comp.SetPerspective(1)
		self._cutsceneCompleted = True
		# 清除已有的音频和文字timer
		movieTimers = self._cutsceneItems['movie'].get('timers', [])
		for t in movieTimers:
			engineApiGac.CancelTimer(t)
		for mid in self._playedSounds:
			self._audioComp.StopCustomMusicById(mid)
		self._playedSounds = []
		if len(self._cutsceneQueen) > 0:
			self._cutsceneConfig = self._cutsceneQueen.pop(0)
			self.InitCutscenes()
		else:
			if self._playedMusic is not None:
				self._audioComp.StopCustomMusicById(self._playedMusic, 0.2)
			for mid in self._playedSounds:
				self._audioComp.StopCustomMusicById(mid)
			self._playedSounds = []
			self._audioComp.DisableOriginMusic(False)
			Instance.mUIManager.PopUI()
			if self._completedCallback:
				self._completedCallback()

	def Destroy(self):
		super(SurviveCutscene, self).Destroy()
		movieTimers = self._cutsceneItems['movie'].get('timers', [])
		for t in movieTimers:
			engineApiGac.CancelTimer(t)
		# 清除上一个场景的音频文字timer
		if self._lastTimer:
			for timerId in self._lastTimer:
				engineApiGac.CancelTimer(timerId)

	def SetCompletedCallback(self, callback):
		self._completedCallback = callback

	def CutsceneUpdate(self):
		if self._wakeUpTween:
			self._wakeUpTween.Update()
		if self._movieScaleTween:
			self._movieScaleTween.Update()
		if self._movieMoveYTween:
			self._movieMoveYTween.Update()
		if self._movieMoveXTween:
			self._movieMoveXTween.Update()
		if self._movieFadeTween:
			self._movieFadeTween.Update()
		if self._isPressSkipBtn:
			if self._updateTime >= self._skipBtnPressTime*60:
				self._skipProgressBar.SetValue(1)
				self._updateTime = self._skipBtnPressTime*60
			else:
				self._updateTime+=1
				self._skipProgressBar.SetValue(self._updateTime/(self._skipBtnPressTime*60.0))
			

	@ViewBinder.binding(ViewBinder.BF_BindString, "#main.gametick")
	def OnGameTick(self):
		self.CutsceneUpdate()

	def OnSkipButtonDown(self,args):
		"""跳过剧情按钮按下时"""
		self._skipBtnStateTimer = engineApiGac.AddTimer(self._skipBtnPressTime,self.LongPressSkipBtn)
		clientApiMgr.SetUIVisible(self._skipProgressBar,True)
		self._updateTime = 0
		self._isPressSkipBtn = True
	def OnSkipButtonUp(self,args):
		"""跳过剧情按钮抬起时"""
		self._isPressSkipBtn = False
		clientApiMgr.SetUIVisible(self._skipProgressBar,False)
		if self._skipBtnStateTimer:
			engineApiGac.CancelTimer(self._skipBtnStateTimer),'CancelTimer'
			self._skipBtnStateTimer = None
			self._OnRealCutsceneCompleted()
	def LongPressSkipBtn(self):
		"""长按后触发全跳过"""
		self._cutsceneQueen = []
		self._OnRealCutsceneCompleted()
		