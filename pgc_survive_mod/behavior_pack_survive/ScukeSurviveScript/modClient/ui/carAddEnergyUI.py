# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.cfg import energyConfig
import copy
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
ViewBinder = clientApi.GetViewBinderCls()


class CarAddEnergyUI(ModBaseUI):
	"""载具 加能源UI"""
	def __init__(self, namespace, name, param):
		super(CarAddEnergyUI, self).__init__(namespace, name, param)
		# 能源
		self._energy = param.get("energy")
		self._maxEnergy = param.get("maxEnergy") + 0.0
		self._baseMaxEnergy = carConfig.BaseCarAttrConfig.get("maxEnergy", 100) + 0.0
		# 载具id
		self._entityId = param.get("entityId")
		# 点击一键选择时候增加能源数量（默认为一格，不满一格时候补充到一格）
		self._maxPreAddEnergy = self._maxEnergy/11
		# 玩家背包当中可以作为能源添加的材料列表：[{"newItemName": , "newAuxValue": , "count": }]
		self._playerHasMaterialList = []
		# 选择的材料数据: {(itemName, aux): count}
		self._selectMaterialDict = {}
		# 格子UI的对象表：{index: {"deduct": obj, "select": obj, "select_count": obj}}
		self._materialUIObjDict = {}

		# 获取可以添加能源的的物品字典
		self._energyItemsConfigDic = energyConfig._AddEnergyItems
		# ui界面中玩家拥有物品和未拥有时候的不同字体和背景颜色
		self._uiItemsColorConfigDic = energyConfig._uiItemsColor
		
		# 选中的格子
		self._selectIndex = None
		# 扣除按钮的映射
		self._deductBtnDict = {}

		# 当前新增的能源值
		self._addEnergy = 0

		# 提示的timer
		self._tipsTimer = None

		# 长按一键选择材料时选择材料的timer
		self._selectEnergyDonwTimer = None
		# 长按一键选择材料按钮时候的计时(-1代表当前不是长按状态计时，大于1时代表正在计时，用于update中删除)
		self._isSelectEnergyDonwTime = 0

		self._eventFunctions = {
			"close": self.CloseUI,
			"update_mat": self.UpdateMaterialUI,
		}

		self._createState = False
		pass

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		if self._tipsTimer:
			engineApiGac.CancelTimer(self._tipsTimer)
			self._tipsTimer = None
		pass

	def Create(self):
		# 界面
		self._energyPanel = self.GetBaseUIControl("/panel_energy")
		
		# 关闭按钮
		self._closeBtn = self._energyPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)

		# top
		topPanel = self._energyPanel.GetChildByPath("/panel_top")
		# 能源
		self._energyText = topPanel.GetChildByPath("/energy").asLabel()
		eneryBarBg = topPanel.GetChildByPath("/bar_energy").asImage()
		self._energyCurrentBar = eneryBarBg.GetChildByPath("/current").asImage()
		self._energyNextBar = eneryBarBg.GetChildByPath("/next").asImage()
		self._addEnergyLabel = topPanel.GetChildByPath("/add_energy").asLabel()
		# 左侧油量预警图标
		self._iconImg = topPanel.GetChildByPath("/icon").asImage()

		# buttom
		bottomPanel = self._energyPanel.GetChildByPath("/panel_bottom")
		# 材料框
		materialPanel = bottomPanel.GetChildByPath("/panel_materials")
		materialPanelPath = materialPanel.GetPath()
		self._materialView = ScrollViewWidget(self, materialPanelPath, "/btn_drag", 2)
		self._materialListView = ListViewWidget(self, materialPanelPath, "/btn_drag/panel", "/btn_drag/panel/material_1", self.SetMaterialInfo, self.OnSelectMaterialClicked, self._materialView, 0)
		# 添加按钮
		self._addEnergyBtn = bottomPanel.GetChildByPath("/btn_add_energy").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._addEnergyBtn, self.OnAddEnergyClicked)
		# 一键选择按钮
		self._selectEnergyBtn = bottomPanel.GetChildByPath("/btn_automatic_select_energy").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._selectEnergyBtn, self.OnSelectEnergyDonw,self.OnSelectEnergyUp)
		# 提示UI
		self._tipsLabel = bottomPanel.GetChildByPath("/tips").asLabel()


		Instance.mEventMgr.RegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)

		# 初始化
		self.InitUI()

		self._createState = True
		pass

	def Update(self):
		if self._createState:
			self._materialView.Update()
			self._materialListView.Update()
		if self._isSelectEnergyDonwTime> 0:
			self._isSelectEnergyDonwTime -= 1
		elif self._isSelectEnergyDonwTime == 0:
			self.PrePressSelectEnergy()
			self._isSelectEnergyDonwTime = -1
		pass

	def CarSubscribeEvent(self, args):
		"""载具订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass


	# region UI显示、关闭
	def InitUI(self):
		"""初始化UI"""
		self.UpdateMaterialUI()
		pass

	def UpdateMaterialUI(self, args={}):
		"""更新加能量UI、材料UI"""
		self.SetMaterialsUI()
		self.SetEnergyUI(args)
		pass

	def CloseUI(self, args=None):
		"""关闭UI"""
		clientApi.PopScreen()
		pass
	
	def IsCanAdd(self):
		"""是否可以加能源"""
		state = (self._addEnergy + self._energy) < self._maxEnergy
		if state is False:
			# 提示能源已满
			self.SetTips(1)
		return state

	def SetTips(self, tipsId):
		"""设置提示信息，tipsId没有对应的配置，则关闭提示"""
		text = carConfig.GetTips(tipsId)
		showState = False
		if self._tipsTimer:
			engineApiGac.CancelTimer(self._tipsTimer)
			self._tipsTimer = None
		if text:
			showState = True
			self._tipsLabel.SetText(text)
			# 延迟关闭
			self._tipsTimer = engineApiGac.AddTimer(3, clientApiMgr.SetUIVisible, self._tipsLabel, False)
		clientApiMgr.SetUIVisible(self._tipsLabel, showState)
		pass
	# endregion

	# region 能源UI
	def SetEnergyUI(self, args={}):
		"""设置能源UI"""
		energy = args.get("energy")
		if energy is None:
			energy = self._energy
		self._energy = int(energy)
		if self._energy>self._maxEnergy:
			self._energy = self._maxEnergy
		# 显示基于基础最大能源的百分比
		self._energyText.SetText("{:.2%}%%".format(self._energy / self._baseMaxEnergy))
		ratio = self._energy / self._maxEnergy
		ratio = 1 - ratio
		# 因贴图问题，对ratio需要做限制（贴图前后有部分是不属于进度条内容的，需要裁切）
		ratio = MathUtils.Lerp(0.045, 0.955, ratio)
		self._energyCurrentBar.SetSpriteClipRatio(ratio)
		self._energyNextBar.SetSpriteClipRatio(ratio)
		self.UpdateTryAddEnergyUI()
		# 如果能源低于某个百分比，则显示红色图标（低于的值根据UI计算）
		if 1 - ratio <= 0.165:
			self._iconImg.SetSpriteColor((0.82, 0.28, 0.28))
		else:
			self._iconImg.SetSpriteColor((0.08, 0.15, 0.14))
		pass

	def UpdateTryAddEnergyUI(self):
		"""设置加能量UI"""
		energy = 0
		for key, count in self._selectMaterialDict.iteritems():
			energy += carConfig.GetAddEnergyMaterialNum(key[0]) * count
		if energy > 0:
			addEnergy = self._energy + energy
			ratio = 1 - addEnergy / self._maxEnergy
			text = "+{:.2%}%%".format(energy / (self._maxEnergy + 0.0))
			# 判断当前是否一次性选择了加满，用于长按一键选择按钮时候
			if addEnergy >= self._maxEnergy:
				ratio = 0
				text = "+{:.2%}%%".format(1-self._energy/(self._maxEnergy + 0.0))
			self._energyNextBar.SetSpriteClipRatio(ratio)
			# 显示基于基础最大能源的百分比
			self._addEnergyLabel.SetText(text)
		else:
			# 关闭
			self._energyNextBar.SetSpriteClipRatio(1)
			self._addEnergyLabel.SetText("")
		# 修改按钮状态
		if energy > 0 and self._addEnergy <= 0:
			# 可点击
			clientApiMgr.SetButtonGray(self._addEnergyBtn, False)
			clientApiMgr.SetButtonTextColor(self._addEnergyBtn, electricConfig.NormalTextColor)
		elif energy <= 0 and self._addEnergy > 0:
			clientApiMgr.SetButtonGray(self._addEnergyBtn, True)
			clientApiMgr.SetButtonTextColor(self._addEnergyBtn, electricConfig.GrayTextColor)
		# 判断当前是否一次性选择了加满，用于长按一键选择按钮时候
		if energy+self._energy >= self._maxEnergy:
			self._addEnergy  = self._maxEnergy-self._energy
		else:
			self._addEnergy = energy
		pass
	# endregion
	# region 一键选择按钮
	def PreSelectEnergy(self):
		"""点击一键选择添加满到一格材料"""
		# 没有材料则进行返回
		if len(self._playerHasMaterialList) == 0:
			return
		# 判断当前是否选择材料是否可以添加满能源，如果是则提示
		if self._addEnergy +self._energy >= self._maxEnergy:
			self.SetTips(2)
			return
		playerHasMaterialList = copy.deepcopy(sorted(self._playerHasMaterialList, key=lambda x: self._energyItemsConfigDic.get(x['newItemName'], float('inf'))))
		# 如果有选择的材料则继承上一次的选择材料，在这基础上操作
		if self._selectMaterialDict:
			for item in playerHasMaterialList:
				key = (item['newItemName'], item['newAuxValue'])
				if key in self._selectMaterialDict:
					item['count'] -= self._selectMaterialDict[key]
		if self._energy >0:
			if self._energy+self._addEnergy < self._maxPreAddEnergy:
				needAddEnergy = self._maxPreAddEnergy-self._energy
			elif self._energy+self._addEnergy > self._maxPreAddEnergy:
				needAddEnergy = self._maxPreAddEnergy - (self._energy+self._addEnergy) % self._maxPreAddEnergy
			else:
				needAddEnergy = self._maxPreAddEnergy
		else:
			# 说明当前没有可添加能源
			if self._addEnergy == 0 and self._energy == 0:
				needAddEnergy = self._maxPreAddEnergy
			# 说明现在已有可添加能源不满一格
			elif  self._addEnergy % self._maxPreAddEnergy == 0:
				if self._addEnergy > 0:
					needAddEnergy = self._maxPreAddEnergy
				else:
					needAddEnergy = self._maxPreAddEnergy-self._addEnergy
			# 说明现在已有可添加能源超过一格
			else:
				needAddEnergy = self._maxPreAddEnergy-self._addEnergy % self._maxPreAddEnergy
		for item in playerHasMaterialList:
			count = item.get("count")
			newItemName = item.get("newItemName")
			newAuxValue = item.get("newAuxValue")
			itemEnergy = self._energyItemsConfigDic[newItemName]
			key = (newItemName,newAuxValue)
			if count*itemEnergy >= needAddEnergy:
				count -= int(abs(count*itemEnergy-needAddEnergy)/itemEnergy)
				if key in self._selectMaterialDict:
					self._selectMaterialDict[key] += count
				else:
					self._selectMaterialDict[key] = count
				break
			else:
				if key in self._selectMaterialDict:
					self._selectMaterialDict[key] += count
				else:
					self._selectMaterialDict[key] = count
				needAddEnergy -= count*itemEnergy
		
		self.UpdateTryAddEnergyUI()
		self._materialListView.UpdateView()
	def PrePressSelectEnergy(self):
		"""长按一键选择全部材料加满"""
		# 没有材料则进行返回
		if len(self._playerHasMaterialList) == 0:
			return
		# 判断当前是否选择材料是否可以添加满能源，如果是则提示
		if self._addEnergy +self._energy >= self._maxEnergy:
			self.SetTips(2)
			return
		# 清空当前选择的材料并刷新ui
		if self._selectMaterialDict:
			self._selectMaterialDict.clear()
			self._materialListView.UpdateView()
			self._addEnergy = 0
		# 对玩家拥有的材料按能源值进行从小到大排序
		playerHasMaterialList = copy.deepcopy(sorted(self._playerHasMaterialList, key=lambda x: self._energyItemsConfigDic.get(x['newItemName'], float('inf'))))
		for item in playerHasMaterialList:
			count = item.get("count")
			newItemName = item.get("newItemName")
			newAuxValue = item.get("newAuxValue")
			itemEnergy = self._energyItemsConfigDic[newItemName]
			key = (newItemName,newAuxValue)
			# 判断当前选择材料是否可以加满一格或全部
			if self._energy+self._addEnergy+count*itemEnergy >=self._maxEnergy:
				count -= int(abs(self._maxEnergy-(self._energy+self._addEnergy+count*itemEnergy))/itemEnergy)
				self._selectMaterialDict[key] = count
				self._addEnergy +=count*itemEnergy
				break
			else:
				self._selectMaterialDict[key] = count
				self._addEnergy +=count*itemEnergy
		self.UpdateTryAddEnergyUI()
		self._materialListView.UpdateView()
	# endregion

	# region 材料UI
	def SetTryAddEnergy(self):
		"""设置加能量"""
		if self._addEnergy > 0:
			# 发数据到服务端，扣除物品、加能源
			info = {
				"to_server": True,	# 转发
				"stage": "add_energy",
				"entityId": self._entityId,
				"materials": self._selectMaterialDict,
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, info)
		pass

	def SetMaterialsUI(self):
		"""设置能源材料UI"""
		# 重置数据，不重置selectIndex，还需要根据该值去关闭选中框
		self._addEnergy = 0
		self._selectMaterialDict.clear()
		self._materialUIObjDict.clear()
		# 获取玩家背包物品
		itemCountDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		# 筛选玩家背包中有的可加能源的物品
		materialList = []
		materialNotPlayerList = []
		itemCountDict = itemCountDict.iteritems()
		if itemCountDict:
			for item, count in itemCountDict:
				if self._energyItemsConfigDic.get(item[0], 0) > 0:
					if item[0] in self._energyItemsConfigDic:
						materialList.append({"newItemName": item[0], "newAuxValue": item[1], "count": count}) 
		self._playerHasMaterialList = materialList
		# 筛选玩家背包中没有的可加能源的物品
		if materialList:
			materialNameList = []
			for material in materialList:
				materialNameList.append(material['newItemName'])
			for energyItems in self._energyItemsConfigDic:
				if energyItems not in materialNameList:
					materialNotPlayerList.append({'newItemName':energyItems,'newAuxValue': 0, 'count': 0})
		else:
			for energyItems in self._energyItemsConfigDic:
				materialNotPlayerList.append({'newItemName':energyItems,'newAuxValue': 0, 'count': 0})
		self._materialListView.UpdateData(materialList + materialNotPlayerList)
		pass

	def SetSelectMaterial(self, ctrl, item, index, updateUI=False):
		"""设置选择的材料"""
		# 判断是否满能源,如果不能添加
		# self._addEnergy += self._energyItemsConfigDic[item.get("newItemName")]
		if updateUI or self.IsCanAdd():
			key = (item.get("newItemName"), item.get("newAuxValue"))
			# 更新选择的数量
			count = self._selectMaterialDict.get(key, 0)
			if updateUI:
				# 仅刷新UI
				count = min(item.get("count", 0), count)
				# 如果是当前选中的，则显示选中框，否则隐藏
				selectObj = ctrl.GetChildByPath("/panel/select")
				if self._selectIndex == index:
					clientApiMgr.SetUIVisible(selectObj, True)
				else:
					clientApiMgr.SetUIVisible(selectObj, False)
			else:
				if count >= item.get("count", 0):
					return
				# 选中操作
				count = min(item.get("count", 0), count + electricConfig.SelectMaterialCount)
				self._selectMaterialDict[key] = count
				# 更新增加能源UI
				self.UpdateTryAddEnergyUI()
				# 刷新窗口内的控件
				self._selectIndex = index
				self._materialListView.UpdateView()
			
			# 选择数量显示
			selectCountObj = ctrl.GetChildByPath("/panel/select_count").asLabel()
			selectCountObj.SetText(str(count))
			selectCountObj.SetVisible(count > 0)
			# 删除按钮
			deductObj = ctrl.GetChildByPath("/panel/btn_deduct").asButton()
			clientApiMgr.SetUIVisible(deductObj, True)
			deductPath = deductObj.GetPath()
			if self._deductBtnDict.get(deductPath) is not True:
				clientApiMgr.SetBtnTouchUpCallback(deductObj, self.OnDeductMaterialClicked)
			self._deductBtnDict[deductPath] = index
		# else:
		# 	self._addEnergy -= self._energyItemsConfigDic[item.get("newItemName")]
		pass
	
	def SetDeductMaterialSelected(self, index, ctrl=None):
		"""扣除材料的选中"""
		if ctrl is None:
			# 点击扣除按钮操作
			# 清除材料的数据
			item = self._materialListView.GetDataFromIndex(index)
			if item:
				key = (item.get("newItemName"), item.get("newAuxValue"))
				self._selectMaterialDict.pop(key, None)
			# 刷新窗口内的控件
			self._materialListView.UpdateView()
			# 更新增加能源UI
			self.UpdateTryAddEnergyUI()
			# 更新材料选择UI
			self._materialListView.UpdateView()
		else:
			# 刷新UI
			# 选中框
			selectObj = ctrl.GetChildByPath("/panel/select")
			clientApiMgr.SetUIVisible(selectObj, self._selectIndex == index)
			# 选择数量显示
			selectCountObj = ctrl.GetChildByPath("/panel/select_count").asLabel()
			if selectCountObj:
				selectCountObj.SetText("")
				clientApiMgr.SetUIVisible(selectCountObj, False)
			# 删除按钮
			deductObj = ctrl.GetChildByPath("/panel/btn_deduct")
			clientApiMgr.SetUIVisible(deductObj, False)
		pass
	
	def SetMaterialInfo(self, path, ctrl, index, data):
		"""设置单个材料的物品UI"""
		itemName = data.get("newItemName")
		count = data.get("count", 0)
		aux = data.get("newAuxValue", 0)
		itemObj = ctrl.GetChildByPath("/panel/item").asItemRenderer()
		itemObj.SetUiItem(itemName, aux)
		countObj = ctrl.GetChildByPath("/panel/count").asLabel()
		countObj.SetText('x%d' % count)
		imageObj = ctrl.GetChildByPath("/panel").asImage()
		notObj = ctrl.GetChildByPath("/panel/not").asImage()
		notObj.SetVisible(count == 0)
		if count == 0:
			countObj.SetTextColor(self._uiItemsColorConfigDic['materialNotPlayerTextColor'])
			imageObj.SetSpriteColor(self._uiItemsColorConfigDic['materialNotPlayerSpriteColor'])
		else:
			countObj.SetTextColor(self._uiItemsColorConfigDic['materialTextColor'])
			imageObj.SetSpriteColor(self._uiItemsColorConfigDic['materialSpriteColor'])
		wattObj = ctrl.GetChildByPath("/panel/watt").asLabel()
		if itemName in self._energyItemsConfigDic:
			wattObj.SetText(str(self._energyItemsConfigDic[itemName]))
		# 设置选中状态
		if self._selectMaterialDict.get((itemName, aux), 0) > 0:
			self.SetSelectMaterial(ctrl, data, index, updateUI=True)
		else:
			# 清除选中效果
			self.SetDeductMaterialSelected(index, ctrl)
		pass

	def GetMaterialSubObj(self, index, subPath, matObj=None):
		"""获取材料的子控件"""
		objVal = self._materialUIObjDict.get(index)
		if not objVal:
			objVal = {}
			self._materialUIObjDict[index] = objVal
		obj = objVal.get(subPath)
		if not obj and matObj:
			obj = matObj.GetChildByPath(subPath)
			if obj:
				if subPath == "/panel/item":
					obj = obj.asItemRenderer()
				elif subPath == "/panel/select_count":
					obj = obj.asLabel()
				elif subPath == "/panel/count":
					obj = obj.asLabel()
				elif subPath == "/panel/btn_deduct":
					obj = obj.asButton()
					clientApiMgr.SetBtnTouchUpCallback(obj, self.OnDeductMaterialClicked, {"index": index})
			objVal[subPath] = obj
		return obj
	# endregion

	# region 按钮
	def OnCloseClicked(self, args):
		"""关闭UI"""
		self.CloseUI()
		pass

	def OnSelectMaterialClicked(self, path, ctrl, index, data, args):
		"""点击材料物品"""
		self.SetSelectMaterial(ctrl, data, index)
		pass

	def OnDeductMaterialClicked(self, args):
		"""点击扣除材料按钮"""
		buttonPath = args.get("ButtonPath")
		index = self._deductBtnDict.get(buttonPath)
		self.SetDeductMaterialSelected(index)
		pass

	def OnAddEnergyClicked(self, args):
		"""点击加能量按钮"""
		self.SetTryAddEnergy()
		pass
	
	def OnSelectEnergyDonw(self,args):
		"""点击一键选择按钮"""
		self._isSelectEnergyDonwTime = 60

	def OnSelectEnergyUp(self,args):
		"""松开一键选择按钮"""
		if self._isSelectEnergyDonwTime >0:
			self.PreSelectEnergy()
			self._isSelectEnergyDonwTime = -1
	# endregion
