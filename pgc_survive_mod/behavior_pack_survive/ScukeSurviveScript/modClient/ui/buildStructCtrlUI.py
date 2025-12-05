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


class BuildStructCtrlUI(ModBaseUI):
	"""一键建造 建造操作UI"""
	def __init__(self, namespace, name, param):
		super(BuildStructCtrlUI, self).__init__(namespace, name, param)
		
		# 当前选择的建筑id
		self._selectStructId = None
		# 锁定状态
		self._lockState = False

		# 提示的timer
		self._tipsTimer = None

		# 打开按钮想显示的状态
		self._openBtnState = False
		
		# 事件功能方法
		self._eventFunctions = {
			# 打开按钮
			"open_btn": self.ShowOpenBtn,
			# 打开控制UI
			"open_ctrl_ui": self.ShowControlUI,
		}
		pass

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.BuildStructUIEvent, self.BuildStructUISubscribeEvent)
		self._eventFunctions.clear()
		if self._tipsTimer:
			engineApiGac.CancelTimer(self._tipsTimer)
			self._tipsTimer = None
		pass

	def Create(self):
		# 物品手持时的UI
		self._itemPanel = self.GetBaseUIControl("/panel_item")
		# 打开菜单按钮
		openMenuBtn = self._itemPanel.GetChildByPath("/btn_open").asButton()
		clientApiMgr.SetBtnTouchUpCallback(openMenuBtn, self.OnOpenBtnClicked)

		self._viewPanel = self.GetBaseUIControl("/panel_view")

		# 移动UI
		movePanel = self._viewPanel.GetChildByPath("/panel_move")
		# 旋转
		rotateBtn = movePanel.GetChildByPath("/right/btn_rotate").asButton()
		clientApiMgr.SetBtnTouchUpCallback(rotateBtn, self.OnRotateBtnClicked)
		# 前
		frontBtn = movePanel.GetChildByPath("/left/btn_front").asButton()
		clientApiMgr.SetBtnTouchUpCallback(frontBtn, self.OnMoveBtnClicked, {"offsetRot": 0})
		# 后
		backBtn = movePanel.GetChildByPath("/left/btn_back").asButton()
		clientApiMgr.SetBtnTouchUpCallback(backBtn, self.OnMoveBtnClicked, {"offsetRot": 180})
		# 左
		leftBtn = movePanel.GetChildByPath("/left/btn_left").asButton()
		clientApiMgr.SetBtnTouchUpCallback(leftBtn, self.OnMoveBtnClicked, {"offsetRot": -90})
		# 右
		rightBtn = movePanel.GetChildByPath("/left/btn_right").asButton()
		clientApiMgr.SetBtnTouchUpCallback(rightBtn, self.OnMoveBtnClicked, {"offsetRot": 90})
		# 上
		upBtn = movePanel.GetChildByPath("/right/btn_up").asButton()
		clientApiMgr.SetBtnTouchUpCallback(upBtn, self.OnMoveBtnClicked, {"offsetY": 1})
		# 下
		downBtn = movePanel.GetChildByPath("/right/btn_down").asButton()
		clientApiMgr.SetBtnTouchUpCallback(downBtn, self.OnMoveBtnClicked, {"offsetY": -1})

		# 控制UI
		ctrlPanel = self._viewPanel.GetChildByPath("/panel_ctrl")
		# 关闭按钮
		closeBtn = ctrlPanel.GetChildByPath("/btn_close").asButton()
		clientApiMgr.SetBtnTouchUpCallback(closeBtn, self.OnCloseBtnClicked)
		# 轮盘，走打开轮盘的按钮逻辑
		wheelBtn = ctrlPanel.GetChildByPath("/btn_wheel").asButton()
		clientApiMgr.SetBtnTouchUpCallback(wheelBtn, self.OnOpenBtnClicked)
		# 锁定
		self._lockBtn = ctrlPanel.GetChildByPath("/btn_lock").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._lockBtn, self.OnLockBtnClicked)
		# 建造
		buildBtn = ctrlPanel.GetChildByPath("/btn_build").asButton()
		clientApiMgr.SetBtnTouchUpCallback(buildBtn, self.OnBuildBtnClicked)

		# 提示
		self._tipsLabel = self._viewPanel.GetChildByPath("/tips").asLabel()

		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.BuildStructUIEvent, self.BuildStructUISubscribeEvent)
		pass

	# region 功能
	def BuildStructUISubscribeEvent(self, args):
		"""订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass

	def ShowControlUI(self, args):
		"""打开控制UI"""
		self.ResetData()
		structId = args.get("structId")
		self._selectStructId = structId
		# 显示UI
		clientApiMgr.SetUIVisible(self._viewPanel, True)
		self.SetLockState(init=True)
		if self._itemPanel.GetVisible():
			self.ShowOpenBtn({"state": False})
			self._openBtnState = True
		pass

	def SetLockState(self, init=False):
		"""设置锁定状态"""
		if not init:
			# 状态反转
			self._lockState = not self._lockState
			# 更改客户端逻辑
			Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "lock_geo", "state": self._lockState})
		# 修改UI: 修改文字、图标
		# TODO:
		tipId = 11 if self._lockState else 12
		clientApiMgr.SetButtonText(self._lockBtn, buildStructConfig.GetTips(tipId))
		pass

	def SetStartBuild(self):
		"""开始建造"""
		# 判断是否可以建造：材料是否足够；如果不够，则提示
		if self.CheckHasEnoughMaterials(structId=self._selectStructId):
			Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "start_build", "structId": self._selectStructId})
			# 关闭UI
			self.SetCloseUI(isCancel=False)
		else:
			# 提示
			self.SetTips(True, 1)
		pass

	def SetCloseUI(self, isCancel=True):
		"""关闭控制UI"""
		clientApiMgr.SetUIVisible(self._viewPanel, False)
		# 取消建造逻辑
		if isCancel:
			Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "cancel_build"})
		self.ResetData()
		self.SetTips(False)
		# 需根据当前打开按钮的状态，恢复按钮的显示
		if self._openBtnState:
			self.ShowOpenBtn({"state": True})
		pass

	def ResetData(self):
		"""重置数据"""
		self._selectStructId = None
		self._lockState = False
		pass

	def SetTips(self, state, tipId=None):
		"""设置提示信息，tipsId没有对应的配置，则关闭提示"""
		# 无论哪一种，都需要取消timer
		if self._tipsTimer:
			engineApiGac.CancelTimer(self._tipsTimer)
			self._tipsTimer = None
		if state is False:
			# 关闭提示
			clientApiMgr.SetUIVisible(self._tipsLabel, False)
		text = buildStructConfig.GetTips(tipId)
		if text:
			clientApiMgr.SetUIVisible(self._tipsLabel, True)
			self._tipsLabel.SetText(text)
			self._tipsTimer = engineApiGac.AddTimer(buildStructConfig.TipsShowTime, clientApiMgr.SetUIVisible, self._tipsLabel, False)
		pass
	
	def CheckHasEnoughMaterials(self, structId):
		"""检查是否有足够的材料"""
		itemCoundDict = clientApiMgr.GetPlayerInventoryItemsCount(self.mPlayerId)
		cfg = buildStructConfig.StructIdCfg.get(structId)
		materials = cfg.get("materials", [])
		hasEnought = True
		for item in materials:
			count = itemCoundDict.get((item[0], 0), 0)
			if count < item[1]:
				hasEnought = False
				break
		return hasEnought
	# endregion

	# region 操作界面按钮响应
	def OnRotateBtnClicked(self, args=None):
		"""旋转按钮"""
		Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "rotate"})
		pass

	def OnMoveBtnClicked(self, args):
		"""前后左右上下按钮"""
		params = args.get("AddTouchEventParams", {})
		offsetRot = params.get("offsetRot")
		offsetY = params.get("offsetY")
		Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "move", "offsetRot": offsetRot, "offsetY": offsetY})
		# 锁定建筑
		if self._lockState is False:
			self.SetLockState()
		pass

	def OnCloseBtnClicked(self, args=None):
		"""关闭按钮"""
		self.SetCloseUI()
		pass

	def OnLockBtnClicked(self, args=None):
		"""锁定按钮"""
		self.SetLockState()
		pass

	def OnBuildBtnClicked(self, args=None):
		"""建造按钮"""
		self.SetStartBuild()
		pass
	# endregion

	# region 道具按钮
	def ShowOpenBtn(self, args):
		"""显示/隐藏建造按钮"""
		state = args.get("state")
		# 如果当前显示控制UI，则不显示打开按钮
		if state:
			if self._viewPanel.GetVisible() is False:
				clientApiMgr.SetUIVisible(self._itemPanel, True)
			else:
				self._openBtnState = True
		else:
			clientApiMgr.SetUIVisible(self._itemPanel, False)
			self._openBtnState = False
		pass

	def OnOpenBtnClicked(self, args):
		"""建造按钮点击事件"""
		# 打开选择建筑界面
		Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "open_select_ui", "state": True})
		pass
	# endregion
