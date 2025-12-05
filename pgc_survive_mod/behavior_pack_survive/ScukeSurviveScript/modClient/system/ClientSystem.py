# -*- coding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.common.log.logManager import LogManager
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import disassembleConfig

EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType


class ClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(ClientSystem, self).__init__(namespace, systemName)
		self._loadCompleted = False
		self.InitManager()

	def InitManager(self):
		print("==========InitManager=========")
		from ScukeSurviveScript.modClient.manager.clientMgrList import ClientManagerList
		import re
		strinfo = re.compile(r'Gac$')
		for mgrCls in ClientManagerList:
			mgr = mgrCls(self)
			identifyName = mgrCls.__name__ if not hasattr(mgrCls, '__identify__') else mgrCls.__identify__
			setattr(Instance, "m" + strinfo.sub("", identifyName), mgr)


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
		# 注册拆解台配方
		dusassenbleMod = "ScukeDisassembleMod"
		disassembleRecipesSystem = clientApi.GetSystem(dusassenbleMod, "{}RecipesClientSystem".format(dusassenbleMod))
		if disassembleRecipesSystem:
			DisassembleRecipes = disassembleConfig.GetDisassembleRecipes()
			for itemName in DisassembleRecipes:
				disassembleRecipesSystem.AddModRecipes(itemName, [DisassembleRecipes[itemName]])
		pass

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnLoadCompleted(self, data):
		self._loadCompleted = True
		loadingUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveLoading)
		if loadingUI:
			loadingUI.SetActive(False)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnShelterBorn(self, data):
		self._loadCompleted = True
		loadingUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveLoading)
		if loadingUI:
			engineApiGac.AddTimer(0.3, loadingUI.SetActive, False)

