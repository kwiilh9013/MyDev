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


MeleeBtnPath = "/PanelMain/"

MeleeBtnMap = [
	(MeleeBtnPath, "Button_Attack")
]

MainBtnMap = [
	("/PanelMain/", "resetBtn"), ("/PanelMain/", "quitBtn"), ("/PanelMain/", "saveBtn"),
	("/PanelMain/confirmBg/", "yesBtn"), ("/PanelMain/confirmBg/", "noBtn")
]


class MeleeSetting(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(MeleeSetting, self).__init__(namespace, name, param)
		self._confirmPanel = None
		self._client = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.SettingClientSystem)
		self._btnDict = {}
		self._selectBtnList = []
		self._meleeBtnData = copy.deepcopy(self._client._settingDict['meleeBtnData'])
		self._meleeBtnMovePos = {}
		self._meleeBtnPressDownPos = {}
		self._meleeDefaultData = {}
		self.AlphaSliderPercentValue = 1.0
		self.SizeSliderPercentValue = 0.5

	def Create(self):
		super(MeleeSetting, self).Create()
		self.CreateBtn()

	def CreateBtn(self):
		for x in MeleeBtnMap:
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
		map(lambda y: self._meleeDefaultData.update({y[1]: {}}), MeleeBtnMap)
		map(lambda y: self._meleeDefaultData[y[1]].update({"relaPos": list(self._btnDict[y[1]].GetPosition()),
														 "relaSize": self._btnDict[y[1]].GetSize()[0], "alpha": 1.0}), MeleeBtnMap)
		for z in MeleeBtnMap:
			self._btnDict[z[1]].asButton().SetSize(
				(self._meleeDefaultData[z[1]]['relaSize'] + self._meleeBtnData[z[1]]['relaSize'],
				 self._meleeDefaultData[z[1]]['relaSize'] + self._meleeBtnData[z[1]]['relaSize']), True)
			self._btnDict[z[1]].asButton().SetPosition(
				(self._meleeDefaultData[z[1]]['relaPos'][0] + self._meleeBtnData[z[1]]['relaPos'][0],
				 self._meleeDefaultData[z[1]]['relaPos'][1] + self._meleeBtnData[z[1]]['relaPos'][1]))
			self._btnDict[z[1]].asButton().SetAlpha(self._meleeBtnData[z[1]]['alpha'])

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
				for key in MeleeBtnMap:
					DefaultPos = self._meleeDefaultData[key[1]]['relaPos']
					NowPos = self._btnDict[key[1]].GetPosition()
					self._meleeBtnData[key[1]]['relaPos'] = [NowPos[0] - DefaultPos[0],  NowPos[1] - DefaultPos[1]]
					self._meleeBtnData[key[1]]['relaSize'] = round(self._meleeBtnData[key[1]]['relaSize'], 3)
				self._client._settingDict['meleeBtnData'] = self._meleeBtnData
				self._client.UpdateBtnPos("melee", {"newData": self._meleeBtnData, "defaultData": self._meleeDefaultData})
				clientApi.PopScreen()
		elif Type == "saveBtn":
			self._confirmPanel.SetVisible(True)
		elif Type == 'resetBtn':
			for key, value in self._meleeDefaultData.items():
				self._btnDict[key].SetPosition(tuple(value['relaPos']))
				self._btnDict[key].SetSize((value['relaSize'], value['relaSize']), True)
				self._btnDict[key].SetAlpha(1.0)
				self._meleeBtnData[key].update({"relaPos": [0, 0], "relaSize": 0.0, "alpha": 1.0})
				self.GetBaseUIControl(MeleeBtnPath + key + "/selected").SetVisible(False)
				self._meleeBtnMovePos.clear()
			self._selectBtnList = []
		if Type.startswith('Button_'):
			if abs(self._meleeBtnPressDownPos[Type][0] - posX) > 3 or abs(self._meleeBtnPressDownPos[Type][1] - posY) > 3:
				self._meleeBtnMovePos.clear()
				return
			if Type not in self._selectBtnList:
				self._selectBtnList.append(Type)
			else:
				self._selectBtnList.remove(Type)
			self.GetBaseUIControl(MeleeBtnPath + Type + "/selected").asImage().SetVisible(Type in self._selectBtnList)

	def OnBtnPressDown(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		self._meleeBtnPressDownPos[Type] = (posX, posY)

	def OnBtnMove(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		btn = self._btnDict[Type]
		curPos = btn.GetPosition()
		if Type in self._meleeBtnMovePos:
			deltaX = posX - self._meleeBtnMovePos[Type][0]
			deltaY = posY - self._meleeBtnMovePos[Type][1]
			btn.SetPosition((curPos[0] + deltaX, curPos[1] + deltaY))
		self._meleeBtnMovePos[Type] = (posX, posY)

	@ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished, "#MeleeSetting.AlphaSliderChange")
	def AlphaSliderChange(self, value, isFinish, _unused):
		if 0.0 < value < 1.0:
			for i in self._selectBtnList:
				self._meleeBtnData[i]['alpha'] = round(value, 3)
				self._btnDict[i].asButton().SetAlpha(self._meleeBtnData[i]['alpha'])
		self.AlphaSliderPercentValue = value  # 百分比类型滑动条保存值
		if isFinish:
			self.AlphaSliderPercentValue = 1.0
		return ViewRequest.Refresh

	@ViewBinder.binding(ViewBinder.BF_BindFloat, "#MeleeSetting.AlphaSliderValue")
	def AlphaSliderValue(self):
		return self.AlphaSliderPercentValue  # 百分比类型滑动条返回值

	@ViewBinder.binding(ViewBinder.BF_BindInt, "#MeleeSetting.AlphaSliderStep")
	def AlphaSliderStep(self):
		return 1  # 百分比类型滑动条

	@ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished, "#MeleeSetting.SizeSliderChange")
	def SizeSliderChange(self, value, isFinish, _unused):
		if 0.0 < value < 1.0:
			for i in self._selectBtnList:
				size = self._meleeDefaultData[i]['relaSize']
				self._meleeBtnData[i]['relaSize'] += round((value-self.SizeSliderPercentValue)*10, 3)
				self._meleeBtnData[i]['relaSize'] = min(max(self._meleeBtnData[i]['relaSize'], -size + 5), 150)
				self._btnDict[i].asButton().SetSize((size + self._meleeBtnData[i]['relaSize'], size + self._meleeBtnData[i]['relaSize']), True)
		self.SizeSliderPercentValue = value  # 百分比类型滑动条保存值
		if isFinish:
			self.SizeSliderPercentValue = 0.5
		return ViewRequest.Refresh

	@ViewBinder.binding(ViewBinder.BF_BindFloat, "#MeleeSetting.SizeSliderValue")
	def SizeSliderValue(self):
		return self.SizeSliderPercentValue  # 百分比类型滑动条返回值

	@ViewBinder.binding(ViewBinder.BF_BindInt, "#MeleeSetting.SizeSliderStep")
	def SizeSliderStep(self):
		return 1  # 百分比类型滑动条