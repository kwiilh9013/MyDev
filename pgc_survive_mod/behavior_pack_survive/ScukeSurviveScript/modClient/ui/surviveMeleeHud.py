# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modCommon import modConfig
import mod.client.extraClientApi as extraClientApi
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance


class MeleeHud(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(MeleeHud, self).__init__(namespace, name, param)
		self._btnSetDict = {}
		self._hasSet = False
		self._hasDfData = False

	def Create(self):
		super(MeleeHud, self).Create()
		self._MeleeCrossHairs = {}
		self._MeleeCrossHairType = None
		self._MeleeScatter = None
		self._MeleeHit = None
		self._MeleeKill = None
		self._MeleeHitShowTimer = None
		self._MeleeKillShowTimer = None

		self._MeleeAttackBtns = {}
		self._CurMeleeAttackBtn = None


		self._MeleePanel = self.GetBaseUIControl('/Panel_Melee')

		self._ButtonAttack = self.GetBaseUIControl('/Panel_Melee/Button_Attack').asButton()
		self._ButtonAttack.AddTouchEventParams({"isSwallow": False})
		self._ButtonAttack.SetButtonTouchDownCallback(self.OnButtonAttackDown)
		self._ButtonAttack.SetButtonTouchUpCallback(self.OnButtonAttackUp)
		self._ButtonAttack.SetButtonTouchCancelCallback(self.OnButtonAttackUp)

		self._btnSetDict = {
			"Button_Attack": self._ButtonAttack
		}
		self.meleeClientSystem = extraClientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.MeleeClientSystem)

		meleeClientSystemName = modConfig.ClientSystemEnum.MeleeClientSystem
		self.ListenForEvent(meleeClientSystemName, 'UIUpdateMeleeLevel', self, self.UpdateMeleeLevel)

		self.OnDropMelee()
		self.InitBaseballBatAttackBtn('scuke_survive:melee_baseball_bat')
		self.InitBaseballBatAttackBtn('scuke_survive:melee_baseball_bat_m')
		self.InitBaseballBatAttackBtn('scuke_survive:melee_baseball_bat_golden')
		# 支持的准星类型
		self.InitCrossHair('machine')
		self.InitCrossHair('sniper')
		self.InitCrossHair('rifle')
		self.InitCrossHair('shot')
		self.InitCrossHair('submachine')
		self.InitCrossHair('cannon')
		self.InitCrossHair('grenade')
		Instance.mEventMgr.RegisterEvent(eventConfig.SettingDataSubscribtEvent, self.SettingDataSubscribtEvent)

	def Destroy(self):
		super(MeleeHud, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.SettingDataSubscribtEvent, self.SettingDataSubscribtEvent)

	def SettingDataSubscribtEvent(self, args):
		stage = args.get("stage", None)
		if stage != "melee":
			return
		meleeClient = extraClientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
		if not meleeClient._initBtn:return
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
							if key not in meleeClient._defaultBtnData:
								meleeClient._defaultBtnData.update({key: [dfPos, dfSize]})
						else:
							dfPos = meleeClient._defaultBtnData[key][0]
							dfSize = meleeClient._defaultBtnData[key][1]
						relaPos = posData.get(key, {"relaPos": [0, 0]})['relaPos']
						targetPos = (dfPos[0] + relaPos[0], dfPos[1] + relaPos[1])
						relaSize = posData.get(key, {"relaSize": 0.0})['relaSize']
						targetSize = round(dfSize[0], 3) + relaSize
						self._btnSetDict[key].SetPosition(targetPos)
						self._btnSetDict[key].SetSize((targetSize, targetSize), True)
						self._btnSetDict[key].SetAlpha(posData.get(key, {"alpha": 1.0})['alpha'])
					self._hasDfData = True

	def InitCrossHair(self, type):
		path = '/Panel_Melee/Panel_CrossHair/%s' % type
		panel = self.GetBaseUIControl(path)
		scatter = self.GetBaseUIControl(path + '/scatter')
		hit = self.GetBaseUIControl(path + '/hit')
		kill = self.GetBaseUIControl(path + '/kill')
		self._MeleeCrossHairs[type] = {
			'panel': panel,
			'scatter': scatter,
			'hit': hit,
			'kill': kill
		}
		hit.SetVisible(False)
		kill.SetVisible(False)

	def InitBaseballBatAttackBtn(self, id):
		type = 'baseball_bat'
		path = '/Panel_Melee/Button_Attack/Panel_AttackType/%s' % type
		panel = self.GetBaseUIControl(path)
		levels = [
			self.GetBaseUIControl(path + '/bg/level1'),
			self.GetBaseUIControl(path + '/bg/level2'),
			self.GetBaseUIControl(path + '/bg/level3')
		]
		item = {
			'panel': panel,
			'levels': levels
		}
		self._MeleeAttackBtns[id] = item

	def ActiveMeleeAttackBtn(self, id):
		for attackBtn in self._MeleeAttackBtns.itervalues():
			panel = attackBtn['panel']
			panel.SetVisible(False)
			if 'levels' in attackBtn:
				levels = attackBtn['levels']
				for levelImg in levels:
					levelImg.SetVisible(False)

		for k, attackBtn in self._MeleeAttackBtns.iteritems():
			panel = attackBtn['panel']
			if k == id:
				panel.SetVisible(True)
				self._CurMeleeAttackBtn = attackBtn


	def ActiveCrossHair(self, type):
		for k, crossHair in self._MeleeCrossHairs.iteritems():
			panel = crossHair['panel']
			state = k == type
			panel.SetVisible(state)
			if state:
				self._MeleeScatter = crossHair['scatter']
				self._MeleeHit = crossHair['hit']
				self._MeleeKill = crossHair['kill']
				self._MeleeCrossHairType = type
				self._MeleeHit.SetVisible(False)
				self._MeleeKill.SetVisible(False)

	def UpdateCrossHair(self, args):
		angle = args['angle']
		config = args['config']
		if self._MeleeCrossHairType != config['type']:
			self.ActiveCrossHair(config['type'])
		if self._MeleeScatter:
			size = config['size']
			if 'zoomSize' in config and args['zoom']:
				size = config['zoomSize']
			size += config['angleSize'] * angle
			self._MeleeScatter.SetSize((size, size), True)

	def OnCarryMelee(self, identifier):
		self._MeleePanel.SetVisible(True)
		self.ActiveMeleeAttackBtn(identifier)

	def OnDropMelee(self):
		self._MeleePanel.SetVisible(False)

	def OnButtonAttackDown(self, args):
		if self.meleeClientSystem:
			self.meleeClientSystem.KeyDown()

	def OnButtonAttackUp(self, args):
		if self.meleeClientSystem:
			self.meleeClientSystem.KeyUp()

	def UpdateMeleeLevel(self, args):
		level = args['level']
		if self._CurMeleeAttackBtn and 'levels' in self._CurMeleeAttackBtn:
			levels = self._CurMeleeAttackBtn['levels']
			for i in range(len(levels)):
				levels[i].SetVisible(i < level)


	def UpdateCrossHair(self, args):
		angle = args['angle']
		config = args['config']
		if self._MeleeCrossHairType != config['type']:
			self.ActiveCrossHair(config['type'])
		if self._MeleeScatter:
			size = config['size']
			if 'zoomSize' in config and args['zoom']:
				size = config['zoomSize']
			size += config['angleSize'] * angle
			self._MeleeScatter.SetSize((size, size), True)

	def UpdateCrossHairHit(self, args):
		if not self._MeleeHit:
			return
		if self._MeleeHitShowTimer:
			engineApiGac.CancelTimer(self._MeleeHitShowTimer)
		self._MeleeHit.SetVisible(True)
		self._MeleeHitShowTimer = engineApiGac.AddTimer(0.08, self._HitShowTimerEnd)

	def UpdateCrossHairKill(self, args):
		if not self._MeleeKill:
			return
		if self._MeleeKillShowTimer:
			engineApiGac.CancelTimer(self._MeleeKillShowTimer)
		self._MeleeKill.SetVisible(True)
		self._MeleeKillShowTimer = engineApiGac.AddTimer(0.2, self._KillShowTimerEnd)

	def _HitShowTimerEnd(self):
		if not self._MeleeHit:
			return
		self._MeleeHit.SetVisible(False)
		self._MeleeHitShowTimer = None

	def _KillShowTimerEnd(self):
		if not self._MeleeKill:
			return
		self._MeleeKill.SetVisible(False)
		self._MeleeKillShowTimer = None
