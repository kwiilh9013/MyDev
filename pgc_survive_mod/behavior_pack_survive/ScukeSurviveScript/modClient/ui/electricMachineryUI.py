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
from ScukeSurviveScript.modCommon.cfg.electric.electricRecipeConfig import GetElectricWorkbenchRecipes, GetElectricItemRecipe ,GetElectricItemRepairRecipe
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class ElectricMachineryUI(ModBaseUI):
	"""机械工作台UI"""
	def __init__(self, namespace, name, param):
		super(ElectricMachineryUI, self).__init__(namespace, name, param)
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
		self._craftDicCfg = GetElectricWorkbenchRecipes(self._blockName)

		# 当前选中的状态，默认显示强化界面
		self._isSelectEnhancementTab = False
		# 强化功能研发中提示销毁timer id
		self._tipsTimer = None
		
		# 当前选中的合成物品对象
		self._selectCraftItemIndex = None
		# 当前选中的物品id和axu
		self._selectCraftItemName = {}
		# 物品耐久度字典
		self._itemDurabilityDic = {}
		# 物品修复所需要的材料字典
		self._repairMaterialsDic = {}

		# 玩家背包内的物品数量数据
		self._inventoryCountDict = None
		# 玩家背包物品槽位数据
		self._inventorySlotDict = None
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
		super(ElectricMachineryUI, self).Destroy()
		self._createState = False
		if self._craftingTimer:
			engineApiGac.CancelTimer(self._craftingTimer)
			self._craftingTimer = None
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricUISubscriptEvent, self.ElectricUISubscriptEvent)
		pass

	def Create(self):
		super(ElectricMachineryUI, self).Create()
		# 机械工作台UI
		machineryPanel = self.GetBaseUIControl("/panel_machinery")

		# 关闭按钮
		self._closeBtn = machineryPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)

		# 标题
		self._title = machineryPanel.GetChildByPath("/title").asLabel()
		self._workStateText = self._title.GetChildByPath("/work_state").asLabel()
		self._workStateTextBg = self._workStateText.GetChildByPath("/bg").asImage()
		self._workStateTextPoint = self._workStateText.GetChildByPath("/point").asImage()
		self._kwText = self._workStateText.GetChildByPath("/bg_line/kw").asLabel()


		# left
		leftPanel = machineryPanel.GetChildByPath("/panel_left")
		# 滚动框
		listPanel = leftPanel.GetChildByPath("/sroll_view")
		listPath = listPanel.GetPath()
		self._craftItemView = ScrollViewWidget(self, listPath, "/btn_drag", 1)
		self._craftListView = ListViewWidget(self, listPath, "/btn_drag/panel", "/btn_drag/panel/item_base", self.SetCraftListItemInfo, self.OnSelectCraftItemClicked, self._craftItemView, 2)
		# 向下箭头，用来提示还有内容，可以往下滑动
		self._craftListViewArrow = listPanel.GetChildByPath("/next")
		# 强化
		self._enhancementBtn = leftPanel.GetChildByPath('/enhancement').asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._enhancementBtn, self.OnEnhancementClicked)
		self._enhancementSelectImage = leftPanel.GetChildByPath('/enhancement/select').asImage()
		# 修复
		self._repairBtn = leftPanel.GetChildByPath('/repair').asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._repairBtn, self.OnRepairClicked)
		self._repairSelectImage = leftPanel.GetChildByPath('/repair/select').asImage()


		# center
		self._centerPanel = machineryPanel.GetChildByPath("/panel_center")
		# 提示强化功能研发中tips
		self._tips = self._centerPanel.GetChildByPath("/tips").asLabel()
		# 耐久显示
		durabilityBarPanel = self._centerPanel.GetChildByPath("/durability_bar_panel")
		self._repairBar = durabilityBarPanel.GetChildByPath("/durability_bar").asProgressBar()
		self._repairBarText = durabilityBarPanel.GetChildByPath("/durability_text").asLabel()
		self._repairBarTitle = self._centerPanel.GetChildByPath("/durability").asLabel()
		# 模型显示
		self._craftItemDoll = self._centerPanel.GetChildByPath("/input_panel_item_model/paper_doll").asNeteasePaperDoll()
		# 材料
		matPanel = self._centerPanel.GetChildByPath("/panel_materials")
		matViewPath =matPanel.GetPath()
		self._materialScrollView = ScrollViewWidget(self, matViewPath, "/btn_drag", 2)
		self._materialListView = ListViewWidget(self, matViewPath, "/btn_drag/panel", "/btn_drag/panel/bg", self.SetMaterialItemInfo, None, self._materialScrollView, 2)
		# 箭头用来提示还有内容，可以往右滑动
		self._matViewDownArrow = matPanel.GetChildByPath("/next")


		# right
		rightPanel = machineryPanel.GetChildByPath("/panel_right")
		# 物品信息
		self._craftItemName = rightPanel.GetChildByPath("/item_name").asLabel()
		self._craftItemTips = rightPanel.GetChildByPath("/panel/btn_drag/tips").asLabel()
		self._craftItemTipsView = ScrollViewWidget(self, rightPanel.GetPath() + "/panel", "/btn_drag", 1)
		
		# 合成按钮
		self._craftBtn = rightPanel.GetChildByPath("/panel_materials/btn_craft").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._craftBtn, self.OnCraftClicked)

		# 强化或者修复进度
		self._craftingBarPanel = machineryPanel.GetChildByPath("/panel_crafting")
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
			self._craftItemTipsView.Update()
			self._materialListView.Update()
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
		# 设置初始状态左侧合成ui
		if self._isSelectEnhancementTab:
			clientApiMgr.SetUIVisible(self._enhancementSelectImage,True)
			clientApiMgr.SetUIVisible(self._repairSelectImage,False)
		else:
			clientApiMgr.SetUIVisible(self._enhancementSelectImage,False)
			clientApiMgr.SetUIVisible(self._repairSelectImage,True)
		craftList = []
		# 根据初始状态选择检测物品是否需要耐久检测
		isDurability = not self._isSelectEnhancementTab
		craftList = self.GetPlayerSlotItemInfo(isDurability)
		self._craftListView.UpdateData(craftList)
		# 初始没有可修复时候隐藏
		if not craftList:
			clientApiMgr.SetUIVisible(self._centerPanel,False)
			clientApiMgr.SetUIVisible(self._craftBtn,False)
		# 当列数超过8个时候提示下拉
		if len(craftList) > 8:
			clientApiMgr.SetUIVisible(self._craftListViewArrow, True)
		else:
			clientApiMgr.SetUIVisible(self._craftListViewArrow, False)
		# 设置工作状态UI
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
		if self._isSelectEnhancementTab:
			text = "研发中"
			clientApiMgr.SetButtonGray(self._craftBtn, True)
			clientApiMgr.SetButtonText(self._craftBtn, text)
			return
		else:
			text = "修复"
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

	# region 获取玩家槽位物品等信息
	def GetPlayerSlotItemInfo(self,isDurability):
		"""获取玩家槽位物品等信息，可选择是否需要耐久度检测，开启后只会返回有耐久的物品"""
		craftList = []
		self._itemDurabilityDic = {}
		# 获取玩家 物品:槽位 信息
		self._inventorySlotDict = clientApiMgr.GetPlayerInventoryItems(self.mPlayerId)
		# 需要耐久检测
		if isDurability:
			for slot in self._inventorySlotDict:
				slotDic =  self._inventorySlotDict[slot]
				itemName=slotDic['newItemName']
				if itemName in self._craftDicCfg['repair']:
					itemDurability,newAuxValue,userData =slotDic['durability'],slotDic['newAuxValue'],slotDic['userData']
					# 判断耐久是否低于max耐久，如果低于则代表可以修复,添加到左侧列表
					if itemDurability<clientApiMgr.GetItemMaxDurability(itemName):
						# 将耐久储存到字典中，方便后面计算所需要材料时候用
						self._itemDurabilityDic[itemName+str(slot)] = itemDurability
						Dic = {'item': {'count': 1, 'newItemName': itemName,'newAuxValue':newAuxValue,"slot":slot},'view_model':self._craftDicCfg['repair'][itemName],'newItemName':itemName,'newAuxValue':newAuxValue,'userData':userData}
						craftList.append(Dic)
			return craftList
		# 不需要耐久检测
		else:
			for slot in self._inventorySlotDict:
				slotDic =  self._inventorySlotDict[slot]
				itemName=slotDic['newItemName']
				if itemName in self._craftDicCfg['repair']:
					itemDurability,newAuxValue,userData =slotDic['durability'],slotDic['newAuxValue'],slotDic['userData']
					Dic = {'item': {'count': 1, 'newItemName': itemName,'newAuxValue':newAuxValue,"slot":slot},'view_model':self._craftDicCfg['repair'][itemName],'newItemName':itemName,'newAuxValue':newAuxValue,'userData':userData}
					craftList.append(Dic)
		return craftList
	# endregion

	# region 物品列表
	def SetSelectCraftItem(self, ctrl, index, data):
		"""设置选中物品"""
		item = data.get("item")
		if self._selectCraftItemIndex != index:
			# 选中
			if self._selectCraftItemIndex is None:
				# 初次选中，不刷新
				self._selectCraftItemIndex = index
			else:
				self._selectCraftItemIndex = index
				# 刷新窗口所有控件（目的是刷新选中状态）
				self._craftListView.UpdateView()
			if item:
				self._selectCraftItemName['newItemName'] = item.get("newItemName")
				self._selectCraftItemName['newAuxValue'] = item.get("newAuxValue")
				self._selectCraftItemName['slot'] = item.get("slot")
				# 显示模型
				if data.get("view_model"):
					self._craftItemDoll.RenderEntity(data["view_model"])
					clientApiMgr.SetUIVisible(self._craftItemDoll, True)
				# 显示详情
				name = clientApiMgr.GetItemHoverName(item)
				tips = clientApiMgr.GetItemHoverText(item)
				titleItemName = clientApiMgr.GetItemHoverName(data)
				# 强化和修复时不同逻辑
				if self._isSelectEnhancementTab:
					stage = '强化'
					self._title.SetText("机械工作台/"+stage+"功能研发中")
					name = '研发中'
					tips = '研发中 敬请期待...'
					titleItemName = '研发中'
				else:
					stage = '修复'
					# 显示耐久
					itemDurability = float(self._itemDurabilityDic[self._selectCraftItemName['newItemName']+str(self._selectCraftItemName['slot'])])
					self._repairBar.SetValue(self.GetDurabilityProportion(self._selectCraftItemName['newItemName'],self._selectCraftItemName['slot']))
					self._repairBarText.SetText(str(int(itemDurability))+"/"+str(clientApiMgr.GetItemMaxDurability(item.get("newItemName"))))
				self._title.SetText("机械工作台/"+stage+"/"+titleItemName)
				self._craftItemName.SetText(name)
				self._craftItemTips.SetText(tips)
				# 显示材料
				self.SetMaterialsUI()
		else:
			# 修复好了某个道具
			pass
		pass

	def SetCraftListItemInfo(self, path, ctrl, index, data):
		"""设置物品列表slot信息"""
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
		repairItemName = self._selectCraftItemName['newItemName']
		# 刷新列表s
		repairRecipe = GetElectricItemRepairRecipe(repairItemName)
		Recipe = GetElectricItemRecipe(repairItemName)
		self._materialListView.UpdateData(repairRecipe['repair'] if repairRecipe is not None else Recipe['input'])
		# 初始化物品+槽位 对应的所需的修复材料数量
		repairMaterialsKey = repairItemName+str(self._selectCraftItemName['slot'])
		self._repairMaterialsDic[repairMaterialsKey] = []
		pass

	def SetMaterialItemInfo(self, path, ctrl, index, data):
		"""设置材料详细信息"""
		itemName = data.get("newItemName")
		aux = data.get("newAuxValue", 0)
		itemObj = ctrl.GetChildByPath("/item_renderer").asItemRenderer()
		itemObj.SetUiItem(itemName, aux)
		# 玩家背包物品是否为空
		if self._inventoryCountDict is None:
			self._inventoryCountDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		

		# 强化和修复逻辑
		if self._isSelectEnhancementTab:
			count = data.get("count", 1)
		else:
			# 计算 耐久和最大耐久的比值与1的差值，乘以制作材料向上取整后便是修复所需要材料
			durabilityProportion = 1-self.GetDurabilityProportion(self._selectCraftItemName['newItemName'],self._selectCraftItemName['slot']) # 比例差值
			count = int(data.get("count", 1)*durabilityProportion)+1 # 向上取整
			# 将修复所需要的材料保存到字典中方便后面发到服务端扣除物品
			repairMaterialsKey = self._selectCraftItemName['newItemName']+str(self._selectCraftItemName['slot'])
			if repairMaterialsKey in self._repairMaterialsDic:
				self._repairMaterialsDic[repairMaterialsKey].append({"newItemName": itemName,"newAuxValue":aux, "count": count})

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
		nameObj = ctrl.GetChildByPath("/item_name").asLabel()
		countobj = ctrl.GetChildByPath("/item_count").asLabel()
		nameObj.SetText(name)
		countobj.SetText("{}{}/{}".format(redStr, count, hasCount))
		# 如果index超过5，则显示右拉的箭头
		if index == 5:
			clientApiMgr.SetUIVisible(self._matViewDownArrow, True)
		pass
	# endregion

	# # region 强化按钮
	# def EnhancementClicked(self):
	# 	"""强化按钮操作"""
	# 	clientApiMgr.SetUIVisible(self._tips,True)
	# 	if self._tipsTimer:
	# 		engineApiGac.CancelTimer(self._tipsTimer)
	# 	self._tipsTimer = engineApiGac.AddTimer(2,self.tipsTimer)
	
	# def tipsTimer(self):
	# 	self._tipsTimer = None
	# 	clientApiMgr.SetUIVisible(self._tips,False)
		# self._isSelectEnhancementTab = True
		# self._selectCraftItemIndex = None
		# clientApiMgr.SetUIVisible(self._enhancementSelectImage,True)
		# clientApiMgr.SetUIVisible(self._repairSelectImage,False)
		# clientApiMgr.SetUIVisible(self._repairBar,False)
		# clientApiMgr.SetUIVisible(self._repairBarText,False)
		# clientApiMgr.SetUIVisible(self._repairBarTitle,False)
		# craftList = []
		# # 不需要耐久检测
		# isDurability = not self._isSelectEnhancementTab
		# craftList = self.GetPlayerSlotItemInfo(isDurability)
		# self._craftListView.UpdateData(craftList)
	# endregion

	# region 修复按钮
	def RepairClicked(self):
		"""修复按钮操作"""
		self._isSelectEnhancementTab = False
		self._selectCraftItemIndex = None
		clientApiMgr.SetUIVisible(self._enhancementSelectImage,False)
		clientApiMgr.SetUIVisible(self._repairSelectImage,True)
		clientApiMgr.SetUIVisible(self._repairBar,True)
		clientApiMgr.SetUIVisible(self._repairBarText,True)
		clientApiMgr.SetUIVisible(self._repairBarTitle,True)
		craftList = []
		# 需要耐久检测
		isDurability = not self._isSelectEnhancementTab
		craftList = self.GetPlayerSlotItemInfo(isDurability)
		self._craftListView.UpdateData(craftList)
	# endregion
	
	# region 进度条操作
	def SetCrafting(self):
		"""设置进度条操作"""
		# 校验
		if self._isSelectEnhancementTab:
			return
		if self._hasDynamo:
			if self._hasEnoughMaterials:
				# 显示合成进度
				self.SetCraftingBarUI(True)
		pass

	def SetCraftingBarUI(self, state):
		"""设置进度条和机械工作台UI"""
		clientApiMgr.SetUIVisible(self._craftingBarPanel, state)
		if state:
			# 获取时间
			self._craftingTime = 0
			recipe = GetElectricItemRecipe(self._selectCraftItemName['newItemName'])
			if recipe:
				self._craftingTotalTime = recipe.get("time", 0)
			# 重置UI进度
			self._craftingBar.SetValue(0)
			# 启动timer
			if not self._craftingTimer:
				self._craftingTimer = engineApiGac.AddRepeatedTimer(self._craftingInterval, self.UpdateCraftingBarTimer)
		else:
			# 修复完成后刷新列表
			if not self._isSelectEnhancementTab:
				craftList = []
				isDurability = not self._isSelectEnhancementTab
				craftList = self.GetPlayerSlotItemInfo(isDurability)
				for itemDic in craftList:
					ItemName = itemDic['newItemName']
					if ItemName == self._selectCraftItemName['newItemName']:
						craftList.remove(itemDic)
				# 列表为空时候说明这是最后一个修复的物品，将ui进行初始化，提示背包没有损耗物品
				if not craftList:
					self._craftItemName.SetText("注意")
					self._craftItemTips.SetText("背包中没有损耗的装备")
					self._title.SetText("机械工作台待机中......")
					self._repairBarText.SetText("无")
					clientApiMgr.SetUIVisible(self._centerPanel,False)
					clientApiMgr.SetUIVisible(self._craftBtn,False)
				else:
					clientApiMgr.SetUIVisible(self._centerPanel,True)
					clientApiMgr.SetUIVisible(self._craftBtn,True)
				self._craftListView.UpdateData(craftList)
				self._selectCraftItemIndex = None
				if len(craftList) > 8:
					clientApiMgr.SetUIVisible(self._craftListViewArrow, True)
				else:
					clientApiMgr.SetUIVisible(self._craftListViewArrow, False)
			# 停止timer
			if self._craftingTimer:
				engineApiGac.CancelTimer(self._craftingTimer)
				self._craftingTimer = None
			# 刷新剩余材料物品
			self._inventoryCountDict = None
			self.SetMaterialsUI()
		pass

	def UpdateCraftingBarTimer(self):
		"""更新进度UI"""
		if self._craftingTime < self._craftingTotalTime:
			self._craftingTime += self._craftingInterval
			rate = self._craftingTime / self._craftingTotalTime
			self._craftingBar.SetValue(rate)
			# 设置界面当中的耐久条
			if not self._isSelectEnhancementTab:
				itemDurability = self.GetDurabilityProportion(self._selectCraftItemName['newItemName'],self._selectCraftItemName['slot'])
				self._repairBar.SetValue((1-itemDurability)*rate+itemDurability)
			if rate >= 1.0:
				# 进度跑满
				# 发消息到服务端
				# 判断是在强化还是在修复当中
				if self._isSelectEnhancementTab:
					info = {
						"to_server": True,
						"stage": "craft",
						"key": self._key,
						"item": self._selectCraftItemName['newItemName'],
					}
				else:
					info = {
						"to_server": True,
						"stage": "set_durability",
						"key": self._key,
						"item": self._selectCraftItemName['newItemName'],
						"slot":self._selectCraftItemName['slot'],
						"materials":self._repairMaterialsDic[self._selectCraftItemName['newItemName']+str(self._selectCraftItemName['slot'])]
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.ElectricSubscriptEvent, info)
				# 延迟关闭UI
				engineApiGac.AddTimer(0.1, self.SetCraftingBarUI, False)
				self.SetMaterialsUI()
		pass
	# endregion

	# region 获取物品耐久与最大耐久比例
	def GetDurabilityProportion(self,itemName,slot):
		itemDurability = float(self._itemDurabilityDic.get(itemName+str(slot),1))
		maxItemDurability = float(clientApiMgr.GetItemMaxDurability(itemName))
		return itemDurability/maxItemDurability 
	# endregion

	# region 按钮
	def OnEnhancementClicked(self,args):
		"""强化按钮"""
		self.EnhancementClicked()
		pass
	def OnRepairClicked(self,args):
		"""修复按钮"""
		self.RepairClicked()
		pass
	def OnCloseClicked(self, args):
		"""关闭UI"""
		self.CloseUI()
		pass
	
	def OnSelectCraftItemClicked(self, path, ctrl, index, data, args):
		"""点击列表中的物品"""
		self.SetSelectCraftItem(ctrl, index, data)
		pass
	
	def OnCraftClicked(self, args):
		"""点击按钮"""
		self.SetCrafting()
		pass

	# endregion
