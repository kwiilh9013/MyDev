# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
import mod.client.extraClientApi as extraClientApi
import ScukeSurviveScript.ScukeCore.client.engineApiGac as engineApiGac


class GunHud(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(GunHud, self).__init__(namespace, name, param)
		self._btnSetDict = {}
		self._hasSet = False
		self._hasDfData = False

	def Create(self):
		super(GunHud, self).Create()
		self._active = False

		self._GunCrossHairs = {}
		self._GunCrossHairType = None
		self._GunScatter = None
		self._GunHit = None
		self._GunKill = None
		self._GunHitShowTimer = None
		self._GunKillShowTimer = None

		self._gunCrossHairState = True
		self._S_showCrossHair = True

		self._GunPanel = self.GetBaseUIControl('/Panel_Gun')
		self._GunCrosshair = self.GetBaseUIControl('/Panel_Gun/Panel_CrossHair')

		self._ButtonFire = self.GetBaseUIControl('/Panel_Gun/Button_Fire').asButton()
		self._ButtonFire.AddTouchEventParams({"isSwallow": False})
		self._ButtonFire.SetButtonTouchDownCallback(self.OnButtonFireDown)
		self._ButtonFire.SetButtonTouchUpCallback(self.OnButtonFireUp)
		self._ButtonFire.SetButtonTouchCancelCallback(self.OnButtonFireUp)
		self._ButtonFire.SetButtonScreenExitCallback(self.OnButtonFireUp)

		self._ButtonFire_Left = self.GetBaseUIControl('/Panel_Gun/Button_Fire_Left').asButton()
		self._ButtonFire_Left.AddTouchEventParams({"isSwallow": True})
		self._ButtonFire_Left.SetButtonTouchDownCallback(self.OnButtonFireDown)
		self._ButtonFire_Left.SetButtonTouchUpCallback(self.OnButtonFireUp)
		self._ButtonFire_Left.SetButtonTouchCancelCallback(self.OnButtonFireUp)
		self._ButtonFire_Left.SetButtonScreenExitCallback(self.OnButtonFireUp)

		self._ButtonAim = self.GetBaseUIControl('/Panel_Gun/Button_Aim').asButton()
		self._ButtonAimSize = self._ButtonAim.GetSize()
		self._ButtonAim.AddTouchEventParams({"isSwallow": True})
		self._ButtonAim.SetButtonTouchDownCallback(self.OnButtonAimDown)
		self._ButtonAimState = self.GetBaseUIControl('/Panel_Gun/Button_Aim/default').asImage()

		self._ButtonReload = self.GetBaseUIControl('/Panel_Gun/Button_Reload').asButton()
		self._ButtonReload.AddTouchEventParams({"isSwallow": True})
		self._ButtonReload.SetButtonTouchDownCallback(self.OnButtonReloadDown)

		self._AmmoCount = self.GetBaseUIControl('/Panel_Gun/Button_Reload/Ammo_Count').asLabel()
		self._AmmoCount.SetText('0/0')
		self._ReloadProgress = self.GetBaseUIControl('/Panel_Gun/Button_Reload/Reload_Progress').asProgressBar()
		self._ReloadTime = self.GetBaseUIControl('/Panel_Gun/Button_Reload/Reload_Progress/Reload_Time').asLabel()
		self._ReloadProgress.SetVisible(False)

		self._ButtonKick = self.GetBaseUIControl('/Panel_Gun/Button_Kick').asButton()
		self._ButtonKick.AddTouchEventParams({"isSwallow": True})
		self._ButtonKick.SetButtonTouchDownCallback(self.OnButtonKickDown)

		self._gunClientSystem = extraClientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.GunClientSystem)
		self._zoomState = None
		self._btnSetDict = {
			"Button_Aim": self._ButtonAim,
			"Button_Kick": self._ButtonKick,
			"Button_Fire": self._ButtonFire,
			"Button_Reload": self._ButtonReload,
			"Button_Fire_Left": self._ButtonFire_Left
		}
		'''
		self._S_buttonMap = self._gunClientSystem.Setting['buttonMap']['value']
		self._buttonItem = [
			{
				'path': '/Panel_Gun/Button_Fire',
				'key': 'fire_right',
			},
			{
				'path': '/Panel_Gun/Button_Fire_Left',
				'key': 'fire_left',
			},
			{
				'path': '/Panel_Gun/Button_Aim',
				'key': 'aim',
			},
			{
				'path': '/Panel_Gun/Button_Reload',
				'key': 'reload',
			},
			{
				'path': '/Panel_Gun/Button_Kick',
				'key': 'kick',
			}
		]
		for item in self._buttonItem:
			btn = self.GetBaseUIControl(item['path']).asButton()
			item['size'] = btn.GetSize()
			item['pos'] = btn.GetPosition()
			item['ctrl'] = btn
		self.ApplySetting(self._S_buttonMap)
		'''
		gunClientSystemName = modConfig.ClientSystemEnum.GunClientSystem
		self.ListenForEvent(gunClientSystemName, 'UIUpdateClip', self, self.UpdateClip)
		self.ListenForEvent(gunClientSystemName, 'UIUpdateCrossHair', self, self.UpdateCrossHair)
		self.ListenForEvent(gunClientSystemName, 'UIUpdateCrossHairHit', self, self.UpdateCrossHairHit)
		self.ListenForEvent(gunClientSystemName, 'UIUpdateCrossHairKill', self, self.UpdateCrossHairKill)
		self.ListenForEvent(gunClientSystemName, 'UIUpdateReloadProgress', self, self.UpdateReloadProgress)
		self.ListenForEvent(gunClientSystemName, 'OnUpdateGunSetting', self, self.OnUpdateGunSetting)


		engineSystemName = extraClientApi.GetEngineSystemName()
		systemNamespace = extraClientApi.GetEngineNamespace()
		self.ListenForEvent(engineSystemName, 'OnKeyPressInGame', self, self.OnKeyPress, systemNamespace)
		self.ListenForEvent(engineSystemName, 'OnCarriedNewItemChangedClientEvent', self, self.OnCarriedNewItemChanged, systemNamespace)
		carriedData = clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLocalPlayerId()).GetCarriedItem()
		self.OnCarriedNewItemChanged(carriedData)

		self.OnDropGun()
		# 支持的准星类型
		self.InitCrossHair('machine')
		self.InitCrossHair('sniper')
		self.InitCrossHair('rifle')
		self.InitCrossHair('shot')
		self.InitCrossHair('submachine')
		self.InitCrossHair('cannon')
		self.InitCrossHair('grenade')
		self.InitCrossHair('grenade')
		self.InitCrossHair('charger')
		Instance.mEventMgr.RegisterEvent(eventConfig.SettingDataSubscribtEvent, self.SettingDataSubscribtEvent)

	def Destroy(self):
		super(GunHud, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.SettingDataSubscribtEvent, self.SettingDataSubscribtEvent)

	def SettingDataSubscribtEvent(self, args):
		stage = args.get("stage", None)
		if stage != "gun":
			return
		gunClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
		if not gunClient._initBtn:return
		posData = args.get("posData")
		if posData:
			if "defaultData" in posData:
				for key, value in self._btnSetDict.items():
					dfPos = posData['defaultData'].get(key, {"relaPos": [100, 100]})['relaPos']
					dfSize = posData['defaultData'].get(key, {"relaSize": 25.0})['relaSize']
					relaPos = posData['newData'].get(key, {"relaPos": [0, 0]})['relaPos']
					targetPos = (dfPos[0] + relaPos[0], dfPos[1] + relaPos[1])
					relaSize = posData['newData'].get(key, {"relaSize": 0.0})['relaSize']
					targetSize = round(dfSize, 3) + relaSize
					self._btnSetDict[key].SetPosition(targetPos)
					self._btnSetDict[key].SetSize((targetSize, targetSize), True)
					self._btnSetDict[key].SetAlpha(posData['newData'].get(key, {"alpha": 1.0})['alpha'])
			else:
				if not self._hasSet:
					self._hasSet = True
					for key, value in self._btnSetDict.items():
						dfPos = self._btnSetDict[key].GetPosition()
						dfSize = self._btnSetDict[key].GetSize()
						if dfPos[0] > 0 and dfPos[1] > 0 and not self._hasDfData:
							if key not in gunClient._defaultBtnData:
								gunClient._defaultBtnData.update({key: [dfPos, dfSize]})
						else:
							dfPos = gunClient._defaultBtnData[key][0]
							dfSize = gunClient._defaultBtnData[key][1]
						relaPos = posData.get(key, {"relaPos": [0, 0]})['relaPos']
						targetPos = (dfPos[0] + relaPos[0], dfPos[1] + relaPos[1])
						relaSize = posData.get(key, {"relaSize": 0.0})['relaSize']
						targetSize = round(dfSize[0], 3) + relaSize
						self._btnSetDict[key].SetPosition(targetPos)
						self._btnSetDict[key].SetSize((targetSize, targetSize), True)
						self._btnSetDict[key].SetAlpha(posData.get(key, {"alpha": 1.0})['alpha'])
					self._hasDfData = True

	def OnKeyPress(self, args):
		if not self._active:
			return
		screenName = args['screenName']
		key = int(args['key'])
		isDown = int(args['isDown']) == 1
		if screenName == "hud_screen" and isDown:
			if key == extraClientApi.GetMinecraftEnum().KeyBoardType.KEY_R:
				self.OnButtonReloadDown(None)
			elif key == extraClientApi.GetMinecraftEnum().KeyBoardType.KEY_V:
				self.OnButtonKickDown(None)

	def OnCarriedNewItemChanged(self, args):
		if args is None:
			return

	def InitCrossHair(self, type):
		path = '/Panel_Gun/Panel_CrossHair/%s' % type
		panel = self.GetBaseUIControl(path)
		scatter = self.GetBaseUIControl(path + '/scatter')
		hit = self.GetBaseUIControl(path + '/hit')
		kill = self.GetBaseUIControl(path + '/kill')
		self._GunCrossHairs[type] = {
			'panel': panel,
			'scatter': scatter,
			'hit': hit,
			'kill': kill
		}
		hit.SetVisible(False)
		kill.SetVisible(False)

	def ActiveCrossHair(self, type):
		for k, crossHair in self._GunCrossHairs.iteritems():
			panel = crossHair['panel']
			state = k == type
			panel.SetVisible(state)
			if state:
				self._GunScatter = crossHair['scatter']
				self._GunHit = crossHair['hit']
				self._GunKill = crossHair['kill']
				self._GunCrossHairType = type
				self._GunHit.SetVisible(False)
				self._GunKill.SetVisible(False)

	def OnCarryGun(self, config):
		if 'fireHud' in config:
			fireHud = config['fireHud']
			self.SetButtonImage('/Panel_Gun/Button_Fire', fireHud)
			self.SetButtonImage('/Panel_Gun/Button_Fire_Left', fireHud)
		self._zoomState = None
		self._GunPanel.SetVisible(True)
		self._UpdateAimState()
		self._active = True

	def OnDropGun(self):
		self._zoomState = None
		self._GunPanel.SetVisible(False)
		self._active = False

	def OnButtonFireDown(self, args):
		if self._gunClientSystem:
			self._gunClientSystem.KeyDown()

	def OnButtonFireUp(self, args):
		if self._gunClientSystem:
			self._gunClientSystem.KeyUp()

	def OnButtonAimDown(self, args):
		if self._gunClientSystem:
			self._gunClientSystem.SwitchZoomState()

	def Update(self):
		self._UpdateAimState()

	def _UpdateAimState(self):
		if self._gunClientSystem:
			state = self._gunClientSystem.GetZoomState()
			if state != self._zoomState:
				if state:
					self._ButtonAimState.SetSpriteColor((0.46, 1.0, 0.47))
				else:
					self._ButtonAimState.SetSpriteColor((1, 1, 1))
			self._zoomState = state
	def OnButtonKickDown(self, args):
		if self._gunClientSystem:
			self._gunClientSystem.Kick()

	def OnButtonReloadDown(self, args):
		if self._gunClientSystem:
			self._gunClientSystem.Reload()

	def UpdateClip(self, args):
		cur = args['clip']
		max = args['maxClip']
		self._AmmoCount.SetText('%d/%d' % (cur, max))

	def UpdateCrossHair(self, args):
		angle = args['angle']
		config = args['config']
		if self._GunCrossHairType != config['type']:
			self.ActiveCrossHair(config['type'])
		if self._GunScatter:
			size = config['size']
			if 'zoomSize' in config and args['zoom']:
				size = config['zoomSize']
			size += config['angleSize'] * angle
			self._GunScatter.SetSize((size, size), True)
		if config['type'] == 'charger':
			chargeInfo = args['charge']
			path = '/Panel_Gun/Panel_CrossHair/charger/charge/l%d'
			i = 0
			while i < 3:
				img = self.GetBaseUIControl(path % i).asImage()
				level = -1 if chargeInfo is None else chargeInfo['level']
				if i < level:
					img.SetSpriteColor((0.98, 0.93, 0.45))
					img.SetAlpha(1.0)
				else:
					img.SetSpriteColor((1, 1, 1))
					img.SetAlpha(0.5)
				i += 1


	def SetCrossHairVisible(self, visible):
		if self._S_showCrossHair:
			self._GunCrosshair.SetVisible(visible)
		else:
			self._GunCrosshair.SetVisible(False)
		self._gunCrossHairState = visible

	def UpdateCrossHairHit(self, args):
		if not self._GunHit:
			return
		if self._GunHitShowTimer:
			engineApiGac.CancelTimer(self._GunHitShowTimer)
		self._GunHit.SetVisible(True)
		self._GunHitShowTimer = engineApiGac.AddTimer(0.08, self._HitShowTimerEnd)

	def UpdateCrossHairKill(self, args):
		if not self._GunKill:
			return
		if self._GunKillShowTimer:
			engineApiGac.CancelTimer(self._GunKillShowTimer)
		self._GunKill.SetVisible(True)
		self._GunKillShowTimer = engineApiGac.AddTimer(0.2, self._KillShowTimerEnd)

	def _HitShowTimerEnd(self):
		if not self._GunHit:
			return
		self._GunHit.SetVisible(False)
		self._GunHitShowTimer = None

	def _KillShowTimerEnd(self):
		if not self._GunKill:
			return
		self._GunKill.SetVisible(False)
		self._GunKillShowTimer = None

	def UpdateReloadProgress(self, args):
		total = args['duration']
		visible = total > 0
		percent = 1.0 - args['percent']
		leftTime = total * percent / 1000.0
		self._ReloadTime.SetText('%.1fs' % round(leftTime, 1))
		# self._ReloadProgress.SetValue(percent)
		self._ReloadProgress.SetVisible(visible)


	def OnUpdateGunSetting(self, args):
		self._S_showCrossHair = args['showCrossHair']['value']
		self._S_buttonMap = args['buttonMap']['value']
		if self._S_showCrossHair:
			self._GunCrosshair.SetVisible(self._gunCrossHairState)
		else:
			self._GunCrosshair.SetVisible(False)
		self.ApplySetting(self._S_buttonMap)

	def SetButtonAlpha(self, btn, alpha):
		btn.GetChildByName('pressed').asImage().SetAlpha(alpha)
		btn.GetChildByName('default').asImage().SetAlpha(alpha)
		btn.GetChildByName('hover').asImage().SetAlpha(alpha)
		btn.GetChildByName('bg').asImage().SetAlpha(alpha)

	def ApplySetting(self, setting):
		for item in self._buttonItem:
			key = item['key']
			ctrl = item['ctrl']
			size = item['size']
			pos = item['pos']
			s = setting[key]
			ctrl.SetSize(MathUtils.TupleMul(size, s['size'] / 100.0), True)
			self.SetButtonAlpha(ctrl, s['alpha'] / 100.0)
			ctrl.SetPosition(MathUtils.TupleAdd(pos, s['pos']))