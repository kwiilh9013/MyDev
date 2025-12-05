# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.electric.electricBase import ElectricBase
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon.cfg import molangConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ElectricDynamo(ElectricBase):
	"""发电机逻辑"""
	def __init__(self, severHandler, blockName, pos, dimension, param={}):
		super(ElectricDynamo, self).__init__(severHandler, blockName, pos, dimension, param)

		# 当前使用的功率
		self._useKW = 0
		# 最大功率
		self._maxKW = self.mCfg.get("kw")

		# 当前能源值
		self._currentEnergy = 0
		# 最大能源值
		self._maxEnergy = self.mCfg.get("max_energy")

		# 供电范围
		self._radius = self.mCfg.get("radius")

		# 加载数据
		self.LoadBlockData()
		# 点击方块的CD
		self._clickBlockTime = 0

		# 扣能源的timer
		self._deductTimer = None

		self._eventFunctions = {
			"open": self.OpenUI,
			"add_energy": self.AddEnergy,
			"work": self.SetWork,
			# 检测是否有可用发电机
			"check_canuse_dynamo": self.CheckCanUseDynamo,
			# 使用/解除使用功率
			"set_use_kw": self.SetUseKW,
			# 扣能源
			"deduct_energy": self.DeductEnergy,
		}
		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		pass

	def Destroy(self, breaks=False):
		if self._deductTimer:
			engineApiGas.CancelTimer(self._deductTimer)
			self._deductTimer = None
		if breaks:
			# 同步状态
			self.mWorkState = False
			self.SetWorkStateMsg()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		super(ElectricDynamo, self).Destroy(breaks)
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

	# region 订阅逻辑
	def CheckCanUseDynamo(self, args):
		"""检测是否有可用发电机"""
		useDynamo = args.get("useDynamo")
		dimension = args.get("dimension")
		pos = args.get("pos")
		kw = args.get("kw")
		canUse, dist = self.IsCauUse(dimension, pos, kw)
		if canUse:
			# 此时还没有可用的发电机
			if not useDynamo:
				# 标记可用当前发电机
				args["useDynamo"] = {
					"key": self.mKey,
					"dist": dist,
				}
			else:
				# 判断距离，如果本发电机距离更近，则切换到本发电机
				hasDist = useDynamo.get("dist")
				if hasDist and hasDist > dist:
					# 切换到本发电机
					args["useDynamo"] = {
						"key": self.mKey,
						"dist": dist,
					}
		pass

	def IsCauUse(self, targetDimension, targetPos, targetKW):
		"""本发电机是否可接入某个设备"""
		dist = None
		isCan = False
		# 本发电机启动才能供应
		if self.mWorkState:
			if self.mDimension == targetDimension:
				if self._useKW + targetKW <= self._maxKW:
					# 判断是否在范围内
					if commonApiMgr.InRectangleRange(self.mPos, self._radius, targetPos):
						# 判断距离远近
						dist = commonApiMgr.GetManhattanDistance(self.mPos, targetPos)
						isCan = True
		return isCan, dist
	
	def SetUseKW(self, args):
		"""设置电器占用发电机功率"""
		dynamoKey = args.get("dynamoKey")
		if dynamoKey == self.mKey:
			kw = args.get("kw")
			state = args.get("state")
			if state:
				# 占用功率
				self._useKW += kw
			else:
				# 解除占用
				self._useKW -= kw
			# 同步到客户端，更新UI
			info = {
				"stage": "update_kw",
				"kw": self._useKW,
				"key": self.mKey,
			}
			self.SendUIInfo(info)
		pass
	
	def DeductEnergy(self, args):
		"""扣能源"""
		dynamoKey = args.get("dynamoKey")
		if dynamoKey == self.mKey:
			if self.mWorkState:
				# 根据传递过来的功率、合成时间，计算扣除的能源值
				kw = args.get("kw")
				craftTime = args.get("time")
				# 根据当前的功率，计算此时应当扣多少能源
				energy = electricConfig.GetEnergyConsumption(kw, craftTime)
				# 扣除能源
				self._currentEnergy -= energy
				if self._currentEnergy <= 0:
					# 停止工作
					self.SetWork({"work": False})
					self._currentEnergy = 0
				else:
					# 更新剩余能源
					info = {
						"stage": "update_energy",
						"energy": self._currentEnergy,
						"key": self.mKey,
					}
					self.SendUIInfo(info)
		pass
	# endregion

	# region UI
	def OpenUI(self, args):
		"""打开UI"""
		playerId = args.get("__id__")
		# 同步数据到客户端
		info = {
			"stage": "open",
			"blockName": self.mBlockName,
			"pos": self.mPos,
			"dimension": self.mDimension,
			"key": self.mKey,
			"energy": self._currentEnergy,
			"kw": self._useKW,
			"work": self.mWorkState,
		}
		self.SendMsgToClient(playerId, eventConfig.ElectricEvent, info)
		pass
	# endregion

	# region 能源
	def AddEnergy(self, args):
		"""添加能源"""
		materials = args.get("materials")
		if materials:
			# 判断当前能源是否满的
			if self._currentEnergy >= self._maxEnergy:
				return
			
			playerId = args.get("__id__")
			# 扣除材料物品
			materialList = []
			addEnergy = 0
			for item, count in materials.iteritems():
				if type(item) == tuple:
					mat = {"newItemName": item[0], "newAuxValue": item[1], "count": count}
					addEnergy += electricConfig.GetAddEnergyMaterialNum(item[0]) * count
				else:
					mat = {"newItemName": item, "count": count}
					addEnergy += electricConfig.GetAddEnergyMaterialNum(item) * count
				materialList.append(mat)
			res = serverApiMgr.DeductMultiItemsCount(playerId, materialList)
			if res:
				# 扣除成功
				self._currentEnergy += addEnergy
				# 刷新客户端UI
				info = {
					"stage": "update_mat",
					"energy": self._currentEnergy,
					"kw": self._useKW,
					"work": self.mWorkState,
					"key": self.mKey,
				}
				self.SendUIInfo(info)
		pass
	# endregion

	# region 启动
	def SetWork(self, args):
		"""设置工作状态"""
		work = args.get("work")
		# 如果没有能源了，则改为关闭
		if self._currentEnergy <= 0:
			work = False
		self.mWorkState = work
		if self.mWorkState is False:
			# 取消占用功率
			self._useKW = 0
		# 同步到客户端，更新UI
		info = {
			"stage": "update_work",
			"work": self.mWorkState,
			"key": self.mKey,
		}
		self.SendUIInfo(info)
		# 同步到其他设备
		self.SetWorkStateMsg()
		# 同步动画状态
		if self.mWorkState:
			self.animeState(1)
		else:
			self.animeState(0)
		# # 启动/停止扣能源
		# if self.mWorkState:
		# 	if self._deductTimer is None:
		# 		self._deductTimer = engineApiGas.AddRepeatTimer(electricConfig.DeductEnergyCD, self.DeductEnergyTimer)
		# else:
		# 	if self._deductTimer:
		# 		engineApiGas.CancelTimer(self._deductTimer)
		# 		self._deductTimer = None
		
		pass

	def SetWorkStateMsg(self):
		"""停止工作消息"""
		# 状态同步到其他设备
		electricInfo = {
			"stage": "dynamo_work",
			"state": self.mWorkState,
			"key": self.mKey,
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.ElectricLogicSubscriptEvent, electricInfo)
		pass

	def DeductEnergyTimer(self):
		"""扣能源timer"""
		if self._useKW > 0:
			# 根据当前的功率，计算此时应当扣多少能源
			energy = electricConfig.GetEnergyConsumption(self._useKW)
			# 扣除能源
			self._currentEnergy -= energy
			if self._currentEnergy <= 0:
				# 停止工作
				self.SetWork({"work": False})
			else:
				# 更新剩余能源
				info = {
					"stage": "update_energy",
					"energy": self._currentEnergy,
					"key": self.mKey,
				}
				self.SendUIInfo(info)
		pass

	# endregion

	# region 数据存储
	def LoadBlockData(self):
		"""加载方块数据"""
		super(ElectricDynamo, self).LoadBlockData()
		blockData = self.mBlockDataComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[electricConfig.BlockEntityDataKey]
			if not data:
				data = {}
			# 当前能源
			self._currentEnergy = data.get("energy", 0)
			# 开启状态
			self.mWorkState = data.get("work_state", False)
		pass

	def SaveBlockData(self):
		"""保存方块数据"""
		super(ElectricDynamo, self).SaveBlockData()
		blockData = self.mBlockDataComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[electricConfig.BlockEntityDataKey]
			if not data:
				data = {}
			data["energy"] = self._currentEnergy
			data["work_state"] = self.mWorkState
			blockData[electricConfig.BlockEntityDataKey] = data
		pass
	# endregion
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
