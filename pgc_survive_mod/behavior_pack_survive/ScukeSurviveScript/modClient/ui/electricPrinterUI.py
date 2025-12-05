# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.widget.tabViewWidget import TabViewWidget
from ScukeSurviveScript.modCommon.cfg.electric.electricRecipeConfig import GetElectricWorkbenchRecipes, GetElectricItemRecipe
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class ElectricPrinterUI(ModBaseUI):
	"""打印机UI"""
	def __init__(self, namespace, name, param):
		super(ElectricPrinterUI, self).__init__(namespace, name, param)
		self._blockName = param.get("blockName")
		self._pos = param.get("pos")
		self._dimension = param.get("dimension")
		# 是否有电力供应
		self._hasDynamo = param.get("dynamo")

		# 唯一key
		self._key = param.get("key")

		# cfg数据
		self._cfg = electricConfig.GetElectricConfig(self._blockName)
		self._kw = self._cfg.get("kw")

		# 合成列表数据
		self._craftListCfg = GetElectricWorkbenchRecipes(self._blockName)

		# 当前选中的分页索引
		self._selectTabIndex = 0
		# 当前选中的合成物品对象
		self._selectCraftItemIndex = None
		# 当前选中的物品id
		self._selectCraftItemName = None

		# 玩家背包内的物品数据
		self._inventoryCountDict = None
		# 材料是否充足
		self._hasEnoughMaterials = False

		# 合成进度timer间隔
		self._craftingInterval = 0.05
		# 合成进度timer
		self._craftingTimer = None
		# 合成进度计时
		self._craftingTime = 0
		self._craftingTotalTime = 0

		self._eventFunctions = {
			"close": self.CloseUI,
			"update_dynamo": self.SetWorkStateUI,
		}

		self._createState = False
		pass

	def Destroy(self):
		super(ElectricPrinterUI, self).Destroy()
		self._createState = False
		if self._craftingTimer:
			engineApiGac.CancelTimer(self._craftingTimer)
			self._craftingTimer = None
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricUISubscriptEvent, self.ElectricUISubscriptEvent)
		pass

	def Create(self):
		super(ElectricPrinterUI, self).Create()
		# 发电机UI
		printerPanel = self.GetBaseUIControl("/panel_printer")

		# 关闭按钮
		self._closeBtn = printerPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)

		# 标题
		self._title = printerPanel.GetChildByPath("/title").asLabel()
		self._workStateText = self._title.GetChildByPath("/work_state").asLabel()
		self._workStateTextBg = self._workStateText.GetChildByPath("/bg").asImage()
		self._workStateTextPoint = self._workStateText.GetChildByPath("/point").asImage()
		self._kwText = self._workStateText.GetChildByPath("/bg_line/kw").asLabel()

		# left
		leftPanel = printerPanel.GetChildByPath("/panel_left")
		# 滚动框
		listPanel = leftPanel.GetChildByPath("/sroll_view")
		listPath = listPanel.GetPath()
		self._craftItemView = ScrollViewWidget(self, listPath, "/btn_drag", 1)
		self._craftListView = ListViewWidget(self, listPath, "/btn_drag/panel", "/btn_drag/panel/item_base", self.SetCraftListItemInfo, self.OnSelectCraftItemClicked, self._craftItemView, 2)
		# 向下箭头，用来提示还有内容，可以往下滑动
		self._craftListViewArrow = listPanel.GetChildByPath("/next")
		# 分页
		tabsPanel = leftPanel.GetChildByPath("/panel_tabs")
		self._craftTabView = TabViewWidget(self, tabsPanel.GetPath(), [
			"/stack_panel/btn_gun",
			"/stack_panel/btn_bullet",
			"/stack_panel/btn_item",
			"/stack_panel/btn_melee_weapons",
			"/stack_panel/btn_armor",
			"/stack_panel/btn_carpart",
		], None, self.OnCratTabChanged)

		# center
		centerPanel = printerPanel.GetChildByPath("/panel_center")
		self._craftItemDoll = centerPanel.GetChildByPath("/input_panel_item_model/paper_doll").asNeteasePaperDoll()
		self._craftItemIcon = centerPanel.GetChildByPath("/item").asItemRenderer()

		# right
		rightPanel = printerPanel.GetChildByPath("/panel_right")
		# 物品信息
		self.craftItemName = rightPanel.GetChildByPath("/item_name").asLabel()
		self._craftItemTips = rightPanel.GetChildByPath("/panel/btn_drag/tips").asLabel()
		self._craftItemTipsView = ScrollViewWidget(self, rightPanel.GetPath() + "/panel", "/btn_drag", 1)
		# 材料
		matPanel = rightPanel.GetChildByPath("/panel_materials")
		matViewPanel = matPanel.GetChildByPath("/sroll_view")
		matViewPath = matViewPanel.GetPath()
		self._materialScrollView = ScrollViewWidget(self, matViewPath, "/btn_drag", 1)
		self._materialListView = ListViewWidget(self, matViewPath, "/btn_drag/panel", "/btn_drag/panel/material_base", self.SetMaterialItemInfo, None, self._materialScrollView, 0)
		# 向下箭头，用来提示还有内容，可以往下滑动
		self._matViewDownArrow = matViewPanel.GetChildByPath("/next")

		# 合成按钮
		self._craftBtn = matPanel.GetChildByPath("/btn_craft").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._craftBtn, self.OnCraftClicked)

		# 合成进度
		self._craftingBarPanel = printerPanel.GetChildByPath("/panel_crafting")
		self._craftingBar = self._craftingBarPanel.GetChildByPath("/bar").asProgressBar()
		
		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricUISubscriptEvent, self.ElectricUISubscriptEvent)

		# 初始化
		self.InitUI()

		self._createState = True
		pass

	def Update(self):
		if self._createState:
			self._craftItemView.Update()
			self._craftListView.Update()
			self._materialScrollView.Update()
			self._materialListView.Update()
			self._craftItemTipsView.Update()
		pass

	def ElectricUISubscriptEvent(self, args):
		"""电器订阅事件"""
		key = args.get("key")
		blockName = args.get("blockName")
		dimension = args.get("dimension")
		pos = args.get("pos")
		if key == self._key or (blockName == self._blockName and dimension == self._dimension and pos == self._pos):
			stage = args.get("stage")
			func = self._eventFunctions.get(stage)
			if func:
				func(args)
		pass

	# region UI显示、关闭
	def InitUI(self):
		"""初始化UI"""
		# 初始化选中第一个分页，在TabViewWidget中处理了
		self.SetWorkStateUI()
		# 设置功率
		self._kwText.SetText("功率：{} W".format(self._kw))
		pass

	def CloseUI(self, args=None):
		"""关闭UI"""
		canClose = True
		if args:
			canClose = False
			if self._blockName == args.get("blockName"):
				if self._dimension == args.get("dimension"):
					if self._pos == args.get("pos"):
						canClose = True
		if canClose:
			clientApi.PopScreen()
		pass

	def SetWorkStateUI(self, args={}):
		"""设置供电状态UI"""
		hanDynamo = args.get("dynamo")
		if hanDynamo is None:
			hanDynamo = self._hasDynamo
		self._hasDynamo = hanDynamo
		if hanDynamo:
			self._workStateText.SetText("电力供应中")
			self._workStateText.SetTextColor(electricConfig.WorkTextColor2)
			self._workStateTextBg.SetSpriteColor(electricConfig.WorkTextBgColor2)
			self._workStateTextPoint.SetSpriteColor(electricConfig.WorkTextColor2)
			self.SetCraftBtnState(self._hasEnoughMaterials)
		else:
			self._workStateText.SetText("电力未供应")
			self._workStateText.SetTextColor(electricConfig.WorkTextColor1)
			self._workStateTextBg.SetSpriteColor(electricConfig.WorkTextBgColor1)
			self._workStateTextPoint.SetSpriteColor(electricConfig.WorkTextColor1)
			self.SetCraftBtnState(False)
		pass

	def SetCraftBtnState(self, state):
		"""设置合成按钮状态"""
		text = "合成"
		if not self._hasDynamo:
			text = "电力不足"
			clientApiMgr.SetButtonGray(self._craftBtn, True)
		else:
			if state:
				clientApiMgr.SetButtonGray(self._craftBtn, False)
			else:
				text = "材料不足"
				clientApiMgr.SetButtonGray(self._craftBtn, True)
		clientApiMgr.SetButtonText(self._craftBtn, text)
		pass

	# endregion

	# region 合成物品列表
	def SetSelectTabs(self, index):
		"""设置选中的分页"""
		self._selectTabIndex = index
		self._selectCraftItemIndex = None
		# 更新列表
		key = self._craftListCfg["tabs"][self._selectTabIndex]
		craftList = self._craftListCfg[key]
		self._craftListView.UpdateData(craftList)
		# 如果数量超过8个，就显示箭头（根据UI效果而定）
		if len(craftList) > 8:
			clientApiMgr.SetUIVisible(self._craftListViewArrow, True)
		else:
			clientApiMgr.SetUIVisible(self._craftListViewArrow, False)
		pass

	def SetSelectCraftItem(self, ctrl, index, data):
		"""设置选中合成物品"""
		if self._selectCraftItemIndex != index:
			# 选中
			if self._selectCraftItemIndex is None:
				# 初次选中，不刷新
				self._selectCraftItemIndex = index
			else:
				self._selectCraftItemIndex = index
				# 刷新窗口所有控件（目的是刷新选中状态）
				self._craftListView.UpdateView()
			item = data.get("item")
			if item:
				self._selectCraftItemName = item.get("newItemName")
				# 显示模型
				if data.get("view_model"):
					self._craftItemDoll.RenderEntity(data["view_model"])
					clientApiMgr.SetUIVisible(self._craftItemDoll, True)
					clientApiMgr.SetUIVisible(self._craftItemIcon, False)
				else:
					self._craftItemIcon.SetUiItem(self._selectCraftItemName, item.get("newAuxValue", 0))
					clientApiMgr.SetUIVisible(self._craftItemIcon, True)
					clientApiMgr.SetUIVisible(self._craftItemDoll, False)
				# 显示详情
				name = clientApiMgr.GetItemHoverName(item)
				self.craftItemName.SetText(name)
				tips = clientApiMgr.GetItemHoverText(item)
				self._craftItemTips.SetText(tips)
				# 显示材料
				self.SetMaterialsUI()
		pass

	def SetCraftListItemInfo(self, path, ctrl, index, data):
		"""设置合成物品列表slot信息"""
		item = data.get("item")
		if item:
			itemName = item.get("newItemName")
			itemObj = ctrl.GetChildByPath("/item").asItemRenderer()
			itemObj.SetUiItem(itemName, item.get("newAuxValue", 0))
			name = clientApiMgr.GetItemHoverName(item)
			nameObj = ctrl.GetChildByPath("/name").asLabel()
			nameObj.SetText(name)
			# 设置选中效果
			if self._selectCraftItemIndex is None and index == 0:
				# 选择第一项
				self.SetSelectCraftItem(ctrl, index, data)
				ctrl.asImage().SetSpriteColor(electricConfig.PrinterSelectTextColor)
			elif index == self._selectCraftItemIndex:
				ctrl.asImage().SetSpriteColor(electricConfig.PrinterSelectTextColor)
			else:
				ctrl.asImage().SetSpriteColor(electricConfig.PrinterNormalTextColor)
		pass
	# endregion

	# region 材料信息
	def SetMaterialsUI(self):
		"""设置物品的材料信息"""
		# 重置按钮状态
		self._hasEnoughMaterials = True
		self.SetCraftBtnState(True)
		clientApiMgr.SetUIVisible(self._matViewDownArrow, False)
		# 刷新列表
		recipe = GetElectricItemRecipe(self._selectCraftItemName)
		self._materialListView.UpdateData(recipe.get("input", []))
		pass

	def SetMaterialItemInfo(self, path, ctrl, index, data):
		"""设置材料信息"""
		itemName = data.get("newItemName")
		aux = data.get("newAuxValue", 0)
		# icon
		itemObj = ctrl.GetChildByPath("/icon").asItemRenderer()
		itemObj.SetUiItem(itemName, aux)
		# 玩家背包物品
		if self._inventoryCountDict is None:
			self._inventoryCountDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		count = data.get("count", 1)
		hasCount = self._inventoryCountDict.get((itemName, aux), 0)
		redStr = ""
		# 材料是否充足
		if count > hasCount:
			redStr = "§c"
			self._hasEnoughMaterials = False
			# 按钮改成材料不足
			self.SetCraftBtnState(False)
		# 名字 + 数量
		name = clientApiMgr.GetItemHoverName(data)
		nameObj = ctrl.GetChildByPath("/name").asLabel()
		self._hasEnoughMaterials
		nameObj.SetText("{} {}{}/{}".format(name, redStr, count, hasCount))
		# 如果index超过3，则显示下拉的箭头
		if index == 3:
			clientApiMgr.SetUIVisible(self._matViewDownArrow, True)
		pass
	# endregion

	# region 合成操作
	def SetCrafting(self):
		"""设置合成操作"""
		# 校验
		if self._hasDynamo:
			if self._hasEnoughMaterials:
				# 显示合成进度
				self.SetCraftingBarUI(True)
		pass

	def SetCraftingBarUI(self, state):
		"""设置合成进度UI"""
		clientApiMgr.SetUIVisible(self._craftingBarPanel, state)
		if state:
			# 获取合成时间
			self._craftingTime = 0
			recipe = GetElectricItemRecipe(self._selectCraftItemName)
			if recipe:
				self._craftingTotalTime = recipe.get("time", 0)
			# 重置UI进度
			self._craftingBar.SetValue(0)
			# 启动timer
			if not self._craftingTimer:
				self._craftingTimer = engineApiGac.AddRepeatedTimer(self._craftingInterval, self.UpdateCraftingBarTimer)
		else:
			# 停止timer
			if self._craftingTimer:
				engineApiGac.CancelTimer(self._craftingTimer)
				self._craftingTimer = None
			# 刷新剩余材料物品
			self._inventoryCountDict = None
			self.SetMaterialsUI()
		pass

	def UpdateCraftingBarTimer(self):
		"""更新合成进度UI"""
		if self._craftingTime < self._craftingTotalTime:
			self._craftingTime += self._craftingInterval
			rate = self._craftingTime / self._craftingTotalTime
			self._craftingBar.SetValue(rate)
			if rate >= 1.0:
				# 进度跑满
				# 发消息到服务端，服务端给物品
				info = {
					"to_server": True,
					"stage": "craft",
					"key": self._key,
					"item": self._selectCraftItemName,
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.ElectricSubscriptEvent, info)
				# 延迟关闭UI
				engineApiGac.AddTimer(0.1, self.SetCraftingBarUI, False)
		pass
	# endregion


	# region 按钮
	def OnCloseClicked(self, args):
		"""关闭UI"""
		self.CloseUI()
		pass

	def OnCratTabChanged(self, prev, current):
		"""选中分页"""
		self.SetSelectTabs(current)
		pass
	
	def OnSelectCraftItemClicked(self, path, ctrl, index, data, args):
		"""点击合成列表中的物品"""
		self.SetSelectCraftItem(ctrl, index, data)
		pass
	
	def OnCraftClicked(self, args):
		"""合成按钮"""
		self.SetCrafting()
		pass
	# endregion
