# -*- coding: utf-8 -*-

from ScukeConvertTableScript.ScukeCore.common.log.logManager import LogManager
from ScukeConvertTableScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi
import re
from ScukeConvertTableScript.modClient.manager.clientMgrList import ClientManagerList
from ScukeConvertTableScript.ScukeCore.client import engineApiGac
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance
from ScukeConvertTableScript.modClient.ui.uiDef import UIDef
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr

EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType


class ClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(ClientSystem, self).__init__(namespace, systemName)
		self._loadCompleted = False
		self.InitManager()
		self.itemSellCache = []
		self.itemSellLimit = 63
		self.itemBuyCache = []
		self.itemBuyLimit = 63
		self.timingData = {}
		# 定时购买和定时卖出同时只能生效一个
		self.timingAutoTimer = None

	def ExeSellListItem(self):
		# 执行出售列表中的物品，需要背包拥有这些物品
		# 客户端物品校验
		invItem = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
		if invItem.count(None) == 36: return
		if self.itemSellCache.count(None) == 60: return
		param = {"pid": self.mPlayerId, "data": self.itemSellCache, "limitCount": self.itemSellLimit, "timing": True}
		self.SendMsgToServer("PlayerExeSellListItems", param)

	def ExeBuyListItem(self):
		# 执行购买列表中的物品
		invItem = clientApiMgr.GetPlayerInventoryItemList(self.mPlayerId)
		if invItem.count(None) == 0: return
		if self.itemBuyCache.count(None) == 60: return
		param = {"pid": self.mPlayerId, "data": self.itemBuyCache, "limitCount": self.itemBuyLimit, "timing": True}
		self.SendMsgToServer("PlayerExeBuyListItems", param)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def UpdateClientSysAutoItemData(self, args):
		# 更新玩家自动交易物品数据
		pid, sellList, buyList = args["pid"], args["sell"], args["buy"]
		sellValue, buyValue = args["sellValue"], args["buyValue"]
		self.itemBuyCache = buyList
		self.itemSellCache = sellList
		self.itemSellLimit = sellValue
		self.itemBuyLimit = buyValue

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def UpdateClientTimingData(self, args):
		# 更新玩家定时买卖数据，并开始定时买卖操作
		pid, data = args["pid"], args["data"]
		self.timingData = data
		engineApiGac.CancelTimer(self.timingAutoTimer)
		self.timingAutoTimer = None
		if self.timingData["toggleBuyState"]:
			sec = self.timingData["buyTimingSec"]
			self.timingAutoTimer = "start"
			self.TimingExe(sec, "buy")
		elif self.timingData["toggleSellState"]:
			sec = self.timingData["sellTimingSec"]
			self.timingAutoTimer = "start"
			self.TimingExe(sec, "sell")

	def TimingExe(self, t, mode):
		# 定时执行
		if self.timingAutoTimer is None: return
		if mode == "sell":
			self.ExeSellListItem()
		elif mode == "buy":
			self.ExeBuyListItem()
		self.timingAutoTimer = engineApiGac.AddTimer(t, self.TimingExe, t, mode)

	def InitManager(self):
		print("==========InitManager=========")
		strinfo = re.compile(r'Gac$')
		for mgrCls in ClientManagerList:
			mgr = mgrCls(self)
			setattr(Instance, "m" + strinfo.sub("", mgrCls.__name__), mgr)

	@EngineEvent(priority=10)
	def UiInitFinished(self, args):
		# 这里需要把优先级提到最高，否则其他模块在该事件时设置UI，可能会设置失败
		self.NotifyToServer(modConfig.OnUiInitFinishedEvent, {"playerId": self.mPlayerId})
		Instance.mUIManager.UiInitFinished(args)
		if self._loadCompleted:
			loadingUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveLoading)
			if loadingUI:
				loadingUI.SetActive(False)

	@EngineEvent()
	def OnMouseMiddleDownClientEvent(self, args):
		if args['isDown'] == 0:
			return
		self.NotifyToServer("OnClientDebugTest", {
			'playerId': clientApi.GetLocalPlayerId()
		})

	@EngineEvent()
	def LoadClientAddonScriptsAfter(self, args=None):
		"""加载客户端脚本完成事件"""
		# 在此次做初始化逻辑
		pass
