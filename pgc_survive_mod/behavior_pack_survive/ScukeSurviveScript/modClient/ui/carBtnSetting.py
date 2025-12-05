# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()


CarBtnPath = "/PanelMain/"

CarBtnMap = [
	(CarBtnPath + "panel_speedup/", "btn_up"), (CarBtnPath + "panel_speedup/", "btn_cut"),
	(CarBtnPath + "panel_turn/", "btn_turn_left"), (CarBtnPath + "panel_turn/", "btn_turn_right"),
	(CarBtnPath, "btn_geton"), (CarBtnPath, "btn_energy"), 
	(CarBtnPath + "panel_skill/", "btn_skill1"), (CarBtnPath + "panel_skill/", "btn_skill2"), 
	(CarBtnPath + "panel_skill/skill_fly/", "btn_fly"), (CarBtnPath + "panel_skill/skill_fly/", "btn_up"), 
	(CarBtnPath + "panel_skill/skill_fly/", "btn_down"), 
]

MainBtnMap = [
	("/PanelMain/", "resetBtn"), ("/PanelMain/", "quitBtn"), ("/PanelMain/", "saveBtn"),
	("/PanelMain/confirmBg/", "yesBtn"), ("/PanelMain/confirmBg/", "noBtn")
]


class CarBtnSetting(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(CarBtnSetting, self).__init__(namespace, name, param)
		self._confirmPanel = None
		self._client = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.SettingClientSystem)
		self._btnDict = {}
		self._selectBtnList = []
		self._carBtnData = commonApiMgr.DeepCopy(self._client._settingDict['carBtnData'])
		self._carBtnMovePos = {}
		self._carBtnPressDownPos = {}
		self._carDefaultData = {}
		self.AlphaSliderPercentValue = 1.0
		self.SizeSliderPercentValue = 0.5

	def Create(self):
		super(CarBtnSetting, self).Create()
		self.CreateBtn()

	def CreateBtn(self):
		for x in CarBtnMap:
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
		map(lambda y: self._carDefaultData.update({y[1]: {}}), CarBtnMap)
		map(lambda y: self._carDefaultData[y[1]].update({"relaPos": list(self._btnDict[y[1]].GetPosition()),
														 "relaSize": self._btnDict[y[1]].GetSize()[0], "alpha": 1.0}), CarBtnMap)
		for z in CarBtnMap:
			val = self._carBtnData.get(z[1])
			if val is None:
				val = {
                    "relaPos": None,
                    "relaSize": 0.0,
                    "alpha": 1.0
				}
				self._carBtnData[z[1]] = val
			# 改为使用当前值，而非相对默认值
			size = self._carBtnData[z[1]]['relaSize']
			if size == 0:
				size = self._carDefaultData[z[1]]['relaSize']
				self._carBtnData[z[1]]['relaSize'] = size
			self._btnDict[z[1]].SetSize((size, size), True)
			pos = self._carBtnData[z[1]]['relaPos']
			if pos is None:
				pos = self._carDefaultData[z[1]]['relaPos']
				self._carBtnData[z[1]]['relaPos'] = pos
			self._btnDict[z[1]].SetPosition((pos[0], pos[1]))
			self._btnDict[z[1]].SetAlpha(self._carBtnData[z[1]]['alpha'])

	def Update(self):
		pass

	def OnBtnPress(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		ButtonPath = args['ButtonPath']
		if Type == "quitBtn":
			clientApi.PopScreen()
		elif Type in ["yesBtn", "noBtn"]:
			self._confirmPanel.SetVisible(False)
			if Type == 'yesBtn':
				for key in CarBtnMap:
					# 改为使用当前值，而非相对默认值
					NowPos = self._btnDict[key[1]].GetPosition()
					self._carBtnData[key[1]]['relaPos'] = [NowPos[0],  NowPos[1]]
					self._carBtnData[key[1]]['relaSize'] = self._btnDict[key[1]].GetSize()[0]
				self._client._settingDict['carBtnData'] = self._carBtnData
				# 更新载具UI的位置
				self._client.UpdateBtnPos("car", self._carBtnData)
				clientApi.PopScreen()
		elif Type == "saveBtn":
			self._confirmPanel.SetVisible(True)
		elif Type == 'resetBtn':
			# 重置
			for mapVal in CarBtnMap:
				btnPath = mapVal[0]
				key = mapVal[1]
				value = self._carDefaultData.get(key)
				if value is None:
					continue
				self._btnDict[key].SetPosition(tuple(value['relaPos']))
				self._btnDict[key].SetSize((value['relaSize'], value['relaSize']), True)
				self._btnDict[key].SetAlpha(1.0)
				self._carBtnData[key].update({"relaPos": [0, 0], "relaSize": 0.0, "alpha": 1.0})
				self.GetBaseUIControl(btnPath + key + "/selected").SetVisible(False)
			self._carBtnMovePos.clear()
			self._selectBtnList = []
		if Type.startswith('btn_'):
			# 点击按钮
			if abs(self._carBtnPressDownPos[Type][0] - posX) > 3 or abs(self._carBtnPressDownPos[Type][1] - posY) > 3:
				self._carBtnMovePos.clear()
				return
			if Type not in self._selectBtnList:
				self._selectBtnList.append(Type)
			else:
				self._selectBtnList.remove(Type)
			self.GetBaseUIControl(ButtonPath + "/selected").SetVisible(Type in self._selectBtnList)

	def OnBtnPressDown(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		self._carBtnPressDownPos[Type] = (posX, posY)

	def OnBtnMove(self, args):
		Type = args['AddTouchEventParams']['type']
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		btn = self._btnDict[Type]
		curPos = btn.GetPosition()
		if Type in self._carBtnMovePos:
			deltaX = posX - self._carBtnMovePos[Type][0]
			deltaY = posY - self._carBtnMovePos[Type][1]
			btn.SetPosition((curPos[0] + deltaX, curPos[1] + deltaY))
		self._carBtnMovePos[Type] = (posX, posY)

	@ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished, "#CarBtnSetting.AlphaSliderChange")
	def AlphaSliderChange(self, value, isFinish, _unused):
		if 0.0 < value < 1.0:
			for i in self._selectBtnList:
				self._carBtnData[i]['alpha'] = round(value, 3)
				self._btnDict[i].SetAlpha(self._carBtnData[i]['alpha'])
		self.AlphaSliderPercentValue = value  # 百分比类型滑动条保存值
		if isFinish:
			self.AlphaSliderPercentValue = 1.0
		return ViewRequest.Refresh

	@ViewBinder.binding(ViewBinder.BF_BindFloat, "#CarBtnSetting.AlphaSliderValue")
	def AlphaSliderValue(self):
		return self.AlphaSliderPercentValue  # 百分比类型滑动条返回值

	@ViewBinder.binding(ViewBinder.BF_BindInt, "#CarBtnSetting.AlphaSliderStep")
	def AlphaSliderStep(self):
		return 1  # 百分比类型滑动条

	@ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished, "#CarBtnSetting.SizeSliderChange")
	def SizeSliderChange(self, value, isFinish, _unused):
		if 0.0 < value < 1.0:
			for i in self._selectBtnList:
				size = self._carDefaultData[i]['relaSize']
				self._carBtnData[i]['relaSize'] += round((value-self.SizeSliderPercentValue)*10, 3)
				self._carBtnData[i]['relaSize'] = min(max(self._carBtnData[i]['relaSize'], -size + 5), 150)
				self._btnDict[i].SetSize((size + self._carBtnData[i]['relaSize'], size + self._carBtnData[i]['relaSize']), True)
		self.SizeSliderPercentValue = value  # 百分比类型滑动条保存值
		if isFinish:
			self.SizeSliderPercentValue = 0.5
		return ViewRequest.Refresh

	@ViewBinder.binding(ViewBinder.BF_BindFloat, "#CarBtnSetting.SizeSliderValue")
	def SizeSliderValue(self):
		return self.SizeSliderPercentValue  # 百分比类型滑动条返回值

	@ViewBinder.binding(ViewBinder.BF_BindInt, "#CarBtnSetting.SizeSliderStep")
	def SizeSliderStep(self):
		return 1  # 百分比类型滑动条