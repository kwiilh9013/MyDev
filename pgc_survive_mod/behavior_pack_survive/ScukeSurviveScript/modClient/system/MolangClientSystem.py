# -*- coding: utf-8 -*-
import math
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon.cfg import molangConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.car import carConfig
compFactory = clientApi.GetEngineCompFactory()


class MolangClientSystem(BaseClientSystem):
	"""molang表达式 客户端"""
	def __init__(self, namespace, systemName):
		super(MolangClientSystem, self).__init__(namespace, systemName)
		
		# 注册molang
		queryComp = compFactory.CreateQueryVariable(self.mLevelId)
		for key in molangConfig.QueryEnum.MolangList:
			queryComp.Register(key, 0.0)

		# 实体对象
		self._entityDict = {}
		
		pass

	def Destroy(self):
		super(MolangClientSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.MolangUpdateEvent, self.MolangUpdateEvent)
		pass
	
	# region 事件
	@EngineEvent()
	def LoadClientAddonScriptsAfter(self, args=None):
		"""客户端加载mod完成事件"""
		# 订阅事件
		Instance.mEventMgr.RegisterEvent(eventConfig.MolangUpdateEvent, self.MolangUpdateEvent)
		pass

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		"""客户端添加实体事件"""
		entityId = args.get("id")
		engineTypeStr = args.get("engineTypeStr")
		self.CreateLogicObj(entityId, engineTypeStr)
		pass

	@EngineEvent()
	def RemoveEntityClientEvent(self, args):
		"""客户端移除实体事件"""
		entityId = args.get("id")
		self.PopLogicObj(entityId)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.MolangServerSystem)
	def MolangUpdateEvent(self, args):
		"""更新molang事件，订阅事件也走这里的逻辑"""
		stage = args.get("stage")
		entityId = args.get("entityId")
		if stage == "set_molangs":
			# 批量设置molang
			molangValue = args.get("molangValue")
			for key, val in molangValue.iteritems():
				self.SetEntityMolang(entityId, key, val)

			# 针对载具的逻辑
			riders = args.get("riders")
			if riders:
				# 设置乘客的molang
				obj = self.GetLogicObj(entityId)
				if obj:
					pitchRot = molangValue.get(molangConfig.QueryEnum.CarPitchRot, 0)
					rollRot = molangValue.get(molangConfig.QueryEnum.CarRollRot, 0)
					obj.SetRidersRidePos(riders, pitchRot, rollRot)
		elif stage == "set_molang":
			# 设置某个molang
			molang = args.get("molang")
			value = args.get("value")
			self.SetEntityMolang(entityId, molang, value)
		elif stage == "set_entitys_molang":
			# 设置多个实体的多个molang
			entities = args.get("entities")
			for entity in entities:
				for key, val in args.get("molangValue", {}).iteritems():
					self.SetEntityMolang(entity, key, val)
		elif stage == "set_block_molangs":
			# 设置方块的molang
			pos = args.get("pos")
			molangValue = args.get("molangValue")
			for key, val in molangValue.iteritems():
				self.SetBlockMolang(pos, key, val)
		pass

	# endregion

	# region 功能
	def SetEntityMolang(self, entityId, molang, value):
		"""设置实体molang值"""
		queryComp = compFactory.CreateQueryVariable(entityId)
		return queryComp.Set(molang, value)

	def SetBlockMolang(self, pos, molang, value):
		"""设置方块molang值"""
		blockComp = compFactory.CreateBlockInfo(self.mLevelId)
		return blockComp.SetBlockEntityMolangValue(pos, molang, value)

	def GetBlockMolang(self, pos, molang):
		"""获取方块molang值"""
		blockComp = compFactory.CreateBlockInfo(self.mLevelId)
		val = blockComp.GetBlockEntityMolangValue(pos, molang)
		return val
	
	def CreateLogicObj(self, entityId, engineTypeStr):
		"""创建逻辑对象"""
		obj = self._entityDict.get(entityId)
		if obj is None:
			cfg = molangConfig.GetMolangCfg(engineTypeStr)
			if cfg:
				obj = MolangEntityCar(self, entityId, engineTypeStr)
				self._entityDict[entityId] = obj
		return obj
	
	def GetLogicObj(self, entityId):
		"""获取逻辑对象"""
		return self._entityDict.get(entityId)
	
	def PopLogicObj(self, entityId):
		"""删除逻辑对象"""
		obj = self._entityDict.pop(entityId, None)
		if obj:
			obj.Destroy()
		pass
	# endregion


class MolangEntityCar(CommonEventRegister):
	"""用于设置molang的实体对象"""
	def __init__(self, clientHandler, entityId, engineTypeStr):
		CommonEventRegister.__init__(self, clientHandler)
		self._clientHandler = clientHandler
		self._entityId = entityId
		self._engineTypeStr = engineTypeStr
		self._cfg = molangConfig.GetMolangCfg(engineTypeStr)

		# 乘客的molang数据，用于插值计算: {entityId: {"current": (x,y,z), "target": (x,y,z)}}
		self._ridersMolangDict = {}
		self._pitchRollMolangDict = {}
		# 插值比例
		self._lerpRatio = 0.02

		# 发消息到服务端，获取molang值
		info = {
			"stage": "get_molang",
			"entityId": entityId,
		}
		self.SendMsgToServer(eventConfig.MolangUpdateEvent, info)

		self._blockComp = compFactory.CreateBlockInfo(self._clientHandler.mLevelId)
		self._posComp = compFactory.CreatePos(self._entityId)

		# 根据config，启动对应的timer
		self._waterTimer = None
		if self._cfg.get("in_water") or self._cfg.get("in_lava"):
			self._waterTimer = engineApiGac.AddRepeatedTimer(0.1, self.UpdateInWaterTimer)
		self._isInWaterOrLava = None
		self._inWater = None
		self._inLava = None

		# 监听渲染tick
		Instance.mEventMgr.RegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameRenderTick)
		pass

	def Destroy(self):
		"""销毁实体对象"""
		CommonEventRegister.OnDestroy(self)
		Instance.mEventMgr.UnRegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameRenderTick)
		if self._waterTimer:
			engineApiGac.CancelTimer(self._waterTimer)
			self._waterTimer = None
		self._cfg = None
		del self
		pass

	def UpdateInWaterTimer(self):
		"""更新是否在水中或岩浆中"""
		pos = self._posComp.GetFootPos()
		if pos is None:
			return
		block = self._blockComp.GetBlock(commonApiMgr.GetBlockPosByEntityPos(pos))
		if not block:
			return
		
		inWater = False
		if self._cfg.get("in_water"):
			inWater = "water" in block[0]
			if inWater != self._inWater:
				self._inWater = inWater
				self._clientHandler.SetEntityMolang(self._entityId, molangConfig.QueryEnum.InWater, 1 if inWater else 0)
		inLava = False
		if self._cfg.get("in_lava"):
			inLava = "lava" in block[0]
			if inLava != self._inLava:
				self._inLava = inLava
				self._clientHandler.SetEntityMolang(self._entityId, molangConfig.QueryEnum.InLava, 1 if inLava else 0)
		lastState = self._isInWaterOrLava
		self._isInWaterOrLava = inWater or inLava

		# 同步到UI，修改UI表现
		# TODO: 优化，需减少订阅的频率
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": "inwater", "value": self._isInWaterOrLava})

		# 如果在水中，高度直接往下降
		if lastState is not None and lastState != self._isInWaterOrLava:
			for val in self._ridersMolangDict.values():
				if val.get("target"):
					val["target"] = (
						val["target"][0],
						# 下降的值，需和动画里保持一致
						val["target"][1] - (12 if self._isInWaterOrLava else -12),
						val["target"][2]
					)
		pass

	# region 载具的乘客位置
	def SetRidersRidePos(self, riders, pitchRot, rollRot):
		"""设置乘客的乘骑位置"""
		# 如果没有记录该实体，则进行记录
		# 如果有旧的实体不在列表中了，则清除、并重置数据
		# 如果该实体有之前的设置数据，则做插值计算

		# 角度倾斜（插值）
		lerpRot = (pitchRot, rollRot)
		if not self._pitchRollMolangDict:
			# 初始化，记录值
			self._pitchRollMolangDict = {"current": lerpRot, "target": lerpRot}
		else:
			# 计算插值
			val = self._pitchRollMolangDict
			val["target"] = lerpRot
			lerpRot = commonApiMgr.VectorLerp(val.get("current", lerpRot), val["target"], self._lerpRatio)
			val["current"] = lerpRot

		# 位置倾斜（根据座位计算、插值）
		oldList = self._ridersMolangDict.keys()
		seatId = 0
		for rider in riders:
			val = self._ridersMolangDict.get(rider)
			# 计算乘骑位置
			seatCfg = carConfig.GetRidePos(seatId)
			targetPos = (
				(math.cos(math.radians(seatCfg["xyRot"] - rollRot)) * seatCfg["xyLen"] - seatCfg["pos"][0]) * 16,
				(math.sin(math.radians(seatCfg["zyRot"] - pitchRot)) * seatCfg["zyLen"] - seatCfg["pos"][1]) * 16,
				-(math.cos(math.radians(seatCfg["zyRot"] - pitchRot)) * seatCfg["zyLen"] - seatCfg["pos"][2]) * 16,
			)
			if val is None:
				# 直接设置
				val = {"current": targetPos, "target": targetPos}
				self._ridersMolangDict[rider] = val
			else:
				oldList.remove(rider)
				# 更新，插值计算
				val["target"] = targetPos
				val["current"] = commonApiMgr.VectorLerp(val["current"], val["target"], self._lerpRatio)
			# 设置位置偏移
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosX, val["current"][0])
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosY, val["current"][1])
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosZ, val["current"][2])
			# 设置倾斜
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.CarPitchRot, lerpRot[0])
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.CarRollRot, lerpRot[1])

			# # 如果是本地玩家，则修改相机锚点
			# if rider == self._clientHandler.mPlayerId:
			# 	# x+ = 往右, z+ = 往前
			# 	camerAnchor = (targetPos[0] * 0.0625, targetPos[1] * 0.0625, targetPos[2] * 0.0625)
			# 	cameraComp = compFactory.CreateCamera(self._clientHandler.mLevelId)
			# 	cameraComp.SetCameraAnchor(camerAnchor)
			seatId += 1
		# 剩下的实体，则重置角度
		for rider in oldList:
			self._ridersMolangDict.pop(rider, None)
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosX, 0)
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosY, 0)
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosZ, 0)
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.CarPitchRot, 0)
			self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.CarRollRot, 0)
			if rider == self._clientHandler.mPlayerId:
				cameraComp = compFactory.CreateCamera(self._clientHandler.mLevelId)
				cameraComp.SetCameraAnchor((0, 0, 0))
		pass

	def OnGameRenderTick(self, args):
		"""渲染tick事件"""
		# 玩家偏移位置的插值计算
		# 如果前后两个点的距离小于某个值，则不再计算插值（为简化计算，这里用曼哈顿距离作为比较）
		# 倾斜角度插值
		lerpRot = None
		if self._pitchRollMolangDict:
			val = self._pitchRollMolangDict
			if val.get("current") and val.get("target"):
				dist = math.fabs(val["current"][0] - val["target"][0]) + math.fabs(val["current"][1] - val["target"][1])
				if dist > 0.1:
					lerpRot = commonApiMgr.VectorLerp(val["current"], val["target"], self._lerpRatio)
					val["current"] = lerpRot
		for rider, val in self._ridersMolangDict.iteritems():
			currentPos = val["current"]
			targetPos = val["target"]
			dist = math.fabs(currentPos[0] - targetPos[0]) + math.fabs(currentPos[1] - targetPos[1]) + math.fabs(currentPos[2] - targetPos[2])
			if dist > 0.1:
				# 计算插值
				val["current"] = commonApiMgr.VectorLerp(currentPos, targetPos, self._lerpRatio)
				# 设置位置
				self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosX, val["current"][0])
				self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosY, val["current"][1])
				self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.RiderPosZ, val["current"][2])
			# 设置倾斜
			if lerpRot:
				self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.CarPitchRot, lerpRot[0])
				self._clientHandler.SetEntityMolang(rider, molangConfig.QueryEnum.CarRollRot, lerpRot[1])
		pass
	# endregion
