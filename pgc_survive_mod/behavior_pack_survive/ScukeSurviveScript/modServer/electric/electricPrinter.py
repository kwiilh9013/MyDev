# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.electric.electricRecipeConfig import GetElectricItemRecipe
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.electric.electricBase import ElectricBase
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ElectricPrinter(ElectricBase):
	"""打印机逻辑"""
	def __init__(self, severHandler, blockName, pos, dimension, param={}):
		super(ElectricPrinter, self).__init__(severHandler, blockName, pos, dimension, param)

		# 功率
		self._kw = self.mCfg.get("kw", 0)
		# 可用的发电机的key
		self._useDynamoKey = None

		# 点击方块的CD
		self._clickBlockTime = 0

		self._eventFunctions = {
			"open": self.OpenUI,
			"craft": self.SetCraftItems,
			"dynamo_work": self.SetDynamoWorkState,
		}

		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		pass

	def Destroy(self, breaks=False):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		# 解除占用
		self.SetUseKw(False)
		super(ElectricPrinter, self).Destroy(breaks)
		pass

	# region 事件
	@EngineEvent()
	def ServerBlockUseEvent(self, args):
		"""点击方块事件"""
		blockName = args.get("blockName")
		dimensionId = args.get("dimensionId")
		pos = (args.get("x"), args.get("y"), args.get("z"))
		if blockName == self.mBlockName and dimensionId == self.mDimension and pos == self.mPos:
			t = time.time()
			if t - self._clickBlockTime > 0.3:
				args["cancel"] = True
				self._clickBlockTime = t
				playerId = args.get("playerId")
				self.OpenUI({"__id__": playerId})
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ElectricClientSystem)
	def ElectricEvent(self, args):
		"""电器事件"""
		key = args.get("key")
		if key == self.mKey:
			stage = args.get("stage")
			func = self._eventFunctions.get(stage)
			if func:
				func(args)
		pass

	def ElectricLogicSubscriptEvent(self, args):
		"""电器订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region UI
	def OpenUI(self, args):
		"""打开UI"""
		playerId = args.get("__id__")
		# 获取附近可用的发电机
		if self._useDynamoKey:
			hasDynamo = True
		else:
			hasDynamo = self.GetCanUseDynamo()
		# 同步数据到客户端
		info = {
			"stage": "open",
			"blockName": self.mBlockName,
			"pos": self.mPos,
			"dimension": self.mDimension,
			"key": self.mKey,
			"dynamo": hasDynamo,
		}
		self.SendMsgToClient(playerId, eventConfig.ElectricEvent, info)
		pass
	# endregion

	# region 电力
	def GetCanUseDynamo(self):
		"""获取可用的发电机"""
		# 触发订阅事件，查询发电机
		info = {
			"stage": "check_canuse_dynamo",
			"key": self.mKey,
			"dimension": self.mDimension,
			"pos": self.mPos,
			"kw": self._kw,
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.ElectricLogicSubscriptEvent, info)
		# 获取返回结果
		useDynamo = info.get("useDynamo")
		if useDynamo:
			if self._useDynamoKey != useDynamo.get("key"):
				# 解除占用
				self.SetUseKw(False)
				# 占用
				self._useDynamoKey = useDynamo.get("key")
				self.SetUseKw(True)
			return True
		self._useDynamoKey = None
		return False
	
	def SetUseKw(self, state):
		"""设置占用/解除占用电力功率"""
		if self._useDynamoKey:
			kwInfo = {
				"stage": "set_use_kw",
				"state": state,
				"kw": self._kw,
				"dynamoKey": self._useDynamoKey,
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.ElectricLogicSubscriptEvent, kwInfo)
		pass

	def SetDynamoWorkState(self, args):
		"""发电机工作状态同步"""
		key = args.get("key")
		state = args.get("state")
		check = False
		if key == self._useDynamoKey and state is False:
			# 发电机停止工作
			check = True
		elif self._useDynamoKey is None and state:
			# 有新的发电机启动
			check = True
		if check:
			# 重新找发电机
			hasDynamo = self.GetCanUseDynamo()
			# 更新状态到客户端
			info = {
				"stage": "update_dynamo",
				"key": self.mKey,
				"dynamo": hasDynamo,
			}
			self.SendUIInfo(info)
		pass
	# endregion

	# region 合成物品
	def SetCraftItems(self, args):
		"""设置合成物品"""
		playerId = args.get("__id__")
		item = args.get("item")
		# 配方
		recipe = GetElectricItemRecipe(item)
		outputItem = recipe.get("output")
		if outputItem:
			# 扣除材料物品
			res = serverApiMgr.DeductMultiItemsCount(playerId, recipe.get("input", []))
			if res:
				# 扣除成功
				# 将物品给到玩家
				serverApiMgr.SpawnItemsToInventory(self.mServer, playerId, [outputItem])
				# 弹窗
				info = {
					"playerId": playerId,
					"rewards": {outputItem.get("newItemName"): outputItem.get("count", 1)},
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.GetRewardsPopupEvent, info)
				# 消耗电力，根据自己的功率+合成时间
				electricInfo = {
					"stage": "deduct_energy",
					"kw": self._kw,
					"time": outputItem.get("time", 1),
					"dynamoKey": self._useDynamoKey,
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.ElectricLogicSubscriptEvent, electricInfo)
				# 广播合成消息
				self.mServer.BroadcastEvent(eventConfig.ElectricCraftingItemsEvent, {"playerId": playerId, "itemName": outputItem.get("newItemName"), "count": outputItem.get("count", 1)})
		else:
			print("_________ ERROR：物品配方没有设置获得物品的数据，itemName=", item)
		pass
	# endregion
