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


class ElectricHeaterSmallUI(ModBaseUI):
	"""小太阳UI"""
	def __init__(self, namespace, name, param):
		super(ElectricHeaterSmallUI, self).__init__(namespace, name, param)
		self._blockName = param.get("blockName")
		self._pos = param.get("pos")
		self._dimension = param.get("dimension")
		# 是否有电力供应
		self._hasDynamo = param.get("dynamo")
		# 当前工作状态
		self._workState = param.get("work")
		# 唯一key
		self._key = param.get("key")

		# cfg数据
		self._cfg = electricConfig.GetElectricConfig(self._blockName)
		self._kw = self._cfg.get("kw")

		self._eventFunctions = {
			"close": self.CloseUI,
			"update_work": self.SetWorkUI,
			"update_dynamo": self.SetWorkStateUI,
		}
		pass

	def Destroy(self):
		super(ElectricHeaterSmallUI, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricUISubscriptEvent, self.ElectricUISubscriptEvent)
		pass

	def Create(self):
		super(ElectricHeaterSmallUI, self).Create()
		# 小太阳UI
		heaterSmallPanel = self.GetBaseUIControl("/panel_heater_small")

		# center
		centerPanel = heaterSmallPanel.GetChildByPath("/panel_center")
		# 关闭按钮
		self._closeBtn = centerPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._closeBtn, self.OnCloseClicked)
		# 标题
		titlePanel = centerPanel.GetChildByPath("/title_panel")
		workStagePanel = titlePanel.GetChildByPath("/title_text_panel/work_stage_panel")
		self._workStateText = workStagePanel.GetChildByPath("/work_state").asLabel()
		self._workStateTextBg = workStagePanel.GetChildByPath("/bg").asImage()
		self._workStateTextPoint = workStagePanel.GetChildByPath("/point").asImage()
		title = centerPanel.GetChildByPath("/title_panel/title_text_panel/title")
		self._kwText = title.GetChildByPath("/bg_line/kw").asLabel()
		# 标题中的icon
		self._workIcon = titlePanel.GetChildByPath("/icon").asImage()
		# 启动后左上角闪电图标
		self._workStateImg = centerPanel.GetChildByPath("/bg/titleimg/work_state_2")
		
		btnPanel = centerPanel.GetChildByPath("/btn_panel")
		# 开启供电按钮
		self._workBtn = btnPanel.GetChildByPath("/btn_work").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._workBtn, self.OnWorkClicked)
		# 显示范围按钮
		self._showRangeBtn = btnPanel.GetChildByPath("/panel/btn_show_range").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._showRangeBtn, self.OnShowRangeClicked)
		
		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricUISubscriptEvent, self.ElectricUISubscriptEvent)

		# 初始化
		self.InitUI()
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
	# region 工作状态设置
	def SetWork(self,state):
		"""设置工作状态"""
		if self._hasDynamo:
			info = {
				"to_server": True,
				"stage": "work",
				"work": state,
				"key": self._key,
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.ElectricSubscriptEvent, info)
		
	# endregion

	# region UI显示、关闭
	def InitUI(self):
		"""初始化UI"""
		# 设置工作状态ui
		self.SetWorkStateUI()
		# 设置范围显示
		self.SetShowRange(setNot=False)
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
			if self._workState:
				self._workStateText.SetText("供暖进行中")
				self._workIcon.SetSpriteColor(electricConfig.WorkTextBgColor2)
				clientApiMgr.SetButtonText(self._workBtn, "停止供暖")
			else:
				self._workIcon.SetSpriteColor(electricConfig.WorkTextBgColor1)
				self._workStateText.SetText("电力供应中")
				clientApiMgr.SetButtonText(self._workBtn, "开始供暖")
			clientApiMgr.SetUIVisible(self._workStateImg, True)
			self._workStateText.SetTextColor(electricConfig.WorkTextColor2)
			self._workStateTextBg.SetSpriteColor(electricConfig.WorkTextBgColor2)
			self._workStateTextPoint.SetSpriteColor(electricConfig.WorkTextColor2)
		else:
			clientApiMgr.SetUIVisible(self._workStateImg, False)
			self._workStateText.SetText("电力未供应")
			self._workStateText.SetTextColor(electricConfig.WorkTextColor1)
			self._workStateTextBg.SetSpriteColor(electricConfig.WorkTextBgColor1)
			self._workStateTextPoint.SetSpriteColor(electricConfig.WorkTextColor1)
		pass

	def SetWorkUI(self, args={}):
		"""设置工作状态的UI"""
		work = args.get("work")
		if work is None:
			work = self._workState
		self._workState = work
		# 修改UI
		if self._hasDynamo:
			if work:
				clientApiMgr.SetButtonText(self._workBtn, "停止供暖")
				self._workIcon.SetSpriteColor(electricConfig.WorkTextBgColor2)
				self._workStateText.SetText("供暖进行中")
				texturesState = True
			else:
				clientApiMgr.SetButtonText(self._workBtn, "开始供暖")
				self._workStateText.SetText("供暖未启动")
				self._workIcon.SetSpriteColor(electricConfig.WorkTextBgColor1)
			clientApiMgr.SetUIVisible(self._workStateImg, True)
			self._workStateText.SetTextColor(electricConfig.WorkTextColor2)
			self._workStateTextBg.SetSpriteColor(electricConfig.WorkTextBgColor2)
			self._workStateTextPoint.SetSpriteColor(electricConfig.WorkTextColor2)
		else:
			clientApiMgr.SetButtonText(self._workBtn, "请供电")
			clientApiMgr.SetUIVisible(self._workStateImg, False)
			self._workStateText.SetText("电力未供应")
			self._workIcon.SetSpriteColor(electricConfig.WorkTextBgColor1)
			self._workStateText.SetTextColor(electricConfig.WorkTextColor1)
			self._workStateTextBg.SetSpriteColor(electricConfig.WorkTextBgColor1)
			self._workStateTextPoint.SetSpriteColor((1, 1, 1))
	# endregion

	# region 范围显示
	def SetShowRange(self, setNot=True):
		"""设置显示范围
		:param setNot: 取反
		"""
		blockComp = compFactory.CreateBlockInfo(self.mLevelId)
		val = blockComp.GetBlockEntityMolangValue(self._pos, "variable.show_range")
		state = True if val else False
		if setNot:
			state = not state
		blockComp.SetBlockEntityMolangValue(self._pos, "variable.show_range", state)
		# 设置UI
		texture = electricConfig.ShowRangeBtnTextureOn if state else electricConfig.ShowRangeBtnTextureOff
		clientApiMgr.SetButtonImage(self._showRangeBtn, texture)
		pass
	# endregion

	# region 更新工作状态渲染控制器状态显示
	def SetBlockTextures(self,state):
		"""
		设置工作状态动画与粒子显示
		"""
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
	def OnWorkClicked(self, args):
		"""开启小太阳"""
		self.SetWork(not self._workState)
		pass

	def OnShowRangeClicked(self, args):
		"""显示小太阳范围"""
		self.SetShowRange()
		pass
	# endregion
