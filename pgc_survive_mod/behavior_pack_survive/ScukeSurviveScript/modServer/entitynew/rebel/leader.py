# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameCompEnum
from ScukeSurviveScript.modServer.entitynew.rebel.soldier import EntityRebelSoldier
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
HealthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH


class EntityRebelLeader(EntityRebelSoldier):
	"""反叛军 队长"""
	def __init__(self, server, entityId, engineTypeStr):
		super(EntityRebelLeader, self).__init__(server, entityId, engineTypeStr)

		cfg = self.mConfig
		# 召唤士兵的低血量阈值
		summonRebelRatio = cfg["summon_ratio"]
		self._lowSummonRebelHealth = self._maxHealth * summonRebelRatio
		self._isSummonRebelState = None
		# 无人机
		self._summonFlyingdroneCD = cfg["flyingdrone_cd"]
		self._summonFlyingdroneTick = 0
		pass

	def Destroy(self):
		super(EntityRebelLeader, self).Destroy()

	def GetNextComponent(self):
		# 根据当前手持的武器，执行不同的逻辑
		targetId = self.GetAttackTargetId()
		if not targetId:
			# 回血
			return self.RecoverHealth(False)
		
		# # 尝试召唤反叛军
		# res = self.TrySummonRebel()
		# if res:
		# 	return res

		dist = self.GetTargetDistanceXZ(targetId)
		if dist <= self._attackDist:
			# 近战
			return self.GetComponent(GameCompEnum.MeleeAttack1)
		elif dist <= self._shootDist:
			if self.mIsRangedAttack:
				# 射击
				res = self.TrySummonFlyingdrone()
				if res:
					return res
				# 判断是否可看见目标
				entityId = self.mEntityId
				canSee = self._gameComp.CanSee(entityId, targetId, 24.0, True, 90.0, 60.0)
				if canSee:
					return self.GetComponent(GameCompEnum.Shoot1)
				
		# 非攻击时间
		# 尝试治疗
		return self.RecoverHealth()

	def TrySummonRebel(self):
		"""尝试召唤反叛军"""
		# 初始化召唤士兵的状态（仅能召唤一次）
		if self._isSummonRebelState is None:
			isSummon = engineApiGas.GetExtraData(self.mEntityId, "isSummonRebel")
			if isSummon:
				self._isSummonRebelState = True
			else:
				self._isSummonRebelState = False
		if not self._isSummonRebelState:
			# 判断血量是否满足，满足后则进行召唤
			if self._attrComp.GetAttrValue(HealthEnum) < self._lowSummonRebelHealth:
				self._isSummonRebelState = True
				engineApiGas.SetExtraData(self.mEntityId, "isSummonRebel", True)
				return self.GetComponent(GameCompEnum.SummonRebel)
		return None
	
	def TrySummonFlyingdrone(self):
		"""尝试召唤自爆无人机"""
		if self.mTick - self._summonFlyingdroneTick < self._summonFlyingdroneCD:
			return None
		self._summonFlyingdroneTick = self.mTick
		return self.GetComponent(GameCompEnum.SummonFlyingdrone)
