# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
from ScukeSurviveScript.modServer.electric.electricBase import ElectricBase
from ScukeSurviveScript.modCommon.cfg import molangConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ElectricHeaterLarge(ElectricBase):
	"""取暖器逻辑"""
	def __init__(self, severHandler, blockName, pos, dimension, param={}):
		super(ElectricHeaterLarge, self).__init__(severHandler, blockName, pos, dimension, param)

		# 功率
		self._kw = self.mCfg.get("kw", 0)
		# 扣除能源间隔
		self._kwTime = self.mCfg.get("kw_time",1)
		# 扣除能源计时器
		self._kwTimer = None
		# 可用的发电机的key
		self._useDynamoKey = None
		# 点击方块的CD
		self._clickBlockTime = 0
		# 加载方块数据
		self.LoadBlockData()
		# 加载数据
		self._eventFunctions = {
			"open": self.OpenUI,
			"work": self.SetWork,
			"dynamo_work": self.SetDynamoWorkState,
		}
		self.GetCanUseDynamo()
		self.SetWork({"work":self.mWorkState})
		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		pass

	def Destroy(self, breaks=False):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		# 解除占用
		self.SetUseKw(False)
		if breaks:
			# 同步状态
			self.mWorkState = False
		if self._kwTimer:
			engineApiGas.CancelTimer(self._kwTimer)
			self._kwTimer = None
		super(ElectricHeaterLarge, self).Destroy(breaks)
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
			"work": self.mWorkState,
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
		# 根据是否有发电机key设置工作状态
		if not self._useDynamoKey:
			self.mWorkState = False
		if self.mWorkState:
			self.animeState(1)
		else:
			self.animeState(0)
		pass
	# endregio

	# region 设置工作状态
	def SetWork(self, args):
		"""设置工作状态"""
		self.mWorkState = args.get("work")
		self.hasWork(self.mWorkState)
		# 同步到客户端，更新UI
		info = {
			"stage": "update_work",
			"work": self.mWorkState,
			"key": self.mKey,
		}
		if self.mWorkState:
			self.animeState(1)
		else:
			self.animeState(0)
		self.SendUIInfo(info)
	# endregio

	# region 根据工作状态扣除能源
	def hasWork(self,state):
		if state:
			electricInfo = {
				"stage": "deduct_energy",
				"kw": self._kw,
				"time": self._kwTime,
				"dynamoKey": self._useDynamoKey,
			}
			if self._kwTimer:
				engineApiGas.CancelTimer(self._kwTimer)
			self._kwTimer = engineApiGas.AddRepeatTimer(self._kwTime ,Instance.mEventMgr.NotifyEvent,eventConfig.ElectricLogicSubscriptEvent,electricInfo)
		else:
			if self._kwTimer:
				engineApiGas.CancelTimer(self._kwTimer)
				self._kwTimer = None
	# endregio

	# region 设置动画状态
	def animeState(self,workingStateValue):
		"""动画状态控制"""
		info = {
				"stage": "set_block",
				"pos": self.mPos,
				"dimension": self.mDimension,
				"molangValue": {molangConfig.VariableEnum.WorkingState: workingStateValue},
			}
		Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
	# endregion

	# region 数据存储
	def LoadBlockData(self):
		"""加载方块数据"""
		super(ElectricHeaterLarge, self).LoadBlockData()
		blockData = self.mBlockDataComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[electricConfig.BlockEntityDataKey]
			if not data:
				data = {}
			# 获取工作状态
			self.mWorkState = data.get("work_state", False)
			# 设置工作状态
			self.SetWork({"work":self.mWorkState})
			if self.mWorkState:
				self.animeState(1)
			else:
				self.animeState(0)
		pass

	def SaveBlockData(self):
		"""保存方块数据"""
		super(ElectricHeaterLarge, self).SaveBlockData()
		blockData = self.mBlockDataComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[electricConfig.BlockEntityDataKey]
			if not data:
				data = {}
			data["work_state"] = self.mWorkState
			blockData[electricConfig.BlockEntityDataKey] = data
		pass
	# endregion