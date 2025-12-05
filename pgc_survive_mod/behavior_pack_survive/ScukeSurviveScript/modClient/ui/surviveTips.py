# -*- coding: utf-8 -*-
import time

from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modCommon import modConfig, eventConfig
import ScukeSurviveScript.ScukeCore.client.engineApiGac as engineApiGac
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler, TweenList, DelayTween


class SurviveTips(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(SurviveTips, self).__init__(namespace, name, param)
		Instance.mEventMgr.RegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameTick)
		self._itemRender = None

	def Create(self):
		super(SurviveTips, self).Create()

		self._TipsLabel = self.GetBaseUIControl('/Tips_Label').asLabel()
		self._TipsLabel.SetVisible(False)
		self._TipsTimer = None

		self._snackBar = self.GetBaseUIControl('/snackbar')
		self._snackBarImage = self.GetBaseUIControl('/snackbar/image').asImage()
		self._snackBarTitle = self.GetBaseUIControl('/snackbar/title').asLabel()
		self._snackBarContent = self.GetBaseUIControl('/snackbar/content').asLabel()
		self._snackBarInitPos = self._snackBar.GetFullPosition('x')
		self._snackBarShowPos = self._snackBarInitPos['absoluteValue']
		self._snackBarHidePos = self._snackBar.GetSize()[0]+5
		self._SetSnackBarPos(self._snackBarHidePos)
		self._snackBarTween = None
		self._snackBarRequestList = []
		self._itemRender = self.GetBaseUIControl("/snackbar/itemRender").asItemRenderer()
		self._itemRender.SetVisible(False)
		self._announceItems = []
		self.InitAnnounce()

	def InitAnnounce(self):
		self._announceItems = []
		curtains = [
			'/announce/curtain0',
			'/announce/curtain1',
			'/announce/curtain2',
			'/announce/curtain3',
		]
		for curtain in curtains:
			ctrlsPath = self.GetAllChildrenPath(curtain)
			children = []
			for p in ctrlsPath:
				children.append(self.GetBaseUIControl(p))
			item = {
				'path': curtain,
				'ctrl': self.GetBaseUIControl(curtain),
				'children': children,
				'tween': None,
			}
			self._announceItems.append(item)

	def ShowTips(self, args):
		if self._TipsTimer:
			engineApiGac.CancelTimer(self._TipsTimer)
		text = args['text']
		duration = args['duration']
		self._TipsLabel.SetText(text)
		self._TipsLabel.SetVisible(True)
		self._TipsTimer = engineApiGac.AddTimer(duration, self.HideTips)

	def HideTips(self):
		if self._TipsTimer:
			engineApiGac.CancelTimer(self._TipsTimer)
			self._TipsTimer = None
		self._TipsLabel.SetVisible(False)


	def ShowSnackBar(self, args):
		self._snackBarRequestList.append({
			'dir': 1,
			'time': 0,
			'data': args
		})

	def DoSnackBarTween(self):
		top = self._snackBarRequestList[0]
		showPos = self._snackBarShowPos
		hidePos = self._snackBarHidePos
		if top['dir'] == 1 and top['time'] == 0:
			data = top['data']
			if "type" in data and data['type'] == 'item':
				self._itemRender.SetVisible(True)
				self._itemRender.SetUiItem(data['name'], 0, False)
				self._snackBarImage.SetVisible(False)
			else:
				self._snackBarImage.SetVisible(True)
				self._itemRender.SetVisible(False)
			self._snackBarImage.SetSprite(data['icon'])
			self._snackBarTitle.SetText(data['title'])
			self._snackBarContent.SetText(data['content'])
			self._snackBarTween = TweenHandler('easeOutQuad', 0.3, hidePos, showPos, self.SnackBarTweenUpdate, self.SnackBarTweenEnd)
			return True
		elif top['dir'] == -1 and top['time'] > 0:
			self._snackBarTween = TweenHandler('easeOutQuad', 0.3, showPos, hidePos, self.SnackBarTweenUpdate, self.SnackBarTweenEnd)
			return True
		return False

	def SnackBarTweenUpdate(self, value):
		self._SetSnackBarPos(value)

	def _SetSnackBarPos(self, value):
		self._snackBar.SetFullPosition('x', {'absoluteValue': value, 'followType': 'none', 'relativeValue': 0.0})

	def SnackBarTweenEnd(self):
		self._snackBarTween = None
		top = self._snackBarRequestList[0]
		if top['dir'] == 1:
			top['time'] = time.time()
		else:
			top['time'] = -1
		top['dir'] = -top['dir']

	def ShowAnnounce(self, configs):
		i = 0
		n = min(len(self._announceItems), len(configs))
		while i < n:
			config = configs[i]
			if config:
				item = self._announceItems[i]
				def _ActiveWrap(_item, active):
					return lambda: self._SetCurtainActive(_item, active)
				def _UpdateWrap(_item):
					return lambda value: self._UpdateCurtainTween(_item, value)
				item['tween'] = TweenList([
					DelayTween(config['offset'], _ActiveWrap(item, True)),
					TweenHandler('linear', config['fadein'], 0, 1, _UpdateWrap(item)),
					DelayTween(config['keep']),
					TweenHandler('linear', config['fadeout'], 1, 0, _UpdateWrap(item), _ActiveWrap(item, False))
				])
			i += 1

	def _SetCurtainActive(self, item, active):
		ctrl = item['ctrl']
		ctrl.SetVisible(active)
		self._UpdateCurtainTween(item, 0)
		if not active:
			item['tween'] = None

	def _UpdateCurtainTween(self, item, value):
		children = item['children']
		for child in children:
			child.SetAlpha(value)

	def OnGameTick(self, args):
		if self.Inited:
			if self._snackBarTween:
				self._snackBarTween.Update()
			elif len(self._snackBarRequestList) > 0:
				top = self._snackBarRequestList[0]
				duration = top['data']['duration']
				curTime = time.time()
				if top['time'] >= 0:
					if curTime - top['time'] >= duration:
						self.DoSnackBarTween()
				else:
					self._snackBarRequestList.pop(0)
			for item in self._announceItems:
				if item['tween']:
					item['tween'].Update()

	def Destroy(self):
		super(SurviveTips, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameTick)
