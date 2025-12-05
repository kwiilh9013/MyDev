# -*- coding: utf-8 -*-
import math
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
compFactory = clientApi.GetEngineCompFactory()


class EffectClientSystem(BaseClientSystem):
	"""
	特效系统
	没有地方丢的特效，统一丢这里
	"""
	def __init__(self, namespace, systemName):
		super(EffectClientSystem, self).__init__(namespace, systemName)

		self._dimensionId = 0

		# 特效设置范围
		self._effectSetMaxDistance = 128

		# 发动机特效的数据：{dim: {pos: {effectId, } } }
		self._engineEffectDict = {}
		# 玩家位置，用于判断是否移动
		self._enginePlyPos = None

		self._posComp = compFactory.CreatePos(self.mPlayerId)

		self._eventFunctions = {
			"engine": self.PlayEngineEffects,
			"multi_engine": self.PlayMultiEngineEffects,
		}
		# 注册订阅
		# Instance.mEventMgr.RegisterEvent(eventConfig.GameTickSubscribeEvent, self.GameTickSubscribeEvent)
		pass

	def Destroy(self):
		super(EffectClientSystem, self).Destroy()
		# 注销订阅
		# Instance.mEventMgr.UnRegisterEvent(eventConfig.GameTickSubscribeEvent, self.GameTickSubscribeEvent)
		pass

	# region 事件
	@EngineEvent()
	def OnScriptTickClient(self, args=None):
		"""脚本tick事件"""
		self.UpdateEffectTimer()
		pass

	@EngineEvent()
	def UiInitFinished(self, args=None):
		"""UI初始化完成事件"""
		self._dimensionId = clientApiMgr.GetCurrentDimension()

		# 重新设置一遍特效
		self.RePlayEngineEffects()
		pass

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def EffectPlayEvent(self, args):
		"""从建筑系统来的播放特效事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region 发动机特效
	def PlayMultiEngineEffects(self, args):
		"""播放多个发动机特效"""
		engineList = args.get("engine_list")
		for value in engineList:
			info = {
				"dimension": value[0],
				"pos": value[1],
			}
			self.PlayEngineEffects(info)
		pass

	def PlayEngineEffects(self, args):
		"""播放发动机特效"""
		dimension = args.get("dimension")
		pos = args.get("pos")
		# 记录特效数据（不重复播放）
		dimVal = self._engineEffectDict.get(dimension)
		if dimVal is None:
			dimVal = {}
			self._engineEffectDict[dimension] = dimVal
		effectVal = dimVal.get(pos)
		if effectVal is None:
			effectVal = {}
			dimVal[pos] = effectVal
			# 播放特效
			effectList = self.CreateEngineEffects(pos)
			effectVal["effectList"] = effectList
		pass

	def RePlayEngineEffects(self):
		"""重新播放发动机特效，用于传送维度之后"""
		dimension = self._dimensionId
		dimVal = self._engineEffectDict.get(dimension)
		if dimVal:
			for pos, effectVal in dimVal.iteritems():
				effectList = effectVal.get("effectList")
				if effectList:
					# 删除
					for effectId in effectList:
						clientApiMgr.RemoveMicroParticle(effectId)
				# 重新创建特效
				effectList = self.CreateEngineEffects(pos)
				effectVal["effectList"] = effectList
		pass

	def CreateEngineEffects(self, pos):
		"""创建发动机特效"""
		effectNameList = (
			"scuke_survive:engine_light",
			"scuke_survive:engine_light3",
		)
		effectList = []
		for effect in effectNameList:
			# 如果pos是在未加载区域，则粒子会不显示。当前方案是通过update将粒子重新显示在加载范围内
			effId = clientApiMgr.CreateMicroParticle(effect, pos)
			effectList.append(effId)
		return effectList

	def UpdateEffectTimer(self):
		"""更新发动机特效"""
		# 判断玩家是否移动
		plyPos = self._posComp.GetPos()
		if self._enginePlyPos == plyPos:
			return
		self._enginePlyPos = plyPos

		dimVal = self._engineEffectDict.get(self._dimensionId)
		if dimVal:
			for pos, effectVal in dimVal.iteritems():
				# 更新特效位置
				effectList = effectVal.get("effectList")
				if effectList:
					# 重新计算特效的位置 = 玩家位置和发动机位置之间的一个点，和玩家固定距离
					dist = commonApiMgr.GetDistanceXZ(plyPos, pos)
					distNum = dist - self._effectSetMaxDistance
					if distNum > 0:
						newPos = commonApiMgr.VectorLerpLength(plyPos, pos, self._effectSetMaxDistance)
						for effId in effectList:
							# 超出距离，更新位置
							clientApiMgr.SetMicroParticlePos(effId, newPos)
							clientApiMgr.SetMicroParticleVariable(effId, "variable.camera_distance", distNum)
					else:
						# 位置范围内，重置
						for effId in effectList:
							clientApiMgr.SetMicroParticlePos(effId, pos)
							clientApiMgr.SetMicroParticleVariable(effId, "variable.camera_distance", 0)
		pass
	
	# endregion
