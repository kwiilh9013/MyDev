# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameCompEnum
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.entitynew.gameEntityBase import GameEntityBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
import random
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
compFactory = serverApi.GetEngineCompFactory()

class EntityWitch(GameEntityBase):
	"""boss 尖叫者"""
	def __init__(self, server, entityId, engineTypeStr):
		super(EntityWitch, self).__init__(server, entityId, engineTypeStr)

		# 上一个组件的类型
		self._lastCompType = None
		config = self.mConfig
		# 生成生物上限
		self._summonMaximum = config['summon_maximum']
		# 生成生物间隔
		self._cdTime = config['summon_cd']
		# 检测玩家行动范围
		self._canFindDistance = config['can_find_distance']
		# 玩家惊扰witch最近距离
		self._canStartleWitchDistance = config['can_startle_witch_distance']
		# 攻击距离
		self._attackDist = config['attack_dist']** 2
		self._allPlayerId = engineApiGas.GetPlayerList()
		self._time = 0
		self._canSummon = False
		self._startleWitch = False
		self._isCrying = False
		pass

	# GameCompEnum.WitchSummonEtity
	# GameCompEnum.WitchSitUp
	# GameCompEnum.WitchSitDown
	# GameCompEnum.WitchSitCry
	# GameCompEnum.WitchMoveUp
	# GameCompEnum.WitchMoveDown
	# GameCompEnum.WitchMoveCry
	# GameCompEnum.WitchMeleeAttack1
	# GameCompEnum.WitchMeleeAttack2

	# region 事件
	@EngineEvent()
	def OnMobHitMobServerEvent(self,args):
		"""玩家碰撞Witch"""
		mobId = args['mobId']
		if mobId in self._allPlayerId:
			hittedMobList = args['hittedMobList']
			if self.mEntityId in hittedMobList:
				distance = self.GetDistance(mobId,self.mEntityId)
				if distance<=self._canFindDistance:
					self._startleWitch =True
		pass
	@EngineEvent()
	def ServerPlayerTryDestroyBlockEvent(self,args):
		"""玩家在Witch附近破坏方块"""
		playerId = args["playerId"]
		distance = self.GetDistance(playerId,self.mEntityId)
		if distance<=self._canFindDistance:
			self._startleWitch =True
		pass
	@EngineEvent()
	def EntityPlaceBlockAfterServerEvent(self, args):
		"""玩家在witch附近放置方块"""
		entityId = args["entityId"]
		if entityId in self._allPlayerId:
			distance = self.GetDistance(entityId,self.mEntityId)
			if distance<=self._canFindDistance:
				self._startleWitch =True
		pass
	@EngineEvent()
	def DamageEvent(self, args):
		"""玩家攻击Witch"""
		entityId = args["entityId"]
		if entityId == self.mEntityId:
			self._startleWitch =True
		pass
	# endregion
	
	def GetNextComponent(self):
		targetId = self.GetAttackTargetId()
		if targetId:
			self._isCrying = False
			# 判断上一个状态是否是哭泣，是则进行起身动画
			if self._lastCompType:
				if self._lastCompType == GameCompEnum.WitchSitDownToCry:
					compType = GameCompEnum.WitchSitUp
					self._lastCompType = compType
					return self.GetComponent(compType)
				elif self._lastCompType == GameCompEnum.WitchMoveDownToCry:
					compType = GameCompEnum.WitchMoveUp
					self._lastCompType = compType
					return self.GetComponent(compType)
			# 如果能召唤则先召唤
			if self._canSummon:
				if self._cdTime != 0:
					self._canSummon = False
				if len(self.GetComponent(GameCompEnum.WitchSummonEtity)._summonEntityIdList)<self._summonMaximum:
					compType = GameCompEnum.WitchSummonEtity
					self._lastCompType = compType
					return self.GetComponent(compType)
			# 距离过近时进行攻击
			dist = self.GetTargetDistanceXZ(targetId)
			if dist <= self._attackDist:
				if random.randint(0,1)==0:
					compType = GameCompEnum.WitchMeleeAttack1
				else:
					compType = GameCompEnum.WitchMeleeAttack2
				self._lastCompType = compType
				return self.GetComponent(compType)
		else:
			# 判断是否被惊醒
			if self._startleWitch:
				# 判断上一个状态是否是哭泣，是则进行起身动画
				self._startleWitch = False
				self._isCrying = False
				if self._lastCompType == GameCompEnum.WitchSitDownToCry:
					compType = GameCompEnum.WitchSitUp
					self._lastCompType = compType
					return self.GetComponent(compType)
				elif self._lastCompType == GameCompEnum.WitchMoveDownToCry:
					compType = GameCompEnum.WitchMoveUp
					self._lastCompType = compType
					return self.GetComponent(compType)
			# 没被惊醒后则重新哭泣
			else:
				if self._lastCompType not in (GameCompEnum.WitchSitDownToCry, GameCompEnum.WitchMoveDownToCry) and self._isCrying == False:
					if random.randint(0,1)==0:
						compType = GameCompEnum.WitchSitDownToCry
					else:
						compType = GameCompEnum.WitchMoveDownToCry
					self._lastCompType = compType
					self._isCrying = True
					return self.GetComponent(compType)

			
	def Update(self):
		if self._cdTime != 0:
			if not self._canSummon:
				self._time+=1
			if self._time == self._cdTime:
				self._canSummon =True
				self._time = 0
		else:
			self._canSummon =True
		return super(EntityWitch,self).Update()
	
	# region 其他API
	def GetDistance(self,playerId,entityId):
		playerPos = engineApiGas.GetEntityPos(playerId)
		entityPos = engineApiGas.GetEntityPos(entityId)
		return commonApiMgr.GetDistance(playerPos, entityPos)
	# endregion