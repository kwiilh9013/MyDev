# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetPartSkillConfig, PartEnum
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.widget.imageNumberWidget import ImageNumberWidget
from ScukeSurviveScript.modClient.ui.widget.imageMultiNumberWidget import ImageMultiNumberWidget
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
ViewBinder = clientApi.GetViewBinderCls()


NumberTextures = [
	"textures/ui/scuke_survive/numbers/num_0",
	"textures/ui/scuke_survive/numbers/num_1",
	"textures/ui/scuke_survive/numbers/num_2",
	"textures/ui/scuke_survive/numbers/num_3",
	"textures/ui/scuke_survive/numbers/num_4",
	"textures/ui/scuke_survive/numbers/num_5",
	"textures/ui/scuke_survive/numbers/num_6",
	"textures/ui/scuke_survive/numbers/num_7",
	"textures/ui/scuke_survive/numbers/num_8",
	"textures/ui/scuke_survive/numbers/num_9",
]
# 停车档的贴图
ParkNumerTexture = "textures/ui/scuke_survive/numbers/num_p"
# 倒车档的贴图
ReverseNumerTexture = "textures/ui/scuke_survive/numbers/num_r"


# 图标默认颜色
IconDefaultColor = (0.21, 0.3, 0.27)
# 图标红色
IconRedColor = (1, 0.17, 0)
# 图标亮色
IconLightColor = (0.51, 0.67, 0.62)

# 在水中时的icon颜色
InWaterIconColor = {
	True: IconLightColor,
	False: IconDefaultColor,
}


class CarUI(ModBaseUI):
	"""载具UI"""
	def __init__(self, namespace, name, param):
		super(CarUI, self).__init__(namespace, name, param)
		# 看向的实体id
		self._lookatEntityId = None
		
		# region 属性
		# 时速缓存
		self._speed = None
		# 当前耐久的缓存，用于判断是否掉耐久
		self._currentDurabilityRatio = None
		# 损坏载具id
		self._brokenEntityId = None

		# 延迟关闭维修进度的timer
		self._closeRepairUITimer = None

		# 基础最大耐久，用于计算百分比数值
		self._baseMaxDurability = carConfig.BaseCarAttrConfig.get("maxDurability", 100) - 1.0
		self._baseMaxEnergy = carConfig.BaseCarAttrConfig.get("maxEneergy", 100) + 0.0
		# 能源值的缓存
		self._energyRatio = 0
		# 在水中的缓存
		self._inWaterState = None
		# 倒车档的状态
		self._cutState = None
		# endregion

		# region 改造
		# 装载的配件数据: {remoldType: partId}
		self._usePartData = {}
		# 配件技能按钮对应的配件id: {btnIndex: partId}
		self._skillBtnToPartData = {}
		# endregion

		# region 技能
		# 导弹提示是否显示
		self._missileTipState = False
		# 技能cd数据
		self._skillCDDict = {}
		self._skillCDTimer = None
		# 飞行的进度条更新timer
		self._flyBarTimer = None
		# endregion

		# 调整按钮位置的映射，用于设置界面修改按钮位置等
		self._btnPosSetMap = {}

		# 设置属性的方法
		self._setParamFunctions = {
			"speed": self.SetSpeedText,
			"durability": self.SetDurabilityText,
			"energy": self.SetEnergyText,
			"inwater": self.SetInWaterState,
			"lookat": self.SetLookatUI,
			"repair": self.SetRepairUI,
			"broken_car": self.ShowBrokenCarUI,
			"mercenary": self.ShowMercenaryUI,
			"cds": self.ShowSkillCD,
			"flyState": self.ShowFlyUI,
		}
		pass

	def Destroy(self):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		Instance.mEventMgr.UnRegisterEvent(eventConfig.SettingDataSubscribtEvent, self.SettingDataSubscribtEvent)
		if self._closeRepairUITimer:
			engineApiGac.CancelTimer(self._closeRepairUITimer)
		pass

	def Create(self):
		# 驾驶员相关UI
		self._carCtrlPanel = self.GetBaseUIControl("/panel_ctrl")
		# 前进后退按钮
		self._speedUpBtn = self._carCtrlPanel.GetChildByPath("/panel_speedup/btn_up").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._speedUpBtn, self.OnDownUpBtnDownClicked, self.OnDownUpBtnUpClicked, {"downStage": "up", "upStage": "cancel"})
		self._speedCutBtn = self._carCtrlPanel.GetChildByPath("/panel_speedup/btn_cut").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._speedCutBtn, self.OnDownUpBtnDownClicked, self.OnDownUpBtnUpClicked, {"downStage": "cut", "upStage": "cancel"})
		# 转向按钮
		self._turnLeftBtn = self._carCtrlPanel.GetChildByPath("/panel_turn/btn_turn_left").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._turnLeftBtn, self.OnDownUpBtnDownClicked, self.OnDownUpBtnUpClicked, {"downStage": "left", "upStage": "tCancel"})
		self._turnRightBtn = self._carCtrlPanel.GetChildByPath("/panel_turn/btn_turn_right").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._turnRightBtn, self.OnDownUpBtnDownClicked, self.OnDownUpBtnUpClicked, {"downStage": "right", "upStage": "tCancel"})
		self._btnPosSetMap["btn_up"] = self._speedUpBtn
		self._btnPosSetMap["btn_cut"] = self._speedCutBtn
		self._btnPosSetMap["btn_turn_left"] = self._turnLeftBtn
		self._btnPosSetMap["btn_turn_right"] = self._turnRightBtn
		# 时速
		self._speedBar = self._carCtrlPanel.GetChildByPath("/panel_speedshow/bar").asProgressBar()
		carCtrlPath = self._carCtrlPanel.GetPath()
		self._speedText = ImageMultiNumberWidget(self, carCtrlPath + "/panel_speedshow/speed", ["/unit1", "/unit2", "/unit3"], NumberTextures)
		self._speedGearText = ImageNumberWidget(self, carCtrlPath + "/panel_speedshow/gear", "/unit", NumberTextures)
		# 耐久
		self._durabilityLabel = self._carCtrlPanel.GetChildByPath("/panel_durability/text").asLabel()
		self._durabilityBar = self._carCtrlPanel.GetChildByPath("/panel_durability/bar").asProgressBar()
		self._emptyDurabilityImg = self._carCtrlPanel.GetChildByPath("/panel_durability/empty_sfx")

		# 能源
		self._energyLabel = self._carCtrlPanel.GetChildByPath("/panel_energy/text").asLabel()
		self._energyBar = self._carCtrlPanel.GetChildByPath("/panel_energy/bar").asProgressBar()
		self._emptyEnergyImg = self._carCtrlPanel.GetChildByPath("/panel_energy/empty_sfx")

		# 能源图标
		self._energyIcon = self._carCtrlPanel.GetChildByPath("/panel_speedshow/icon_energy").asImage()
		self._waterIcon = self._carCtrlPanel.GetChildByPath("/panel_speedshow/icon_water").asImage()

		# 驾驶员、乘客共有的UI
		self._commonPanel = self.GetBaseUIControl("/panel_common")
		# 下车
		self._getoffBtn = self._commonPanel.GetChildByPath("/btn_getoff").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._getoffBtn, self.OnBtnUpClicked, {"stage": "getoff"})
		# 雇佣兵下车按钮
		self._mercenaryGetoffBtn = self._commonPanel.GetChildByPath("/btn_getoff_mercenary").asButton()
		clientApiMgr.SetBtnTouchUpCallback(self._mercenaryGetoffBtn, self.OnBtnUpClicked, {"stage": "getoff_mercenary"})
		# 受伤图
		self._hurtImg = self._commonPanel.GetChildByPath("/hurt")
		# 有动画的控件，在初始化UI时会自动播放一遍，需在此时停止动画的播放
		self._hurtImg.StopAnimation()

		# 指向时显示的UI
		self._lookatPanel = self.GetBaseUIControl("/panel_lookat")
		# 上车
		self._getonBtn = self._lookatPanel.GetChildByPath("/btn_geton").asButton()
		clientApiMgr.SetBtnTouchDownCallback(self._getonBtn, self.OnBtnDownClickedToEntity, {"stage": "geton"})
		# 加能源
		self._addEnergyBtn = self._lookatPanel.GetChildByPath("/btn_energy").asButton()
		clientApiMgr.SetBtnTouchDownCallback(self._addEnergyBtn, self.OnBtnDownClickedToEntity, {"stage": "energy_ui"})
		# 上车与下车按钮
		self._btnPosSetMap["btn_geton"] = (self._getonBtn, self._getoffBtn, )
		# 加能源和雇佣兵下车按钮
		self._btnPosSetMap["btn_energy"] = (self._addEnergyBtn, self._mercenaryGetoffBtn, )

		# 维修界面
		self._repairPanel = self.GetBaseUIControl("/panel_repair")
		# 维修进度
		self._repairBarPanel = self._repairPanel.GetChildByPath("/repair_bar")
		# 维修进度条
		self._repairBar = self._repairBarPanel.GetChildByPath("/bar").asProgressBar()
		# 文字
		self._repairText = self._repairBarPanel.GetChildByPath("/text").asLabel()

		# 针对损坏载具的修复UI
		self._brokenCarPanel = self.GetBaseUIControl("/panel_broken_car")
		self._brokenOpenBtn = self._brokenCarPanel.GetChildByPath("/btn_open").asButton()
		clientApiMgr.SetBtnTouchDownCallback(self._brokenOpenBtn, self.OnOpenBrokenCarClicked)

		# 改造配件的技能UI
		# 技能按钮
		self._skillPanel = self.GetBaseUIControl("/panel_skill")
		skill1 = self._skillPanel.GetChildByPath("/btn_skill1").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(skill1, self.OnStartSkillClickDown, self.OnStartSkillClickUp, {"skillIndex": 0})
		skill2 = self._skillPanel.GetChildByPath("/btn_skill2").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(skill2, self.OnStartSkillClickDown, self.OnStartSkillClickUp, {"skillIndex": 1})
		self._skillBtnList = [skill1, skill2]
		self._btnPosSetMap["btn_skill1"] = skill1
		self._btnPosSetMap["btn_skill2"] = skill2
		# 专属UI：氮气飞行，索引2
		self._flyPanel = self._skillPanel.GetChildByPath("/skill_fly")
		self._skillBtnList.append(self._flyPanel)
		# 开启按钮
		self._flyStateBtn = self._flyPanel.GetChildByPath("/btn_fly").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._flyStateBtn, self.OnStartSkillClickDown, self.OnStartSkillClickUp, {"skillIndex": 2})
		self._btnPosSetMap["btn_fly"] = self._flyStateBtn
		# 其他UI
		self._flyStartPanel = self._flyPanel.GetChildByPath("/panel_fly")
		# 上升下降按钮
		self._upBtn = self._flyStartPanel.GetChildByPath("/btn_up").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._upBtn, self.OnFlyDownClicked, self.OnFlyCancelClicked, {"state": "up"})
		self._downBtn = self._flyStartPanel.GetChildByPath("/btn_down").asButton()
		clientApiMgr.SetBtnTouchDonwUpCallback(self._downBtn, self.OnFlyDownClicked, self.OnFlyCancelClicked, {"state": "down"})
		self._btnPosSetMap["btn_up"] = self._upBtn
		self._btnPosSetMap["btn_down"] = self._downBtn
		# 氮气进度条
		self._flyBar = self._flyStartPanel.GetChildByPath("/bar").asProgressBar()

		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		Instance.mEventMgr.RegisterEvent(eventConfig.SettingDataSubscribtEvent, self.SettingDataSubscribtEvent)
		pass

	# region 事件
	def CarSubscribeEvent(self, args):
		"""订阅事件"""
		stage = args.get("stage")
		funct = self._setParamFunctions.get(stage)
		if funct:
			# 设置属性UI
			funct(args)
		elif stage == "show":
			# 显示/隐藏
			self.ShowCarUI(args.get("state", False), args)
		pass
	# endregion

	# region 指向UI
	def SetLookatUI(self, args):
		"""设置指向时显示的UI"""
		state = args.get("state", False)
		entityId = args.get("entityId")
		clientApiMgr.SetUIVisible(self._lookatPanel, state)
		self._lookatEntityId = entityId
		pass
	# endregion

	# region 驾驶UI
	def ShowCarUI(self, state, args={}):
		"""显示/隐藏载具UI"""
		clientApiMgr.SetUIVisible(self._commonPanel, state)
		isRider = state and args.get("isRider", False)
		clientApiMgr.SetUIVisible(self._carCtrlPanel, isRider)
		if isRider:
			self.SetSpeedText({"value": 0})
		# 隐藏雇佣兵UI，由另一个方法来显示
		self.ShowMercenaryUI({"state": False})
		# 隐藏hud
		Instance.mEventMgr.NotifyEvent(eventConfig.HudShowSubscriptEvent, {"state": not state})
		# 显示改造配件UI
		self.ShowPartSkillUI(state, args)
		if state:
			# 显示技能CD
			self.ShowSkillCD(args, init=True)
		pass

	def SetSpeedText(self, args):
		"""设置时速文本、进度条"""
		# 因计算时速频率高，需要做判断
		speed = int(args.get("value", self._speed))
		if self._speed != speed:
			self._speed = speed
			self._speedText.SetNumber(self._speed)
			# 档位显示
			cut = args.get("cut", False)
			gear = carConfig.GetGearNum(speed)
			if self._speed <= 0:
				# 停车
				self._speedGearText.SetTexture(ParkNumerTexture)
				if cut != self._cutState and cut is False:
					self._speedGearText.SetColor(IconLightColor)
			elif cut is True:
				# 倒退
				if cut != self._cutState:
					self._speedGearText.SetTexture(ReverseNumerTexture)
					self._speedGearText.SetColor(IconRedColor)
			else:
				self._speedGearText.SetNumber(gear)
				if cut != self._cutState and cut is False:
					self._speedGearText.SetColor(IconLightColor)
			self._cutState = cut
			# 档位进度
			lastLimit = carConfig.GetGearSpeedLimit(gear - 1)
			limit = carConfig.GetGearSpeedLimit(gear)
			if lastLimit == limit:
				ratio = 0
			else:
				ratio = min((speed - lastLimit) / (limit - lastLimit + 0.0), 1.0)
			self._speedBar.SetValue(ratio)
		pass

	def SetDurabilityText(self, args):
		"""设置耐久文本、进度条"""
		durabilityRatio = args.get("value")
		self._durabilityBar.SetValue(durabilityRatio)
		# 耐久百分比的数值显示=config的初始耐久，这样改造之后，耐久将会超过100%，算是改造的一个反馈
		durability = args.get("durability")
		self._durabilityLabel.SetText("{:.0%}%".format(durability / self._baseMaxDurability))
		# 空警告
		if durabilityRatio <= 0 and self._currentDurabilityRatio >= 0:
			clientApiMgr.SetUIVisible(self._emptyDurabilityImg, True)
		elif durabilityRatio > 0 and self._currentDurabilityRatio <= 0:
			clientApiMgr.SetUIVisible(self._emptyDurabilityImg, False)
		# 设置掉耐久UI
		if self._currentDurabilityRatio and self._currentDurabilityRatio > durabilityRatio:
			self._hurtImg.PlayAnimation()
		self._currentDurabilityRatio = durabilityRatio
		pass

	def SetEnergyText(self, args):
		"""设置能源文本、进度条"""
		energyRatio = args.get("value")
		self._energyBar.SetValue(energyRatio)
		# 能源百分比的数值显示=config的初始能源，这样改造之后，能源将会超过100%，算是改造的一个反馈
		energy = args.get("energy")
		self._energyLabel.SetText("{:.0%}%".format(energy / self._baseMaxEnergy))
		# 空警告
		if energyRatio <= 0 and self._energyRatio >= 0:
			clientApiMgr.SetUIVisible(self._emptyEnergyImg, True)
		elif energyRatio > 0 and self._energyRatio <= 0:
			clientApiMgr.SetUIVisible(self._emptyEnergyImg, False)
		# 修改图标颜色
		if energyRatio < 0.1 and self._energyRatio >= 0.1:
			self._energyIcon.SetSpriteColor(IconRedColor)
		elif energyRatio >= 0.1 and self._energyRatio < 0.1:
			self._energyIcon.SetSpriteColor(IconDefaultColor)
		self._energyRatio = energyRatio
		pass

	def SetInWaterState(self, args):
		"""设置在水中的状态"""
		inWaterState = args.get("value", False)
		# 修改图标颜色
		if self._inWaterState != inWaterState:
			color = InWaterIconColor[inWaterState]
			self._waterIcon.SetSpriteColor(color)
		self._inWaterState = inWaterState
		pass
	# endregion

	# region 维修
	def SetRepairUI(self, args):
		"""设置维修进度、进度条"""
		ratio = args.get("ratio")
		clientApiMgr.SetUIVisible(self._repairPanel, True)
		clientApiMgr.SetUIVisible(self._repairBarPanel, True)
		self._repairBar.SetValue(ratio)
		# 耐久百分比的数值显示=config的初始耐久，这样改造之后，耐久将会超过100%，算是改造的一个反馈
		durability = args.get("durability")
		self._repairText.SetText("{:.0%}%".format(durability / self._baseMaxDurability))
		# 延迟关闭
		delayCloseTime = args.get("delayCloseTime", 1.5)
		if self._closeRepairUITimer:
			engineApiGac.CancelTimer(self._closeRepairUITimer)
		self._closeRepairUITimer = engineApiGac.AddTimer(delayCloseTime, clientApiMgr.SetUIVisible, self._repairPanel, False)
		pass
	# endregion
	
	# region 按钮响应
	def OnDownUpBtnDownClicked(self, args):
		"""同时监听按下松开的按钮，按下的逻辑"""
		params = args.get("AddTouchEventParams", {})
		stage = params.get("downStage")
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": stage})
		pass

	def OnDownUpBtnUpClicked(self, args):
		"""同时监听按下松开的按钮，松开的逻辑"""
		params = args.get("AddTouchEventParams", {})
		stage = params.get("upStage")
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": stage})
		pass

	def OnBtnUpClicked(self, args):
		"""按钮松开的逻辑"""
		params = args.get("AddTouchEventParams", {})
		stage = params.get("stage")
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": stage})
		pass

	def OnBtnDownClickedToEntity(self, args):
		"""上车/加能源 按钮按下的逻辑"""
		# 因为交互方式问题，需在按下时就执行逻辑；否则在松开之前，UI就已关闭
		params = args.get("AddTouchEventParams", {})
		stage = params.get("stage")
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": stage, "entityId": self._lookatEntityId})
		pass
	# endregion

	# region 修复载具
	def ShowBrokenCarUI(self, args={}):
		"""显示/隐藏损坏载具修复UI"""
		state = args.get("state", False)
		entityId = args.get("entityId")
		clientApiMgr.SetUIVisible(self._brokenCarPanel, state)
		self._brokenEntityId = entityId
		pass

	def OnOpenBrokenCarClicked(self, args):
		"""打开损坏载具修复UI的逻辑"""
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": "open_broken_car", "entityId": self._brokenEntityId})
		pass
	# endregion

	# region 雇佣兵
	def ShowMercenaryUI(self, args={}):
		"""显示/隐藏雇佣兵上下车UI"""
		state = args.get("state", False)
		# 隐藏雇佣兵下车按钮
		clientApiMgr.SetUIVisible(self._mercenaryGetoffBtn, state)
		pass
	# endregion

	# region 改造配件技能
	def ShowPartSkillUI(self, state, args={}):
		"""显示改造配件技能UI"""
		clientApiMgr.SetUIVisible(self._skillPanel, state)
		if not state:
			# 关闭整个界面
			return
		
		showIndexList = []
		self._skillBtnToPartData.clear()
		showMissile = False
		# 配件数据
		self._usePartData = args.get("usePartData", {})
		# 遍历配件，查询这些配件是否有技能，如果有、且需要显示按钮，则根据cfg显示按钮
		for partType, partId in self._usePartData.iteritems():
			# 配件config
			skillCfg = GetPartSkillConfig(partId)
			if skillCfg:
				# 显示技能按钮
				btnIndex = skillCfg.get("btnIndex")
				if btnIndex is not None:
					if btnIndex not in showIndexList:
						showIndexList.append(btnIndex)
					else:
						print("________ ERROR CarUI.ShowPartSkillUI: 重复显示技能按钮: {}, 部件：{}".format(btnIndex, partId))
						continue
					self._skillBtnToPartData[btnIndex] = partId
					btn = self._skillBtnList[btnIndex]
					clientApiMgr.SetUIVisible(btn, True)
					if skillCfg.get("btnIconPath"):
						icon = btn.GetChildByPath("/icon").asImage()
						icon.SetSprite(skillCfg["btnIconPath"])
					if skillCfg.get("btnName"):
						label = btn.GetChildByPath("/button_label").asLabel()
						label.SetText(skillCfg["btnName"])
					if partId == PartEnum.Missile:
						showMissile = True
			pass
		if len(showIndexList) <= 0:
			# 关闭整个UI
			clientApiMgr.SetUIVisible(self._skillPanel, False)
		else:
			# 隐藏剩余的按钮
			for i in xrange(len(self._skillBtnList)):
				if i not in showIndexList:
					clientApiMgr.SetUIVisible(self._skillBtnList[i], False)
			clientApiMgr.SetUIVisible(self._skillPanel, True)
		# 显示导弹技能的长按提示
		if self._missileTipState is False and showMissile:
			self._missileTipState = True
			gameComp = clientApi.GetEngineCompFactory().CreateGame(self.mPlayerId)
			gameComp.SetTipMessage("长按发射按钮可锁定多个目标")
		pass

	def PlaySkills(self, partId, clickState="up"):
		"""释放技能, longTime=长按时间"""
		# 判断cd
		if self.GetSkillCD(partId) <= 0 and self._energyRatio > 0:
			# 调用方法，指向放技能的逻辑
			Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": "playSkill", "skillStage": clickState, "partId": partId})
		pass

	def OnStartSkillClickDown(self, args):
		"""技能按钮 按下"""
		params = args.get("AddTouchEventParams", {})
		skillIndex = params.get("skillIndex")
		partId = self._skillBtnToPartData.get(skillIndex)
		if partId:
			self.PlaySkills(partId, "down")
		pass

	def OnStartSkillClickUp(self, args):
		"""技能按钮 松开"""
		params = args.get("AddTouchEventParams", {})
		skillIndex = params.get("skillIndex")
		# 释放技能
		partId = self._skillBtnToPartData.get(skillIndex)
		if partId:
			self.PlaySkills(partId, "up")
		pass
	# endregion

	# region 飞行UI
	def ShowFlyUI(self, args={}):
		"""显示飞行UI, 上升下降按钮、进度条等"""
		state = args.get("state", False)
		clientApiMgr.SetUIVisible(self._flyStartPanel, state)
		if state:
			skillCfg = GetPartSkillConfig(PartEnum.Fly)
			# 修改图标
			if skillCfg.get("icons"):
				iconObj = self._flyStateBtn.GetChildByPath("/icon").asImage()
				iconObj.SetSprite(skillCfg["icons"][1])
			# 重置进度条
			self._flyBar.SetValue(1.0)
			info = {
				"time": 0.0,
				"total": skillCfg.get("duration", 10),
			}
			self._flyBarTimer = engineApiGac.AddRepeatedTimer(0.1, self.UpdateFlyBarTimer, info)
		else:
			skillCfg = GetPartSkillConfig(PartEnum.Fly)
			# 修改图标
			if skillCfg.get("icons"):
				iconObj = self._flyStateBtn.GetChildByPath("/icon").asImage()
				iconObj.SetSprite(skillCfg["icons"][0])
			if self._flyBarTimer:
				engineApiGac.CancelTimer(self._flyBarTimer)
				self._flyBarTimer = None
		pass

	def UpdateFlyBarTimer(self, info):
		"""更新飞行进度条"""
		info["time"] += 0.1
		self._flyBar.SetValue(1 - info["time"] / info["total"])
		pass

	def OnFlyDownClicked(self, args):
		"""飞行按钮按下事件"""
		params = args.get("AddTouchEventParams", {})
		state = params.get("state")
		info = {
			"stage": "flyUpDown",
			"state": state,
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, info)
		pass

	def OnFlyCancelClicked(self, args):
		"""飞行按钮松开事件"""
		params = args.get("AddTouchEventParams", {})
		state = params.get("state")
		info = {
			"stage": "flyUpDown",
			"state": state + "_cancel",
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, info)
		pass

	# endregion

	# region 技能cd
	def ShowSkillCD(self, args={}, init=False):
		"""显示技能cd"""
		cds = args.get("cds")
		if cds is None:
			cds = {}
		# 设置所有控件的cd
		for btnIndex, partId in self._skillBtnToPartData.iteritems():
			btn = self._skillBtnList[btnIndex]
			cd = cds.get(partId)
			if init:
				# 初始化时，根据数据设置一遍所有按钮
				if cd is None:
					cd = 0
				self.SetBtnCDUI(partId, btn, cd)
			elif cd is not None:
				# 非初始化时，只设置有数据的技能
				self.SetBtnCDUI(partId, btn, cd)
		pass

	def GetSkillCD(self, skillId):
		"""获取技能cd"""
		return self._skillCDDict.get(skillId, {}).get("cd", 0)

	def SetBtnCDUI(self, skillId, btn, cd):
		"""设置技能cdUI"""
		# 特殊处理部分按钮
		if btn == self._flyPanel:
			btn = self._flyStateBtn
		cdObj = btn.GetChildByPath("/cd")
		if cd:
			cd = int(cd)
			clientApiMgr.SetUIVisible(cdObj, True)
			label = cdObj.GetChildByPath("/time").asLabel()
			label.SetText(str(cd))
			# 启动timer，更新cd
			self._skillCDDict[skillId] = {"cd": cd, "cdObj": cdObj, "label": label}
			if not self._skillCDTimer:
				self._skillCDTimer = engineApiGac.AddRepeatedTimer(1, self.UpdateSkillCDUITimer)
		else:
			clientApiMgr.SetUIVisible(cdObj, False)
			self._skillCDDict.pop(skillId, None)
		pass

	def UpdateSkillCDUITimer(self):
		"""更新技能cdUI"""
		if self._skillCDDict:
			for skillId, data in self._skillCDDict.items():
				data["cd"] -= 1
				if data["cd"] <= 0:
					clientApiMgr.SetUIVisible(data["cdObj"], False)
					self._skillCDDict.pop(skillId, None)
				else:
					data["label"].SetText(str(data["cd"]))
		else:
			engineApiGac.CancelTimer(self._skillCDTimer)
			self._skillCDTimer = None
		pass

	# endregion

	# region 设置UI位置
	def SettingDataSubscribtEvent(self, args):
		"""设置UI位置事件"""
		stage = args.get("stage")
		if stage != "car":
			return
		posData = args.get("posData")
		if posData:
			for key, btnVal in posData.iteritems():
				btns = self._btnPosSetMap.get(key)
				if type(btns) == tuple:
					# 多个按钮
					for btn in btns:
						self.SetBtnPosSize(btn, btnVal)
				else:
					# 单个按钮
					self.SetBtnPosSize(btns, btnVal)
		pass

	def SetBtnPosSize(self, btn, data):
		"""设置按钮位置、大小、透明度等表现"""
		pos = data.get("relaPos")
		if pos:
			btn.SetPosition((pos[0], pos[1]))
		alpha = data.get("alpha")
		if alpha is not None and alpha > 0:
			btn.SetAlpha(alpha)
		size = data.get("relaSize")
		if size and size > 0:
			btn.SetSize((size, size), True)
		pass
	# endregion
