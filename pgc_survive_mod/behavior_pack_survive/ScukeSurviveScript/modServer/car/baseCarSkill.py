# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetPartSkillConfig, PartEnum
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.molangConfig import QueryEnum
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BaseCarSkill(CommonEventRegister):
	"""基地车 技能 服务端"""
	def __init__(self, severHandler, entityId, carObj):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		# 载具主对象
		self._carObj = carObj
		# 坐骑id
		self._entityId = entityId

		# 技能CD数据: 
		self._skillCDDict = {}

		# 导弹timer
		self._missileTimer = None
		self._missileLockedTimer = None
		# 锁定的目标数据
		self._missileLockTargetList = []
		# 导弹追踪数据
		self._missileToTargetDict = {}
		# 导弹生成队列
		self._missileCreateList = []

		# 飞行状态
		self._flyState = False
		# 上下飞行的timer
		self._flyVectorTimer = None
		self._flyUpDownVector = (0, 0, 0)
		self.ResetVector()
		# 飞行下降过程的标记
		self._flyOnGroundState = False
		# 飞行下降过程的着地检测timer
		self._flyOnGroundTimer = None
		# 飞行的持续时间
		self._flyDurationTimer = None

		self._posComp = compFactory.CreatePos(self._entityId)
		self._rotComp = compFactory.CreateRot(self._entityId)
		self._effectComp = None
		self._motionComp = None

		self._eventFunctions = {
			"missile_lock": self.StartMissileLockedTargets,
			"missile_pre": self.PreShootMissile,
			"missile_pos": self.ShootMissile,
			"flyState": self.SetStartFlyState,
			"flyUpDown": self.SetFlyUpDown,
		}
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self._server = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def OnGroundServerEvent(self, args):
		"""实体着地事件"""
		entityId = args.get("id")
		if entityId == self._entityId:
			self.FlyOnGround()
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.CarClientSystem)
	def CarSkillsEvent(self, args):
		"""载具 技能事件"""
		entityId = args.get("entityId")
		if entityId == self._entityId:
			stage = args.get("stage")
			func = self._eventFunctions.get(stage)
			if func:
				func(args)
		pass
	# endregion

	# region 导弹
	def StartMissileLockedTargets(self, args):
		"""开始锁定目标"""
		# 判断cd
		if self.GetSkillCD(PartEnum.Missile) <= 0 and self._carObj.GetCurrentEnergy() > 0:
			playerId = args.get("__id__")
			if not self._missileLockedTimer:
				self._missileLockTargetList = []
				skillCfg = GetPartSkillConfig(PartEnum.Missile)
				self._missileLockedTimer = engineApiGas.AddRepeatTimer(skillCfg.get("lockFrequency", 0.5), self.MissileLockedTargetTimer, playerId, skillCfg)
			# 播放预备动画
			info = {
				"entityId": self._entityId,
				"stage": "set_entity",
				"molangValue": {QueryEnum.MissileShootNum: 0.5},
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass

	def MissileLockedTargetTimer(self, playerId, skillCfg):
		"""锁定目标timer"""
		if len(self._missileLockTargetList) < skillCfg.get("maxCount", 6):
			# 获取附近的怪物
			filters = {
				"any_of": [
					{ "test": "is_family", "subject": "other", "value": "monster" },
				]
			}
			entityList = engineApiGas.GetEntitiesAround(self._entityId, skillCfg.get("radius", 16), filters)
			# print("___________ entityList", entityList)
			# 筛选出在前方区域的目标
			pos = self._posComp.GetPos()
			rot = self._rotComp.GetRot()
			rotVector = serverApi.GetDirFromRot(rot)
			viewRot = skillCfg.get("viewRot", 45)
			for entityId in entityList:
				if entityId not in self._missileLockTargetList:
					epos = engineApiGas.GetEntityPos(entityId)
					if commonApiMgr.IsCanSee(pos, epos, rotVector, viewRot):
						# 记录
						self._missileLockTargetList.append(entityId)
						# 客户端显示锁定特效
						info = {
							"stage": "missile_lock",
							"entityId": entityId,
						}
						self.SendMsgToClient(playerId, eventConfig.CarSkillsEvent, info)
						break
		pass

	def PreShootMissile(self, args):
		"""停止锁定目标，准备发射"""
		skillId = PartEnum.Missile
		if self._missileLockedTimer:
			engineApiGas.CancelTimer(self._missileLockedTimer)
			self._missileLockedTimer = None
		# 处理锁定数据
		if not self._missileLockTargetList:
			self._missileLockTargetList = [None]
		# 记录数据，封装导弹追踪的目标（如果目标数量少于导弹数量，则多个导弹追踪同一个目标
		skillCfg = GetPartSkillConfig(skillId)
		targetLen = len(self._missileLockTargetList)
		for i in xrange(skillCfg.get("maxCount", 6)):
			target = self._missileLockTargetList[i % targetLen]
			self._missileCreateList.append(target)
		self._missileLockTargetList = []
		# 进入技能cd，消耗资源
		cd = self.SetSkillCD(skillId, skillCfg)
		# 同步cd到客户端
		playerId = args.get("__id__")
		info = {
			"stage": "cds",
			"cds": {skillId: cd},
		}
		self.SendMsgToClient(playerId, eventConfig.CarSkillsEvent, info)
		pass

	def ShootMissile(self, args):
		"""发射导弹"""
		pos = args.get("pos")
		if pos:
			# 发射导弹
			if self._missileCreateList:
				skillCfg = GetPartSkillConfig(PartEnum.Missile)
				target = self._missileCreateList.pop(0)
				maxCount = len(skillCfg["boneNames"])
				index = maxCount - len(self._missileCreateList)
				# 生成抛射物
				projectile = skillCfg.get("projectile")
				if projectile:
					# 往天上发射
					rot = engineApiGas.GetEntityRot(self._entityId)
					rot = (-70, rot[1])
					power = skillCfg.get("power")
					proId = serverApiMgr.SpawnProjectile(self._carObj.GetRider(), projectile, pos, rot, power=power)
					# 如果有追踪目标，才记录数据
					if proId:
						self._missileToTargetDict[proId] = {"time": time.time(), "target": target}
						# 启动timer，设置导弹追踪功能
						if not self._missileTimer:
							self._missileTimer = engineApiGas.AddRepeatTimer(0.3, self.MissileToTargetTimer)
					# 播放动画
					info = {
						"entityId": self._entityId,
						"stage": "set_entity",
						"molangValue": {QueryEnum.MissileShootNum: index},
					}
					Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
					if maxCount == index:
						# 延迟重置动画
						info = {
							"entityId": self._entityId,
							"stage": "set_entity",
							"molangValue": {QueryEnum.MissileShootNum: 0},
						}
						engineApiGas.AddTimer(0.7, Instance.mEventMgr.NotifyEvent, eventConfig.MolangUpdateEvent, info)
		pass
	
	def MissileToTargetTimer(self):
		"""导弹跟踪timer"""
		# 导弹追踪
		if self._missileToTargetDict:
			t = None
			# 根据目标位置， 重新计算抛射物角度
			for proId, targetVal in self._missileToTargetDict.items():
				# 前面一段时间，不会追踪
				if targetVal.get("time") is not None:
					if t is None:
						t = time.time()
					if t - targetVal["time"] < 1.0:
						continue
				target = targetVal.get("target")
				if target is None:
					# 往前发射，只需要改一次
					rot = engineApiGas.GetEntityRot(self._entityId)
					rot = (40, rot[1])
					rotVector = serverApi.GetDirFromRot(rot)
					motionComp = compFactory.CreateActorMotion(proId)
					motionComp.SetMotion(rotVector)
					self._missileToTargetDict.pop(proId, None)
					continue
				else:
					# 追踪目标
					pos = engineApiGas.GetEntityPos(proId)
					tpos = engineApiGas.GetEntityPos(target)
					if pos is None or tpos is None:
						self._missileToTargetDict.pop(proId, None)
						continue
					tsize = engineApiGas.GetEntitySize(target)
					if tsize is None:
						self._missileToTargetDict.pop(proId, None)
						continue
					tpos = (tpos[0], tpos[1] + tsize[1] * 0.5, tpos[2])
					# 修改抛射物方向
					rotVector = commonApiMgr.GetVector(pos, tpos)
					rotVector = commonApiMgr.VectorNormalize(rotVector)
					motionComp = compFactory.CreateActorMotion(proId)
					motionComp.SetMotion(rotVector)
		else:
			engineApiGas.CancelTimer(self._missileTimer)
			self._missileTimer = None
		pass

	# endregion

	# region 飞行
	def SetStartFlyState(self, args):
		"""设置飞行状态"""
		playerId = args.get("__id__")
		state = args.get("state")
		lastState = self._flyState
		# 如果没耐久或能源，则无法开启
		if state is False or self._carObj.IsCanSteer() is False or self.GetSkillCD(PartEnum.Fly) > 0:
			self._flyState = False
		else:
			self._flyState = not self._flyState
		if self._flyState:
			# 开启飞行
			skillCfg = GetPartSkillConfig(PartEnum.Fly)
			# 重置技能持续时间
			if self._flyDurationTimer:
				engineApiGas.CancelTimer(self._flyDurationTimer)
			self._flyDurationTimer = engineApiGas.AddTimer(skillCfg.get("duration", 10), self.SetFlyDurationTimer, playerId)
			# 动画
			info = {
				"entityId": self._entityId,
				"stage": "set_entity",
				"molangValue": {QueryEnum.CarFly: 1},
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
			# 延迟启动（和动画对上）
			if self._motionComp is None:
				self._motionComp = compFactory.CreateActorMotion(self._entityId)
			def timer():
				if self.GetFlyState():
					self._flyVectorTimer = engineApiGas.AddRepeatTimer(0.05, self.FlyVectorTimer)
			engineApiGas.AddTimer(0.8, timer)
			# 更新飞行状态，停止倾斜逻辑
			info = {
				"entityId": self._entityId, 
				"flyState": self._flyState, 
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
			self._flyOnGroundState = False
			if self._flyOnGroundTimer:
				engineApiGas.CancelTimer(self._flyOnGroundTimer)
				self._flyOnGroundTimer = None
			# 悬停音效
			if skillCfg.get("hover_sound"):
				info = {
					"stage": "fly_sound",
					"path": skillCfg.get("hover_sound"),
					"entityId": self._entityId,
					"loop": True,
				}
				self.SendMsgToAllClient(eventConfig.CarSkillsEvent, info)
		elif lastState is True:
			# 关闭飞行
			if self._flyDurationTimer:
				engineApiGas.CancelTimer(self._flyDurationTimer)
				self._flyDurationTimer = None
			if self._flyVectorTimer:
				engineApiGas.CancelTimer(self._flyVectorTimer)
				self._flyVectorTimer = None
			# cd
			cd = self.SetSkillCD(PartEnum.Fly)
			playerId = args.get("__id__")
			info = {
				"stage": "cds",
				"cds": {PartEnum.Fly: cd},
			}
			self.SendMsgToClient(playerId, eventConfig.CarSkillsEvent, info)
			# 重置数据
			self.ResetVector()
			# 10秒缓降
			if self._effectComp is None:
				self._effectComp = compFactory.CreateEffect(self._entityId)
			self._effectComp.AddEffectToEntity(minecraftEnum.EffectType.SLOW_FALLING, 30, 0, False)
			# 开启timer，检测着地状态，当着地后，才播放动画
			self._flyOnGroundState = True
			self._flyOnGroundTimer = engineApiGas.AddRepeatTimer(1, self.FlyOnGroundTimer)
		# 修改客户端UI
		if playerId and lastState != self._flyState:
			info = {
				"stage": "flyState",
				"state": self._flyState,
			}
			# 如果是关闭，则另外返回cd
			self.SendMsgToClient(playerId, eventConfig.CarSkillsEvent, info)
		pass

	def SetFlyUpDown(self, args):
		"""设置上下飞行"""
		state = args.get("state")
		if "cancel" in state:
			# 松开按钮，上下的vector重置
			self.ResetVector()
			# 悬停音效
			skillCfg = GetPartSkillConfig(PartEnum.Fly)
			if skillCfg.get("hover_sound"):
				info = {
					"stage": "fly_sound",
					"path": skillCfg.get("hover_sound"),
					"entityId": self._entityId,
					"loop": True,
				}
				self.SendMsgToAllClient(eventConfig.CarSkillsEvent, info)
		else:
			# 按下按钮
			skillCfg = GetPartSkillConfig(PartEnum.Fly)
			self._flyUpDownVector = (0, skillCfg.get("upSpeed", 0.5) if state == "up" else skillCfg.get("udownSpeed", -0.5), 0)
			# 上下飞音效
			if skillCfg.get("updown_sound"):
				info = {
					"stage": "fly_sound",
					"path": skillCfg.get("updown_sound"),
					"entityId": self._entityId,
					"loop": True,
				}
				self.SendMsgToAllClient(eventConfig.CarSkillsEvent, info)
		pass

	def FlyVectorTimer(self):
		"""飞行timer，上下飞行、悬停"""
		self._motionComp.SetMotion(self._flyUpDownVector)
		pass

	def ResetVector(self):
		"""重置飞行vector"""
		self._flyUpDownVector = (0, 0.015, 0)
		pass

	def SetFlyDurationTimer(self, playerId):
		"""飞行持续时间timer"""
		self._flyDurationTimer = None
		# 结束飞行
		self.SetStartFlyState({"__id__": playerId, "state": False})
		pass

	def FlyOnGroundTimer(self):
		"""飞行着地timer"""
		if self._flyOnGroundState:
			# 射线检测底下是否是水、岩浆
			dimension = self._carObj.GetDimension()
			pos = self._posComp.GetFootPos()
			blockList = serverApi.getEntitiesOrBlockFromRay(dimension, pos, (0, -1, 0), 2, False, minecraftEnum.RayFilterType.OnlyBlocks)
			onGround = False
			if blockList:
				for block in blockList:
					if block.get("type") == "Block" and block.get("hitPos"):
						identifier = block.get("identifier", "")
						if "air" not in identifier:
							onGround = True
							break
			if onGround:
				self.FlyOnGround()
		pass

	def FlyOnGround(self):
		"""飞行着地，落地后播放动画"""
		# 如果当前是飞行下降过程，才执行逻辑
		if self._flyOnGroundState:
			self._flyOnGroundState = False
			# 清除缓降
			self._effectComp.RemoveEffectFromEntity(minecraftEnum.EffectType.SLOW_FALLING)
			# 播放动画
			info = {
				"entityId": self._entityId,
				"stage": "set_entity",
				"molangValue": {QueryEnum.CarFly: 0},
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
			# 恢复倾斜逻辑
			info = {
				"entityId": self._entityId, 
				"flyState": self._flyState,
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
			# 停止音效
			info = {
				"stage": "fly_sound",
				"entityId": self._entityId,
			}
			self.SendMsgToAllClient(eventConfig.CarSkillsEvent, info)
			# 停止timer
			if self._flyOnGroundTimer:
				engineApiGas.CancelTimer(self._flyOnGroundTimer)
				self._flyOnGroundTimer = None
		pass

	def GetFlyState(self):
		return self._flyState
	# endregion

	# region 技能cd、消耗
	def GetSkillCD(self, skillId):
		"""获取技能cd"""
		lastT = self._skillCDDict.get(skillId)
		if not lastT:
			return 0
		return max(lastT - time.time(), 0)
	
	def SetSkillCD(self, skillId, skillCfg=None):
		"""设置技能cd"""
		if skillCfg is None:
			skillCfg = GetPartSkillConfig(skillId)
		cd = skillCfg.get("cd", 0)
		if cd:
			self._skillCDDict[skillId] = time.time() + cd
		# 消耗资源
		self.SetSkillConsume(skillId, skillCfg)
		return cd
	
	def SetSkillConsume(self, skillId, skillCfg=None):
		"""设置技能消耗"""
		if skillCfg is None:
			skillCfg = GetPartSkillConfig(skillId)
		energy = skillCfg.get("energy", 0)
		if energy:
			self._carObj.SetConsumeEnergy(energy)
			return True
		return False
	# endregion

