# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.server.entity.component.activeComponentBase import ActiveComponentBase
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameActionEnum
from ScukeSurviveScript.modCommon import modConfig
import random


class SummonEntityComp(ActiveComponentBase):
	"""生成实体组件"""
	def __init__(self, entityObj, config):
		super(SummonEntityComp, self).__init__(entityObj, config)

		config = self.mConfig
		pass

	@AddActionMapping(GameActionEnum.SummonEntity)
	def SummonEntity(self, cfg):
		"""
		生成生物
		"""
		pos = engineApiGas.GetEntityFootPos(self.mEntityId)
		if not pos:
			return
		# 每波生成的怪物数量
		count = cfg.get('count', 1)
		# 生成最远半径
		radius = cfg.get('radius', 1)
		height = cfg.get('height', 0)
		# 是否会随天数强化
		phaseEnhance = cfg.get('phase_enhance')
		if phaseEnhance:
			# 调用phase系统来生成生物
			phaseSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PhaseServerSystem)
			if phaseSys:
				if 'engineTypeStr' in cfg:
					# 仅生成一种生物
					dim = engineApiGas.GetEntityDimensionId(self.mEntityId)
					pos = engineApiGas.GetEntityPos(self.mEntityId)
					rot = engineApiGas.GetEntityRot(self.mEntityId)
					engineTypeStr = cfg['engineTypeStr']
					for i in xrange(count):
						if radius:
							offset = (random.randint(-radius, radius), height, random.randint(-radius, radius))
						else:
							offset = (0, height, 0)
						phaseSys.SetSpawnMonsterFromAttrRatio(engineTypeStr, dim, (pos[0] + offset[0], pos[1] + 1, pos[2] + offset[2]), rot)
		else:
			serverSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.ServerSystem)
			if serverSystem:
				if 'engineTypeStr' in cfg:
					# 仅生成一种生物
					engineTypeStr = cfg['engineTypeStr']
					for i in xrange(count):
						if radius:
							offset = (random.randint(-radius, radius), height, random.randint(-radius, radius))
						else:
							offset = (0, height, 0)
						serverApiMgr.SpawnEntityById(serverSystem, self.mEntityId, engineTypeStr, offset=offset)
					pass
		pass
