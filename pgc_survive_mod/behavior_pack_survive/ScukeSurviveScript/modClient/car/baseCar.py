# -*- coding: UTF-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.singleton import Singleton
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.modCommon.cfg.molangConfig import QueryEnum
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.car.baseCarSkillClient import BaseCarSkillClient
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class VectorEnum:
	"""向量枚举"""
	Up = (0, 1)
	Cut = (0, -1)
	Cancel = (0, 0)

# 乘骑时的键盘按键映射
RideKeyboardMappings = {
	# 移动
	(str(minecraftEnum.KeyBoardType.KEY_W), "1"): "up",
	(str(minecraftEnum.KeyBoardType.KEY_W), "0"): "cancel",
	(str(minecraftEnum.KeyBoardType.KEY_S), "1"): "cut",
	(str(minecraftEnum.KeyBoardType.KEY_S), "0"): "cancel",
	(str(minecraftEnum.KeyBoardType.KEY_A), "1"): "left",
	(str(minecraftEnum.KeyBoardType.KEY_A), "0"): "tCancel",
	(str(minecraftEnum.KeyBoardType.KEY_D), "1"): "right",
	(str(minecraftEnum.KeyBoardType.KEY_D), "0"): "tCancel",
}
# 非乘骑时的按键映射
UnRideKeyboardMappings = {
	# 上车
	(str(minecraftEnum.KeyBoardType.KEY_F), "0"): "geton",
}


class BaseCar(Singleton, CommonEventRegister):
	"""
	基地车 客户端，单例
	以玩家为owner逻辑
	"""
	def __init__(self, clientHandler):
		CommonEventRegister.__init__(self, clientHandler)
		self._client = clientHandler
		self._levelId = self._client.mLevelId
		self._playerId = self._client.mPlayerId
		
		# 坐骑id
		self._rideId = None
		# 是否驾驶员
		self._isRider = False
		self._riderArgs = {}
		# 是否显示雇佣兵下车UI，用于UI初始化时
		self._mercenaryUIState = False
		# 上骑时传递的能源数据
		self._rideEnergyDict = None
		# 看向的实体id
		self._lookatEntityId = None

		self._rideRotComp = None
		self._ridePosComp = None

		# 上骑时初始的镜头偏移
		self._cameraOffset = None
		# 上骑时，人称视角模式
		self._perspective = None

		# 载具上一帧的角度
		self._lastRot = None
		# 相机角度和载具角度的差值
		self._rotDiff = 0

		# 计算时速timer
		self._speedTimer = None
		# tick的cd
		self._speedTimerCD = 0.5
		# 换算km/h需乘的参数
		self._speedToKmhParam = 3.6 * (1 / self._speedTimerCD)
		self._ridePos = None

		# 当前移动方向
		self._currentMoveVector = None

		# 维修timer
		self._repairTimer = None
		self._repairEntityId = None

		# 瘫痪数据
		self._inhibitDict = {}

		self._cameraComp = compFactory.CreateCamera(self._levelId)
		self._posComp = compFactory.CreatePos(self._playerId)
		self._motionComp = compFactory.CreateActorMotion(self._playerId)
		self._viewComp = compFactory.CreatePlayerView(self._playerId)

		# 订阅事件回调函数
		self._carSubscribeFunctions = {
			# 发消息到服务端类型
			"up": self.SendCtrlToServer,
			"cut": self.SendCtrlToServer,
			"cancel": self.SendCtrlToServer,
			"left": self.SendCtrlToServer,
			"right": self.SendCtrlToServer,
			"tCancel": self.SendCtrlToServer,
			"getoff": self.SendCtrlToServer,
			# 上车
			"geton": self.SendCtrlToServerToEntity,
			# 加能源，需发消息到服务端获取能源值
			"energy_ui": self.SendCtrlToServerToEntity,
			# 显示修复UI
			"open_broken_car": self.ShowBrokenCarUI,
			# 雇佣兵下车
			"getoff_mercenary": self.SendCtrlToServer,
		}
		# 注册订阅
		Instance.mEventMgr.RegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		
		# 服务端消息回调
		self._carCtrlFunctions = {
			"up": self.SetMoveVector,
			"cut": self.SetMoveVector,
			# 更新能源值
			"energy": self.UpdateEnergy,
			# 打开加能源UI
			"energy_ui": self.ShowAddEnergyUI,
			# 更新加能源UI
			"update_mat": self.TranspondSubscriptToUI,
			# 上骑
			"startRiding": self.StartRiding,
			# 修理
			"repair": self.UpdateRepairUI,
			# 雇佣兵上下车
			"mercenary": self.ShowMercenaryUI,

			# 打开改造UI
			"open_remold": self.ShowRemoldUI,
			# 更新改造UI
			"update_remold": self.TranspondSubscriptToUI,

			# 瘫痪表现
			"inhibit": self.SetInhibitEffects,
		}

        # 运行平台是否是电脑
		self._isWin = True if clientApi.GetPlatform() == 0 else False
        # 如果当前是电脑，才监听键盘按键事件
		if self._isWin:
			self._client.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnKeyPressInGame", self, self.OnKeyPressInGameEvent)
		
		# 技能对象
		self._skillsObj = BaseCarSkillClient(self._client, self)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		Instance.mEventMgr.UnRegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		if self._isWin:
			self._client.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnKeyPressInGame", self, self.OnKeyPressInGameEvent)
		self._client = None
		if self._speedTimer:
			engineApiGac.CancelTimer(self._speedTimer)
			self._speedTimer = None
		if self._repairTimer:
			engineApiGac.CancelTimer(self._repairTimer)
			self._repairTimer = None
		self._skillsObj.Destroy()
		# 清除对象自己
		del self
		pass

	# region 事件
	@EngineEvent()
	def UiInitFinished(self, args=None):
		# 如果当前是驾驶状态，则再设置一遍UI（需延迟）
		if self._rideId:
			def initUI():
				self.TranspondSubscriptToUI(self._riderArgs)
				if self._isRider:
					self.UpdateEnergy(self._rideEnergyDict)
					self.UpdateDurability()
					if self._mercenaryUIState:
						self.ShowMercenaryUI({"stage": "mercenary", "state": True})
			engineApiGac.AddTimer(0.1, initUI)
		pass

	@EngineEvent()
	def OnKeyPressInGameEvent(self, args):
		screenName = args.get("screenName")
		key = args.get("key")
		isDown = args.get("isDown")
		# 如果是电脑版、处于主界面、乘骑、驾驶员
		if self._isWin and screenName == "hud_screen":
			if self._rideId and self._isRider:
				stage = RideKeyboardMappings.get((key, isDown))
				if stage:
					self.CarSubscribeEvent({"stage": stage})
			elif self._lookatEntityId:
				stage = UnRideKeyboardMappings.get((key, isDown))
				if stage:
					self.CarSubscribeEvent({"stage": stage})
		pass

	@EngineEvent()
	def HealthChangeClientEvent(self, args):
		"""血量改变事件"""
		entityId = args.get("entityId")
		if entityId == self._rideId:
			# 伤害改变
			toHealth = args.get("to")
			self.UpdateDurability(toHealth)
		pass

	@EngineEvent()
	def ApproachEntityClientEvent(self, args):
		"""靠近实体事件"""
		playerId = args.get("playerId")
		entityId = args.get("entityId")
		if playerId == self._playerId:
			# 如果看向的是载具，则显示UI
			engineTypeStr = self._client.GetEngineTypeStr(entityId)
			if engineTypeStr == carConfig.CarEngineTypeStr:
				# 显示看向的UI
				self.TranspondSubscriptToUI({"stage": "lookat", "state": True, "entityId": entityId})
				self._lookatEntityId = entityId
			else:
				# 如果不是，则关闭UI
				self.TranspondSubscriptToUI({"stage": "lookat", "state": False})
				self._lookatEntityId = None

			# 损坏的载具
			if engineTypeStr == carConfig.BrokenCarEngineTypeStr:
				self.TranspondSubscriptToUI({"stage": "broken_car", "state": True, "entityId": entityId})
			else:
				self.TranspondSubscriptToUI({"stage": "broken_car", "state": False})
		pass

	@EngineEvent()
	def LeaveEntityClientEvent(self, args):
		"""远离实体事件"""
		playerId = args.get("playerId")
		if playerId == self._playerId:
			# 关闭看向的UI
			self.TranspondSubscriptToUI({"stage": "lookat", "state": False})
			self.TranspondSubscriptToUI({"stage": "broken_car", "state": False})
			self._lookatEntityId = None
		pass

	@EngineEvent()
	def StartUsingItemClientEvent(self, args):
		"""开始使用物品事件"""
		playerId = args.get("playerId")
		itemDict = args.get("itemDict")
		if playerId == self._playerId and itemDict:
			itemName = itemDict.get("newItemName")
			self.SetRepairState(True, itemName)
		pass
	
	@EngineEvent()
	def StopUsingItemClientEvent(self, args):
		"""停止使用物品事件"""
		playerId = args.get("playerId")
		itemDict = args.get("itemDict")
		if playerId == self._playerId and itemDict:
			self.SetRepairState(False)
		pass

	@EngineEvent()
	def AddPlayerCreatedClientEvent(self, args):
		"""玩家进入视野范围后事件"""
		playerId = args.get("playerId")
		self.SetBuildInHandAnim(playerId)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.CarServerSystem)
	def CarCtrlEvent(self, args):
		"""载具控制事件"""
		stage = args.get("stage")
		func = self._carCtrlFunctions.get(stage)
		if func:
			func(args)
		pass
	
	def CarSubscribeEvent(self, args):
		"""订阅事件"""
		toServer = args.pop("to_server", None)
		if toServer is True:
			# 数据转发到服务端
			self.SendMsgToServer(eventConfig.CarCtrlEvent, args)
		else:
			stage = args.get("stage")
			func = self._carSubscribeFunctions.get(stage)
			if func:
				func(args)
		pass
	# endregion
	
	# region 功能
	def StartRiding(self, args):
		"""设置乘骑"""
		self._rideId = args.get("rideId")
		self._isRider = args.get("isRider", False)
		self._rideRotComp = compFactory.CreateRot(self._rideId)
		# 拉远镜头
		if self._cameraOffset is None:
			cameraOffset = carConfig.BaseCarConfig.get("cameraOffset")
			if cameraOffset:
				self._cameraOffset = self._cameraComp.GetCameraOffset()
				self._cameraComp.SetCameraOffset(cameraOffset)
		# 隐藏原版UI
		self.HideOriginUI(True)
		# 分离相机
		self._cameraComp.DepartCamera()
		# 3.2接口BUG：DepartCamera后无法拖动视野；改为分离后设置相机角度为载具角度相同
		rot = engineApiGac.GetRot(self._rideId)
		engineApiGac.AddTimer(0.01, self._cameraComp.SetCameraRotation, (30, -rot[1] - 20, 0))
		# 切换到第三人称
		perspective = self._viewComp.GetPerspective()
		if perspective != 1:
			self._perspective = perspective
			self._viewComp.SetPerspective(1)
		
		# 显示UI
		self._riderArgs = args
		self._riderArgs["stage"] = "show"
		self._riderArgs["state"] = True
		self.TranspondSubscriptToUI(self._riderArgs)
		# 如果是驾驶员
		if self._isRider:
			# 如果是驾驶员，更新能源
			self.UpdateEnergy(args)
			# 锁定输入
			self.LockInputVector(VectorEnum.Up)
			# 更新耐久
			self.UpdateDurability()
			# 启动timer
			self._ridePosComp = compFactory.CreatePos(self._rideId)
			if self._speedTimer is None:
				self._speedTimer = engineApiGac.AddRepeatedTimer(self._speedTimerCD, self.UpdateSpeedTimer)

			# 监听渲染tick
			Instance.mEventMgr.RegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameRenderTick)
		pass

	def StopRiding(self):
		"""停止乘骑/下骑"""
		self._rideId = None
		self._isRider = False
		self._rideRotComp = None
		self._ridePosComp = None
		self._motionComp.UnlockInputVector()
		self._rotDiff = 0
		# 恢复镜头
		if self._cameraOffset:
			self._cameraComp.SetCameraOffset(self._cameraOffset)
			self._cameraOffset = None
			self._cameraComp.SetCameraRotation((0, 0, 0))
		self.HideOriginUI(False)
		self._cameraComp.UnDepartCamera()
		# 恢复人称视角
		if self._perspective is not None:
			self._viewComp.SetPerspective(self._perspective)
			self._perspective = None

		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, {"stage": "show", "state": False})
		# 取消timer
		if self._speedTimer:
			engineApiGac.CancelTimer(self._speedTimer)
			self._speedTimer = None
		# 取消监听
		Instance.mEventMgr.UnRegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameRenderTick)
		pass

	def SendCtrlToServer(self, args):
		"""发送控制消息到服务端"""
		# 发消息到服务端，由服务端执行逻辑
		info = {
			"stage": args.get("stage"),
		}
		self.SendMsgToServer(eventConfig.CarCtrlEvent, info)
		pass

	def SendCtrlToServerByArgs(self, args):
		"""发送控制消息到服务端，消息转发"""
		# 发消息到服务端，由服务端执行逻辑
		self.SendMsgToServer(eventConfig.CarCtrlEvent, args)
		pass

	def SendCtrlToServerToEntity(self, args):
		"""发送上车、加能源 消息到服务端"""
		# 发消息到服务端，由服务端执行逻辑
		info = {
			"stage": args.get("stage"),
			"entityId": args.get("entityId", self._lookatEntityId),
		}
		self.SendMsgToServer(eventConfig.CarCtrlEvent, info)
		pass

	def SetMoveVector(self, args):
		"""设置移动向量"""
		stage = args.get("stage")
		if stage == "up":
			# 加速
			self.LockInputVector(VectorEnum.Up)
		elif stage == "cut":
			# 刹车/倒退
			self.LockInputVector(VectorEnum.Cut)
		pass

	def OnGameRenderTick(self, args=None):
		"""渲染tick事件"""
		# 如果载具角度有转变，则同时转变镜头角度
		rot = self._rideRotComp.GetRot()
		if self._lastRot:
			self._rotDiff += commonApiMgr.GetRotBy180(rot[1] - self._lastRot[1])
			self._rotDiff = commonApiMgr.GetRotBy180(self._rotDiff)
		if abs(self._rotDiff) > 1:
			num = carConfig.BaseCarConfig["cameraFollowSpeed"]
			# 如果是倒退，则转速再降低
			if self._currentMoveVector is VectorEnum.Cut:
				num *= 0.35
			num = num if self._rotDiff > 0 else - num
			# print("______________ OnGameRenderTick", num, self._rotDiff, abs(self._rotDiff))
			crot = self._cameraComp.GetCameraRotation()
			# 受伤时，rotation是会改变的，而如果在受伤的同时修改，就会导致镜头角度恢复不回去
			# self._cameraComp.SetCameraRotation((crot[0], crot[1] + num, crot[2]))
			self._cameraComp.SetCameraRotation((crot[0], crot[1] + num, 0))
			self._rotDiff -= num
		self._lastRot = rot
		pass

	def UpdateSpeedTimer(self):
		"""计算时速"""
		pos = self._ridePosComp.GetPos()
		speed = 0
		if self._ridePos and self._ridePos != pos:
			# 计算速度
			speed = commonApiMgr.GetDistanceXZ(self._ridePos, pos)
			# print("___________ client car speed", speed, speed * self._speedToKmhParam)
			# 换算为千格/时: 该timer每*秒执行一次，m/s换算km/h需乘3.6
			speed = speed * self._speedToKmhParam
		self._ridePos = pos
		# 更新UI
		info = {
			"stage": "speed",
			"value": speed,
			"cut": self._currentMoveVector is VectorEnum.Cut,
		}
		self.TranspondSubscriptToUI(info)
		pass
	# endregion

	
	# region 瘫痪
	def SetInhibitEffects(self, args):
		"""设置瘫痪状态"""
		state = args["state"]
		entityId = args["entityId"]
		if state:
			# 播放特效
			if entityId not in self._inhibitDict:
				parId = clientApiMgr.CreateMicroParticleBindEntity(carConfig.InhibitParticle, entityId)
				self._inhibitDict[entityId] = parId
				# 如果玩家当前是乘骑该车，则显示UI的表现
		else:
			parId = self._inhibitDict.pop(entityId, None)
			if parId:
				# 清除特效
				clientApiMgr.RemoveMicroParticle(parId)
				# 恢复UI
		pass
	# endregion

	
	# region UI相关
	def UpdateDurability(self, health=None):
		"""更新耐久度"""
		# 耐久即血量
		attrComp = compFactory.CreateAttr(self._rideId)
		if health is None:
			health = attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
		maxHealth = attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
		if health and maxHealth:
			# 锁血1
			health -= 1.0
			ratio = health / (maxHealth - 1.0)
			self.TranspondSubscriptToUI({"stage": "durability", "value": ratio, "durability": health})
		pass

	def UpdateEnergy(self, args):
		"""更新能源UI"""
		energy = args.get("energy")
		maxEnergy = args.get("maxEnergy")
		self._rideEnergyDict = args
		# 数据合理性校验
		if maxEnergy and maxEnergy > 0:
			ratio = energy / (maxEnergy + 0.0)
			self.TranspondSubscriptToUI({"stage": "energy", "value": ratio, "energy": energy})
		pass

	def ShowAddEnergyUI(self, args=None):
		"""显示加能量的界面"""
		# 如果当前是在主界面
		if clientApiMgr.IsScreenUI():
			# 获取玩家背包物品
			materials = self.GetPlayerEnergyMaterials()
			# 显示UI
			createParams = {
				"materials": materials,
				"entityId": args.get("entityId"),
				"energy": args.get("energy"),
				"maxEnergy": args.get("maxEnergy"),
			}
			Instance.mUIManager.PushUI(UIDef.UI_CarAddEnergy, createParams)
		pass

	def GetPlayerEnergyMaterials(self):
		"""获取玩家能源材料列表"""
		itemListDict = clientApiMgr.GetPlayerInventoryItemList(self._playerId)
		materials = {}
		if itemListDict:
			for item in itemListDict:
				if item:
					addNum = carConfig.GetAddEnergyMaterialNum(item.get("newItemName"))
					if addNum:
						key = (item.get("newItemName"), item.get("newAuxValue"))
						val = materials.get(key)
						if val is None:
							val = {"count": 0,}
							materials[key] = val
						materials[key]["count"] += item.get("count", 1)
		return materials
	
	def SetRepairState(self, state, itemName=None):
		"""设置维修功能的开启、关闭"""
		if state:
			# 校验物品
			repairCfg = carConfig.RepairConfig
			if itemName == repairCfg.get("itemName"):
				if self._repairTimer is None:
					self._repairTimer = engineApiGac.AddRepeatedTimer(repairCfg.get("repairCD", 1), self.RepairTimer)
				# 设置粒子效果显示
				compFactory.CreateQueryVariable(self._playerId).Set(QueryEnum.UseItem,1)
				# 先执行一遍维修
				self.RepairTimer()
		else:
			if self._repairTimer:
				engineApiGac.CancelTimer(self._repairTimer)
				self._repairTimer = None
				# 设置粒子效果取消
				compFactory.CreateQueryVariable(self._playerId).Set(QueryEnum.UseItem,0)
				# 停止维修，扣物品耐久
				info = {
					"stage": "stop_repair",
					"entityId": self._repairEntityId,
				}
				self.SendMsgToServer(eventConfig.CarCtrlEvent, info)
				self._repairEntityId = None
		pass

	def RepairTimer(self):
		"""维修功能的timer"""
		# 获取准星对准的实体，如果是载具、且有损耗耐久
		pickData = self._cameraComp.PickFacing()
		if pickData and pickData.get("type") == "Entity":
			entityId = pickData.get("entityId")
			engineComp = compFactory.CreateEngineType(entityId)
			if engineComp.GetEngineTypeStr() == carConfig.CarEngineTypeStr:
				attrComp = compFactory.CreateAttr(entityId)
				health = attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
				maxHealth = attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
				if health < maxHealth:
					hitPos = (pickData.get("hitPosX"), pickData.get("hitPosY"), pickData.get("hitPosZ"))
					pos = self._posComp.GetPos()
					dist = commonApiMgr.GetDistanceSqrt(pos, hitPos)
					if dist <= 49:
						self._repairEntityId = entityId
						# 发消息到服务端，进行维修
						info = {
							"stage": "repair",
							"entityId": entityId,
						}
						self.SendMsgToServer(eventConfig.CarCtrlEvent, info)
		pass

	def UpdateRepairUI(self, args=None):
		"""更新维修界面"""
		repairCfg = carConfig.RepairConfig
		args["delayCloseTime"] = repairCfg.get("repairCD", 1) + 1
		self.TranspondSubscriptToUI(args)
		pass

	def ShowBrokenCarUI(self, args=None):
		"""显示/隐藏损坏载具修复UI"""
		# 如果当前是在主界面
		if clientApiMgr.IsScreenUI():
			createParams = {
				"entityId": args.get("entityId"),
			}
			Instance.mUIManager.PushUI(UIDef.UI_CarRepair, createParams)
		pass

	def ShowMercenaryUI(self, args=None):
		"""显示/隐藏雇佣兵上下车UI"""
		self._mercenaryUIState = args.get("state", False)
		self.TranspondSubscriptToUI(args)
		pass
	# endregion

	# region 改造相关
	def ShowRemoldUI(self, args):
		"""显示/隐藏改造UI"""
		if clientApiMgr.IsScreenUI():
			Instance.mUIManager.PushUI(UIDef.UI_CarRemold, args)
		pass
	# endregion

	# region 通用消息转发
	def TranspondSubscriptToUI(self, args):
		"""直接转发订阅消息给UI"""
		Instance.mEventMgr.NotifyEvent(eventConfig.CarSubscribeEvent, args)
		pass
	# endregion

	# region 动画
	def SetBuildInHandAnim(self, playerId):
		"""设置建造手持动画"""
		cfg = carConfig.AddAnimations
		# 添加动画
		renderComp = compFactory.CreateActorRender(playerId)
		renderComp.AddPlayerAnimation(cfg["animKey"], cfg["animName"])
		renderComp.AddPlayerScriptAnimate(cfg["animKey"], cfg["condition"])
		renderComp.RebuildPlayerRender()
		pass
	# endregion

	# region 属性、方法
	def GetRideId(self):
		return self._rideId
	
	def HideOriginUI(self, state):
		"""隐藏原版UI"""
		clientApi.HideHorseHealthGui(state)
		clientApi.HideMoveGui(state)
		clientApi.HideSneakGui(state)
		clientApi.HideJumpGui(state)
		pass

	def LockInputVector(self, vector):
		"""锁定输入向量"""
		self._motionComp.LockInputVector(vector)
		self._currentMoveVector = vector
		pass
	
	# endregion
