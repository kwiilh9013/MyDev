# -*- coding: utf-8 -*-
import datetime
import ast
from ScukeConvertTableScript.ScukeCore.common import config
from ScukeConvertTableScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeConvertTableScript.ScukeCore.common.api import itemApi
from ScukeConvertTableScript.ScukeCore.common.api.commonApiMgr import DeepCopy
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.modCommon.cfg import ItemEMCConfig, ItemSortConfig
from ScukeConvertTableScript.ScukeCore.server import engineApiGas
from ScukeConvertTableScript.ScukeCore.server.api import serverApiMgr
from ScukeConvertTableScript.modCommon.cfg.shulkerBoxEnum import ShulkerBoxEnum
import mod.server.extraServerApi as serverApi


class TableMainServer(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(TableMainServer, self).__init__(namespace, systemName)
		self.notice = serverApi.GetEngineCompFactory().CreateGame(engineApiGas.levelId).SetNotifyMsg
		self.playerClientSelectItemCache = {}
		self.hasPower = None
		# 每个地图单独计算物品emc价值
		self.emcConfig = DeepCopy(ItemEMCConfig._AllItemEmc)
		self.emcConfigKey = "scuke_emcConfig"
		self.emcValueKey = "scuke_emcValue"
		self.emcItemsKey = "scuke_emcMemoryItems"
		self.timingExKey = "scuke_emcTimingExchangeRecord"
		self.settingKey = "scuke_emcSetting"
		self.shulkerBoxKeys = ShulkerBoxEnum.__dict__.keys()
		self.playerEMCStorge = {}
		self.playerMemoryItems = {}
		self.playerAutoItems = {}
		# 玩家定时买卖数据
		self.playerTimingData = {}
		# 玩家自动交易产出数据 pid: [str1, str2, ...]
		self.playerTimingRecordData = {}
		# 全局设置
		self.globalSettings = {
			# 其他房客可以设置定价单价
			"otherCanMakePrice": False,
			# 团队知识共享
			"teamMemorySharing": False,
			# 物品定价跨存档，仅房主可用
			"itemEmcIsGlobal": False,
			# 团队EMC值共享
			"teamEmcSharing": False,
			# meta元素UI表现
			"metaVisualUI": True
		}
		# 已被改过价格的物品emc配置数据和其他模组联动的物品EMC数据
		self.hasMakePriceEmcConfig = {}
		# 团队管理
		self._teamEmc = {}
		self._allPlayerTeam = {}

	def Update(self):
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.LinkServer)
	def OnLinkEmcDataSend(self, args):
		# 其他模组联动方案
		udCfg = args["data"]
		cnName = args["sysName"]
		# 将还没有的配置更新过来，防止覆盖修改后的配置
		for key, value in udCfg.items():
			if key not in self.hasMakePriceEmcConfig:
				self.hasMakePriceEmcConfig.update({key: value})
		# self.hasMakePriceEmcConfig.update(udCfg)
		self.notice("§a%s EMC联动成功！" % cnName)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def UpdateGlobalSettingData(self, args):
		# 更新全局设置数据，同时根据情况做出其他处理
		self.globalSettings.update(args["data"])
		self.BroadcastToAllClient("UpdateSettingData", {"data": self.globalSettings})
		self.SaveSettingData()
		# 如果取消了全局emc存储配置，则将房主的配置清空为{}
		globalBool = self.globalSettings["itemEmcIsGlobal"]
		# 将全局emc数据保存在客户端配置中
		self.NotifyToClient(self.hasPower, "SaveGlobalEmcConfig", {"data": self.hasMakePriceEmcConfig if globalBool else {}})
		self.UpdateAllTeamEmcText()
		self.UpdateAllTeamMemoryItems()

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TryPushTableMainUI(self, args):
		pid = args["pid"]
		param = {
			"emcValue": self.GetTeamEMCStr(pid),
			"emcCfg": self.hasMakePriceEmcConfig,
			"memoryList": self.GetTeamMemoryItems(pid),
			"hasPower": pid == self.hasPower,
			"autoItemSellCacheList": self.playerAutoItems[pid]["sell"],
			"autoItemBuyCacheList": self.playerAutoItems[pid]["buy"],
			"autoSellValue": self.playerAutoItems[pid].get("sellValue", 63),
			"autoBuyValue": self.playerAutoItems[pid].get("buyValue", 63),
			"timingData": self.playerTimingData[pid],
			"timingRecordData": self.playerTimingRecordData[pid],
			"globalSetting": self.globalSettings,
			"isCanForget": not self.IsPlayerHasTeam(pid)
		}
		self.NotifyToClient(pid, "PushTableMainUI", param)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TryExchangeSlotItem(self, args):
		# 对指定槽位的物品进行交换或移动
		pid = args["pid"]
		itemComp = engineApiGas.compFactory.CreateItem(pid)
		itemArrayList = args["data"]
		# 用于判定是不是批量合堆
		isStack = args["isStacking"]
		if not itemArrayList: return
		notifyToClientList = []
		LenList = len(itemArrayList)
		lastCount = 0
		targetItem = itemArrayList[0][6]
		toSlot = None
		for index, value in enumerate(itemArrayList):
			fromSlotItemDict = itemApi.FormatItemInfo(value[2])
			toSlotItemDict = itemApi.FormatItemInfo(value[6])
			fromSlot, toSlot = value[3], value[4]
			moveCount = value[5]
			# 记录移动后的槽位中的物品
			moveToItemDict = DeepCopy(fromSlotItemDict)
			moveToItemDict["count"] = moveCount
			# 移动后起始槽位剩余的物品数量
			residueCount = fromSlotItemDict["count"] - moveCount
			# 如果目标槽位和起始槽位的物品一致，且堆叠数量没超过最大数量就合堆
			if itemApi.IsTwoItemSame(toSlotItemDict, moveToItemDict, engineApiGas.compFactory, engineApiGas.levelId):
				engineApiGas.SetInvItemNum(pid, fromSlot, residueCount)
				if not toSlotItemDict:
					itemComp.SetPlayerAllItems({(0, toSlot): moveToItemDict})
				else:
					if not isStack:
						addMoveLastCount = toSlotItemDict["count"] + moveCount
						engineApiGas.SetInvItemNum(pid, toSlot, addMoveLastCount)
					else:
						lastCount += moveCount
			# 如果两个槽位的物品不一致
			else:
				itemComp.SetPlayerAllItems({(0, toSlot): fromSlotItemDict})
				itemComp.SetPlayerAllItems({(0, fromSlot): toSlotItemDict})
			notifyToClientList.append([value[0], value[1], value[3], value[4], value[7]])
		if isStack:
			targetItem["count"] += lastCount
			itemComp.SetPlayerAllItems({(0, toSlot): targetItem})
		# 通知客户端做出物品飞行动画
		self.NotifyToClient(pid, "StartItemFlyingAnim", {"data": notifyToClientList})

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def OnItemGrouping(self, args):
		# 对物品进行分堆操作
		pid, fromSlot = args["pid"], args["fromSlot"]
		toSlots = args["toSlots"]
		self.SetPlayerSelectItem(pid, args["cacheItem"])
		ret = self.GetPlayerSelectItem(pid)
		if not ret: return
		totalCount = ret["count"]
		slotNum = len(toSlots)
		sCount = totalCount // slotNum
		lCount = totalCount % slotNum
		toSlotItem = DeepCopy(ret)
		fromSlotItem = DeepCopy(ret)
		toSlotItem["count"] = sCount
		fromSlotItem["count"] = lCount
		itemComp = engineApiGas.compFactory.CreateItem(pid)
		k = {}
		for slot in toSlots:
			k.update({(0, slot): toSlotItem})
		itemComp.SetPlayerAllItems(k)
		itemComp.SetPlayerAllItems({(0, fromSlot): fromSlotItem})
		self.NotifyToClient(pid, "RefreshInventoryUI", {})

	# region 单次买卖
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def OnSellingItem(self, args):
		pid, data = args["pid"], args["data"]
		slot = data[0]
		count = data[3]
		name = data[1]
		aux = data[2]
		emcPrice = self.GetEmcPrice(name, aux)
		totalPrice = count * emcPrice
		itemComp = engineApiGas.compFactory.CreateItem(pid)
		itemDict = itemComp.GetPlayerItem(0, slot, True)
		newDict = itemApi.FormatItemInfo(itemDict)
		itemComp.SetPlayerAllItems({(0, slot): {}})
		newDict["count"] = 1
		addEnchValue = self.GetItemEnchantEMCValue(newDict)
		totalPrice += count * addEnchValue
		# itemName, aux, itemDict
		memoryData = (data[1], data[2], newDict)
		# 如果潜影盒里有道具，则额外计算道具的价值，但不会将里面的道具添加到记忆列表中
		if data[1].split(":")[1] in self.shulkerBoxKeys:
			addPrice = self.GetContainerItemsEmc(newDict)
			if addPrice > 0:
				totalPrice += addPrice
		self.AddPlayerEMC(pid, totalPrice)
		self.UpdatePlayerMemoryItems(pid, memoryData, "add", None)
		emc = self.GetTeamEMC(pid)
		self.NotifyToClient(pid, "RefreshInventoryUI", {"emcValue": emc, "endSelecting": True})
		self.UpdateTeamEmcText(pid)
		self.NotifyToClient(pid, "UpdateEMCValue", {"value": emc})
		# 更新已卖出物品列表信息
		self.NotifyToClient(pid, "UpdateEyePanelData", {"memoryList": self.playerMemoryItems[pid]})
		self.UpdateTeamMemoryItems(pid)
		self.SendMsgToClient(pid, 'HasSellItem', {"itemName": name})

	def GetEmcPrice(self, name, aux):
		"""获得物品的价值"""
		emcPrice = 1
		if (name, aux) in self.hasMakePriceEmcConfig:
			emcPrice = self.hasMakePriceEmcConfig.get((name, aux), ["", 1])[1]
		else:
			emcPrice = self.emcConfig.get((name, aux), ["", 1])[1]
		return emcPrice

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def OnBuyingItem(self, args):
		pid = args["pid"]
		itemDict = args["item"]
		slot = args.get("slot", None)
		name, aux = itemDict["newItemName"], itemDict["newAuxValue"]
		count = itemDict["count"]
		emcPrice = self.GetEmcPrice(name, aux)
		totalPrice = count * emcPrice
		addEnchValue = self.GetItemEnchantEMCValue(itemDict)
		totalPrice += count * addEnchValue
		# 如果潜影盒里有道具
		if name.split(":")[1] in self.shulkerBoxKeys:
			addPrice = self.GetContainerItemsEmc(itemDict)
			if addPrice > 0:
				totalPrice += addPrice
		myEmc = self.GetTeamEMC(pid)
		if totalPrice > myEmc:
			self.NotifyToClient(pid, "OnEMCCannotBuy", {})
			return
		self.SubPlayerEMC(pid, totalPrice)
		emc = self.GetTeamEMC(pid)
		# 返回购买物品影响的槽位和槽位内的物品itemDict
		retSlotDict = serverApiMgr.SpawnItemsToInventory(self, pid, [itemDict, ])
		buyFlyData = {"fromSlot": slot, "toSlots": retSlotDict.keys()}
		self.NotifyToClient(pid, "RefreshInventoryUI", {"emcValue": emc, "endSelecting": True, "flyData": buyFlyData})
		self.UpdateTeamEmcText(pid)
		self.NotifyToClient(pid, "UpdateEMCValue", {"value": emc})
		self.SendMsgToClient(pid, 'HasBuyItem', {"itemName": name})

	# endregion

	def GetItemEnchantEMCValue(self, itemDict):
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
				ret = self.emcConfig.get((udItemName, udItemAux), ["", 1])
				udItemPrice = ret[1] * udItemCount
				addPrice += udItemPrice
			return addPrice
		return addPrice

	def GetPlayerSelectItem(self, pid):
		return self.playerClientSelectItemCache.get(pid, None)

	def SetPlayerSelectItem(self, pid, itemDict):
		self.playerClientSelectItemCache[pid] = itemDict

	# region 玩家进入退出服务端事件
	@EngineEvent()
	def AddServerPlayerEvent(self, args):
		"""
		玩家加入，初始化和读取各项数据
		1.emc物品记忆
		2.emc剩余值
		3.自动买卖记录
		"""
		pid = args["id"]
		self.playerMemoryItems[pid] = []
		self.playerAutoItems[pid] = {
			"sell": [None for i in range(0, 60)],
			"buy": [None for i in range(0, 60)],
			"sellValue": 63,
			"buyValue": 63
		}
		self.playerTimingData[pid] = {
			"buyState": False,
			"sellState": False,
			"buySValue": 0.0,
			"sellSValue": 0.0
		}
		self.LoadPlayerMemoryItems(pid)
		self.LoadPlayerEMC(pid)
		self.LoadTimingRecordData(pid)
		self.LoadSettingData()
		self.UpdateTeamMemoryItems(pid)
		self.UpdateTeamEmcText(pid)
		if len(serverApi.GetPlayerList()) < 2:
			self.hasPower = pid
			engineApiGas.SetCommand("/gamerule sendcommandfeedback false", pid, False)

	@EngineEvent()
	def PlayerIntendLeaveServerEvent(self, args):
		"""
		玩家离开，保存各项数据，如果是房主，额外保存物品emc价值数据
		1.emc剩余值
		2.emc物品记忆
		3.自动买卖记录
		"""
		pid = args["playerId"]
		self.SavePlayerEMC(pid)
		self.SavePlayerMemoryItems(pid)
		self.SaveTimingRecordData(pid)
		if pid == self.hasPower:
			self.SaveWorldEmcConfig()
			self.SaveSettingData()
			if self.globalSettings["itemEmcIsGlobal"]:
				# 将全局emc数据保存在客户端配置中
				self.NotifyToClient(pid, "SaveGlobalEmcConfig", {"data": self.hasMakePriceEmcConfig})

	def GetPlayerEMC(self, pid):
		return self.playerEMCStorge.get(pid, 0)

	# region 对EMC值进行增加删除
	def AddPlayerEMC(self, pid, value):
		"""添加玩家EMC值,同时刷新团队EMC总量"""
		if self.globalSettings['teamEmcSharing']:
			if pid in self._allPlayerTeam:
				opid = pid
			else:
				opid = self.FindOwner(pid)
			if opid in self._teamEmc:
				self._teamEmc[opid] += value
			else:
				self._teamEmc[opid] = value
		self.playerEMCStorge[pid] += value
		self.SavePlayerEMC(pid)

	def SubPlayerEMC(self, pid, value):
		"""减少玩家EMC值,同时刷新团队EMC总量"""
		if self.globalSettings['teamEmcSharing']:
			if pid in self._allPlayerTeam:
				opid = pid
			else:
				opid = self.FindOwner(pid)
			totelEmc = self._teamEmc[opid]
			tlist = self._allPlayerTeam[opid]
			for emcPid in self.playerEMCStorge:
				if emcPid == opid or emcPid in tlist:
					subValue = float(value) * (float(self.playerEMCStorge[emcPid]) / float(totelEmc))
					if subValue - int(subValue) > 0.5:
						subValue = int(subValue) + 1
					else:
						subValue = int(subValue)
					self.playerEMCStorge[emcPid] -= subValue
					self._teamEmc[opid] -= subValue
					self.SavePlayerEMC(emcPid)
		else:
			self.playerEMCStorge[pid] -= value
			if self.playerEMCStorge[pid] < 0:
				pass
		self.SavePlayerEMC(pid)

	# endregion

	def SetPlayerEMC(self, pid, value):
		self.playerEMCStorge[pid] = value

	def SavePlayerEMC(self, pid):
		value = self.GetPlayerEMC(pid)
		serverApiMgr.SetExtraData(pid, self.emcValueKey, value)
		serverApiMgr.compFactory.CreateExtraData(pid).SaveExtraData()

	def LoadPlayerEMC(self, pid):
		ret = serverApiMgr.GetExtraData(pid, self.emcValueKey)
		self.SetPlayerEMC(pid, ret if ret is not None else 0)

	def LoadPlayerMemoryItems(self, pid):
		ret = serverApiMgr.GetExtraData(pid, self.emcItemsKey)
		if ret:
			self.playerMemoryItems[pid] = ret

	def SavePlayerMemoryItems(self, pid):
		serverApiMgr.SetExtraData(pid, self.emcItemsKey, self.playerMemoryItems[pid])
		serverApiMgr.compFactory.CreateExtraData(pid).SaveExtraData()

	def LoadSettingData(self):
		ret = serverApiMgr.GetExtraData(None, self.settingKey)
		if ret and type(ret) == dict:
			self.globalSettings.update(ret)

	def SaveSettingData(self):
		serverApiMgr.SetExtraData(None, self.settingKey, self.globalSettings)
		serverApiMgr.compFactory.CreateExtraData(serverApiMgr.levelId).SaveExtraData()

	def LoadWorldEmcConfig(self):
		# 读取存档的物品EMC价值数据
		cfg = serverApiMgr.GetExtraData(None, self.emcConfigKey)
		if cfg and type(cfg) == dict:
			self.emcConfig.update(cfg)
			self.hasMakePriceEmcConfig.update(cfg)

	def SaveWorldEmcConfig(self):
		serverApiMgr.SetExtraData(None, self.emcConfigKey, self.hasMakePriceEmcConfig)
		serverApiMgr.compFactory.CreateExtraData(serverApiMgr.levelId).SaveExtraData()

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.TableMainClient)
	def LoadGlobalEmcConfig(self, args):
		# 从房主处读取全局emc定价配置
		pid, data = args["pid"], args["emcData"]
		if pid != self.hasPower: return
		if not data and type(data) == dict:
			# 如果客户端传递的全局数据是空的字典，则更改设置
			self.globalSettings["itemEmcIsGlobal"] = False
		if data and type(data) == dict:
			# 同时需要更改设置
			self.globalSettings["itemEmcIsGlobal"] = True
			self.emcConfig.update(data)
			self.hasMakePriceEmcConfig.update(data)
			# 改价后通知所有客户端，变更价格
			self.BroadcastToAllClient("UpdateEmcConfig", {"cfg": self.hasMakePriceEmcConfig})

	def LoadTimingRecordData(self, pid):
		# 加载定时买卖数据
		data = serverApiMgr.GetExtraData(pid, self.timingExKey)
		if data and type(data) == list:
			self.playerTimingRecordData[pid] = data
		else:
			self.playerTimingRecordData[pid] = []

	def SaveTimingRecordData(self, pid):
		# 保存定时买卖数据
		serverApiMgr.SetExtraData(pid, self.timingExKey, self.playerTimingRecordData[pid])
		serverApiMgr.compFactory.CreateExtraData(pid).SaveExtraData()

	@EngineEvent()
	def LoadServerAddonScriptsAfter(self, args=None):
		self.LoadWorldEmcConfig()

	def UpdatePlayerMemoryItems(self, pid, data, method, index=None):
		# 记录已售出的物品，需要同时记录物品itemDict
		if method == "del":
			if data in self.playerMemoryItems[pid]:
				self.playerMemoryItems[pid].remove(data)
		if method == "add":
			if data not in self.playerMemoryItems[pid]:
				self.playerMemoryItems[pid].append(data)
		self.SavePlayerMemoryItems(pid)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TryToForgetOneItem(self, args):
		# 遗忘某个物品
		pid, index = args["pid"], args["itemIndex"]
		self.playerMemoryItems[pid].pop(index)
		# 更新已卖出物品列表信息
		self.NotifyToClient(pid, "UpdateEyePanelData", {"memoryList": self.playerMemoryItems[pid]})

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def OnMakePrice(self, args):
		# emc物品更改定价
		pid, emcItem = args["pid"], args["data"]
		if pid != self.hasPower and not self.globalSettings["otherCanMakePrice"]:
			return
		self.emcConfig.update(emcItem)
		self.hasMakePriceEmcConfig.update(emcItem)
		# 改价后通知所有客户端，变更价格
		self.BroadcastToAllClient("UpdateEmcConfig", {"cfg": self.hasMakePriceEmcConfig})
		self.SaveWorldEmcConfig()
		if self.globalSettings["itemEmcIsGlobal"]:
			# 将全局emc数据保存在客户端配置中
			self.NotifyToClient(self.hasPower, "SaveGlobalEmcConfig", {"data": self.hasMakePriceEmcConfig})

	# region 一键卖出
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TrySellInvAllItems(self, args):
		# 尝试将背包所有物品卖出
		pid = args["pid"]
		itemList = serverApiMgr.GetInventoryItems(pid)
		itemComp = engineApiGas.compFactory.CreateItem(pid)
		sumPrice = 0
		for item in itemList:
			if item is None: continue
			itemName = item["newItemName"]
			aux = item["newAuxValue"]
			count = item["count"]
			emcPrice = self.GetEmcPrice(itemName, aux)
			itemPrice = count * emcPrice
			sumPrice += itemPrice
			# 更新到记忆列表中
			newDict = itemApi.FormatItemInfo(item)
			newDict["count"] = 1
			# itemName, aux, itemDict
			memoryData = (itemName, aux, newDict)
			addEnchValue = self.GetItemEnchantEMCValue(newDict)
			sumPrice += count * addEnchValue
			self.UpdatePlayerMemoryItems(pid, memoryData, "add", None)
			# 如果潜影盒里有道具，则额外计算道具的价值，但不会将里面的道具添加到记忆列表中
			if itemName.split(":")[1] in self.shulkerBoxKeys:
				addPrice = self.GetContainerItemsEmc(newDict)
				if addPrice > 0:
					sumPrice += addPrice
		k = {}
		for i in range(0, 36):
			k.update({(0, i): {}})
		itemComp.SetPlayerAllItems(k)
		self.AddPlayerEMC(pid, sumPrice)
		emc = self.GetTeamEMC(pid)
		self.NotifyToClient(pid, "RefreshInventoryUI", {"emcValue": emc, "endSelecting": True})
		self.UpdateTeamEmcText(pid)
		self.NotifyToClient(pid, "UpdateEMCValue", {"value": emc})
		# 更新已卖出物品列表信息
		self.NotifyToClient(pid, "UpdateEyePanelData", {"memoryList": self.playerMemoryItems[pid]})
		self.UpdateTeamMemoryItems(pid)

	# endregion

	# region 智能买卖
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def UpdateAutoItemList(self, args):
		# 更新玩家的智能买卖列表
		pid, sellList, buyList = args["pid"], args["sell"], args["buy"]
		sellValue, buyValue = args["sellValue"], args["buyValue"]
		self.playerAutoItems[pid].update(
			{"sell": sellList, "buy": buyList, "sellValue": sellValue, "buyValue": buyValue})

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def PlayerExeSellListItems(self, args):
		# 执行物品批量卖出
		pid, data = args["pid"], args["data"]
		limitCount = args["limitCount"]
		isTiming = args.get("timing", False)
		# 标记背包中每一种物品可批量购买和出售的物品
		markItemDict = self.GetMarkItemDict(pid, data)
		# 计算批量卖出的物品的总价值，以及背包需要删除的该物品的数量总和
		allAddEmcValue = 0
		for itemKey, itemDict in markItemDict.items():
			nCount = itemDict["count"]
			aux = itemDict["newAuxValue"]
			itemName = itemDict["newItemName"]
			if nCount <= limitCount:
				continue
			deltaCount = nCount - limitCount
			itemDict["count"] = 1
			emcPrice = self.GetEmcPrice(itemName, aux)
			singlePrice = emcPrice * deltaCount
			allAddEmcValue += singlePrice
			engineApiGas.SetCommand("/clear @s %s %s %s" % (itemName, aux, deltaCount), pid, False)
			self.UpdatePlayerMemoryItems(pid, (itemName, aux, itemDict), "add", None)
			# 保存定时买卖记录
			if isTiming:
				itemInfo = self.GetItemInfo(pid, itemDict)
				self.AddTimingExchangeRecord(pid, "sell", itemInfo, deltaCount)
		if allAddEmcValue == 0: return
		self.AddPlayerEMC(pid, allAddEmcValue)
		emc = self.GetTeamEMC(pid)
		self.NotifyToClient(pid, "RefreshInventoryUI", {"emcValue": emc, "endSelecting": True})
		self.UpdateTeamEmcText(pid)
		self.NotifyToClient(pid, "UpdateEMCValue", {"value": emc})
		# 更新已卖出物品列表信息
		self.NotifyToClient(pid, "UpdateEyePanelData", {"memoryList": self.playerMemoryItems[pid]})
		self.UpdateTeamMemoryItems(pid)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def PlayerExeBuyListItems(self, args):
		# 执行物品批量买入
		pid, data = args["pid"], args["data"]
		limitCount = args["limitCount"]
		isTiming = args.get("timing", False)
		markItemDict = self.GetMarkItemDict(pid, data)
		allSubEmcValue = 0
		nowEmc = self.GetTeamEMC(pid)
		# 如果背包内没有这类需要购买的物品
		keyList = []
		for i, k in enumerate(data):
			if k is not None:
				keyList.append((k["newItemName"], k["newAuxValue"], k))
		for key in keyList:
			if (key[0], key[1]) not in markItemDict:
				key[2]["count"] = 0
				markItemDict[(key[0], key[1])] = key[2]
		for itemKey, itemDict in markItemDict.items():
			nCount = itemDict["count"]
			aux = itemDict["newAuxValue"]
			itemName = itemDict["newItemName"]
			if nCount >= limitCount:
				continue
			deltaCount = limitCount - nCount
			emcPrice = self.GetEmcPrice(itemName, aux)
			singlePrice = emcPrice * deltaCount
			# EMC不足，终止操作
			if allSubEmcValue + singlePrice > nowEmc:
				break
			allSubEmcValue += singlePrice
			engineApiGas.SetCommand("/give @s %s %s %s" % (itemName, deltaCount, aux), pid, False)
			# 保存定时买卖记录
			if isTiming:
				itemInfo = self.GetItemInfo(pid, itemDict)
				self.AddTimingExchangeRecord(pid, "buy", itemInfo, deltaCount)
		if allSubEmcValue == 0: return
		self.SubPlayerEMC(pid, allSubEmcValue)
		emc = self.GetTeamEMC(pid)
		self.NotifyToClient(pid, "RefreshInventoryUI", {"emcValue": emc, "endSelecting": True})
		self.UpdateTeamEmcText(pid)
		self.NotifyToClient(pid, "UpdateEMCValue", {"value": emc})

	# endregion

	def GetMarkItemDict(self, pid, data):
		invItems = serverApiMgr.GetInventoryItems(pid)
		cInvItems = DeepCopy(invItems)
		markItemDict = {}
		for index, k in enumerate(cInvItems):
			if k is None: continue
			k = itemApi.FormatItemInfo(k)
			k["count"] = 1
			if k in data:
				name = k["newItemName"]
				aux = k["newAuxValue"]
				itemKey = (name, aux)
				# 过滤掉附魔书、武器这类道具，如果是
				maxStack = serverApiMgr.GetItemMaxStackSize(name, aux)
				if maxStack == 1: continue
				itemNew = itemApi.FormatItemInfo(invItems[index])
				if itemKey not in markItemDict:
					markItemDict[itemKey] = itemNew
				else:
					markItemDict[itemKey]["count"] += itemNew["count"]
		return markItemDict

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def UpdateTimingData(self, args):
		# 更新玩家定时买卖数据
		pid, data = args["pid"], args["data"]
		self.playerTimingData[pid] = {
			"buyState": data["toggleBuyState"],
			"sellState": data["toggleSellState"],
			"buySValue": data["buyTimingSec"],
			"sellSValue": data["sellTimingSec"]
		}

	def AddTimingExchangeRecord(self, pid, mode, itemInfo, c=1):
		# 更新定时交易记录
		str1 = "出售了" if mode == "sell" else "购买了"
		dateStr = str(datetime.date.today())
		now = datetime.datetime.now()
		timeStr = now.strftime("%H:%M:%S")
		itemCNName = itemInfo.get("itemName", "未知")
		mergeStr = "%s %s  %s %s x%s" % (dateStr, timeStr, str1, itemCNName, c)
		self.playerTimingRecordData[pid].append(mergeStr)
		if len(self.playerTimingRecordData[pid]) > 50:
			self.playerTimingRecordData[pid].pop(0)
		self.SaveTimingRecordData(pid)
		self.NotifyToClient(pid, "UpdateTimingRecord", {"data": self.playerTimingRecordData[pid]})

	def GetItemInfo(self, pid, itemDict):
		name, aux = itemDict["newItemName"], itemDict["newAuxValue"]
		enchant = "userData" in itemDict and itemDict["userData"] is not None and "ench" in itemDict["userData"]
		comp = engineApiGas.compFactory.CreateItem(pid)
		return comp.GetItemBasicInfo(name, aux, enchant)

	# region 团队管理
	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
	def AcceptInvite(self, args):
		opid, tpid, self._allPlayerTeam = args['opid'], args['tpid'], args['allPlayerTeam']
		if self.globalSettings['teamEmcSharing']:
			# 刷新组队各个成员的EMC UI
			self.UpdateTeamEmcText(opid)
		if self.globalSettings['teamMemorySharing']:
			self.UpdateTeamMemoryItems(opid)
			self.UpdateTeamForgetBtn(opid)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
	def LeaveTeam(self, args):
		opid, tpid, self._allPlayerTeam = args['opid'], args['tpid'], args['allPlayerTeam']
		if self.globalSettings['teamEmcSharing']:
			if opid in self._allPlayerTeam and 'newopid' in args:
				# 说明是队长
				for pid in (opid,args['newopid']):
					self.UpdateTeamEmcText(pid)
			else:
				for pid in (opid,tpid):
					self.UpdateTeamEmcText(pid)
		if self.globalSettings['teamMemorySharing']:
			if opid in self._allPlayerTeam and 'newopid' in args:
				# 说明是队长
				for pid in (opid,args['newopid']):
					self.UpdateTeamMemoryItems(pid)
					self.UpdateTeamForgetBtn(pid)
			else:
				for pid in (opid,tpid):
					self.UpdateTeamMemoryItems(pid)
					self.UpdateTeamForgetBtn(pid)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
	def KickTeam(self, args):
		opid, tpid, self._allPlayerTeam = args['opid'], args['tpid'], args['allPlayerTeam']
		if self.globalSettings['teamEmcSharing']:
			for pid in (opid,tpid):
				self.UpdateTeamEmcText(pid)
		if self.globalSettings['teamMemorySharing']:
			for pid in (opid,tpid):
				self.UpdateTeamMemoryItems(pid)
				self.UpdateTeamForgetBtn(pid)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
	def TransferTeam(self, args):
		opid, tpid, self._allPlayerTeam = args['opid'], args['tpid'], args['allPlayerTeam']
		if self.globalSettings['teamEmcSharing']:
			self.UpdateTeamEmcText(tpid)
		if self.globalSettings['teamMemorySharing']:
			self.UpdateTeamMemoryItems(tpid)
			self.UpdateTeamForgetBtn(tpid)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
	def HasUpdateAllPlayerTeam(self, args):
		self._allPlayerTeam = args['allPlayerTeam']

	def GetTeamMemoryItems(self, pid):
		"""获取指定玩家的知识记忆,并储团队知识"""
		if self.globalSettings["teamMemorySharing"]:
			opid = pid
			if opid not in self._allPlayerTeam:
				opid = self.FindOwner(pid)
			tlist = self._allPlayerTeam.get(opid,None)
			oMemoryItems = DeepCopy(self.playerMemoryItems.get(opid,[]))
			if tlist:
				def RemoveDuplicatesDicts(lst):
					# 辅助函数：将字典转换为字符串表示，用于哈希化
					def dictToHashable(d):
						# 将字典转换为标准字符串表示
						return repr(d)
					# 使用集合去重，并转换回字典
					seen = set()
					uniqueDicts = []
					literal_eval= ast.literal_eval
					for d in lst:
						# 使用 repr 生成可哈希字符串
						hashable = dictToHashable(d)
						# 检查是否已存在，若不存在则添加
						if hashable not in seen:
							seen.add(hashable)
							uniqueDicts.append(literal_eval(hashable))
					return uniqueDicts
				for tpid in tlist:
					tMemoryItems = self.playerMemoryItems.get(tpid,[])
					oMemoryItems += tMemoryItems
				oMemoryItems = RemoveDuplicatesDicts(oMemoryItems) 
		else:
			oMemoryItems = self.playerMemoryItems.get(pid,[])
		return oMemoryItems

	def UpdateTeamMemoryItems(self, pid):
		"""刷新指定玩家的队伍中所有玩家的知识记忆UI"""
		NotifyToClient = self.NotifyToClient
		if self.globalSettings["teamMemorySharing"]:
			opid = pid
			if pid not in self._allPlayerTeam:
				opid = self.FindOwner(pid)
			tMemoryItems = self.GetTeamMemoryItems(pid)
			tlist = self._allPlayerTeam.get(opid)
			NotifyToClient(opid, "RefreshEyePanelDataUI", {"memoryList": tMemoryItems})
			if tlist:
				for tpid in tlist:
					NotifyToClient(tpid, "RefreshEyePanelDataUI", {"memoryList": tMemoryItems})
		else:
			opid = pid
			if pid not in self._allPlayerTeam:
				opid = self.FindOwner(pid)
			oMemoryItems = self.GetTeamMemoryItems(opid)
			tlist = self._allPlayerTeam.get(opid)
			NotifyToClient(opid, "RefreshEyePanelDataUI", {"memoryList": oMemoryItems})
			if tlist:
				for tpid in tlist:
					tMemoryItems = self.GetTeamMemoryItems(tpid)
					NotifyToClient(tpid, "RefreshEyePanelDataUI", {"memoryList": tMemoryItems})

	def UpdateAllTeamMemoryItems(self):
		"""刷新所有玩家的知识记忆UI"""
		for opid in self._allPlayerTeam:
			self.UpdateTeamMemoryItems(opid)
			tlist = self._allPlayerTeam[opid]
			if tlist:
				for tpid in tlist:
					self.UpdateTeamMemoryItems(tpid)

	def IsPlayerHasTeam(self, pid):
		"""
		判断玩家是否处于组队状态
		玩家为队员/玩家是队长且有队员时候 return True
		"""
		if self._allPlayerTeam:
			if pid in self._allPlayerTeam:
				if self._allPlayerTeam[pid]:
					return True
			else:
				return True
		return False

	def FindOwner(self, tpid):
		"""
		寻找某个玩家的队长
		return 队长id/None
		"""
		for opid in self._allPlayerTeam:
			memberPlayerList = self._allPlayerTeam[opid]
			if memberPlayerList:
				for pid in memberPlayerList:
					if tpid == pid:
						return opid
		return None

	def GetTeamEMC(self, pid):
		"""
		获取指定队伍的EMC总值;储存该团队EMC值
		输入 = 玩家id
		返回 = int tmc
		"""
		if self.globalSettings['teamEmcSharing']:
			opid = pid
			if pid not in self._allPlayerTeam:
				opid = self.FindOwner(opid)
			tlist = self._allPlayerTeam.get(opid)
			GetPlayerEMC = self.GetPlayerEMC
			oEmc = GetPlayerEMC(opid)
			emc = oEmc
			if tlist:
				for pid in tlist:
					emc += GetPlayerEMC(pid)
			self._teamEmc[opid] = emc
		else:
			emc = self.GetPlayerEMC(pid)
		return emc
	
	def GetTeamEMCStr(self, pid):
		"""
		获取指定队伍的EMC总值,如果为团队则会有团队字样
		输入 = 玩家id
		返回 = str tmc
		"""
		if self.globalSettings['teamEmcSharing']:
			opid = pid
			if pid not in self._allPlayerTeam:
				opid = self.FindOwner(opid)
			tlist = self._allPlayerTeam.get(opid)
			GetPlayerEMC = self.GetPlayerEMC
			oEmc = GetPlayerEMC(opid)
			emc = oEmc
			if tlist:
				for pid in tlist:
					emc += GetPlayerEMC(pid)
				emc = str(emc)+"(团队)"
		else:
			emc = self.GetPlayerEMC(pid)
		return str(emc)

	def UpdateTeamEmcText(self, pid):
		"""
		刷新指定队伍中所有玩家EMC值显示;储存该团队EMC值
		输入=玩家id
		"""
		if self.globalSettings['teamEmcSharing']:
			NotifyToClient = self.NotifyToClient
			if pid in self._allPlayerTeam:
				opid = pid
			else:
				opid = self.FindOwner(pid)
			emc = self.GetTeamEMC(opid)
			tlist = self._allPlayerTeam.get(opid)
			if tlist:
				emc = str(emc) + '(团队)'
				NotifyToClient(opid, "RefreshEMCTextUI", {"emcValue": emc})
				for tpid in tlist:
					NotifyToClient(tpid, "RefreshEMCTextUI", {"emcValue": emc})
			else:
				NotifyToClient(opid, "RefreshEMCTextUI", {"emcValue": emc})

	def UpdateAllTeamEmcText(self):
		"""
		刷新所有队伍玩家EMC值显示;储存团队EMC值
		"""
		NotifyToClient = self.NotifyToClient
		if self.globalSettings['teamEmcSharing']:
			if self._allPlayerTeam:
				for opid in self._allPlayerTeam:
					emc = self.GetTeamEMC(opid)
					tlist = self._allPlayerTeam[opid]
					if tlist:
						emc=str(emc)+'(团队)'
						NotifyToClient(opid, "RefreshEMCTextUI", {"emcValue": emc})
						for tpid in tlist:
							NotifyToClient(tpid, "RefreshEMCTextUI", {"emcValue": emc})
					else:
						NotifyToClient(opid, "RefreshEMCTextUI", {"emcValue": emc})
		else:
			for opid in self._allPlayerTeam:
				emc = self.GetPlayerEMC(opid)
				tlist = self._allPlayerTeam[opid]
				NotifyToClient(opid, "RefreshEMCTextUI", {"emcValue": emc})
				if tlist:
					for tpid in tlist:
						emc = self.GetPlayerEMC(tpid)
						NotifyToClient(tpid, "RefreshEMCTextUI", {"emcValue": emc})
	
	def UpdateTeamForgetBtn(self, pid):
		"""刷新指定玩家队伍的遗忘"""
		opid = pid
		if opid not in self._allPlayerTeam:
			opid = self.FindOwner(pid)
		if not self.IsPlayerHasTeam(opid):
			self.SendMsgToClient(opid, 'UpdateForgetBtnState', {'isCanForget': True})
		else:
			self.SendMsgToClient(opid, 'UpdateForgetBtnState', {'isCanForget': False})
		tlist = self._allPlayerTeam.get(opid, None)
		if tlist:
			for pid in tlist:
				self.SendMsgToClient(pid, 'UpdateForgetBtnState', {'isCanForget': False})

	@EngineEvent()
	def ServerChatEvent(self, args):
		"""玩家指令监听事件"""
		message = str(args['message'])
		playerId = args['playerId']
		if message == 'reset scukectui':
			args['cancel'] = True
			self.SendMsgToClient(playerId, "ResetHudUI", {})