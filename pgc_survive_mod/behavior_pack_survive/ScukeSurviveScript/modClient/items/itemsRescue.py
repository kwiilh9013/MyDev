# -*- coding: UTF-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.singleton import Singleton
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class ItemsRescue(Singleton, CommonEventRegister):
	"""
	救援道具功能表现 客户端，单例
	以玩家为owner逻辑
	"""
	def __init__(self, clientHandler):
		CommonEventRegister.__init__(self, clientHandler)
		self._client = clientHandler
		self._levelId = self._client.mLevelId
		self._playerId = self._client.mPlayerId
		
		# 救援CD

		# 载具事件回调
		self._carCtrlFunctions = {
			"start_rescue": self.SetRescueUI,
		}

		# 注册UI动画
		cfg = carConfig.GetRescueConfig().get("uiAnimParam")
		self._animNamespace = "sucke_servive_rescue_anim_ui"
		if cfg:
			uiAnimDict = {
				"namespace": self._animNamespace,
				"anim_alpha_0_1": {
					"anim_type": "alpha",
					"duration": cfg.get("0_1_time", 1.0),
					"from": 0,
					"to": 1,
					"next": "@{}.anim_alpha_1_1".format(self._animNamespace)
				},
				"anim_alpha_1_1": {
					"anim_type": "alpha",
					"duration": cfg.get("1_1_time", 1.0),
					"from": 1,
					"to": 1,
					"next": "@{}.anim_alpha_1_0".format(self._animNamespace)
				},
				"anim_alpha_1_0": {
					"anim_type": "alpha",
					"duration": cfg.get("1_0_time", 1.0),
					"from": 1,
					"to": 0
				}
			}
			clientApi.RegisterUIAnimations(uiAnimDict)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		# 清除对象自己
		del self
		pass

	# region 事件
	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.CarServerSystem)
	def CarCtrlEvent(self, args):
		"""载具控制事件，是从CarServerSystem发来的消息"""
		stage = args.get("stage")
		func = self._carCtrlFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion
	
	# region 功能
	def StartRescue(self):
		"""开始救援"""
		# 发消息到服务端，服务端返回是否开始救援的状态
		info = {
			"stage": "start_rescue",
		}
		self.SendMsgToServer(eventConfig.ItemUsedEvent, info)
		pass

	def SetRescueUI(self, args):
		"""设置救援UI"""
		tips = args.get("tips")
		tipText = carConfig.GetTips(tips)
		if tipText:
			# 无法救援，进行提示
			engineApiGac.SetPopupNotice(tipText)
		else:
			# 开始动画效果
			info = {"stage": "black", "propertyName": "alpha", "namespace": self._animNamespace, "animName": "anim_alpha_0_1", "autoPlay": True}
			Instance.mEventMgr.NotifyEvent(eventConfig.FullScreenUIEvent, info)
		pass
	# endregion
