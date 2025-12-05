# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server.entity.component.activeComponentBase import ActiveComponentBase
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameActionEnum
from ScukeSurviveScript.modCommon import modConfig
import random
compFactory = serverApi.GetEngineCompFactory()

class WitchEtityComp(ActiveComponentBase):
	"""witch生成生物组件 主动"""
	def __init__(self, entityObj, config):
		super(WitchEtityComp, self).__init__(entityObj, config)

		config = self.mConfig
		# 生成生物的id列表
		self._summonEntityIdList = []
		pass

	@AddActionMapping(GameActionEnum.WitchSummonEtity)
	def WitchSummonEtity(self,cfg):
		"""
		生成生物
			cfg = {summon_radius= 生成水平面最远半径,entity_cfg=生成生config,{entityIdentifier:count}}
		"""
		entityId = self.mEntityId
		targetId = self.mEntityObj.GetAttackTargetId()
		if not targetId:
			return
		pos = engineApiGas.GetEntityFootPos(entityId)
		if not pos:
			return
		# 每波生成的怪物数量
		count = cfg.get('summon_count',0)
		# 生成最远半径
		radius = cfg.get('summon_radius',1)
		# 生成池类型
		summonPool = cfg['summon_pool']
		poolWeight = cfg.get('summon_pool_weight')
		if not poolWeight:
			poolWeight = commonApiMgr.GetTotalWeight(summonPool)
			cfg['summon_pool_weight'] = poolWeight

		# 调用phase系统来生成生物
		phaseSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PhaseServerSystem)
		if phaseSys:
			dim = engineApiGas.GetEntityDimensionId(self.mEntityId)
			pos = engineApiGas.GetEntityPos(self.mEntityId)
			rot = engineApiGas.GetEntityRot(self.mEntityId)
			for i in xrange(count):
				if radius:
					offset = (random.randint(-radius, radius), 0, random.randint(-radius, radius))
				else:
					offset = (0, 0, 0)
				entityCfg = commonApiMgr.GetValueFromWeightPool(summonPool, poolWeight)
				phaseSys.SetSpawnMonsterFromAttrRatio(entityCfg['type'], dim, (pos[0] + offset[0], pos[1] + 1, pos[2] + offset[2]), rot)
			# 特效
			engineApiGas.SetCommand('/particle scuke:camel_skill_steam_burst '+str(pos[0])+' '+str(pos[1])+' '+str(pos[2]))
	pass
