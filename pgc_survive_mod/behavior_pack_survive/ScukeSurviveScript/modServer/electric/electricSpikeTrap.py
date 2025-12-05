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
getColor = serverApi.GenerateColor
entityTypeEnum = serverApi.GetMinecraftEnum().EntityType
LVID = serverApi.GetLevelId()

class ElectricSpikeTrap(ElectricBase):
	"""地刺逻辑"""
	def __init__(self, severHandler, blockName, pos, dimension, param={}):
		super(ElectricSpikeTrap, self).__init__(severHandler, blockName, pos, dimension, param)

		self._eventFunctions = {
			"dynamo_work": self.SetDynamoWorkState,
		}
		
		# 功率
		self._kw = self.mCfg.get("kw", 0)
		# 可用的发电机的key
		self._useDynamoKey = None
		# 地刺攻击的CD
		self._hurtCD = self.mCfg.get("hurt_cd", 0.5)
		self._hurtCDTimer = None
		# 地刺攻击造成的伤害
		self._hurtDamage = self.mCfg.get("hurt_damage",0)
		#地刺攻击是否击退
		self._hurtKnocked = self.mCfg.get("hurt_knocked",False)

		self._animeTimer = None

		Instance.mEventMgr.RegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		pass

	def Destroy(self, breaks=False):
		Instance.mEventMgr.UnRegisterEvent(eventConfig.ElectricLogicSubscriptEvent, self.ElectricLogicSubscriptEvent)
		# 解除占用
		self.SetUseKw(False)
		#清除计时器
		if self._hurtCDTimer:
			compFactory.CreateGame(LVID).CancelTimer(self._hurtCDTimer)
			self.setCdTimerState()
		super(ElectricSpikeTrap, self).Destroy(breaks)
		pass

	# region 事件
	@EngineEvent()
	def StepOnBlockServerEvent(self, args):
		"""实体移动到实心方块事件"""
		if self._hurtCDTimer == None:
			#判断是否处于cd中
			entityId = args.get("entityId")
			blockName = args.get("blockName")
			if blockName == self.mBlockName:
				dimension = args.get("dimensionId")
				pos = (args.get("blockX"), args.get("blockY"), args.get("blockZ"))
				if dimension == self.mDimension and pos == self.mPos:
					# 有实体踩到方块
					# 判断是否链接到发电机
					if self._useDynamoKey:
						useDynamoKey = True
					else:
						useDynamoKey = self.GetCanUseDynamo()
					if useDynamoKey == True:
						typeFamily = compFactory.CreateAttr(entityId).GetTypeFamily()
						#判断生物类型是否是怪物
						if typeFamily:
							if 'monster' in typeFamily:
								attrComp = compFactory.CreateAttr(entityId)
								health = attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
								if health > 0:
									# 判断实体是否有血量，如果有，就造成伤害
									compFactory.CreateHurt(entityId).Hurt(self._hurtDamage, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, entityId , None, self._hurtKnocked,None)
									# 播放动画
									self.animeState(1)
									# 消耗电力，根据自己的功率+合成时间
									electricInfo = {
										"stage": "deduct_energy",
										"kw": self._kw,
										"time": self.mCfg.get("time", 1),
										"dynamoKey": self._useDynamoKey,
									}
									Instance.mEventMgr.NotifyEvent(eventConfig.ElectricLogicSubscriptEvent, electricInfo)
									self._hurtCDTimer = compFactory.CreateGame(LVID).AddTimer(0.3,self.setCdTimerState)
					else:
						#没有链接到发电机时候玩家踩踏提示
						if compFactory.CreateEngineType(entityId).GetEngineType() == entityTypeEnum.Player:
							compFactory.CreateGame(entityId).SetOneTipMessage(entityId, serverApi.GenerateColor("RED") + "请提供电力")
			pass

	@EngineEvent()
	def StepOffBlockServerEvent(self, args):
		"""实体离开实心方块事件"""
		blockName = args.get("blockName")
		if blockName == self.mBlockName:
			dimension = args.get("dimensionId")
			pos = (args.get("blockX"), args.get("blockY"), args.get("blockZ"))
			if dimension == self.mDimension and pos == self.mPos:
				self.animeState(0)
	
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
			self.GetCanUseDynamo()
		pass

	def animeState(self,workingStateValue):
		"""动画状态控制"""
		info = {
				"stage": "set_block",
				"pos": self.mPos,
				"dimension": self.mDimension,
				"molangValue": {molangConfig.VariableEnum.WorkingState: workingStateValue},
			}
		Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
	
	def setCdTimerState(self):
		"""设置内置cd timer为空"""
		self._hurtCDTimer = None
	# endregion

