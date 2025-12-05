# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.struct import buildStructConfig
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
ViewBinder = clientApi.GetViewBinderCls()


class BuildStructSelectUI(ModBaseUI):
	"""一键建造 选择轮盘UI"""
	def __init__(self, namespace, name, param):
		super(BuildStructSelectUI, self).__init__(namespace, name, param)
		# 方块几何体模型key的列表
		self._blockGeoList = param.get("block_geo_list")
		
		# 选择的建筑类型名字，用于拼接名字
		self._selectTypeName = ""
		self._selectTypeDefaultText = "点击选择建筑类型"

		# 图片路径
		self._structTypeImgPath = "textures/ui/scuke_survive/build/smallwheel_state_{}"
		self._structIdImgPath = "textures/ui/scuke_survive/build/bigwheel_state_{}"

		# 显示的建筑和轮盘id的关系
		self._structWheelIndexToIdDict = {}
		# 选择的建筑id
		self._selectStructId = None

		# 材料格子控件
		self._materialSlotObjList = []

		# 玩家背包物品
		self._itemsCountDict = {}

		# 是否有足够的建造材料
		self._hasEnoughMaterial = False

		# 事件功能方法
		self._eventFunctions = {
		}

		pass

	def Destroy(self):
		# Instance.mEventMgr.UnRegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		self._itemsCountDict.clear()
		pass

	def Create(self):
		structsPanel = self.GetBaseUIControl("/panel_structs")
		# 关闭按钮
		self._closeBtn = structsPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseBtnClicked)

		# 撤销
		revokeBtn = structsPanel.GetChildByPath("/btn_revoke").asButton()
		clientApiMgr.SetBtnTouchUpCallback(revokeBtn, self.OnRevokeBtnClicked)

		# 选择的标题，用于显示当前选择的建筑名字
		self._selectTitle = structsPanel.GetChildByPath("/select_title").asLabel()

		# 建筑类型轮盘
		self._structTypeWheel = structsPanel.GetChildByPath("/panel_select/struct_type").asSelectionWheel()
		self._structTypeWheel.SetTouchUpCallback(self.OnStructTypeWheelClicked)
		self._structTypeWheelSelectImg = self._structTypeWheel.GetChildByPath("/content/select_bg/state_select").asImage()
		# 具体建筑轮盘
		self._structIdWheel = structsPanel.GetChildByPath("/panel_select/structs").asSelectionWheel()
		self._structIdWheel.SetTouchUpCallback(self.OnStructIdWheelClicked)
		self._structIdWheelSelectImg = self._structIdWheel.GetChildByPath("/content/select_bg/state_select").asImage()

		# 建筑信息
		self._structInfoPanel = structsPanel.GetChildByPath("/panel_struct_info")
		# 预览模型
		self._structViewDoll = self._structInfoPanel.GetChildByPath("/input_panel_struct_view/paper_doll").asNeteasePaperDoll()
		# 材料列表
		materialPanel = self._structInfoPanel.GetChildByPath("/panel_materials/material_list")
		slot = 0
		while True:
			slotObj = materialPanel.GetChildByPath("/slot_{}".format(slot))
			if slotObj:
				self._materialSlotObjList.append(slotObj)
				slot += 1
			else:
				break
		# 确定按钮
		self._buildBtn = self._structInfoPanel.GetChildByPath("/panel_materials/btn_build").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._buildBtn, self.OnBuildBtnClicked)

		# 订阅事件
		# Instance.mEventMgr.RegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)

		# 初始化轮盘信息
		self.InitStructTypeWheelInfo()

		# 获取玩家背包物品
		self._itemsCountDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		pass

	# region 功能
	def InitStructTypeWheelInfo(self):
		"""初始化建筑类型轮盘信息"""
		# 类型轮盘
		cfg = buildStructConfig.StructTypeWheelCfg
		for i, val in enumerate(cfg):
			# 类型label
			nameObj = self._structTypeWheel.GetChildByPath("/content/select_type/type_{}".format(i)).asLabel()
			if val is None:
				# 设置为空
				nameObj.SetText("无")
			else:
				# 设置类型名字
				nameObj.SetText(val.get("name", ""))
		# 设置选择文字
		self._selectTitle.SetText(self._selectTypeDefaultText)
		pass

	def SetSelectStructType(self, wheelIndex):
		"""设置选择的建筑类型"""
		# 当取消选择时（点击正方形四个角的空位置），会传递-1过来
		if wheelIndex < 0:
			return

		cfg = buildStructConfig.StructTypeWheelCfg
		if wheelIndex < len(cfg):
			val = cfg[wheelIndex]
			if val:
				# 记录类型名字
				self._selectTypeName = val.get("name", "")
				# 设置文字
				self._selectTitle.SetText(self._selectTypeName)
				# 展开二级界面
				self.SetStructIdWheelInfo(val.get("wheel_structs", {}))
			# 设置选中
			self._structTypeWheelSelectImg.SetSprite(self._structTypeImgPath.format(wheelIndex))
		pass
	
	def SetSelectStructId(self, wheelIndex, showState=True):
		"""设置选择的建筑id"""
		# 当取消选择时（点击正方形四个角的空位置），会传递-1过来
		if wheelIndex < 0:
			return
		
		isShow = False
		if showState:
			structId = self._structWheelIndexToIdDict.get(wheelIndex)
			cfg = buildStructConfig.StructIdCfg.get(structId)
			if cfg:
				isShow = True
				self._selectStructId = structId
				# 设置文字
				self._selectTitle.SetText("{}/{}".format(self._selectTypeName, cfg.get("name", "")))
				# 显示详情
				clientApiMgr.SetUIVisible(self._structInfoPanel, True)
				# 模型
				# dollParam = {
				# 	"block_geometry_model_name": self.GetBlockGeo(structId),
				# 	"scale": cfg.get("view_scale", 0.5),
				# 	"init_rot_y": 120,
				# 	"rotation_axis": (1, 1, 0),
				# 	"molang_dict": {},
				# }
				# self._structViewDoll.RenderBlockGeometryModel(dollParam)
				# 骨骼模型
				dollParam = {
					"skeleton_model_name": "scuke_struct_{}".format(structId),
					"scale": cfg.get("ui_scale", 0.005),
					# "scale": 0.003,
					"init_rot_y": 45,
					"rotation_axis": (1, 1, 0),
				}
				self._structViewDoll.RenderSkeletonModel(dollParam)

				# 消耗材料
				materials = cfg.get("materials", [])
				slot = 0
				self._hasEnoughMaterial = True
				for item in materials:
					slotObj = self._materialSlotObjList[slot]
					clientApiMgr.SetUIVisible(slotObj, True)
					# icon
					itemObj = slotObj.GetChildByPath("/icon").asItemRenderer()
					itemObj.SetUiItem(item[0], 0)
					# 名字 + 数量（不足部分红色显示）
					name = clientApiMgr.GetItemHoverName({"newItemName": item[0]})
					hasCount = self._itemsCountDict.get((item[0], 0), 0)
					nameObj = slotObj.GetChildByPath("/name").asLabel()
					# 判断是否数量足够
					color = ""
					if hasCount < item[1]:
						self._hasEnoughMaterial = False
						color = "§c"
					nameObj.SetText("{} {}{}§r/{}".format(name, color, hasCount, item[1]))
					slot += 1
				# 关闭剩余的控件
				for i in xrange(slot, len(self._materialSlotObjList)):
					slotObj = self._materialSlotObjList[i]
					clientApiMgr.SetUIVisible(slotObj, False)
				# 如果数量不足，则修改按钮为预览，而非确定
				tipId = 13 if self._hasEnoughMaterial else 14
				clientApiMgr.SetButtonText(self._buildBtn, buildStructConfig.GetTips(tipId))
			# 设置选中
			self._structIdWheelSelectImg.SetSprite(self._structIdImgPath.format(wheelIndex))
		else:
			self._structIdWheelSelectImg.SetSprite(self._structIdImgPath.format("default"))

		# 关闭选择
		if not isShow:
			self._selectStructId = None
			self._hasEnoughMaterial = False
			clientApiMgr.SetUIVisible(self._structInfoPanel, False)
			self._selectTitle.SetText(self._selectTypeName)
		pass

	def SetStructIdWheelInfo(self, structDict):
		"""
		设置具体建筑轮盘信息
		:param structDict = {structId: wheelIndex}
		"""
		# 显示UI
		clientApiMgr.SetUIVisible(self._structIdWheel, True)
		# 模型显示的参数（如果控件的rotation为none，则init_rot_y无效）
		dollParam = {
			"block_geometry_model_name": "my_geometry_model",
			"scale": 0.5,
			"init_rot_y": 120,
			"rotation_axis": (1, 1, 0),
			"molang_dict": {},
		}
		# 显示信息
		cfg = buildStructConfig.StructIdCfg
		setIndexList = []
		self._structWheelIndexToIdDict.clear()
		for structId, index in structDict.iteritems():
			val = cfg.get(structId)
			if val:
				setIndexList.append(index)
				self._structWheelIndexToIdDict[index] = structId
				# 显示建筑名字、模型
				infoObj = self._structIdWheel.GetChildByPath("/content/select_type/struct_{}".format(index))
				nameObj = infoObj.GetChildByPath("/name").asLabel()
				dollObj = infoObj.GetChildByPath("/paper_doll").asNeteasePaperDoll()
				clientApiMgr.SetUIVisible(dollObj, True)
				# 名字
				nameObj.SetText(val.get("name", ""))
				# # 模型
				# geoKey = self.GetBlockGeo(structId)
				# dollParam["block_geometry_model_name"] = geoKey
				# dollParam["scale"] = val.get("ui_scale", 0.5)
				# dollObj.RenderBlockGeometryModel(dollParam)
				# 骨骼模型
				dollParam = {
					"skeleton_model_name": "scuke_struct_{}".format(structId),
					"scale": val.get("ui_wheel_scale", 0.005),
					# "scale": 0.005,
					"init_rot_y": 45,
					"rotation_axis": (1, 1, 0),
				}
				dollObj.RenderSkeletonModel(dollParam)
		# 将其余的置空
		for i in xrange(buildStructConfig.WheelMaxCount):
			if i not in setIndexList:
				infoObj = self._structIdWheel.GetChildByPath("/content/select_type/struct_{}".format(i))
				nameObj = infoObj.GetChildByPath("/name").asLabel()
				nameObj.SetText("无")
				dollObj = infoObj.GetChildByPath("/paper_doll")
				clientApiMgr.SetUIVisible(dollObj, False)
		# 关闭详情界面
		self.SetSelectStructId(0, False)
		pass

	def GetBlockGeo(self, structId):
		"""获取建筑模型"""
		geoKey = buildStructConfig.GetBlockGeoKey(structId)
		if geoKey not in self._blockGeoList:
			# 模型未创建，需创建模型
			Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "create_geo", "structId": structId})
			self._blockGeoList.append(geoKey)
		return geoKey

	# endregion

	# region 按钮响应
	def OnStructTypeWheelClicked(self):
		"""建筑类型轮盘点击事件"""
		# 获取当前选择的轮盘索引
		index = self._structTypeWheel.GetCurrentSliceIndex()
		# 设置选择建筑类型
		self.SetSelectStructType(index)
		pass

	def OnStructIdWheelClicked(self):
		"""建筑id轮盘点击事件"""
		# 获取当前选择的轮盘索引
		index = self._structIdWheel.GetCurrentSliceIndex()
		# 设置选择建筑类型
		self.SetSelectStructId(index)
		pass
	
	def OnBuildBtnClicked(self, args):
		"""确定按钮"""
		# 确定选择建筑，进入选址建造阶段
		if self._selectStructId:
			Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "try_build", "structId": self._selectStructId})
		# 关闭UI
		self.OnCloseBtnClicked()
		pass

	def OnRevokeBtnClicked(self, args=None):
		"""撤销按钮"""
		Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "revoke"})
		pass

	def OnCloseBtnClicked(self, args=None):
		"""关闭按钮"""
		clientApi.PopTopUI()
		pass
	# endregion
