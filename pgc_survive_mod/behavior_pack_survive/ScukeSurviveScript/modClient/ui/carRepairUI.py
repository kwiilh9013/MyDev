# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modCommon.cfg.car import carConfig
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class CarRepairUI(ModBaseUI):
	"""修复载具UI"""
	def __init__(self, namespace, name, param):
		super(CarRepairUI, self).__init__(namespace, name, param)
		self._entityId = param.get("entityId")

		self._hasEnoughMaterials = False
		self._inventoryCountDict = None

		self._createState = False
		pass

	def Destroy(self):
		super(CarRepairUI, self).Destroy()
		self._createState = False
		pass

	def Create(self):
		super(CarRepairUI, self).Create()
		# UI
		repiarPanel = self.GetBaseUIControl("/panel_repair")

		# 关闭按钮
		self._closeBtn = repiarPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)

		# 材料
		matPanel = repiarPanel.GetChildByPath("/panel_materials")
		matViewPanel = matPanel.GetChildByPath("/sroll_view")
		matViewPath = matViewPanel.GetPath()
		self._materialScrollView = ScrollViewWidget(self, matViewPath, "/btn_drag", 1)
		self._materialListView = ListViewWidget(self, matViewPath, "/btn_drag/panel", "/btn_drag/panel/material_base", self.SetMaterialItemInfo, None, self._materialScrollView, 0)
		# 向下箭头，用来提示还有内容，可以往下滑动
		self._matViewDownArrow = matViewPanel.GetChildByPath("/next")

		# 修复按钮
		self._repiarBtn = matPanel.GetChildByPath("/btn_repair").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._repiarBtn, self.OnRepairClicked)
		
		# 初始化
		self.InitUI()

		self._createState = True
		pass

	def Update(self):
		if self._createState:
			self._materialScrollView.Update()
			self._materialListView.Update()
		pass

	# region UI显示、关闭
	def InitUI(self):
		"""初始化UI"""
		# 显示材料
		self.SetMaterialsUI()
		pass

	def CloseUI(self, args=None):
		clientApi.PopScreen()
		pass
	
	def SetRepairBtnState(self, state):
		"""设置修复按钮状态"""
		if state:
			text = "修复"
			clientApiMgr.SetButtonGray(self._repiarBtn, True)
		else:
			text = "材料不足"
			clientApiMgr.SetButtonGray(self._repiarBtn, False)
		clientApiMgr.SetButtonText(self._repiarBtn, text)
		pass
	# endregion

	# region 材料信息
	def SetMaterialsUI(self):
		"""设置物品的材料信息"""
		# 重置按钮状态
		self._hasEnoughMaterials = True
		self.SetRepairBtnState(True)
		clientApiMgr.SetUIVisible(self._matViewDownArrow, False)
		# 刷新列表
		repairItems = carConfig.GetRepairNeedItems()
		self._materialListView.UpdateData(repairItems)
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
			self.SetRepairBtnState(False)
		# 名字 + 数量
		name = clientApiMgr.GetItemHoverName(data)
		nameObj = ctrl.GetChildByPath("/name").asLabel()
		nameObj.SetText("{} {}{}/{}".format(name, redStr, count, hasCount))
		# 如果index超过4，则显示下拉的箭头（具体根据UI显示情况来定）
		if index == 4:
			clientApiMgr.SetUIVisible(self._matViewDownArrow, True)
		pass
	# endregion

	# region 修复操作
	def SetRepair(self):
		"""设置修复操作"""
		# 校验
		if self._hasEnoughMaterials:
			info = {
				"to_server": True,
				"stage": "repair_broken",
				"entityId": self._entityId,
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, info)
			# 关闭UI
			self.CloseUI()
		pass
	# endregion


	# region 按钮
	def OnCloseClicked(self, args):
		"""关闭UI"""
		self.CloseUI()
		pass

	def OnRepairClicked(self, args):
		"""合成按钮"""
		self.SetRepair()
		pass
	# endregion
