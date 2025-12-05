# -*- coding: utf-8 -*-
import random

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.battleEventEnum import BattleEventEnum

ViewBinder = clientApi.GetViewBinderCls()

class BattleEventUI(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(BattleEventUI, self).__init__(namespace, name, param)

	def Create(self):
		super(BattleEventUI, self).Create()
		# 守护发动机
		self._GbpPanel = self.GetBaseUIControl('/panel/guardPlanetBooster')
		self._GbpPanel.SetVisible(False)
		self._GbpTimerImg = [
			self._GbpPanel.GetChildByPath('/bg/a0').asImage(),
			self._GbpPanel.GetChildByPath('/bg/a1').asImage(),
			self._GbpPanel.GetChildByPath('/bg/a2').asImage(),
		]
		self._GbpShieldBar = self._GbpPanel.GetChildByPath('/bg/shield_bar').asProgressBar()
		self._GbpShieldBarLeft = self._GbpShieldBar.GetChildByPath('/filled_progress_bar').asImage()
		self._GbpShieldBarIcon = self._GbpPanel.GetChildByPath('/bg/shield_bar/icon').asImage()
		self._GbpOutRangeWarning = self._GbpPanel.GetChildByPath('/bg/warning')
		self._GbpOutRangeWarning.SetVisible(False)
		self._GbpOutRangeWarning.StopAnimation()
		self._GbpTargets = None
		self._GbpOutRange = -1

		# 战斗成功
		self._fightingSuccess = self.GetBaseUIControl('/panel/fightSuccess')
		self._fightingSuccess.SetVisible(False)
		self._fightingFail = self.GetBaseUIControl('/panel/fightFail')
		self._fightingFail.SetVisible(False)

		# //////////////////////////////////////
		self._followHudUI = None
		self._registerBattleUIUpdate = {
			BattleEventEnum.GuardPlanetBooster: self.OnGuardPlanetBoosterUpdate
		}
		engineSystemName = clientApi.GetEngineSystemName()
		systemNamespace = clientApi.GetEngineNamespace()
		self.ListenForEvent(modConfig.ServerSystemEnum.BattleEventServerSystem, 'OnBattleEventInfo', self, self.OnBattleEventInfo)
		self.ListenForEvent(modConfig.ServerSystemEnum.BattleEventServerSystem, 'OnGuardPlanetBoosterSuccess', self, self.OnBattleFightingSuccess)
		self.ListenForEvent(modConfig.ServerSystemEnum.BattleEventServerSystem, 'OnGuardPlanetBoosterFail', self, self.OnBattleFightingFail)
		self.ListenForEvent(modConfig.ServerSystemEnum.BuffServerSystem, 'OnEnergySheildInfo', self, self.OnEnergySheildInfo)
		self.ListenForEvent(engineSystemName, 'HealthChangeClientEvent', self, self.HealthChangeClientEvent, systemNamespace)

	def OnBattleEventInfo(self, data):
		if self._followHudUI is None:
			self._followHudUI = Instance.mUIManager.GetUI(UIDef.UI_FollowHud)
		name = data.get('name', '')
		func = self._registerBattleUIUpdate.get(name, None)
		if func:
			func(data)

	def OnEnergySheildInfo(self, data):
		eid = data['eid']
		if self._GbpTargets is not None and eid in self._GbpTargets and self._GbpPanel.GetVisible():
			total = data['total']
			used = data['used']
			left = max(0.0, 1.0-float(used)/total)
			self._GbpShieldBar.SetValue(left)
			self._GbpShieldBarIcon.SetFullPosition('x', {'absoluteValue': self._GbpShieldBar.GetSize()[0]*left})
			self._GbpShieldBarLeft.StopAnimation()
			self._GbpShieldBarLeft.PlayAnimation()
			if self._followHudUI:
				if left >= 0.9:
					self._followHudUI.ShowNpcTalk(eid, {'text': '能量护盾！展开！', 'alwaysShow': True})
				elif 0.7 < left < 0.8:
					self._followHudUI.ShowNpcTalk(eid, {'text': '...能量护盾还可以撑住...', 'alwaysShow': True})
				elif left <= 0.1:
					self._followHudUI.ShowNpcTalk(eid, {'text': '啊啊啊啊！！救命呀！快救救我！！！！！', 'alwaysShow': True})

	def HealthChangeClientEvent(self, args):
		eid = args['entityId']
		if self._GbpTargets is not None and eid in self._GbpTargets and self._GbpPanel.GetVisible():
			fromValue = args['from']
			toValue = args['to']
			if fromValue > toValue:
				self._GbpShieldBarIcon.StopAnimation()
				self._GbpShieldBarIcon.PlayAnimation()

	def SetCountNumber(self, number, ctrls, path, keepZero=True):
		if number > 999:
			number = 999
		_base = 10
		i = 0
		a = number
		while a >= _base:
			b = a % _base
			ctrls[i].SetSprite(path % b)
			a = a / _base
			i += 1
		ctrls[i].SetSprite(path % a)
		j = 0
		while j < len(ctrls):
			active = j <= i
			ctrls[j].SetVisible(keepZero or active)
			if keepZero and not active:
				ctrls[j].SetSprite(path % 0)
			j += 1

	def OnGuardPlanetBoosterUpdate(self, data):
		passedTime = data['passedTime']
		duration = data['duration']
		index = data['phaseIndex']
		active = index >= 0
		lastActive =  self._GbpPanel.GetVisible()
		if lastActive != active:
			self._GbpPanel.SetVisible(active)
			if active:
				self._GbpShieldBar.SetValue(1.0)
				self._GbpShieldBarIcon.SetFullPosition('x', {'absoluteValue': self._GbpShieldBar.GetSize()[0]})
		if active:
			leftTime = max(0, int(duration-passedTime))
			self.SetCountNumber(leftTime, self._GbpTimerImg, 'textures/ui/scuke_survive/numbers/num_a_%d')
			self._GbpTargets = data['data'].get('@entities', None)
			outRange = data.get('outRange', -1)
			if self._GbpOutRange != outRange:
				warning = outRange >= 0
				self._GbpOutRangeWarning.SetVisible(warning)
				self._GbpOutRangeWarning.StopAnimation()
				if warning:
					self._GbpOutRangeWarning.PlayAnimation()
				self._GbpOutRange = outRange
		else:
			if self._GbpTargets is not None:
				for eid in self._GbpTargets:
					self._followHudUI.HideNpcTalk(eid)
			self._GbpTargets = None
			self._GbpOutRange = -1
			self._GbpOutRangeWarning.SetVisible(False)
			self._GbpOutRangeWarning.StopAnimation()

	def OnBattleFightingSuccess(self, data):
		self._fightingSuccess.SetVisible(True)
		engineApiGac.AddTimer(5.0, self._CloseFightingNotify)

	def OnBattleFightingFail(self, data):
		self._fightingFail.SetVisible(True)
		engineApiGac.AddTimer(5.0, self._CloseFightingNotify)

	def _CloseFightingNotify(self):
		self._fightingSuccess.SetVisible(False)
		self._fightingFail.SetVisible(False)
