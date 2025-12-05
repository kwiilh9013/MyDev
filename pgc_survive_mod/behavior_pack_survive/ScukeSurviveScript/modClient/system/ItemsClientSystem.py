# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.items.itemsRescue import ItemsRescue
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.client import engineApiGac
compFactory = clientApi.GetEngineCompFactory()


class ItemsClientSystem(BaseClientSystem):
	"""物品道具 客户端"""
	def __init__(self, namespace, systemName):
		super(ItemsClientSystem, self).__init__(namespace, systemName)
		
		# 当前手持的物品
		self._carriedItemName = None

		# 订阅事件回调函数
		self._itemUseSubscribeFunctions = {
			# 救援道具
			"car_rescue": self.SetRescueCar,
		}
		self._eventFunctions = {
			"use_projectile": self.SetUseProjectile,
		}
		pass

	def Destroy(self):
		super(ItemsClientSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ItemUseBtnClickedEvent, self.ItemUseBtnClickedEvent)
		pass
	
	# region 事件
	@EngineEvent()
	def UiInitFinished(self, args=None):
		"""UI初始化完成事件"""
		# 再执行一遍手持物品的逻辑，如果玩家进入时便是手持物品，则会不显示UI（UI后创建）
		self._carriedItemName = None
		self.OnCarriedNewItemChangedClientEvent({"itemDict": clientApiMgr.GetPlayerCarriedItem(self.mPlayerId)})
		
		# 注册订阅，在init时订阅，可能会还没初始化eventMgr
		Instance.mEventMgr.RegisterEvent(eventConfig.ItemUseBtnClickedEvent, self.ItemUseBtnClickedEvent)
		
		# 手持动画
		self.SetBuildInHandAnim(self.mPlayerId)
		pass

	@EngineEvent()
	def OnCarriedNewItemChangedClientEvent(self, args):
		"""主手持物品改变事件"""
		itemDict = args.get("itemDict")
		itemName = None
		if itemDict:
			itemName = itemDict.get("newItemName")
		cfg = itemsConfig.GetItemsUIConfig(itemName)
		if cfg:
			# 显示UI
			Instance.mEventMgr.NotifyEvent(eventConfig.ShowItemUseUIEvent, {"state": True, "itemName": itemName})
		elif self._carriedItemName != itemName:
			# 隐藏UI
			Instance.mEventMgr.NotifyEvent(eventConfig.ShowItemUseUIEvent, {"state": False, "itemName": self._carriedItemName})
		
		self._carriedItemName = itemName
		pass
	
	@EngineEvent()
	def AddPlayerCreatedClientEvent(self, args):
		"""玩家进入视野范围后事件"""
		playerId = args.get("playerId")
		self.SetBuildInHandAnim(playerId)
		pass

	def ItemUseBtnClickedEvent(self, args):
		"""订阅事件"""
		stage = args.get("stage")
		func = self._itemUseSubscribeFunctions.get(stage)
		if func:
			func(args)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.ItemsServerSystem)
	def ItemUsedEvent(self, args):
		"""使用物品事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region 功能
	def SetRescueCar(self, args):
		"""救援载具"""
		# 创建救援道具的对象，在对象里处理逻辑
		obj = ItemsRescue(self)
		obj.StartRescue()
		pass

	def SetUseProjectile(self, args):
		"""使用抛射物"""
		playerId = args.get("playerId")
		itemName = args.get("itemName")
		cfg = itemsConfig.GetProjectileConfig(itemName)
		if cfg:
			# 播放动画
			animCfg = cfg.get("use_anim_cfg")
			if animCfg:
				info = {
					"stage": "set_molang", "entityId": playerId, 
					"molang": animCfg["molang"], "value": 1, 
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
				# 延迟恢复molang
				resetInfo = {
					"stage": "set_molang", "entityId": playerId, 
					"molang": animCfg["molang"], "value": 0, 
				}
				engineApiGac.AddTimer(animCfg.get("molang_reset_time", 0.1), Instance.mEventMgr.NotifyEvent, eventConfig.MolangUpdateEvent, resetInfo)
		pass
	# endregion

	# region 属性
	def GetCurrentItemName(self):
		"""获取当前手持物品名称"""
		return self._carriedItemName
	# endregion

	@EngineEvent()
	def ClientShapedRecipeTriggeredEvent(self, args):
		self.NotifyToServer('OnClientShapedRecipe', {
			'playerId': clientApi.GetLocalPlayerId(),
			'recipeId': args['recipeId']
		})
	
	# region 动画
	def SetBuildInHandAnim(self, playerId):
		"""设置建造手持动画"""
		cfg = itemsConfig.GetGrenadeBindAnims()
		# 添加动画
		renderComp = compFactory.CreateActorRender(playerId)
		for animKey, anim in cfg.get("anims", {}).iteritems():
			renderComp.AddPlayerAnimation(animKey, anim)
		for ctrlKey, ctrl in cfg.get("anim_ctrls", {}).iteritems():
			renderComp.AddPlayerAnimationController(ctrlKey, ctrl)
			renderComp.AddPlayerScriptAnimate(ctrlKey, cfg.get("ctrl_condition", ""))
		renderComp.RebuildPlayerRender()
		pass
	# endregion

