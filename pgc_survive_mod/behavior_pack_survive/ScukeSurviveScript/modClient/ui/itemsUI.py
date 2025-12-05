# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
ViewBinder = clientApi.GetViewBinderCls()


class ItemsUI(ModBaseUI):
	"""道具物品 UI"""
	def __init__(self, namespace, name, param):
		super(ItemsUI, self).__init__(namespace, name, param)
		# 按钮列表，顺序会和config上配置的对应上
		# btn0 = 带CD图的按钮
		self._btnList = []
		self._btnMaxCount = 0

		# 记录物品和按钮的对应关系: {itemName: index}
		self._itemAndBtnDict = {}

		# 设置CD进度的timer
		self._btnCDTimers = {}

		pass

	def Destroy(self):
		super(ItemsUI, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ShowItemUseUIEvent, self.ShowItemUseUIEvent)
		pass

	def Create(self):
		super(ItemsUI, self).Create()
		# 按钮UI
		self.itemsBtnPanel = self.GetBaseUIControl("/panel_items_btn")
		# 按钮
		index = 0
		while True:
			# 判断该路径的UI是否存在
			obj = self.itemsBtnPanel.GetChildByPath("/btn{}".format(index))
			if obj:
				# 记录
				btnObj = obj.asButton()
				self._btnList.append(btnObj)
				# 监听响应
				clientApiMgr.SetBtnTouchUpCallback(btnObj, self.OnItemsBtnClicked, {"index": index})
				index += 1
			else:
				break
		self._btnMaxCount = index

		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.ShowItemUseUIEvent, self.ShowItemUseUIEvent)
		pass

	# region 功能
	def ShowItemUseUIEvent(self, args):
		"""道具物品UI的订阅事件"""
		state = args.get("state", False)
		itemName = args.get("itemName")
		self.ShowItemUseUI(state, itemName)
		pass

	def ShowItemUseUI(self, state, itemName):
		"""显示/隐藏道具物品UI"""
		if state:
			cfg = itemsConfig.GetItemsUIConfig(itemName)
			# 显示指定的按钮
			index = cfg.get("buttonIndex", 0)
			btnObj = self.GetBtnObjByIndex(index)
			if btnObj:
				clientApiMgr.SetUIVisible(btnObj, True)
				# 设置图片、文字
				if cfg.get("buttonImage"):
					clientApiMgr.SetButtonImage(btnObj, cfg["buttonImage"], cfg["buttonTexturePress"])
				if cfg.get("buttonText"):
					clientApiMgr.SetButtonText(btnObj, cfg["buttonText"])
				# 记录物品和按钮的对应关系
				self._itemAndBtnDict[itemName] = index
		else:
			# 隐藏
			index = self._itemAndBtnDict.pop(itemName, None)
			btnObj = self.GetBtnObjByIndex(index)
			if btnObj:
				clientApiMgr.SetUIVisible(btnObj, False)
		pass

	def GetBtnObjByIndex(self, index):
		"""根据索引获取按钮对象"""
		if index is not None:
			if index < self._btnMaxCount:
				return self._btnList[index]
			self.logger.error("道具物品使用按钮，索引超过按钮数量，index={}".format(index))
		return None
	# endregion

	# region 按钮响应
	def OnItemsBtnClicked(self, args):
		"""按钮按下事件"""
		params = args.get("AddTouchEventParams", {})
		index = params.get("index")
		itemName = None
		for item, btnIndex in self._itemAndBtnDict.iteritems():
			if btnIndex == index:
				itemName = item
				break
		if itemName:
			cfg = itemsConfig.GetItemsUIConfig(itemName)
			if cfg.get("subscribeEvent"):
				Instance.mEventMgr.NotifyEvent(cfg["subscribeEvent"], cfg.get("subscribeEventParam", {}))
		pass
	# endregion

	