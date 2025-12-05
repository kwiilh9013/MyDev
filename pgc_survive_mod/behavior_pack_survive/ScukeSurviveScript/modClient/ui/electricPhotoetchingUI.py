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
from ScukeSurviveScript.modCommon.cfg.electric.electricRecipeConfig import GetElectricWorkbenchRecipes, GetElectricItemRecipe
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class ElectricPhotoetchingUI(ModBaseUI):
	"""光刻机UI"""
	def __init__(self, namespace, name, param):
		super(ElectricPhotoetchingUI, self).__init__(namespace, name, param)
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
		super(ElectricPhotoetchingUI, self).Destroy()
		self._createState = False
		if self._craftingTimer:
			engineApiGac.CancelTimer(self._craftingTimer)
			self._craftingTimer = None
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricUISubscriptEvent, self.ElectricUISubscriptEvent)
		pass

	def Create(self):
		super(ElectricPhotoetchingUI, self).Create()
		# 光刻机UI
		photoetchingPanel = self.GetBaseUIControl("/panel_photoetching")

		# 关闭按钮
		self._closeBtn = photoetchingPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)

		# 标题
		self._title = photoetchingPanel.GetChildByPath("/title").asLabel()
		self._workStateText = self._title.GetChildByPath("/work_state").asLabel()
		self._workStateTextBg = self._workStateText.GetChildByPath("/bg").asImage()
		self._workStateTextPoint = self._workStateText.GetChildByPath("/point").asImage()
		self._kwText = self._workStateText.GetChildByPath("/bg_line/kw").asLabel()

		# left
		leftPanel = photoetchingPanel.GetChildByPath("/panel_left")
		# 滚动框
		listPanel = leftPanel.GetChildByPath("/sroll_view")
		listPath = listPanel.GetPath()
		self._craftItemView = ScrollViewWidget(self, listPath, "/btn_drag", 1)
		self._craftListView = ListViewWidget(self, listPath, "/btn_drag/panel", "/btn_drag/panel/item_base", self.SetCraftListItemInfo, self.OnSelectCraftItemClicked, self._craftItemView, 2)
		# 向下箭头，用来提示还有内容，可以往下滑动
		self._craftListViewArrow = listPanel.GetChildByPath("/next")

		# center
		centerPanel = photoetchingPanel.GetChildByPath("/panel_center")
		centerCompositePanel = centerPanel.GetChildByPath("/panel_item_composite")
		# 左上
		input1 = centerCompositePanel.GetChildByPath("/input1_panel")
		self._craftInputItemIconTopLeft = input1.GetChildByPath("/image_item_slot_input1/item_input").asItemRenderer()
		self._craftInputLeftLine1 = input1.GetChildByPath("/left_line1").asImage()
		self._craftInputLeftDisLine1 = input1.GetChildByPath("/left_disline1").asImage()
		self._craftInputItemIconTopLeftCount = input1.GetChildByPath("/image_item_slot_input1/count").asLabel()
		# 右上
		input2 = centerCompositePanel.GetChildByPath("/input2_panel")
		self._craftInputItemIconTopRight = input2.GetChildByPath("/image_item_slot_input2/item_input").asItemRenderer()
		self._craftInputRightLine2 = input2.GetChildByPath("/right_line2").asImage()
		self._craftInputRightDisLine2 = input2.GetChildByPath("/right_disline2").asImage()
		self._craftInputItemIconTopRightCount = input2.GetChildByPath("/image_item_slot_input2/count").asLabel()
		# 左下
		input3 = centerCompositePanel.GetChildByPath("/input3_panel")
		self._craftInputItemIconLowerLeft = input3.GetChildByPath("/image_item_slot_input3/item_input").asItemRenderer()
		self._craftInputLeftLine2 = input3.GetChildByPath("/left_line2").asImage()
		self._craftInputLeftDisLine2 = input3.GetChildByPath("/left_disline2").asImage()
		self._craftInputItemIconLowerLeftCount = input3.GetChildByPath("/image_item_slot_input3/count").asLabel()
		# 右下
		input4 = centerCompositePanel.GetChildByPath("/input4_panel")
		self._craftInputItemIconLowerRight = input4.GetChildByPath("/image_item_slot_input4/item_input").asItemRenderer()
		self._craftInputRightLine1 =input4.GetChildByPath("/right_line1").asImage()
		self._craftInputRightDisLine1 = input4.GetChildByPath("/right_disline1").asImage()
		self._craftInputItemIconLowerRightCount = input4.GetChildByPath("/image_item_slot_input4/count").asLabel()
		# 中输出合成物品
		self._craftOutputItemIcon = centerCompositePanel.GetChildByPath("/image_item_slot_output/item_ouput").asItemRenderer()

		# right
		rightPanel = photoetchingPanel.GetChildByPath("/panel_right")
		# 物品信息
		self.craftItemName = rightPanel.GetChildByPath("/item_name").asLabel()
		self._craftItemTips = rightPanel.GetChildByPath("/panel/btn_drag/tips").asLabel()
		self._craftItemTipsView = ScrollViewWidget(self, rightPanel.GetPath() + "/panel", "/btn_drag", 1)
		# 材料
		matPanel = rightPanel.GetChildByPath("/panel_materials")
		# 合成按钮
		self._craftBtn = matPanel.GetChildByPath("/btn_craft").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._craftBtn, self.OnCraftClicked)

		# 合成进度
		self._craftingBarPanel = photoetchingPanel.GetChildByPath("/panel_crafting")
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
		# 设置工作状态ui
		self.SetWorkStateUI()
		# 设置初始状态左侧合成ui
		craftList = self._craftListCfg
		self._craftListView.UpdateData(craftList)
		if len(craftList) > 8:
			clientApiMgr.SetUIVisible(self._craftListViewArrow, True)
		else:
			clientApiMgr.SetUIVisible(self._craftListViewArrow, False)
		# 设置功率
		self._kwText.SetText("功率：{} W".format(self._kw))

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
				# 显示合成物品
				self._craftOutputItemIcon.SetUiItem(self._selectCraftItemName, item.get("newAuxValue", 0))
				# 显示详情
				name = clientApiMgr.GetItemHoverName(item)
				self.craftItemName.SetText(name)
				tips = clientApiMgr.GetItemHoverText(item)
				self._craftItemTips.SetText(tips)
				# 显示材料
				self.SetMaterialsUIAndItemInfo()
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
				ctrl.asImage().SetSpriteColor(electricConfig.PhotoetchingSelectTextColor)
			elif index == self._selectCraftItemIndex:
				ctrl.asImage().SetSpriteColor(electricConfig.PhotoetchingSelectTextColor)
			else:
				ctrl.asImage().SetSpriteColor(electricConfig.PhotoetchingNormalTextColor)
		pass
	# endregion

	# region 材料信息
	def SetMaterialsUIAndItemInfo(self):
		"""设置物品的UI和材料信息"""
		# 重置按钮状态
		self._hasEnoughMaterials = True
		self.SetCraftBtnState(True)

		recipe = GetElectricItemRecipe(self._selectCraftItemName)
		recipeInput = recipe.get("input", [])
		recipeInputCount = len(recipeInput)
		# 合成配方种类对应数量对应的icon和文字数量
		recipeInputDic = {
		1:{"ItemRenderer":self._craftInputItemIconTopLeft,"Label":self._craftInputItemIconTopLeftCount,"Line":self._craftInputLeftLine1,"DisLine":self._craftInputLeftDisLine1},
   		2:{"ItemRenderer":self._craftInputItemIconTopRight,"Label":self._craftInputItemIconTopRightCount,"Line":self._craftInputRightLine2,"DisLine":self._craftInputRightDisLine2},
		3:{"ItemRenderer":self._craftInputItemIconLowerLeft,"Label":self._craftInputItemIconLowerLeftCount,"Line":self._craftInputLeftLine2,"DisLine":self._craftInputLeftDisLine2},
		4:{"ItemRenderer":self._craftInputItemIconLowerRight,"Label":self._craftInputItemIconLowerRightCount,"Line":self._craftInputRightLine1,"DisLine":self._craftInputRightDisLine1}}
		# 获取玩家背包物品
		if self._inventoryCountDict is None:
			self._inventoryCountDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		if recipeInputCount in recipeInputDic:
			# 判断配方种类数量是否在0 到 4之间
			for index in range(recipeInputCount):
				# 遍历input材料，根据数量和四个格位一一对应
				itemData = recipeInput[index]
				# 物品id,aux和数量
				itemName = itemData.get("newItemName")
				itemAux = itemData.get("newAuxValue", 0)
				itemCount = itemData.get("count", 1)
				# 对应格子的物品icon和数量
				itemObj = recipeInputDic[index+1]['ItemRenderer']
				itemNameObj = recipeInputDic[index+1]['Label']
				# 对应格子的合成线
				line = recipeInputDic[index+1]["Line"]
				disLine = recipeInputDic[index+1]["DisLine"]
				# 对应物品在玩家背包的数量
				hasCount = self._inventoryCountDict.get((itemName, itemAux), 0)
				redStr = "§f"
				if itemCount >	hasCount:
					redStr = "§c"
					self._hasEnoughMaterials = False
					# 按钮改成材料不足
					self.SetCraftBtnState(False)
					clientApiMgr.SetUIVisible(line,False)
					clientApiMgr.SetUIVisible(disLine,True)
				else:
					clientApiMgr.SetUIVisible(disLine,False)
					clientApiMgr.SetUIVisible(line,True)
				# 设置icon,名字数量
				itemObj.SetUiItem(itemName, itemAux)
				name = clientApiMgr.GetItemHoverName(itemData)
				itemNameObj.SetText("{} {}{}/{}".format(name, redStr, itemCount, hasCount))
		else:
			print self._selectCraftItemName+'该物品光刻机配方有误超过了4种'
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
			self.SetMaterialsUIAndItemInfo()
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

	# region 设置光刻机动画
	def SetWorkAnime(self,state):
		blockComp = compFactory.CreateBlockInfo(self.mLevelId)
		setBlockEntityMolangValue = blockComp.SetBlockEntityMolangValue
		if state:
			setBlockEntityMolangValue(self._pos,'variable.working_state', 1.0)
		else:
			setBlockEntityMolangValue(self._pos,'variable.working_state', 0.0)
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
