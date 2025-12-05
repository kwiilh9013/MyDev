# -*- coding: utf-8 -*-
import math
import time

import mod.client.extraClientApi as extraClientApi

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon.defines.phaseTagEnum import PhaseTagEnum
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler, TweenList
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import eventConfig

TempRangeNormalIndex = 3
TempRange = [
	(-16, -8),
	(-8, -4),
	(-4, 0),
	(0, 2),
	(2, 6),
	(6, 10),
	(10, 14),
]
ColdColor = (0.25, 0.68, 1.0)
HealthColor = (0.33, 1.0, 0.0)
HeatColor = (1.0, 0.17, 0.0)

TempRangeColor = [
	ColdColor,
	ColdColor,
	ColdColor,
	HealthColor,
	HeatColor,
	HeatColor,
	HeatColor,
]
TempRangePointAngle = [
	(0, 18),
	(18, 55),
	(55, 95),
	(95, 135),
]
ColorK = 1.0/255.0

PhaseTagImgs = {
	PhaseTagEnum.Mars: 'textures/ui/scuke_survive/task/img_p_mars',
	PhaseTagEnum.AsteroidBelt: 'textures/ui/scuke_survive/task/img_p_asteroid_belt2',
	PhaseTagEnum.Jupiter: 'textures/ui/scuke_survive/task/img_p_jupiter',
	'_earth_': 'textures/ui/scuke_survive/task/img_p_earth',
}

BaseScreenPath = '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel'


class SurviveHud(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(SurviveHud, self).__init__(namespace, name, param)

	def Create(self):
		super(SurviveHud, self).Create()
		# Debug
		self._enableDebug = engineApiGac.IsDevMode()
		self._DebugPanel = None
		self._DebugAttrText = None
		self._DebugEnvText = None
		if self._enableDebug:
			self._DebugPanel = self.GetBaseUIControl(BaseScreenPath+'/DebugPanel')
			self._DebugAttrText = self.GetBaseUIControl(BaseScreenPath+'/DebugPanel/Attr_Text').asLabel()
			self._DebugEnvText = self.GetBaseUIControl(BaseScreenPath+'/DebugPanel/Env_Text').asLabel()

		# Menu
		self._ButtonMenuArea = ((0,0), (0,0))
		self._buttonMovePos = None
		self._hudPanel = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common')
		self._topLeftPanel = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left')
		self._ButtonMenu = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu').asButton()
		self._ButtonMenuFlash = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu/flash').asImage()
		self._ButtonMenuFlash.StopAnimation()
		self._ButtonMenuFlashHand = self.GetBaseUIControl(
			BaseScreenPath + '/Panel_Common/panel_top_left/Button_Menu/flash/hand').asImage()
		self._ButtonMenuFlashHand.StopAnimation()
		self._ButtonMenu.AddTouchEventParams({"isSwallow": True})
		self._ButtonMenu.SetButtonTouchMoveCallback(self.OnButtonMenuMove)
		self._ButtonMenu.SetButtonTouchUpCallback(self.OnButtonMenuDown)
		self._ButtonMenu.SetButtonTouchCancelCallback(self.OnButtonMenuCancel)

		self._DayCountImgs = [
			self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu/Day_Image/Unit0').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu/Day_Image/Unit1').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu/Day_Image/Unit2').asImage(),
		]
		self._DayPlanetImg = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu/Day_Image/Planet').asImage()
		self._DayPlanetText = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/panel_top_left/Button_Menu/Day_Image/Planet/label').asLabel()
		self._DayCount_Notify_Panel = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify')
		self._DayCount_Notify_Panel.SetVisible(False)
		self._DayCount_Notify_Tags = {
			PhaseTagEnum.Mars: self.BuildImpactNotify(PhaseTagEnum.Mars),
			PhaseTagEnum.AsteroidBelt: self.BuildImpactNotify(PhaseTagEnum.AsteroidBelt),
			PhaseTagEnum.Jupiter: self.BuildImpactNotify(PhaseTagEnum.Jupiter),
			'_earth_': self.BuildImpactNotify('_earth_'),
		}

		self._BloodMoon = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/BloodMoon')
		self._BloodMoonText = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/BloodMoon/BloodMoon_Text').asLabel()
		self._BloodMoon.SetVisible(False)

		self._MeteoriteImpact = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/MeteoriteImpact')
		self._MeteoriteImpactText = self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/MeteoriteImpact/MeteoriteImpact_Text').asLabel()
		self._MeteoriteImpact.SetVisible(False)


		# State
		### TempState
		self._TempStatePoint = self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/p').asImage()
		self._TempStateWarn = self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/warn').asImage()
		self._TempRangeImgs = [
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/l3').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/l2').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/l1').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/n').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/r1').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/r2').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/temp_state/r3').asImage(),
		]
		self._RadiationStateWarn = self.GetBaseUIControl('/StatePanel/env_panel/radiation_state/warn').asImage()
		self._RadiationRangeImgs = [
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/l5').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/l4').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/l3').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/l2').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/l1').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/r1').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/r2').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/r3').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/r4').asImage(),
			self.GetBaseUIControl(BaseScreenPath+'/StatePanel/env_panel/radiation_state/r5').asImage(),
		]
		livingServerSystemName = modConfig.ServerSystemEnum.LivingServerSystem
		self.ListenForEvent(livingServerSystemName, 'OnApplyLivingStateAttr', self, self.OnApplyLivingStateAttr)
		self._tempPointerTween = None
		self._tempWarningTween = None
		self._tempWarnType = 0
		self._radiationWarningTween = None

		self.gunClientSystem = extraClientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.GunClientSystem)

		phaseServerSystemName = modConfig.ServerSystemEnum.PhaseServerSystem
		self.ListenForEvent(phaseServerSystemName, 'OnUpdatePhaseInfo', self, self.OnUpdatePhaseInfo)
		self.ListenForEvent(phaseServerSystemName, 'OnBloodMoonUpdate', self, self.OnBloodMoonUpdate)
		self.ListenForEvent(phaseServerSystemName, 'OnMeteoriteImpactUpdate', self, self.OnMeteoriteImpactUpdate)

		engineSystemName = extraClientApi.GetEngineSystemName()
		systemNamespace = extraClientApi.GetEngineNamespace()
		self.ListenForEvent(engineSystemName, 'OnKeyPressInGame', self, self.OnKeyPress, systemNamespace)

		# 监听订阅，当触发时，隐藏本hud
		Instance.mEventMgr.RegisterEvent(eventConfig.HudShowSubscriptEvent, self.HudShowSubscriptEvent)
		# 初始化位置
		settingClient = extraClientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
		settingClient._settingDict["hudBtnData"]["Button_Menu"]["dfPos"] = self._ButtonMenu.GetPosition()

	def UpdateButtonMenuArea(self):
		fullSize = self.GetBaseUIControl(BaseScreenPath+'').GetSize()
		minPos = (8, 8)
		maxPos = MathUtils.TupleSub(MathUtils.TupleSub(fullSize, self._ButtonMenu.GetSize()), (88, 80))
		self._ButtonMenuArea = (minPos, maxPos)

	def OnKeyPress(self, args):
		KeyBoardType = extraClientApi.GetMinecraftEnum().KeyBoardType
		screenName = args['screenName']
		key = int(args['key'])
		isDown = int(args['isDown']) == 1
		if screenName == "hud_screen" and isDown:
			if key == KeyBoardType.KEY_TAB:
				self.OnButtonMenuDown(None)
			if self._enableDebug and key == KeyBoardType.KEY_F12:
				self._DebugPanel.SetVisible(not self._DebugPanel.GetVisible())

	def BuildImpactNotify(self, tag):
		if tag == '_earth_':
			return {
				'ctrl': self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s' % tag),
				'daysNumA': [
					self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/a0' % tag).asImage(),
					self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/a1' % tag).asImage(),
					self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/a2' % tag).asImage(),
				],
				'daysNumB': [
					self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/b0' % tag).asImage(),
					self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/b1' % tag).asImage(),
					self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/b2' % tag).asImage(),
				]
			}
		return {
			'ctrl': self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s' % tag),
			'daysNumA': [
				self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/a0' % tag).asImage(),
				self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/a1' % tag).asImage(),
			],
			'daysNumB': [
				self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/b0' % tag).asImage(),
				self.GetBaseUIControl(BaseScreenPath+'/Panel_Common/DayNotify/%s/days/b1' % tag).asImage(),
			]
		}

	def HudShowSubscriptEvent(self, args):
		"""显示、隐藏hud"""
		state = args.get("state", False)
		clientApiMgr.SetUIVisible(self._topLeftPanel, state)
		pass

	def SetHudActive(self, active):
		self._hudPanel.SetVisible(active)
		if not active:
			self.CloseNotifyPanel()
			self.CloseAllEvents()

	def OnButtonMenuMove(self, args):
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		btn = self._ButtonMenu
		minPos = self._ButtonMenuArea[0]
		maxPos = self._ButtonMenuArea[1]
		if self._buttonMovePos:
			deltaX = posX - self._buttonMovePos[0]
			deltaY = posY - self._buttonMovePos[1]
			curPos = btn.GetPosition()
			btn.SetPosition((MathUtils.Clamp(curPos[0] + deltaX, minPos[0], maxPos[0]), MathUtils.Clamp(curPos[1] + deltaY, minPos[1], maxPos[1])))
		else:
			self.UpdateButtonMenuArea()
		self._buttonMovePos = (posX, posY)

	def OnButtonMenuDown(self, args):
		notMoving = self._buttonMovePos is None
		if self._buttonMovePos:
			settingClient = extraClientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
			settingClient._settingDict["hudBtnData"]["Button_Menu"]["newPos"] = self._ButtonMenu.GetPosition()
			settingClient.CommitSettingData({'pid': extraClientApi.GetLocalPlayerId(), 'data': settingClient._settingDict})
		self._buttonMovePos = None
		menuUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveMenu)
		if menuUI is not None:
			return
		if notMoving:
			Instance.mUIManager.PushUI(UIDef.UI_SurviveMenu, {"isHud": 0})
			self._ButtonMenuFlash.StopAnimation()
			self._ButtonMenuFlashHand.StopAnimation()
			self._ButtonMenuFlash.SetVisible(False)

	def OnButtonMenuCancel(self, args):
		self._buttonMovePos = None

	def OnButtonTaskDown(self, args):
		Instance.mUIManager.PushUI(UIDef.UI_TasksUI)


	def OnButtonReloadDown(self, args):
		if self.gunClientSystem:
			self.gunClientSystem.Reload()

	def OnUpdatePhaseInfo(self, data):
		days = data['leftDays']
		earthPhase = days == 0
		tag = data['phase'].get('tag', '')
		if data['keyPointPhase']:
			tag = data['keyPointPhase'].get('tag', '')
		if earthPhase:
			tag = '_earth_'
			days = data['days']
			self._DayPlanetText.SetText('漂流天数')
		else:
			self._DayPlanetText.SetText('距离撞击')
		self.SetDayCountNumber(days, self._DayCountImgs, 'textures/ui/scuke_survive/hud/hud_%d', False)
		self._DayPlanetImg.SetSprite(PhaseTagImgs.get(tag, ''))
		for key, item in self._DayCount_Notify_Tags.iteritems():
			active = key == tag
			item['ctrl'].SetVisible(active)
			if active:
				self.SetDayCountNumber(days, item['daysNumA'], 'textures/ui/scuke_survive/numbers/num_a_%d')
				self.SetDayCountNumber(days, item['daysNumB'], 'textures/ui/scuke_survive/numbers/num_b_%d')

		self._DayCount_Notify_Panel.SetVisible(True)
		engineApiGac.AddTimer(5, self.CloseNotifyPanel)

	def SetDayCountNumber(self, number, ctrls, path, keepZero=True):
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

	def CloseAllEvents(self):
		self._BloodMoon.SetVisible(False)
		self._MeteoriteImpact.SetVisible(False)

	def OnBloodMoonUpdate(self, data):
		visible = data['state']
		if visible:
			self.CloseAllEvents()
		if 'desc' in data:
			desc = data['desc']
			self._BloodMoonText.SetText(desc)
		else:
			visible = False
		self._BloodMoon.SetVisible(visible)
		engineApiGac.AddTimer(3, self.CloseBloodMoon)

	def OnMeteoriteImpactUpdate(self, data):
		visible = data['state']
		if visible:
			self.CloseAllEvents()
		if 'desc' in data:
			desc = data['desc']
			self._MeteoriteImpactText.SetText(desc)
		else:
			visible = False
		self._MeteoriteImpact.SetVisible(visible)
		engineApiGac.AddTimer(3, self.CloseMeteoriteImpact)

	def CloseBloodMoon(self):
		self._BloodMoon.SetVisible(False)

	def CloseMeteoriteImpact(self):
		self._MeteoriteImpact.SetVisible(False)

	def CloseNotifyPanel(self):
		self._DayCount_Notify_Panel.SetVisible(False)

	def FlashMenu(self):
		self._ButtonMenuFlash.SetVisible(True)
		self._ButtonMenuFlash.StopAnimation()
		self._ButtonMenuFlash.PlayAnimation()
		self._ButtonMenuFlashHand.StopAnimation()
		self._ButtonMenuFlashHand.PlayAnimation()

	def DebugUpdateAttr(self, info):
		if not self._DebugAttrText:
			return
		debugStr = ''
		for k, v in info.iteritems():
			debugStr += '%s: %s\n' % (k, str(v))
		self._DebugAttrText.SetText(debugStr)

	def DebugUpdateEnv(self, info):
		if not self._DebugEnvText:
			return
		debugStr = ''
		for k, v in info.iteritems():
			debugStr += '%s: %s\n' % (k, str(v))
		self._DebugEnvText.SetText(debugStr)

	def OnApplyLivingStateAttr(self, data):
		tempInfo = data['tempInfo']
		self.UpdateEnvTempState(tempInfo['temp'], tempInfo['heatResistanceTemp'], tempInfo['coldResistanceTemp'])
		self.UpdateEnvRadiationState(tempInfo['radiation'], tempInfo['radiationAbsorption'])

	def UpdateEnvTempState(self, temp, heatResistanceTemp, coldResistanceTemp):
		normalTempRange = TempRange[TempRangeNormalIndex]
		normalColor = TempRangeColor[TempRangeNormalIndex]
		minTemp = normalTempRange[0]
		maxTemp = normalTempRange[1]
		i = TempRangeNormalIndex + 1
		pointAngle = 0
		if minTemp <= temp <= maxTemp:
			pointAngle = TempRangePointAngle[0][1]*(1.0-2.0*float(temp-minTemp)/(maxTemp-minTemp))
		maxTempWithR = maxTemp - heatResistanceTemp
		while 0 <= i < len(TempRange):
			ran = TempRange[i]
			img = self._TempRangeImgs[i]
			if maxTempWithR >= ran[1]:
				img.SetSpriteColor(normalColor)
			else:
				img.SetSpriteColor(TempRangeColor[i])
			safe = img.GetChildByName('safe')
			if ran[0] <= maxTempWithR < ran[1]:
				p = float(maxTempWithR - ran[0]) / (ran[1] - ran[0])
				safe.SetFullSize('x' if i <= TempRangeNormalIndex + 1 else 'y', {'followType': 'parent', 'relativeValue': p})
				safe.SetVisible(True)
			else:
				safe.SetVisible(False)
			pointAngleRange = TempRangePointAngle[abs(i-TempRangeNormalIndex)]
			if ran[0] <= temp < ran[1]:
				deltaAngle = pointAngleRange[1]-pointAngleRange[0]
				p = float(temp - ran[0]) / (ran[1] - ran[0])
				pointAngle = -(pointAngleRange[0] + deltaAngle * p)
			i += 1
		i = TempRangeNormalIndex - 1
		minTempWithR = minTemp - coldResistanceTemp
		while 0 <= i < len(TempRange):
			ran = TempRange[i]
			img = self._TempRangeImgs[i]
			if minTempWithR <= ran[0]:
				img.SetSpriteColor(normalColor)
			else:
				img.SetSpriteColor(TempRangeColor[i])
			safe = img.GetChildByName('safe')
			if ran[0] < minTempWithR <= ran[1]:
				p = float(ran[1] - minTempWithR) / (ran[1] - ran[0])
				safe.SetFullSize('x' if i >= TempRangeNormalIndex-1 else 'y', {'followType': 'parent', 'relativeValue': p})
				safe.SetVisible(True)
			else:
				safe.SetVisible(False)
			pointAngleRange = TempRangePointAngle[abs(i-TempRangeNormalIndex)]
			if ran[0] <= temp < ran[1]:
				deltaAngle = pointAngleRange[1] - pointAngleRange[0]
				p = float(ran[1] - temp) / (ran[1] - ran[0])
				pointAngle = (pointAngleRange[0] + deltaAngle * p)
			i -= 1
		curRot = self._TempStatePoint.GetRotateAngle()
		self._tempPointerTween = TweenHandler('easeOutQuad', 0.1, curRot, pointAngle, lambda value: self._TempStatePoint.Rotate(value))
		underWarning = False
		if temp < minTempWithR:
			underWarning = True
			self._TempStateWarn.SetSpriteColor(ColdColor)
			self._BegineTempWarning(-1)
		elif temp > maxTempWithR:
			underWarning = True
			self._TempStateWarn.SetSpriteColor(HeatColor)
			self._BegineTempWarning(1)
		else:
			self._tempWarnType = 0
			self._tempWarningTween = None
		self._TempStateWarn.SetVisible(underWarning)

	def _BegineTempWarning(self, type):
		if self._tempWarnType == type:
			return
		self._tempWarnType = type
		self._TempStateWarn.SetAlpha(0.5)
		self._tempWarningTween = TweenList([
			TweenHandler('easeInOutQuad', 1.0, 0.5, 1.0, self._UpdateTempWarning),
			TweenHandler('easeInOutQuad', 1.0, 1.0, 0.5, self._UpdateTempWarning),
		], self._LoopTweenRestart)


	def _UpdateTempWarning(self, value):
		self._TempStateWarn.SetAlpha(value)

	def UpdateEnvRadiationState(self, currentValue, maxValue):
		percent = int(float(currentValue) / maxValue * 10.0)
		i = 0
		while i < 10:
			color = (0.41, 0.44, 0.44)
			if i <= percent:
				color = (0.95, 0.80, 0.19)
			self._RadiationRangeImgs[i].SetSpriteColor(color)
			i += 1
		underWarning = currentValue > maxValue
		if underWarning:
			if self._radiationWarningTween == None:
				self._BegineRadiationWarning()
		else:
			self._radiationWarningTween = None
		self._RadiationStateWarn.SetVisible(underWarning)


	def _BegineRadiationWarning(self):
		self._RadiationStateWarn.SetAlpha(0.5)
		self._radiationWarningTween = TweenList(
			[
			TweenHandler('easeInOutQuad', 1.0, 0.5, 1.0, self._UpdateRadiationWarning),
			TweenHandler('easeInOutQuad', 1.0, 1.0, 0.5, self._UpdateRadiationWarning),
		], self._LoopTweenRestart)

	def _UpdateRadiationWarning(self, value):
		self._RadiationStateWarn.SetAlpha(value)

	def _LoopTweenRestart(self):
		if self._tempWarningTween is not None and self._tempWarningTween.Completed:
			self._tempWarningTween.Reset()
		if self._radiationWarningTween is not None and self._radiationWarningTween.Completed:
			self._radiationWarningTween.Reset()

	def Update(self):
		if self._tempPointerTween:
			self._tempPointerTween.Update()
		if self._tempWarningTween:
			self._tempWarningTween.Update()
		if self._radiationWarningTween:
			self._radiationWarningTween.Update()

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.HudShowSubscriptEvent, self.HudShowSubscriptEvent)
		super(SurviveHud, self).Destroy()
		self._tempPointerTween = None
		self._tempWarningTween = None
