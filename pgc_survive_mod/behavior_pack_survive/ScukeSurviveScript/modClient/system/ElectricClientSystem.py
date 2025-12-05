# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
from ScukeSurviveScript.modCommon.defines import electricEnum
compFactory = clientApi.GetEngineCompFactory()


class ElectricClientSystem(BaseClientSystem):
	"""电力系统 客户端"""
	def __init__(self, namespace, systemName):
		super(ElectricClientSystem, self).__init__(namespace, systemName)
		
		# 方块id和UI对象的映射
		self._blockIdToUIDict = {
			electricEnum.ElectricEnum.DynamoSmall: UIDef.UI_ElectricDynamoUI,
			electricEnum.ElectricEnum.DynamoMiddle: UIDef.UI_ElectricDynamoUI,
			electricEnum.ElectricEnum.DynamoLarge: UIDef.UI_ElectricDynamoUI,
			electricEnum.ElectricEnum.Printer: UIDef.UI_ElectricPrinterUI,
			electricEnum.ElectricEnum.Photoetching: UIDef.UI_ElectricPhotoetchingUI,
			electricEnum.ElectricEnum.Machinery: UIDef.UI_ElectricMachineryUI,
			electricEnum.ElectricEnum.HeaterSmall: UIDef.UI_ElectricHeaterSmallUI,
			electricEnum.ElectricEnum.HeaterLarge: UIDef.UI_ElectricHeaterLargeUI
		}

		self._eventFunctions = {
			"open": self.OpenUI,
			"update_": self.SetUpdateUI,
		}

		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricSubscriptEvent, self.ElectricSubscriptEvent)
		pass

	def Destroy(self):
		super(ElectricClientSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricSubscriptEvent, self.ElectricSubscriptEvent)
		pass
	
	# region 事件
	@EngineEvent()
	def UIInitFinished(self, args):
		"""UI初始化完成事件"""
		pass

	@EngineEvent()
	def ModBlockEntityRemoveClientEvent(self, args):
		"""方块实体移除事件"""
		blockName = args.get("blockName")
		dimensionId = args.get("dimensionId")
		pos = (args.get("posX"), args.get("posY"), args.get("posZ"))
		val = electricConfig.GetElectricConfig(blockName)
		if val:
			# 关闭UI
			info = {
				"stage": "close",
				"blockName": blockName,
				"pos": pos,
				"dimension": dimensionId,
			}
			self.SetUpdateUI(info)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.ElectricServerSystem)
	def ElectricEvent(self, args):
		"""电器事件"""
		stage = args.get("stage")
		if stage.startswith("update_"):
			# 更新UI
			stage = "update_"
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass

	def ElectricSubscriptEvent(self, args):
		"""电器订阅事件"""
		toServer = args.pop("to_server", None)
		if toServer:
			# 转发
			self.SendMsgToServer(eventConfig.ElectricEvent, args)
		else:
			stage = args.get("stage")
			func = self._eventFunctions.get(stage)
			if func:
				func(args)
		pass
	# endregion

	# region 发电机UI
	def OpenUI(self, args):
		"""打开UI"""
		blockName = args.get("blockName")
		uidef = self._blockIdToUIDict.get(blockName)
		if uidef:
			# 如果当前是在主界面
			if clientApiMgr.IsScreenUI():
				Instance.mUIManager.PushUI(uidef, args)
		pass

	def SetUpdateUI(self, args):
		"""设置更新UI"""
		Instance.mEventMgr.NotifyEvent(eventConfig.ElectricUISubscriptEvent, args)
		pass
	# endregion
