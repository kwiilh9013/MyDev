# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.widget.uiBaseWidget import *
from ScukeConvertTableScript.modCommon.cfg.shulkerBoxEnum import ShulkerBoxEnum
ViewBinder = clientApi.GetViewBinderCls()


class ExchangePanel(UiBaseWidget):
	def __init__(self, uiInst, sysInst, path, param):
		UiBaseWidget.__init__(self, uiInst, sysInst, path)
		self.param = param
		self.cfg = DeepCopy(ItemEMCConfig._AllItemEmc)
		self.changeCfg = self.param.get("emcCfg", {})
		self.cfg.update(self.changeCfg)
		self.emcValue = self.param.get("emcValue", 0)
		self.isCanForget = self.param.get("isCanForget", False)
		self.rootPanel = self.GetBaseUiControl("")
		self.bgPath = "/bgPanel"
		self.sIPPath = "/selectItemPanel"
		self.fSPPath = "/funcStackPanel"
		self.hasPower = self.param.get("hasPower", False)
		self.settingsData = self.param.get("globalSetting", {})
		self.registerBtnDict = {
			"forgetBtn": self.fSPPath + "/funcBtnPanel/forgetBtn",
			"makePriceBtn": self.fSPPath + "/funcBtnPanel/makePriceBtn",
			"sellOrBuyBtn": self.fSPPath + "/sellAndBuyPanel/btn",
			"exitBtn": self.fSPPath + "/exitPanel/closeBtn",
			"detailBtn": self.sIPPath + "/infoPanel/titleTxt/detailBtn"
		}
		self.itemRender = None
		self.titleText = None
		self.subTitleText = None
		self.countSliderPanel = None
		self.countSlider = None
		self.countText = None
		self.sliderValue = 1
		self.emcPriceInfoPanel = None
		self.redColor = (255.0 / 255.0, 65.0 / 255.0, 65.0 / 255.0)
		self.greenColor = (43.0 / 255.0, 168.0 / 255.0, 17.0 / 255.0)
		self.itemInfoCache = None
		self.exchangeMode = "sell"
		self.itemCache = None
		self.itemMaxStack = 63
		self.visible = False
		self.totalPrice = 0
		self.presentMode = "sell"
		self.buyTick = 0
		self.shulkerBoxKeys = ShulkerBoxEnum.__dict__.keys()
		self.Create()

	def Create(self):
		for key, path in self.registerBtnDict.iteritems():
			uiUtils.UICreateBtn(self.uiInst, self._btnDict, key, self.path + path, None, self.OnCommonBtnPressUp)
		self.itemRender = self.GetBaseUiControl(self.sIPPath + "/itemPanel/item").asItemRenderer()
		self.titleText = self.GetBaseUiControl(self.sIPPath + "/infoPanel/titleTxt").asLabel()
		self.subTitleText = self.GetBaseUiControl(self.sIPPath + "/infoPanel/subTitleTxt").asLabel()
		self.countSliderPanel = self.GetBaseUiControl("/countSliderMovePanel")
		self.countSlider = self.countSliderPanel.GetChildByPath("/countSlider").asSlider()
		self.countText = self.countSliderPanel.GetChildByPath("/countTxt").asLabel()
		self.emcPriceInfoPanel = self.GetBaseUiControl(self.fSPPath + "/sellAndBuyPanel/emcPriceInfo")
		self.SetRootPanelVisible(False)

	def Destroy(self):
		self.visible = False
		UiBaseWidget.Destroy(self)

	def Update(self):
		if not self.visible: return
		self._mTick0 += 1
		if not self.countSlider: return
		self.sliderValue = max(int(self.countSlider.GetSliderValue() * self.itemMaxStack), 1)
		txt = self.countText.GetText()
		strSlider = str(self.sliderValue)
		if txt != strSlider and txt is not None:
			self.countText.SetText(strSlider)
			self.itemCache["count"] = self.sliderValue
			self.RefreshRootPanel(self.itemCache, "buy")

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateSettingData(self, args):
		self.settingsData = args["data"]

	def OnCommonBtnPressUp(self, args):
		clickType = args['AddTouchEventParams']['type']
		if clickType == "exitBtn":
			self.SetRootPanelVisible(False)
		elif clickType == "sellOrBuyBtn":
			# self.uiInst.animator.SetAllState("angry")
			if self.exchangeMode == "sell":
				data = self.GetSelectItemData()
				if data[0] is None: return
				self.SetRootPanelVisible(False)
				self.uiInst.corePanel.CancelHighlightAndEndGrouping()
				self.sys.NotifyToServer("OnSellingItem", {"data": data, "pid": self.mPlayerId, "itemDict": self.itemCache})
			elif self.exchangeMode == "buy":
				# EMC不足时
				if self.emcValue < self.totalPrice:
					self.OnEMCCannotBuy()
					return
				# 冷却
				t = time.time()
				if t - self.buyTick < 0.25: return
				if self.itemCache:
					self.buyTick = t - 0.01
					slot = self.uiInst.tableEyePanel.lastSelectData[0]
					self.sys.NotifyToServer("OnBuyingItem", {"item": self.itemCache, "pid": self.mPlayerId, "slot": slot})
		elif clickType == "makePriceBtn":
			# 推出定价UI
			# 如果不是管理员或房主没开启房客可定价，则取消定价并提示
			canOtherMakePrice = self.settingsData.get("otherCanMakePrice", False)
			if not self.hasPower and not canOtherMakePrice:
				inst = self._btnDict["makePriceBtn"]
				txt = "§c§l你不是管理员，没有权限定价"
				self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
				self.uiInst.tipInfoPanel.SetTipsShow(inst, txt, None)
				return
			itemName, aux = self.itemCache["newItemName"], self.itemCache["newAuxValue"]
			itemEMCData = self.cfg.get((itemName, aux))
			if itemEMCData is None:
				enchant = "userData" in self.itemCache and self.itemCache["userData"] is not None and "ench" in self.itemCache["userData"]
				info = self.GetItemInfo(self.mPlayerId, itemName, aux, enchant)
				cnName = info["itemName"]
				itemEMCData = [cnName, 1]
			param = {
				"itemDict": self.itemCache,
				"emcData": [(itemName, aux), itemEMCData]
			}
			clientApi.PushScreen(modConfig.ModNameSpace, "ScukeConvertTable_MakePrice", param)
		elif clickType == "forgetBtn":
			# 推出提示UI
			param = {
				"confirmMethod": self.uiInst.tableEyePanel.OnForget,
				"headTxt": "遗忘操作",
				"infoTxt": "是否要将当前选中物品遗忘？"
			}
			clientApi.PushScreen(modConfig.ModNameSpace, "ScukeConvertTable_Notice", param)
		elif clickType == "detailBtn":
			referPanel = self._btnDict["detailBtn"]
			method = engineApiGac.compFactory.CreateItem(self.mPlayerId)
			info = itemApi.SortItemInfo(self.itemCache, method)
			self.uiInst.tipInfoPanel.SetTipsShow(referPanel, info, None, 2.0, True)
			self.uiInst.tipInfoPanel.SetTipsShow(referPanel, info, None, 2.0, True)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def OnEMCCannotBuy(self, args=None):
		referPanel = self.uiInst.corePanel.emcPanel.GetChildByPath("/emcValue")
		txt = "§cEMC值不足！！！" if args is None else "§c管理员已更新该物品EMC价值，EMC值不足"
		self.uiInst.tipInfoPanel.SetTipsShow(referPanel, txt, None)
		self.uiInst.tipInfoPanel.SetTipsShow(referPanel, txt, None)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateEMCValue(self, args):
		self.emcValue = args["value"]

	def GetSelectItemData(self):
		item = self.uiInst.corePanel.selectItemCache
		return self.uiInst.corePanel.newSelectIndex, item["newItemName"], item["newAuxValue"], item["count"]

	def SetRootPanelVisible(self, state):
		self.rootPanel.SetVisible(state)
		self.visible = state

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def ShowExchangeItemData(self, args):
		item = args["item"]
		mode = args["mode"]
		self.presentMode = mode
		if not item: return
		self.itemCache = item
		if mode == "buy":
			itemName = item["newItemName"]
			aux = item["newAuxValue"]
			self.itemMaxStack = itemApi.GetItemMaxStackSize(engineApiGac.compFactory, engineApiGac.levelId, itemName, aux)
		self.RefreshRootPanel(item, mode)

	def GetItemInfo(self, pid, itemName, aux, enchant=False):
		if not engineApiGac or not engineApiGac.compFactory:
			return None
		comp = engineApiGac.compFactory.CreateItem(pid)
		self.itemInfoCache = comp.GetItemBasicInfo(itemName, aux, enchant)
		return self.itemInfoCache

	def RefreshRootPanel(self, itemDict, mode="sell"):
		name, aux = itemDict["newItemName"], itemDict["newAuxValue"]
		enchant = "userData" in itemDict and itemDict["userData"] is not None and "ench" in itemDict["userData"]
		itemInfo = self.GetItemInfo(self.mPlayerId, name, aux, enchant)
		if not itemInfo: return
		cnName = itemInfo["itemName"]
		count = itemDict["count"]
		str1 = "%s x%s" % (cnName, count)
		pData = self.GetItemEMC(name, aux)
		price = pData[0]
		totalPrice = price * count
		self.totalPrice = totalPrice
		str3 = "" if pData[1] else "(未定价)"
		addEnchValue = self.GetItemEnchantEMCValue(itemDict)
		totalPrice += count * addEnchValue
		if addEnchValue > 0:
			str1 += " (含附魔)"
		str2 = "单价 %s 总价 %s %s" % (price, totalPrice, str3)
		self.titleText.SetText(str1)
		self.subTitleText.SetText(str2)
		self.itemRender.SetUiItem(name, aux, enchant, itemDict["userData"])
		self.FuncPanelModeSwitch(mode, price, count)
		# 针对拥有物品的潜影盒，再对其内部物品进行emc计算
		# 物品的aux在"Damage"键中，方块的aux在Block→val中
		spName = name.split(":")[1]
		if spName in self.shulkerBoxKeys:
			addPrice = self.GetContainerItemsEmc(itemDict)
			if addPrice == 0: return
			self.totalPrice += addPrice
			self.titleText.SetText(str1 + " (内含物品)")
			str2 = "单价 %s 总价 %s %s" % (self.totalPrice, self.totalPrice, "")
			self.subTitleText.SetText(str2)
			self.FuncPanelModeSwitch(mode, self.totalPrice, 1)

	@staticmethod
	def GetItemEnchantEMCValue(itemDict):
		# 获取该物品中的附魔EMC值加成
		enchant = itemApi.GetHasEnchant(itemDict)
		if not enchant: return 0
		enchData = itemDict["userData"]["ench"]
		enchantGet = ItemEMCConfig.GetEnchantEMC
		adv = 0
		for ench in enchData:
			level = ench["lvl"]["__value__"]
			enchId = ench["id"]["__value__"]
			emc = enchantGet((enchId, 1))[1] * level
			adv += emc
		return adv

	def GetContainerItemsEmc(self, itemDict):
		# 获取潜影盒内物品的总价值
		addPrice = 0
		enchantGet = ItemEMCConfig.GetEnchantEMC
		if "userData" in itemDict:
			ud = itemDict["userData"]
			if ud is None: return addPrice
			itemDictInside = ud.get("Items", None)
			if itemDictInside is None: return addPrice
			for udItem in itemDictInside:
				udItemName = udItem["Name"]["__value__"]
				udItemAux = udItem["Damage"]["__value__"]
				udItemCount = udItem["Count"]["__value__"]
				# 内容物带附魔
				advSingle = 0
				if "tag" in udItem and "ench" in udItem["tag"]:
					enchData = udItem["tag"]["ench"]
					for ench in enchData:
						level = ench["lvl"]["__value__"]
						enchId = ench["id"]["__value__"]
						emc = enchantGet((enchId, 1))[1] * level
						advSingle += emc
					addPrice += advSingle * udItemCount
				if "Block" in udItem:
					udItemAux = udItem["Block"]["val"]["__value__"]
				ret = self.GetItemEMC(udItemName, udItemAux)
				udItemPrice = ret[0] * udItemCount
				addPrice += udItemPrice
			return addPrice
		return addPrice

	def FuncPanelModeSwitch(self, mode, emcValue=1, count=1):
		def ModeSet(state, txt1, color, txt2):
			self._btnDict["forgetBtn"].SetVisible(state and self.isCanForget)
			self.countSliderPanel.SetVisible(state)
			self._btnDict["sellOrBuyBtn"].GetChildByPath("/label").asLabel().SetText(txt1)
			# self.emcPriceInfoPanel.GetChildByPath("/infoBg").asImage().SetSpriteColor(color)
			# self.emcPriceInfoPanel.GetChildByPath("/triangle").asImage().SetSpriteColor(color)
			view = self.emcPriceInfoPanel.GetChildByPath("/infoBg/scrollView").asScrollView()
			textPath = view.GetScrollViewContentPath()
			self.uiInst.GetBaseUIControl(textPath).asLabel().SetText(txt2)
		self.exchangeMode = mode
		if mode == "sell":
			ModeSet(False, "出售", self.greenColor, "EMC + %s" % (emcValue*count))
		elif mode == "buy":
			ModeSet(True, "购买", self.redColor, "EMC - %s" % (emcValue * self.sliderValue))

	def GetItemEMC(self, itemName, itemAux):
		"""
		获取某个物品的EMC值
		"""
		key = (itemName, itemAux)
		if key in self.cfg:
			return self.cfg[key][1], True
		else:
			return 1, False

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateEmcConfig(self, args):
		"""服务端改价后通知客户端同步改价"""
		self.cfg.update(args["cfg"])
		self.SetRootPanelVisible(False)
	
	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateForgetBtnState(self, args):
		"""更新遗忘按钮显示,当遗忘状态改变时取消显示物品面板"""
		if args['isCanForget'] != self.isCanForget:
			self.SetRootPanelVisible(False)
		self.isCanForget = args['isCanForget']
