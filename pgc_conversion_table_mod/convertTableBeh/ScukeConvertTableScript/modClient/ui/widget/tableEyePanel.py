# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.widget.uiBaseWidget import *
ViewBinder = clientApi.GetViewBinderCls()


class TableEyePanel(UiBaseWidget):
	def __init__(self, uiInst, sysInst, path, param):
		UiBaseWidget.__init__(self, uiInst, sysInst, path)
		self.param = param
		# (itemName, aux): [cnName, emcValue]
		self.cfg = ItemEMCConfig._AllItemEmc
		self.changeCfg = self.param.get("emcCfg", {})
		self.cfg.update(self.changeCfg)
		self.rootPanel = self.GetBaseUiControl("")
		self.panel = self.GetBaseUiControl("/eyePanel")
		self.panelPath = "/eyePanel"
		self.itemGroupPath = self.panelPath + "/itemGroup"
		self.registerBtnDict = {
			"lastPageBtn": self.panelPath + "/lastPageBtn",
			"nextPageBtn": self.panelPath + "/nextPageBtn",
			"clearBtn": self.panelPath + "/searchPanel/clearBtn",
		}
		self.visualTextPanelPath = self.panelPath + "/visualTextPanel"
		self.visualTextPath = self.visualTextPanelPath + "/visualText"
		self.visualTextPanelAllPath = "/tablePanel/mainScreenPanel/mainStackPanel/tableEyePanel" + self.visualTextPanelPath
		self.visualTextAllPath = self.visualTextPanelAllPath + "/visualText"
		self.itemPanelGroupDict = {}
		self.pageTxt = None
		self.pageSum = 1
		self.pageNum = 1
		# 搜索或排序后显示的记忆物品列表
		self.showMemoryItemList = []
		# 总记忆物品列表 [(itemName, aux, itemDict)]
		self.totalMemoryItemList = []
		self.searchBox = None
		self.searchContent = None
		# index, pageNum
		self.lastSelectData = [None, None]
		self.isSelectItemSlot = False
		self.emcValue = self.param.get("emcValue", 0)
		self.eyeCorePanel = None
		# 以物品英文id为key的字典    "itemName": [(itemName, aux), itemDict]
		self.enSearchDict = {}
		# 以中文字符串为key的字典     "物品名称": [(itemName, aux), itemDict]
		self.cnSearchDict = {}
		self.hasCreate = False
		self.vState = True
		self.eyeBallAnim = False
		self.clickPos = (0.0, 0.0)

		# 文字表现UI的Timer
		self.VisualTextShowTimer = {}
		self.VisualTextRemoveTimer = {}
		self.Create()
		self.UpdateSearchDict()

	def UpdateSearchDict(self):
		# 更新检索字典
		self.cnSearchDict.clear()
		self.enSearchDict.clear()
		for k in self.totalMemoryItemList:
			itemKey = (k[0], k[1])
			cnName = self.cfg.get(itemKey, ["未知%s" % k[0], 1])[0]
			self.cnSearchDict.update({cnName: [itemKey, k[2]]})
			self.enSearchDict.update({k[0]: [itemKey, k[2]]})

	def Create(self):
		self.totalMemoryItemList = self.param.get("memoryList", [])
		for key, path in self.registerBtnDict.iteritems():
			uiUtils.UICreateBtn(self.uiInst, self._btnDict, key, self.path + path, None, self.OnCommonBtnPressUp)
		self.CreateItemPanel()
		self.searchBox = self.GetBaseUiControl(self.panelPath + "/searchPanel/searchEditBox").asTextEditBox()
		self.eyeCorePanel = self.GetBaseUiControl(self.panelPath + "/bg/eyeCore")
		self.visualTextPanel = self.GetBaseUiControl(self.visualTextPanelPath)
		self.hasCreate = True

	def CreateItemPanel(self):
		for i in range(0, 12):
			panelPath = self.itemGroupPath + "/itemPanel%s" % i
			self.itemPanelGroupDict["itemPanel_%s" % i] = (self.GetBaseUiControl(panelPath), self.path + panelPath)
			data = self.GetItemPanelData(i)
			if data is not [None, None]:
				btnPath = data[1] + "/ctrlBtn"
				uiUtils.UICreateBtn(self.uiInst, self._btnDict, "itemPanelBtn_%s" % i, btnPath, None, self.OnPanelBtnPressUp)
		self.pageTxt = self.GetBaseUiControl(self.panelPath + "/pageTxt").asLabel()
		self.RefreshItemPanelShow()

	def Destroy(self):
		self.hasCreate = False
		UiBaseWidget.Destroy(self)

	def Update(self):
		# 根据搜索结果更新面板
		if self.searchBox is not None:
			txt = self.searchBox.GetEditText()
			if self.searchContent != txt:
				self.searchContent = txt
				if self.searchContent is None: return
				if self.searchContent != "":
					ret = self.GetSearchResult()
					self.RefreshItemPanelShow(ret)
					# 如果没搜索到结果
					if not ret:
						inst = self.searchBox
						txt = "§c§l未搜索到结果"
						self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
						self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
				else:
					self.RefreshItemPanelShow()
				self.SetExchangePanelData(False, None)
		# 获取触屏位置，设置眼睛看向的位置
		if self.hasCreate and self.vState and not self.eyeBallAnim:
			if clientApi is None: return
			pos = clientApi.GetTouchPos()
			if pos != self.clickPos and pos != (0.0, 0.0):
				self.clickPos = pos
				self.EyeAnimation(pos)

	def EyeAnimation(self, pos):
		cX, cY = self.eyeCorePanel.GetSize()
		glPos = self.eyeCorePanel.GetGlobalPosition()
		correctGlobalPos = MathUtils.TupleAdd(glPos, (cX / 2.0, cY / 2.0))
		vec = MathUtils.TupleSub(pos, correctGlobalPos)
		times = min((vec[0] ** 2 + vec[1] ** 2) ** 0.2 * 0.7, 4.1)
		nVec = (vec[0] / math.sqrt(vec[0] ** 2 + vec[1] ** 2), vec[1] / math.sqrt(vec[0] ** 2 + vec[1] ** 2))
		nVec = MathUtils.TupleMul(nVec, times)
		ball1Inst = self.eyeCorePanel.GetChildByPath("/eyeBall1")
		tX, tY = ball1Inst.GetSize()
		deltaPos = ((cX - tX) / 2.0, (cY - tY) / 2.0 - 3)
		tVec = MathUtils.TupleAdd(nVec, deltaPos)
		ball1Inst.SetPosition(tVec)
		ball2Inst = ball1Inst.GetChildByPath("/eyeBall2")
		b2X, b2Y = ball2Inst.GetSize()
		dtPos2 = ((tX - b2X) / 2.0, (tY - b2Y) / 2.0)
		b2nVec = MathUtils.TupleMul(nVec, 0.4)
		b2Vec = MathUtils.TupleAdd(b2nVec, dtPos2)
		ball2Inst.SetPosition(b2Vec)

	def GetSearchResult(self):
		def addSearchResult(name, aux0, iDict):
			if (name, aux0) not in markKeyList:
				rp((name, aux0, iDict))
				mkp((name, aux0))
		# 开始根据输入字检索
		result = []
		markKeyList = []
		rp = result.append
		mkp = markKeyList.append
		# 中文检索
		cnKeyList = self.cnSearchDict.keys()
		for i in cnKeyList:
			if self.searchContent in i:
				(itemName, aux), itemDict = self.cnSearchDict[i]
				rp((itemName, aux, itemDict))
				mkp((itemName, aux))
				continue
			if i in self.searchContent:
				(itemName, aux), itemDict = self.cnSearchDict[i]
				addSearchResult(itemName, aux, itemDict)
				continue
		enKeyList = self.enSearchDict.keys()
		for k in enKeyList:
			if self.searchContent in k:
				(itemName, aux), itemDict = self.enSearchDict[k]
				addSearchResult(itemName, aux, itemDict)
				continue
			if k in self.searchContent:
				(itemName, aux), itemDict = self.enSearchDict[k]
				addSearchResult(itemName, aux, itemDict)
				continue
		result.sort(key=lambda x: x[0])
		return result

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateEMCValue(self, args):
		self.emcValue = args["value"]

	def GetItemPanelData(self, index):
		return self.itemPanelGroupDict.get("itemPanel_%s" % index, [None, None])

	def GetClickSlotIndex(self, args):
		clickType = args['AddTouchEventParams']['type']
		try:
			slotIndex = int(clickType.split("_")[1])
		except ValueError:
			return None
		return slotIndex

	def SetExchangePanelData(self, visible, item):
		# 设置物品购买、出售面板显示
		if self.uiInst.autoExchangePanel is None: return
		autoV = self.uiInst.autoExchangePanel.rootPanel.GetVisible()
		self.uiInst.exchangePanel.SetRootPanelVisible(visible and not autoV)
		if visible:
			count = self.uiInst.exchangePanel.sliderValue
			item[2]["count"] = count
			self.sys.BroadcastEvent("ShowExchangeItemData", {"item": item[2], "mode": "buy"})

	def OnPanelBtnPressUp(self, args):
		slotIndex = self.GetClickSlotIndex(args)
		if slotIndex is None: return
		isSelect = self.isSelectItemSlot
		self.RefreshItemPanelSelectState(False)
		self.SetExchangePanelData(False, None)
		data = [slotIndex, self.pageNum]
		if self.lastSelectData == data and isSelect:
			self.lastSelectData = [None, None]
			return
		self.lastSelectData = data
		ret = self.RefreshItemPanelSelectState(True)
		if ret[0]:
			self.SetExchangePanelData(True, ret[1])

	def RefreshItemPanelSelectState(self, state, isPageExe=False):
		# 刷新物品面板选中状态显示
		i, p = self.lastSelectData
		if i is None: return
		inst = self.GetItemPanelData(i)[0]
		if inst is None: return
		listLen = len(self.showMemoryItemList)
		index = (self.pageNum-1)*12 + i
		boolV = index <= listLen - 1
		inst.GetChildByPath("/bg/cell_normal").SetVisible(not state or not boolV)
		inst.GetChildByPath("/bg/cell_highlight").SetVisible(boolV)
		inst.GetChildByPath("/bg/cell_select").SetVisible(state and boolV)
		self.isSelectItemSlot = state and boolV
		# 翻页操作
		slotIndex = self.lastSelectData[0]
		if slotIndex is None: slotIndex = 0
		realIndex = slotIndex + (self.pageNum - 1) * 12
		bool2 = realIndex < len(self.showMemoryItemList) and self.lastSelectData[0] is not None
		if p == self.pageNum and isPageExe and bool2:
			inst.GetChildByPath("/bg/cell_normal").SetVisible(False)
			inst.GetChildByPath("/bg/cell_highlight").SetVisible(True)
			inst.GetChildByPath("/bg/cell_select").SetVisible(True)
			self.isSelectItemSlot = True
		item = None
		if boolV:
			item = self.showMemoryItemList[index]
		# 如果选中了有物品的槽位，返回真
		return state and boolV, item

	def OnCommonBtnPressUp(self, args):
		clickType = args['AddTouchEventParams']['type']
		if clickType == "clearBtn":
			self.searchBox.SetEditText("")
			self.RefreshItemPanelShow()
			self.SetExchangePanelData(False, None)
		elif clickType == "lastPageBtn":
			self.pageNum -= 1
			self.RefreshItemPanelShow(self.showMemoryItemList)
			self.RefreshItemPanelSelectState(False, True)
		elif clickType == "nextPageBtn":
			self.pageNum += 1
			self.RefreshItemPanelShow(self.showMemoryItemList)
			self.RefreshItemPanelSelectState(False, True)

	def RefreshPageShow(self, listLen):
		self.pageSum = listLen // 12 + 1
		# 解决空页
		k = listLen % 12
		if k == 0:
			self.pageSum -= 1
		if self.pageNum > self.pageSum:
			self.pageNum = 1
		if self.pageNum < 1:
			self.pageNum = self.pageSum
		self.pageNum = max(min(self.pageNum, self.pageSum), 1)
		self.pageTxt.SetText("%s/%s" % (self.pageNum, self.pageSum))

	def SetRootPanelVisible(self, state):
		self.rootPanel.SetVisible(state)
		self.vState = state

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateEyePanelData(self, args):
		"""
		1.更新总记忆售出列表
		2.刷新轮盘显示
		3.更新搜索字典
		"""
		self.totalMemoryItemList = args["memoryList"]
		self.UpdateSearchDict()
		self.RefreshItemPanelShow()

	def RefreshItemPanelShow(self, memoryList=None):
		# 刷新轮盘显示，根据选择结果的列表
		if memoryList is None: memoryList = self.totalMemoryItemList
		self.showMemoryItemList = memoryList[:]
		for i in range(0, 12):
			itemIt = self.GetItemPanelData(i)[0]
			renderItem = itemIt.GetChildByPath("/renderPanel")
			renderItem.SetVisible(False)
			itemIt.GetChildByPath("/bg/cell_normal").SetVisible(True)
			itemIt.GetChildByPath("/bg/cell_highlight").SetVisible(False)
			itemIt.GetChildByPath("/bg/cell_select").SetVisible(False)
		listLen = len(self.showMemoryItemList)
		self.RefreshPageShow(listLen)
		startIndex = (self.pageNum - 1) * 12
		endIndex = min(startIndex + 12, listLen)
		# 根据当前页码，显示指定页码的指定物品
		for index, data in enumerate(self.showMemoryItemList[startIndex:endIndex]):
			itemInst = self.GetItemPanelData(index)[0]
			itemInst.GetChildByPath("/bg/cell_highlight").SetVisible(True)
			renderItem = itemInst.GetChildByPath("/renderPanel")
			renderItemFly = itemInst.GetChildByPath("/renderPanelFlying")
			renderItem.SetVisible(True)
			item = renderItem.GetChildByPath("/item").asItemRenderer()
			itemFly = renderItemFly.GetChildByPath("/item").asItemRenderer()
			itemName = data[2]["newItemName"]
			aux = data[2]["newAuxValue"]
			enchant = "userData" in data[2] and data[2]["userData"] is not None and "ench" in data[2]["userData"]
			userData = data[2].get("userData", None)
			item.SetUiItem(itemName, aux, enchant, userData)
			itemFly.SetUiItem(itemName, aux, enchant, userData)

	def OnForget(self):
		# 对当前选中的物品进行遗忘操作
		i, p = self.lastSelectData
		realIndex = i + (p - 1) * 12
		forgetItemData = self.showMemoryItemList[realIndex]
		totalMemoryItemIndex = self.totalMemoryItemList.index(forgetItemData)
		self.RefreshItemPanelSelectState(False)
		self.SetExchangePanelData(False, None)
		self.SendMsgToServer("TryToForgetOneItem", {"pid": self.mPlayerId, "itemIndex": totalMemoryItemIndex})

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def RefreshEyePanelDataUI(self, args):
		"""刷新眼睛轮盘知识显示"""
		self.UpdateEyePanelData(args)

	# region meta文字表现
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.VisualUIClient)
	def SetVisualText(self, args):
		text, intervalTime,color ,removeTime, lastLen = args['text'].decode('utf-8'), args["intervalTime"], args["color"], args["removeTime"], args["lastLen"]
		YOffset = args["YOffset"]
		textList = list(text)
		colorList = []
		for i in range(50):
			colorList.append((1, 0, 0))
		visualTextPanelSize = self.visualTextPanel.GetSize()
		visualTextObj = self.GetBaseUiControl(self.visualTextPath).asLabel()
		visualTextObj.SetVisible(True)
		visualTextSize = visualTextObj.GetSize()
		visualTextObj.SetVisible(False)
		posList = self.GenerateTextCoordinates(textList, visualTextPanelSize[0], visualTextPanelSize[1], visualTextSize[0], visualTextSize[1], YOffset)

		for i in range(lastLen):
			cloneTextName = "visualText" + str(i)
			newTextAllPath = self.visualTextPanelAllPath + "/" + cloneTextName
			self.uiInst.RemoveComponent(newTextAllPath, self.visualTextPanelAllPath)

		num = 0
		showTime = 0
		for pos in posList:
			cloneTextName = "visualText" + str(num)
			newTextPath = self.visualTextPanelPath + "/" + cloneTextName
			newTextAllPath = self.visualTextPanelAllPath + "/" + cloneTextName
			cloneValue = self.uiInst.Clone(self.visualTextAllPath, self.visualTextPanelAllPath, cloneTextName, True, True)
			if cloneValue:
				if cloneTextName in self.VisualTextShowTimer:
					engineApiGac.CancelTimer(self.VisualTextShowTimer[cloneTextName])
					self.VisualTextShowTimer.pop(cloneTextName)
				if cloneTextName in self.VisualTextRemoveTimer:
					engineApiGac.CancelTimer(self.VisualTextRemoveTimer[cloneTextName])
					self.VisualTextRemoveTimer.pop(cloneTextName)
				textObj = self.GetBaseUiControl(newTextPath).asLabel()
				textObj.SetText(textList[num])
				textObj.SetPosition(pos)
				if colorList:
					textObj.SetTextColor(colorList[num])
				self.VisualTextShowTimer[cloneTextName] = engineApiGac.AddTimer(showTime, textObj.SetVisible, True)
				self.VisualTextRemoveTimer[cloneTextName] = engineApiGac.AddTimer(removeTime, self.uiInst.RemoveComponent, newTextAllPath, self.visualTextPanelAllPath)
			num += 1
			showTime += intervalTime

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.VisualUIClient)
	def SetVisualUI(self, args):
		# default angry
		self.uiInst.animator.SetAllState(args['state'])
	
	def GenerateTextCoordinates(self, text_list, rect_width, rect_height, char_width, char_height , YOffset = []):
		"""计算文字列表在面板中位置"""
		num_texts = len(text_list)
		total_text_width = num_texts * char_width
		if total_text_width > rect_width:
			spacing = 1
		else:
			# 正常计算间距
			spacing = (rect_width - total_text_width) / (num_texts - 1) if num_texts > 1 else 0
		
		textLen, yLen = len(text_list), len(YOffset)
		if YOffset:
			if textLen < yLen:
				YOffset[:-(yLen - textLen)]
			elif textLen > yLen:
				for i in range(textLen - yLen):
					YOffset.append(0)
		else:
			for i in range(textLen):
				YOffset.append(0)

		coordinates = []
		x = 0  # 起始x坐标
		num = 0
		for _ in text_list:
			y = (rect_height - char_height) / 2 + YOffset[num]
			coordinates.append((x, y))
			x += char_width + spacing
			num += 1
		return coordinates
	# endregion
