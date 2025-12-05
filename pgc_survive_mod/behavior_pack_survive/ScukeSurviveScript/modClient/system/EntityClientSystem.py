# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon.cfg.entity.entityConfig import IsHealthBarBlackList, GetEntityConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.eventConfig import CameraShakingSubscribeEvent
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.cfg.entity.entityAIConfig import GetAllEntityFogCfg
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


HealthBarFrontColor = (0.8, 0.2, 0.2, 1.0)
HealthBarBackColor = (0.3, 0.3, 0.3, 1.0)


class EntityClientSystem(BaseClientSystem):
	"""
	实体客户端系统
	"""
	def __init__(self, namespace, systemName):
		super(EntityClientSystem, self).__init__(namespace, systemName)

		# 血条显示timer
		self._showHealthTimer = None
		self._setStateTimer = None
		self._lastshowEntityId = None

		# 绑定实体音效的数据，客户端实体会延迟添加，所以需延迟绑定
		self._soundBindEntityDict = {}

		# 雾效
		self._fogEntityDict = {}
		self._showFogLength = 48
		self._fogEntityCfg = GetAllEntityFogCfg()
		self._fogTimer = None

		# 组件
		self._cameraComp = compFactory.CreateCamera(self.mLevelId)
		self._gameComp = compFactory.CreateGame(self.mLevelId)
		self._fogComp = compFactory.CreateFog(self.mLevelId)

		self._eventFunctions = {
			"sound": self.PlaySound,
			"em_effect": self.EMMissileHitEffect,
			"molang": self.SetMolangs,
			"particle": self.PlayParticles,
		}
		# 注册订阅
		# Instance.mEventMgr.RegisterEvent(eventConfig.GameTickSubscribeEvent, self.GameTickSubscribeEvent)
		pass

	def Destroy(self):
		super(EntityClientSystem, self).Destroy()
		if self._showHealthTimer:
			engineApiGac.CancelTimer(self._showHealthTimer)
			self._showHealthTimer = None
		if self._setStateTimer:
			engineApiGac.CancelTimer(self._setStateTimer)
			self._setStateTimer = None
		# 注销订阅
		# Instance.mEventMgr.UnRegisterEvent(eventConfig.GameTickSubscribeEvent, self.GameTickSubscribeEvent)
		pass

	# region 事件
	@EngineEvent()
	def LoadClientAddonScriptsAfter(self, args=None):
		"""加载客户端脚本完成事件"""
		# 显示血条
		self.StartShowHealth()
		pass

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		"""添加实体事件"""
		entityId = args.get("id")
		# 隐藏血条
		healthComp = compFactory.CreateHealth(entityId)
		healthComp.ShowHealth(False)
		# 绑定音效
		self.AddEntityToBindSounds(entityId)

		self.UpdateFogEntityData(entityId, isAdd=True)
		pass

	@EngineEvent()
	def RemoveEntityClientEvent(self, args):
		eid = args['id']
		self.UpdateFogEntityData(eid, isAdd=False)
		pass

	@EngineEvent()
	def AddPlayerAOIClientEvent(self, args):
		"""添加玩家事件"""
		playerId = args.get("playerId")
		# 隐藏血条
		healthComp = compFactory.CreateHealth(playerId)
		healthComp.ShowHealth(False)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.EntityServerSystem)
	def EntityEffectEvent(self, args):
		"""实体特效事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region 显示血条
	def StartShowHealth(self):
		"""显示血条"""
		# 显示全局血条
		gameComp = compFactory.CreateGame(self.mLevelId)
		gameComp.ShowHealthBar(True)

		# 启动timer
		if not self._showHealthTimer:
			self._showHealthTimer = engineApiGac.AddRepeatedTimer(0.5, self.ShowHealthTimer)
		if not self._setStateTimer:
			self._setStateTimer = engineApiGac.AddRepeatedTimer(15, self.SetShowHealthStateTimer)
		pass

	def ShowHealthTimer(self):
		"""显示血条的timer"""
		isShow = False
		# 获取准星对准的生物
		pickData = self._cameraComp.PickFacing()
		if pickData and pickData.get("type") == "Entity":
			entityId = pickData.get("entityId")
			if entityId == self._lastshowEntityId:
				isShow = True
			else:
				# 如果是黑名单的，则不显示
				engineTypeStr = engineApiGac.GetEngineTypeStr(entityId)
				if IsHealthBarBlackList(engineTypeStr) is False:
					# 如果有血量
					attrComp = compFactory.CreateAttr(entityId)
					maxHealth = attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
					if maxHealth and maxHealth > 0:
						isShow = True
						# 显示血量
						healthComp = compFactory.CreateHealth(entityId)
						healthComp.ShowHealth(True)
						# 改成红色
						healthComp.SetColor(HealthBarFrontColor, HealthBarBackColor)
						# 修改高度
						healthComp.SetHealthBarDeviation(-0.7)

						# 隐藏旧生物的血条
						healthComp = compFactory.CreateHealth(self._lastshowEntityId)
						healthComp.ShowHealth(False)
						self._lastshowEntityId = entityId

		if isShow is False and self._lastshowEntityId:
			# 隐藏旧生物的血条
			healthComp = compFactory.CreateHealth(self._lastshowEntityId)
			healthComp.ShowHealth(False)
			self._lastshowEntityId = None
		pass

	def SetShowHealthStateTimer(self):
		"""设置显示血条状态的timer，兼容狐狸，需每隔段时间设置一次"""
		gameComp = compFactory.CreateGame(self.mLevelId)
		gameComp.ShowHealthBar(True)
		pass

	# endregion

	# region 音效
	def PlaySound(self, args):
		"""播放音效"""
		# 音量大小，通过api修改的有效，在sound_definitions中配置的无效。
		path = args.get("path")
		entityId = args.get("entityId")
		if entityId:
			# 绑定实体
			if args.get("alive") or self._gameComp.IsEntityAlive(entityId):
				clientApiMgr.PlayCustomMusic(path, (0, 0, 0), volume=args.get("volume", 1.0), loop=args.get("loop", False), entityId=entityId)
			else:
				self._soundBindEntityDict[entityId] = args
		else:
			pos = args.get("pos")
			# 定点
			# 直接播放会因为超过16格而播放失败，需改为绑定玩家播放、使用相对位置
			plyPos = engineApiGac.GetEntityPos(self.mPlayerId)
			offset = commonApiMgr.GetVector(plyPos, pos)
			clientApiMgr.PlayCustomMusic(path, offset, volume=args.get("volume", 1.0), loop=args.get("loop", False), entityId=self.mPlayerId)
		pass

	def AddEntityToBindSounds(self, entityId):
		"""添加实体时，绑定实体音效"""
		args = self._soundBindEntityDict.pop(entityId, None)
		if args:
			args["alive"] = True
			self.PlaySound(args)
		pass
	# endregion

	# region molang
	def PlayParticles(self, args):
		"""播放粒子特效"""
		pass
	# endregion

	# region molang
	def SetMolangs(self, args):
		"""设置molang"""
		molangVal = args.get("molang")
		if not molangVal:
			return
		entityId = args["entityId"]
		queryComp = compFactory.CreateQueryVariable(entityId)
		for key, val in molangVal.iteritems():
			queryComp.Set(key, val)
		pass
	# endregion

	# region 特定生物的特效
	def EMMissileHitEffect(self, args):
		"""电磁弹命中特效"""
		pos = args["pos"]
		cfg = GetEntityConfig(ProjectileEnum.EMMissile)
		# 特效
		clientApiMgr.CreateMicroParticle(cfg["hit_particle"], pos, delayTime=3)
		# 音效
		self.PlaySound({"pos": pos, "path": cfg["hit_sound"]})
		# 镜头晃动效果：根据本地玩家离该位置的距离
		ppos = engineApiGac.GetEntityPos(self.mPlayerId)
		dist = commonApiMgr.GetManhattanDistance(ppos, pos)
		# 晃动幅度：3=幅度，越大晃动越厉害；0.3=衰减速度，越大衰减越快
		amplitude = dist * -0.3 + 3
		if amplitude > 0:
			Instance.mEventMgr.NotifyEvent(CameraShakingSubscribeEvent, {"amplitude": amplitude, "duration": 3})
		pass
	# endregion

	# region 雾效
	def UpdateFogEntityData(self, eid, isAdd=True):
		"""更新雾效数据"""
		if isAdd:
			fogDist = self._fogEntityCfg.get(engineApiGac.GetEngineTypeStr(eid))
			if fogDist:
				self._fogEntityDict[eid] = fogDist
				# 启动timer
				if not self._fogTimer:
					self._fogTimer = engineApiGac.AddRepeatedTimer(1, self.FogTimer)
		else:
			r = self._fogEntityDict.pop(eid, None)
			if r and len(self._fogEntityDict) == 0:
				# 停止timer
				engineApiGac.CancelTimer(self._fogTimer)
				self._fogTimer = None
				self.ShowFog(0)
		pass

	def FogTimer(self):
		"""雾效timer"""
		# 判断附近是否有witch
		selfPos = engineApiGac.GetEntityPos(self.mPlayerId)
		show = 0
		for eid, val in self._fogEntityDict.iteritems():
			pos = engineApiGac.GetEntityPos(eid)
			dist = commonApiMgr.GetDistance(pos, selfPos)
			if dist <= self._showFogLength:
				# 显示雾效
				show = dist * val['strength']
				break
		self.ShowFog(show)
		pass

	def ShowFog(self, showLength):
		"""显示雾效"""
		if showLength:
			fogLength = self._fogComp.GetFogLength()
			t = MathUtils.Lerp(fogLength[1], showLength * 2, 0.3)
			self._fogComp.SetFogLength(showLength, t)
		else:
			self._fogComp.ResetFogLength()
		pass
	# endregion
