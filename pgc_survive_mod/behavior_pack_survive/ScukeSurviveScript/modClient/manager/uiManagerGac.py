# -*- encoding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modCommon.manager.commonMgr import CommonManager
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from mod_log import logger


class UIManagerGac(CommonManager):
	def __init__(self, system):
		super(UIManagerGac, self).__init__(system)
		self.mRegisterFlag = {}
		self.mUIDict = {}

	def UiInitFinished(self, args):
		self.Clear()
		# 通过pushscreen管理的只需要注册就可以
		# 其他绑定在hud上的注册完需要创建一下
		self.RegisterUI(UIDef.UI_SurviveLoading)
		self.CreateUI(UIDef.UI_SurviveLoading, {"isHud": 1})

		self.RegisterUI(UIDef.UI_SurviveScreen)
		self.RegisterUI(UIDef.UI_SurviveTips)
		self.RegisterUI(UIDef.UI_SurviveHud)
		self.RegisterUI(UIDef.UI_GunHud)
		self.RegisterUI(UIDef.UI_MeleeHud)
		self.RegisterUI(UIDef.UI_SurviveMenu)
		self.RegisterUI(UIDef.UI_DialogueUI)
		self.RegisterUI(UIDef.UI_TasksUI)
		self.RegisterUI(UIDef.UI_RewardsUI)
		self.RegisterUI(UIDef.UI_ItemInfoUI)
		self.RegisterUI(UIDef.UI_BindHud)
		self.RegisterUI(UIDef.UI_FollowHud)
		# 图鉴UI
		self.RegisterUI(UIDef.UI_IllustrateUI)
		# 设置UI
		self.RegisterUI(UIDef.UI_SettingUI)
		# 枪械按钮设置UI
		self.RegisterUI(UIDef.UI_GunBtnSettingUI)
		# 近战按钮设置UI
		self.RegisterUI(UIDef.UI_MeleeBtnSettingUI)
		# 帮助界面UI
		self.RegisterUI(UIDef.UI_HelpUI)
		# 载具按钮设置UI
		self.RegisterUI(UIDef.UI_CarBtnSettingUI)
		# 故事过场
		self.RegisterUI(UIDef.UI_SurviveCutscene)
		# 定时炸弹UI
		self.RegisterUI(UIDef.UI_TimeBomb)
		# C4炸弹
		self.RegisterUI(UIDef.UI_C4Bomb)
		# 游戏说明书
		self.RegisterUI(UIDef.UI_GameIntroUI)
		# 战斗事件
		self.RegisterUI(UIDef.UI_BattleEventUI)

		self.CreateUI(UIDef.UI_GameIntroUI, {"isHud": 1})
		self.CreateUI(UIDef.UI_SurviveScreen, {"isHud": 1})
		self.CreateUI(UIDef.UI_SurviveHud, {"isHud": 1})
		self.CreateUI(UIDef.UI_GunHud, {"isHud": 1})
		self.CreateUI(UIDef.UI_MeleeHud, {"isHud": 1})
		self.CreateUI(UIDef.UI_SurviveTips, {"isHud": 1})
		self.CreateUI(UIDef.UI_FollowHud, {"isHud": 1})
		self.CreateUI(UIDef.UI_C4Bomb, {"isHud": 1})
		self.CreateUI(UIDef.UI_BattleEventUI, {"isHud": 1})

		# 载具UI
		self.RegisterUI(UIDef.UI_Car)
		self.CreateUI(UIDef.UI_Car, {"isHud": 1})
		self.RegisterUI(UIDef.UI_CarAddEnergy)
		self.RegisterUI(UIDef.UI_CarRepair)
		self.RegisterUI(UIDef.UI_CarRemold)

		# 功能比较独立的道具物品UI
		self.RegisterUI(UIDef.UI_Items)
		self.CreateUI(UIDef.UI_Items, {"isHud": 1})

		# 一键建造UI
		self.RegisterUI(UIDef.UI_BuildStructCtrl)
		self.CreateUI(UIDef.UI_BuildStructCtrl, {"isHud": 1})
		self.RegisterUI(UIDef.UI_BuildStructSelect)

		# 电力系统UI
		self.RegisterUI(UIDef.UI_ElectricDynamoUI)
		self.RegisterUI(UIDef.UI_ElectricPrinterUI)
		self.RegisterUI(UIDef.UI_ElectricPhotoetchingUI)
		self.RegisterUI(UIDef.UI_ElectricMachineryUI)
		self.RegisterUI(UIDef.UI_ElectricHeaterSmallUI)
		self.RegisterUI(UIDef.UI_ElectricHeaterLargeUI)


	def RegisterUI(self, uiData):
		if not self.mRegisterFlag.get(uiData["ui_key"], False):
			_uiKey = uiData["ui_key"]
			self.mRegisterFlag[_uiKey] = clientApi.RegisterUI(modConfig.ModName, _uiKey, uiData["ui_cls_path"], uiData["ui_namespace"])

	def CreateUI(self, uiData, createParams=None):
		uiKey = uiData["ui_key"]
		ui = clientApi.CreateUI(modConfig.ModName, uiKey, createParams)
		if ui is None:
			logger.error("========create UI Failed %s===========", str(uiData['ui_namespace']))
			return
		hasattr(ui, "InitScreen") and ui.InitScreen()
		self.mUIDict[uiKey] = ui
		return ui

	def PushUI(self, uiData, createParams=None):
		"""
		通过pushscreen的方式创建打开ui，每次打开ui都会将ui类初始化一遍
		:param uiData:
		:return:
		"""
		uiKey = uiData['ui_key']
		ui = clientApi.PushScreen(modConfig.ModName, uiKey, createParams)
		if not ui:
			logger.error('==== %s ====' % '"push UI failed": %s' % uiData['ui_namespace'])
			return
		return ui

	def PopUI(self):
		"""
		通过popscreen的方式关闭由pushscreen打开的ui
		:return:
		"""
		return clientApi.PopScreen()

	def GetTopUI(self):
		return clientApi.GetTopUI()

	def GetUIFromDict(self, uiKey):
		return self.mUIDict.get(uiKey, None)

	def GetUI(self, uiDef):
		return self.GetUIByKey(uiDef['ui_key'])

	def GetUIByKey(self, uiKey):
		if uiKey not in self.mRegisterFlag:
			return None
		ui = self.mUIDict.get(uiKey)
		if ui:
			if not ui.removed:
				return ui
			else:
				return None
		return clientApi.GetUI(modConfig.ModName, uiKey)

	def HasUI(self, uiKey):
		return uiKey in self.mUIDict

	def ShowTips(self, args):
		self.GetUI(UIDef.UI_SurviveTips).ShowTips(args)

	def ShowSnackBar(self, args):
		self.GetUI(UIDef.UI_SurviveTips).ShowSnackBar(args)

	def PushCutscene(self, config):
		cutsceneUI = self.GetUI(UIDef.UI_SurviveCutscene)
		if cutsceneUI:
			cutsceneUI.PushCutscene(config)
		else:
			self.PushUI(UIDef.UI_SurviveCutscene, config)

	def SetCutsceneCompletedCallback(self, callback):
		cutsceneUI = self.GetUI(UIDef.UI_SurviveCutscene)
		if cutsceneUI:
			cutsceneUI.SetCompletedCallback(callback)

	def CreateBindAnchorByEid(self, eid, offset, updateCallback):
		uuid = UIDef.UI_BindHud['ui_key']
		uiNode = clientApi.CreateUI(
			modConfig.ModName,
			uuid,
			{
				"bindEntityId": eid,
				"bindOffset": offset,
				"autoScale": 1
			}
		)
		if uiNode is not None:
			uiNode.SetUpdateCallback(updateCallback)
		return uiNode

	def CreateBindAnchorByPos(self, dim, pos, offset, updateCallback):
		uuid = UIDef.UI_BindHud['ui_key']
		uiNode = clientApi.CreateUI(
			modConfig.ModName,
			uuid,
			{
				"bindWorldPosition": (dim, (pos[0]+offset[0], pos[1]+offset[1], pos[2]+offset[2])),
				"bindOffset": offset,
				"autoScale": 1
			}
		)
		if uiNode is not None:
			uiNode.SetUpdateCallback(updateCallback)
		return uiNode

	def Clear(self):
		for node in self.mUIDict.values():
			node.Destroy()
		self.mUIDict.clear()
		self.mRegisterFlag.clear()
