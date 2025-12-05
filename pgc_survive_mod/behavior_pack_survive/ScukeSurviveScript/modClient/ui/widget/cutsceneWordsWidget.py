# -*- coding: utf-8 -*-
import time

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget
from ScukeSurviveScript.modCommon.handler.typingHandler import TypingHandler
import mod.client.extraClientApi as clientApi

class CutsceneWordsWidget(PoolableWidget):
	def __init__(self, baseUI, path, itemPath, completedCallback=None):
		super(CutsceneWordsWidget, self).__init__(baseUI, path, '', itemPath)
		self._contentContainer = self.GetBaseUIControl('')
		self._itemContainer = self.GetBaseUIControl(itemPath)
		self._typingTimer = None
		self._lines = []
		self._currentLine = None
		self._lineIndex = -1
		self._completedCallback = completedCallback
		self._audioComp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())

	def SetWordsConfig(self, config):
		lines = config['lines']
		self._lines = []
		for line in lines:
			lType = line['type']
			lText = line['text']
			textHandler = lText
			if lType == 'typing':
				textHandler = TypingHandler(lText)
			item = {
				'speed': line.get('speed', 0.3),
				'text': textHandler,
				'showText': '',
				'endText': '',
				'align': line.get('align', 'center'),
				'duration': line.get('duration', 0),
				'time': 0,
			}
			self._lines.append(item)
		while len(self._itemCtrlActive) < len(self._lines):
			index = len(self._itemCtrlActive)
			item = self.AddItemCtrl()
			item['index'] = index
		for item in self._itemCtrlActive:
			item['ctrl'].SetVisible(False)
		self._itemContainer.SetVisible(False)

	def Reset(self):
		self._StopTimer()
		self._currentLine = None
		self._lineIndex = -1
		for item in self._itemCtrlActive:
			item['ctrl'].SetVisible(False)

	def _NextLine(self):
		self._lineIndex += 1
		if self._lineIndex < len(self._lines):
			self._currentLine = self._lines[self._lineIndex]
			item = self.GetActiveItemCtrl(self._lineIndex)
			ctrl = item['ctrl']
			label = ctrl.asLabel()
			label.SetText('')
			label.SetTextAlignment(self._currentLine['align'])
			label.SetVisible(True)
			self._audioComp.PlayCustomMusic('scuke_survive.cutscene.typing', entityId=clientApi.GetLocalPlayerId())
		else:
			self._lineIndex = -1
			if self._completedCallback:
				self._completedCallback()
		self._StopTimer()

	def Play(self):
		if self._currentLine is None and self._lineIndex < 0:
			self._NextLine()
		if self._typingTimer is None:
			self._typingTimer = engineApiGac.AddRepeatedTimer(self._currentLine['speed'], self._UpdateLine)

	def Pause(self):
		self._StopTimer()

	def Restart(self):
		self.Reset()
		self.Play()

	def _UpdateLine(self):
		if self._lineIndex < 0:
			return
		item = self.GetActiveItemCtrl(self._lineIndex)
		lineData = self._currentLine
		ctrl = item['ctrl']
		label = ctrl.asLabel()
		textHandler = lineData['text']
		textHandlerType = type(textHandler)
		if lineData['time'] <= 0:
			ended = False
			if textHandlerType is str:
				lineData['showText'] = textHandler
				ended = True
			elif textHandlerType is TypingHandler:
				prevText = textHandler.Current
				if textHandler.Next() is not None:
					lineData['showText'] = textHandler.Current
				else:
					ended = True
				if prevText == textHandler.Current:
					if lineData['endText'] == '▍':
						lineData['endText'] = ' '
					else:
						lineData['endText'] = '▍'
				else:
					self._audioComp.PlayCustomMusic('scuke_survive.cutscene.typing', entityId=clientApi.GetLocalPlayerId())
					lineData['endText'] = '▍'
			label.SetText(lineData['showText']+lineData['endText'])
			if ended:
				lineData['time'] = time.time()
		elif time.time() - lineData['time'] > 0:
			if textHandlerType is TypingHandler:
				lineData['endText'] = ' '
				label.SetText(lineData['showText'] + lineData['endText'])
			self._NextLine()
			self.Play()


	def _StopTimer(self):
		if self._typingTimer:
			engineApiGac.CancelTimer(self._typingTimer)
		self._typingTimer = None

	@property
	def Completed(self):
		return self._lineIndex < 0

	def Destroy(self):
		super(CutsceneWordsWidget, self).Destroy()
		self._StopTimer()
