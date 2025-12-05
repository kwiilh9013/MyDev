# -*- coding: UTF-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.singleton import Singleton
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetPartSkillConfig, PartEnum
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


class BaseCarSkillClient(Singleton, CommonEventRegister):
	"""
	基地车 技能客户端，单例
	以玩家为owner逻辑
	"""
	def __init__(self, clientHandler, carObj):
		CommonEventRegister.__init__(self, clientHandler)
		self._client = clientHandler
		self._levelId = self._client.mLevelId
		self._playerId = self._client.mPlayerId
		self._carObj = carObj
		

		# 导弹timer
		self._missileGetBonePosTimer = None
		# 锁定特效
		self._missileLockEffects = []

		# 飞行音效，用于停止: {entityId: soundId}
		self._flySoundDict = {}

		# 注册订阅
		Instance.mEventMgr.RegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		
		# 技能处理方法回调
		self._skillFunctions = {
			PartEnum.Missile: self.TryPlayMissile,
			PartEnum.Fly: self.TrySetFlyState,
		}
		# 订阅
		self._carSubscribeFunctions = {
			"playSkill": self.SetPlaySkills,
			"flyUpDown": self.SetFlyUpDownFromBtn,
		}
		# 服务端消息回调
		self._carCtrlFunctions = {
			"missile_lock": self.AddMissileLockEffect,
			"cds": self.SetSkillCDs,
			"flyState": self.SetFlyStateUI,
			"fly_sound": self.PlayFlySounds,
		}

        # # 运行平台是否是电脑
		# self._isWin = True if clientApi.GetPlatform() == 0 else False
        # # 如果当前是电脑，才监听键盘按键事件
		# if self._isWin:
		# 	self._client.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnKeyPressInGame", self, self.OnKeyPressInGameEvent)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		Instance.mEventMgr.UnRegisterEvent(eventConfig.CarSubscribeEvent, self.CarSubscribeEvent)
		# if self._isWin:
		# 	self._client.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnKeyPressInGame", self, self.OnKeyPressInGameEvent)
		self._client = None
		# 清除对象自己
		del self
		pass

	# region 事件
	# @EngineEvent()
	# def OnKeyPressInGameEvent(self, args):
	# 	screenName = args.get("screenName")
	# 	key = args.get("key")
	# 	isDown = args.get("isDown")
	# 	# 如果是电脑版、处于主界面、乘骑、驾驶员
	# 	if self._isWin and screenName == "hud_screen":
	# 	pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.CarServerSystem)
	def CarSkillsEvent(self, args):
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
	
	# region 技能入口
	def SetPlaySkills(self, args):
		"""设置释放技能"""
		partId = args.get("partId")
		func = self._skillFunctions.get(partId)
		if func:
			func(args)
		pass

	def SetSkillCDs(self, args):
		"""设置技能cd"""
		self._carObj.TranspondSubscriptToUI(args)
		pass
	# endregion

	# region 导弹
	def TryPlayMissile(self, args):
		"""尝试释放导弹"""
		skillStage = args.get("skillStage", "up")
		if skillStage == "up":
			# 松开
			# 停止获取目标
			info = {
				"stage": "missile_pre",
				"entityId": self.GetCarId(),
			}
			self.SendMsgToServer(eventConfig.CarSkillsEvent, info)
			# 延迟清除特效
			engineApiGac.AddTimer(1, self.ClearMissileLockEffect)
			# 获取导弹发射位置
			if not self._missileGetBonePosTimer:
				skillCfg = GetPartSkillConfig(PartEnum.Missile)
				bloneNames = skillCfg.get("boneNames", [])
				info = {"count": 0, "maxCount": len(bloneNames), "boneNames": bloneNames}
				self._missileGetBonePosTimer = engineApiGac.AddRepeatedTimer(0.6, self.GetShootMissilePosTimer, info)
			pass
		elif skillStage == "down":
			# 按下。服务端开始锁定怪物（因客户端无法使用is_family筛选，只能到服务端去做）
			info = {
				"stage": "missile_lock",
				"entityId": self.GetCarId(),
			}
			self.SendMsgToServer(eventConfig.CarSkillsEvent, info)
		pass

	def GetShootMissilePosTimer(self, args):
		"""获取发射导弹位置timer"""
		if args.get("count", 0) < args.get("maxCount", 0):
			# 每隔一段时间，获取模型骨骼的位置，发送到服务端，由服务端生成抛射物
			carId = self.GetCarId()
			# 骨骼位置
			boneName = args["boneNames"][args["count"]]
			modelComp = compFactory.CreateModel(carId)
			try:
				# 这是3.0的API
				pos = modelComp.GetBonePositionFromMinecraftObject(boneName)
			except Exception as e:
				# 无法获取位置
				pos = None
			if pos is None:
				# 根据config获取大概的偏移
				skillCfg = GetPartSkillConfig(PartEnum.Missile)
				boneOffsets = skillCfg.get("boneOffsets", [])
				boneOffset = boneOffsets[args["count"]]
				epos = engineApiGac.GetEntityPos(carId)
				erot = engineApiGac.GetRot(carId)
				pos = commonApiMgr.GetNextPosByRot(epos, (0, erot[1] + boneOffset[0]), boneOffset[1])
				pos = (pos[0], pos[1] + boneOffset[2], pos[2])

			info = {
				"stage": "missile_pos",
				"entityId": carId,
				"pos": pos,
			}
			self.SendMsgToServer(eventConfig.CarSkillsEvent, info)
			args["count"] += 1
		else:
			engineApiGac.CancelTimer(self._missileGetBonePosTimer)
			self._missileGetBonePosTimer = None
		pass

	def AddMissileLockEffect(self, args):
		"""给目标添加锁定特效"""
		targetId = args.get("entityId")
		skillCfg = GetPartSkillConfig(PartEnum.Missile)
		effectName = skillCfg.get("lockEffect", "")
		if effectName:
			effectId = clientApiMgr.CreateMicroParticleBindEntity(effectName, targetId)
			self._missileLockEffects.append(effectId)
		pass

	def ClearMissileLockEffect(self):
		"""清除锁定目标特效"""
		if self._missileLockEffects:
			for effectId in self._missileLockEffects:
				clientApiMgr.RemoveMicroParticle(effectId)
		self._missileLockTargets = []
		self._missileLockEffects = []
		pass
	# endregion

	# region 飞行
	def TrySetFlyState(self, args):
		"""尝试设置飞行状态"""
		skillStage = args.get("skillStage", "up")
		if skillStage == "up":
			info = {
				"stage": "flyState",
				"entityId": self.GetCarId(),
			}
			self.SendMsgToServer(eventConfig.CarSkillsEvent, info)
		pass

	def SetFlyStateUI(self, args):
		"""设置飞行状态UI"""
		self._carObj.TranspondSubscriptToUI(args)
		pass

	def SetFlyUpDownFromBtn(self, args):
		"""点击飞行上下按钮"""
		# 转发到服务端
		args["entityId"] = self.GetCarId()
		self.SendMsgToServer(eventConfig.CarSkillsEvent, args)
		pass

	def PlayFlySounds(self, args):
		"""播放飞行音效"""
		entityId = args.get("entityId")
		path = args.get("path")
		loop = args.get("loop", False)
		# 停止之前的音效
		soundId = self._flySoundDict.pop(entityId, None)
		if soundId:
			clientApiMgr.StopCustomMusicById(soundId, 2)
		if path:
			# 播放音效
			soundId = clientApiMgr.PlayCustomMusic(path, (0, 0, 0), loop=loop, entityId=entityId)
			if soundId:
				self._flySoundDict[entityId] = soundId
		pass
	# endregion

	# region 属性方法
	def GetCarId(self):
		return self._carObj.GetRideId()
	# endregion
