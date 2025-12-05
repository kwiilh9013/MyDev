# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetRemoldTypeTabsList, GetRemoldParts, GetPartConfig, RemoldTypeEnum
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.tabViewWidget import TabViewWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


# 模型显示的参数
CarPaperDollParam = {
	"entity_id": "-1",
	"scale": 0.1,
	"init_rot_y": -50,
	"rotation_axis": (1, 1, 0),
	"render_depth": -200,
	"molang_dict": {},
}


class CarRemoldUI(ModBaseUI):
	"""载具 改造UI"""
	def __init__(self, namespace, name, param):
		super(CarRemoldUI, self).__init__(namespace, name, param)
		# 载具id
		self._entityId = param.get("entityId")
		# 改造数据：已解锁的配件列表
		self._unlockPartList = param.get("unlockPartList", [])
		# 改造数据：当前使用的配件
		self._usePartData = param.get("usePartData", {})

		# 当前选中的分页索引
		self._selectTabIndex = 0
		self._selectType = None

		# 当前选中的配件控件
		self._selectPartCtrl = None
		# 当前选中的配件id
		self._selectPartId = None
		# 当前选中的变形模块
		self._selectModuleType = None

		# 玩家背包内的物品数据
		self._inventoryCountDict = None

		self._eventFunctions = {
			"close": self.CloseUI,
			"update_remold": self.UpdateUsePartUI,
		}

		self._createState = False
		pass

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		super(CarRemoldUI, self).Destroy()
		self._createState = False
		pass

	def Create(self):
		super(CarRemoldUI, self).Create()
		# UI
		remoldPanel = self.GetBaseUIControl("/panel_remold")

		# 关闭按钮
		self._closeBtn = remoldPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)

		# 载具模型
		self._paperDoll = remoldPanel.GetChildByPath("/panel_center/input_panel/paper_doll").asNeteasePaperDoll()

		# 没有车辆的提示
		self._tips = remoldPanel.GetChildByPath("/tips")

		# 变形模块
		self._modulePanel = remoldPanel.GetChildByPath("/panel_module")
		# 模块1
		module1Btn = self._modulePanel.GetChildByPath("/btn_1").asButton()
		module1Item = module1Btn.GetChildByPath("/item").asItemRenderer()
		module1Icon = module1Btn.GetChildByPath("/icon")
		clientApiMgr.SetBtnTouchUpCallback(module1Btn, self.OnModule1Clicked)
		# 模块2
		module2Btn = self._modulePanel.GetChildByPath("/btn_2").asButton()
		module2Item = module2Btn.GetChildByPath("/item").asItemRenderer()
		module2Icon = module2Btn.GetChildByPath("/icon")
		clientApiMgr.SetBtnTouchUpCallback(module2Btn, self.OnModule2Clicked)
		# 记录控件列表
		self._moduleBtnDict = {
			RemoldTypeEnum.Module1: (module1Item, module1Icon),
			RemoldTypeEnum.Module2: (module2Item, module2Icon),
		}

		# 右侧
		self._rightPanel = remoldPanel.GetChildByPath("/panel_right")
		# 详情
		contextPanel = self._rightPanel.GetChildByPath("/panel_context")
		self._itemPanel = contextPanel.GetChildByPath("/item")
		self._itemIcon = self._itemPanel.GetChildByPath("/icon").asItemRenderer()
		self._itemName = self._itemPanel.GetChildByPath("/name").asLabel()
		self._itemInfo = contextPanel.GetChildByPath("/info").asLabel()
		# 改造按钮
		self._remoldBtn = contextPanel.GetChildByPath("/btn_remold").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._remoldBtn, self.OnRemoldClicked)
		
		# 分页（需在详情之后初始化）
		tabsPanel = self._rightPanel.GetChildByPath("/panel_tabs")
		self._tabView = TabViewWidget(self, tabsPanel.GetPath(), [
			"/panel/btn_energy",
			"/panel/btn_front_bumper",
			"/panel/btn_body",
			"/panel/btn_sides",
			"/panel/btn_wheel"
		], None, self.OnTabsChanged)

		# 弹窗
		self._topPanel = remoldPanel.GetChildByPath("/panel_top")
		self._topCloseBtn = self._topPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._topCloseBtn, self.OnTopCloseClicked)
		# 滚动框
		scrollPanel = self._topPanel.GetChildByPath("/scroll_view")
		scrollPath = scrollPanel.GetPath()
		self._partScrollView = ScrollViewWidget(self, scrollPath, "/btn_drag", 2)
		# 列表内容
		self._partListView = ListViewWidget(self, scrollPath, "/btn_drag/panel", "/btn_drag/panel/item", self.SetListPartInfo, self.OnTopSelectPartClicked, self._partScrollView, 3)
		# 没有部件时的提示
		self._noPartTips = self._topPanel.GetChildByPath("/tips").asLabel()
		# 切换按钮
		self._installBtn = self._topPanel.GetChildByPath("/btn_install").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._installBtn, self.OnTopInstallClicked)

		# 初始化
		self.InitUI()

		self._createState = True
		pass

	def Update(self):
		if self._createState:
			self._partListView.Update()
			pass
		pass

	# region UI显示、关闭
	def InitUI(self):
		"""初始化UI"""
		# 如果没有entityId，则显示提示
		if not self._entityId:
			clientApiMgr.SetUIVisible(self._tips, True)
			clientApiMgr.SetUIVisible(self._modulePanel, False)
			clientApiMgr.SetUIVisible(self._rightPanel, False)
			return
		
		Instance.mEventMgr.RegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		# 显示车辆模型
		CarPaperDollParam["entity_id"] = self._entityId
		self._paperDoll.RenderEntity(CarPaperDollParam)
		# 变形模块
		self.ShowModuleUI()
		pass

	def CloseUI(self, args=None):
		clientApi.PopScreen()
		pass

	def CarSubscribeEvent(self, args):
		"""载具改造系统 订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass

	def UpdateUsePartUI(self, args):
		"""更新使用的配件信息"""
		useType = args.get("type")
		usePartId = args.get("partId")
		# 关闭弹窗
		self.ShowTopUI(False)
		# 更新数据
		if usePartId is None:
			# 卸下
			self._usePartData.pop(useType, None)
		else:
			self._usePartData[useType] = usePartId
			if usePartId not in self._unlockPartList:
				self._unlockPartList.append(usePartId)
		# 更新UI
		if useType == self._selectType:
			self.ShowUsePartInfo(usePartId)
		else:
			self.ShowModuleUI(moduleType=useType)
		pass
	
	# endregion

	# region 改造选项
	def SetSelectTabs(self, index):
		"""设置选中的分页"""
		self._selectTabIndex = index
		remoteList = GetRemoldTypeTabsList()
		self._selectType = None
		if self._selectTabIndex < len(remoteList):
			self._selectType = remoteList[self._selectTabIndex]
		# 显示当前装配的配件
		self.ShowUsePartInfo()
		pass

	def ShowUsePartInfo(self, partId=None):
		"""显示使用的配件信息"""
		if partId is None:
			partId = self._usePartData.get(self._selectType)
		cfg = GetPartConfig(partId)
		if cfg and cfg.get("itemName"):
			clientApiMgr.SetUIVisible(self._itemPanel, True)
			itemName = cfg.get("itemName")
			self._itemIcon.SetUiItem(itemName, 0)
			name = cfg.get("itemNameText")
			if name is None:
				name = clientApiMgr.GetItemHoverName({"newItemName": itemName})
				cfg["itemNameText"] = name
			self._itemName.SetText(name or "")
			self._itemInfo.SetText(cfg.get("info", "无"))
		else:
			# 没有使用的配件
			clientApiMgr.SetUIVisible(self._itemPanel, False)
			self._itemInfo.SetText("还未安装任何改件")
		pass
	# endregion

	# region 变形模块
	def ShowModuleUI(self, moduleType=None):
		"""显示变形模块UI"""
		moduleBtnDict = self._moduleBtnDict
		if moduleType:
			# 仅更新该类型
			moduleBtnDict = {
				moduleType: self._moduleBtnDict.get(moduleType),
			}
		for moduleType, valList in moduleBtnDict.iteritems():
			# 设置当前使用的配件
			partId = self._usePartData.get(moduleType)
			cfg = GetPartConfig(partId)
			itemObj = valList[0]
			iconObj = valList[1]
			if cfg:
				clientApiMgr.SetUIVisible(iconObj, False)
				clientApiMgr.SetUIVisible(itemObj, True)
				itemName = cfg.get("itemName")
				itemObj.SetUiItem(itemName, 0)
			else:
				clientApiMgr.SetUIVisible(iconObj, True)
				clientApiMgr.SetUIVisible(itemObj, False)
		pass
	# endregion

	# region 按钮
	def OnCloseClicked(self, args):
		"""关闭UI"""
		self.CloseUI()
		pass

	def OnModule1Clicked(self, args):
		"""模块1按钮点击事件"""
		self.ShowTopUI(True, moduleType=RemoldTypeEnum.Module1)
		pass
	
	def OnModule2Clicked(self, args):
		"""模块2按钮点击事件"""
		self.ShowTopUI(True, moduleType=RemoldTypeEnum.Module2)
		pass
	
	def OnTabsChanged(self, prev, current):
		"""切换tab事件"""
		self.SetSelectTabs(current)
		pass

	def OnRemoldClicked(self, args):
		"""改造按钮点击事件"""
		# 显示弹窗界面
		self.ShowTopUI(True)
		pass
	# endregion

	# region 弹窗界面
	def ShowTopUI(self, state, moduleType=None):
		"""显示弹窗界面"""
		clientApiMgr.SetUIVisible(self._topPanel, state)
		if state:
			# 重置数据
			self._selectPartCtrl = None
			self._selectPartId = None
			selectType = self._selectType
			# 如果是变形模块，则显示变形模块的数据
			if moduleType:
				selectType = moduleType
			self._selectModuleType = moduleType
			# 显示列表信息
			partIdList = GetRemoldParts(selectType)
			self._partListView.UpdateData(partIdList)
			pass
		pass

	def SetListPartInfo(self, path, ctrl, index, data):
		"""设置列表里单个item信息"""
		partId = data
		cfg = GetPartConfig(partId)
		if cfg and cfg.get("itemName"):
			itemName = cfg.get("itemName")
			iconObj = ctrl.GetChildByPath("/bg/icon").asItemRenderer()
			iconObj.SetUiItem(itemName, 0)
			name = cfg.get("itemNameText")
			if name is None:
				name = clientApiMgr.GetItemHoverName({"newItemName": itemName})
				cfg["itemNameText"] = name
			nameObj = ctrl.GetChildByPath("/name").asLabel()
			nameObj.SetText(name or "")
			unlock = self.IsUnlock(partId, cfg)
			lockObj = ctrl.GetChildByPath("/bg/lock")
			clientApiMgr.SetUIVisible(lockObj, not unlock)
			# 显示信息
			infoObj = ctrl.GetChildByPath("/info").asLabel()
			info = cfg.get("info", "")
			if "配件正在研发中" in info:
				infoObj.SetText(info)
			else:
				infoObj.SetText("{}{}".format(info, "" if unlock else "\n§c请先制作该改件"))
			# 如果是当前使用的，则显示选中框
			selectType = self.GetSelectType()
			usePart = self._usePartData.get(selectType)
			selectObj = ctrl.GetChildByPath("/selected")
			if partId == usePart:
				clientApiMgr.SetUIVisible(selectObj, True)
				self._selectPartCtrl = ctrl
				self._selectPartId = partId
			else:
				clientApiMgr.SetUIVisible(selectObj, False)
		pass

	def SetSelectPart(self, ctrl, partId):
		"""设置选中的部件"""
		# 已解锁才可选择
		if self.IsUnlock(partId):
			# 设置选中
			if self._selectPartCtrl != ctrl:
				# 背景高亮
				selectObj = ctrl.GetChildByPath("/selected")
				clientApiMgr.SetUIVisible(selectObj, True)
				# 取消上一个选中
				if self._selectPartCtrl:
					selectObj = self._selectPartCtrl.GetChildByPath("/selected")
					clientApiMgr.SetUIVisible(selectObj, False)
			# 记录选中
			self._selectPartCtrl = ctrl
			self._selectPartId = partId
		pass

	def HasPartByInventory(self, partId, cfg=None):
		"""判断是否有对应的物品"""
		if not cfg:
			cfg = GetPartConfig(partId)
		# 玩家背包物品
		if self._inventoryCountDict is None:
			self._inventoryCountDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		# 判断是否有物品
		itemName = cfg.get("itemName")
		if self._inventoryCountDict.get((itemName, 0), 0) > 0:
			return True
		return False
	
	def IsUnlock(self, partId, cfg=None):
		"""判断是否已解锁"""
		# 已解锁、或者背包有配件
		return partId in self._unlockPartList or self.HasPartByInventory(partId, cfg)

	def SetInstallPart(self):
		"""安装当前选中的配件"""
		if self._selectPartId:
			# 和当前使用的配件一样，则直接关闭界面
			selectType = self.GetSelectType()
			usePart = self._usePartData.get(selectType)
			if usePart == self._selectPartId:
				self.ShowTopUI(False)
			else:
				# 发消息到服务端，安装该配件
				info = {
					"to_server": True,
					"stage": "install",
					"entityId": self._entityId,
					"partId": self._selectPartId,
					"remold": selectType,
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, info)
				pass
		pass

	def GetSelectType(self):
		"""获取当前选中的改造类型"""
		selectType = self._selectType
		if self._selectModuleType:
			selectType = self._selectModuleType
		return selectType


	def OnTopCloseClicked(self, args):
		"""关闭弹窗界面"""
		self.ShowTopUI(False)
		pass

	def OnTopInstallClicked(self, args):
		"""安装按钮点击事件"""
		self.SetInstallPart()
		pass

	def OnTopSelectPartClicked(self, path, ctrl, index, data, args):
		"""选择物品事件"""
		self.SetSelectPart(ctrl, data)
		pass
	# endregion