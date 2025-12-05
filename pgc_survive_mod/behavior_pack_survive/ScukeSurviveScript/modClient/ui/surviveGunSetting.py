# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
import mod.client.extraClientApi as extraClientApi
import ScukeSurviveScript.ScukeCore.client.engineApiGac as engineApiGac
import copy
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()


GunBtnPath = "/PanelMain/Panel_Gun/"

GunBtnMap = [
	(GunBtnPath, "Button_Fire"), (GunBtnPath, "Button_Aim"), (GunBtnPath, "Button_Fire_Left"),
	(GunBtnPath, "Button_Reload"), (GunBtnPath, "Button_Kick")
]

MainBtnMap = [
	("/PanelMain/", "resetBtn"), ("/PanelMain/", "quitBtn"), ("/PanelMain/", "saveBtn"),
	("/PanelMain/confirmBg/", "yesBtn"), ("/PanelMain/confirmBg/", "noBtn")
]


class GunSetting(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(GunSetting, self).__init__(namespace, name, param)
		self._confirmPanel = None
		self._client = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.SettingClientSystem)
		self._btnDict = {}
		self._selectBtnList = []
		self._gunBtnData = copy.deepcopy(self._client._settingDict['gunBtnData'])
		self._gunBtnMovePos = {}
		self._gunBtnPressDownPos = {}
		self._gunDefaultData = {}
		self.AlphaSliderPercentValue = 1.0
		self.SizeSliderPercentValue = 0.5

	def Create(self):
		super(GunSetting, self).Create()
		self.CreateBtn()

	def CreateBtn(self):
		for x in GunBtnMap:
			self._btnDict.update({x[1]: self.GetBaseUIControl(x[0] + x[1]).asButton()})
			self._btnDict[x[1]].AddTouchEventParams({"isSwallow": True, 'type': x[1]})
			self._btnDict[x[1]].SetButtonTouchUpCallback(self.OnBtnPress)
			self._btnDict[x[1]].SetButtonTouchDownCallback(self.OnBtnPressDown)
			self._btnDict[x[1]].SetButtonTouchMoveCallback(self.OnBtnMove)
		for x in MainBtnMap:
			self._btnDict.update({x[1]: self.GetBaseUIControl(x[0] + x[1]).asButton()})
			self._btnDict[x[1]].AddTouchEventParams({"isSwallow": True, 'type': x[1]})
			self._btnDict[x[1]].SetButtonTouchUpCallback(self.OnBtnPress)
		self._confirmPanel = self.GetBaseUIControl("/PanelMain/confirmBg").asImage()
		self._confirmPanel.SetVisible(False)
		map(lambda y: self._gunDefaultData.update({y[1]: {}}), GunBtnMap)
		map(lambda y: self._gunDefaultData[y[1]].update({"relaPos": list(self._btnDict[y[1]].GetPosition()),
														 "relaSize": self._btnDict[y[1]].GetSize()[0], "alpha": 1.0}), GunBtnMap)
		for z in GunBtnMap:
			self._btnDict[z[1]].asButton().SetSize(
				(self._gunDefaultData[z[1]]['relaSize'] + self._gunBtnData[z[1]]['relaSize'],
				 self._gunDefaultData[z[1]]['relaSize'] + self._gunBtnData[z[1]]['relaSize']), True)
			self._btnDict[z[1]].asButton().SetPosition(
				(self._gunDefaultData[z[1]]['relaPos'][0] + self._gunBtnData[z[1]]['relaPos'][0],
				 self._gunDefaultData[z[1]]['relaPos'][1] + self._gunBtnData[z[1]]['relaPos'][1]))
			self._btnDict[z[1]].asButton().SetAlpha(self._gunBtnData[z[1]]['alpha'])

	def Update(self):
		pass

	def OnBtnPress(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		if Type == "quitBtn":
			clientApi.PopScreen()
		elif Type in ["yesBtn", "noBtn"]:
			self._confirmPanel.SetVisible(False)
			if Type == 'yesBtn':
				for key in GunBtnMap:
					DefaultPos = self._gunDefaultData[key[1]]['relaPos']
					NowPos = self._btnDict[key[1]].GetPosition()
					self._gunBtnData[key[1]]['relaPos'] = [NowPos[0] - DefaultPos[0],  NowPos[1] - DefaultPos[1]]
					self._gunBtnData[key[1]]['relaSize'] = round(self._gunBtnData[key[1]]['relaSize'], 3)
				self._client._settingDict['gunBtnData'] = self._gunBtnData
				self._client.UpdateBtnPos("gun", {"newData": self._gunBtnData, "defaultData": self._gunDefaultData})
				clientApi.PopScreen()
		elif Type == "saveBtn":
			self._confirmPanel.SetVisible(True)
		elif Type == 'resetBtn':
			for key, value in self._gunDefaultData.items():
				self._btnDict[key].SetPosition(tuple(value['relaPos']))
				self._btnDict[key].SetSize((value['relaSize'], value['relaSize']), True)
				self._btnDict[key].SetAlpha(1.0)
				self._gunBtnData[key].update({"relaPos": [0, 0], "relaSize": 0.0, "alpha": 1.0})
				self.GetBaseUIControl(GunBtnPath + key + "/selected").SetVisible(False)
				self._gunBtnMovePos.clear()
			self._selectBtnList = []
		if Type.startswith('Button_'):
			if abs(self._gunBtnPressDownPos[Type][0] - posX) > 3 or abs(self._gunBtnPressDownPos[Type][1] - posY) > 3:
				self._gunBtnMovePos.clear()
				return
			if Type not in self._selectBtnList:
				self._selectBtnList.append(Type)
			else:
				self._selectBtnList.remove(Type)
			self.GetBaseUIControl(GunBtnPath + Type + "/selected").asImage().SetVisible(Type in self._selectBtnList)

	def OnBtnPressDown(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		self._gunBtnPressDownPos[Type] = (posX, posY)

	def OnBtnMove(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		btn = self._btnDict[Type]
		curPos = btn.GetPosition()
		if Type in self._gunBtnMovePos:
			deltaX = posX - self._gunBtnMovePos[Type][0]
			deltaY = posY - self._gunBtnMovePos[Type][1]
			btn.SetPosition((curPos[0] + deltaX, curPos[1] + deltaY))
		self._gunBtnMovePos[Type] = (posX, posY)

	@ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished, "#GunSetting.AlphaSliderChange")
	def AlphaSliderChange(self, value, isFinish, _unused):
		if 0.0 < value < 1.0:
			for i in self._selectBtnList:
				self._gunBtnData[i]['alpha'] = round(value, 3)
				self._btnDict[i].asButton().SetAlpha(self._gunBtnData[i]['alpha'])
		self.AlphaSliderPercentValue = value  # 百分比类型滑动条保存值
		if isFinish:
			self.AlphaSliderPercentValue = 1.0
		return ViewRequest.Refresh

	@ViewBinder.binding(ViewBinder.BF_BindFloat, "#GunSetting.AlphaSliderValue")
	def AlphaSliderValue(self):
		return self.AlphaSliderPercentValue  # 百分比类型滑动条返回值

	@ViewBinder.binding(ViewBinder.BF_BindInt, "#GunSetting.AlphaSliderStep")
	def AlphaSliderStep(self):
		return 1  # 百分比类型滑动条

	@ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished, "#GunSetting.SizeSliderChange")
	def SizeSliderChange(self, value, isFinish, _unused):
		if 0.0 < value < 1.0:
			for i in self._selectBtnList:
				size = self._gunDefaultData[i]['relaSize']
				self._gunBtnData[i]['relaSize'] += round((value-self.SizeSliderPercentValue)*10, 3)
				self._gunBtnData[i]['relaSize'] = min(max(self._gunBtnData[i]['relaSize'], -size + 5), 150)
				self._btnDict[i].asButton().SetSize((size + self._gunBtnData[i]['relaSize'], size + self._gunBtnData[i]['relaSize']), True)
		self.SizeSliderPercentValue = value  # 百分比类型滑动条保存值
		if isFinish:
			self.SizeSliderPercentValue = 0.5
		return ViewRequest.Refresh

	@ViewBinder.binding(ViewBinder.BF_BindFloat, "#GunSetting.SizeSliderValue")
	def SizeSliderValue(self):
		return self.SizeSliderPercentValue  # 百分比类型滑动条返回值

	@ViewBinder.binding(ViewBinder.BF_BindInt, "#GunSetting.SizeSliderStep")
	def SizeSliderStep(self):
		return 1  # 百分比类型滑动条