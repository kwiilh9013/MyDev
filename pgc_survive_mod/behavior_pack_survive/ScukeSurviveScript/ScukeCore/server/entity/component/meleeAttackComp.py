# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.entity.enum.actionEnum import ActionEnum
from ScukeSurviveScript.ScukeCore.server.entity.component.activeComponentBase import ActiveComponentBase
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
minecraftEnum = serverApi.GetMinecraftEnum()


class MeleeAttackComp(ActiveComponentBase):
	"""近战攻击 组件"""
	def __init__(self, entityObj, config):
		super(MeleeAttackComp, self).__init__(entityObj, config)
		pass
	
	# region Actions
	@AddActionMapping(ActionEnum.AreaAttack)
	def AreaAttack(self, cfg):
		"""
		范围攻击(前方区域)
			cfg = {radius=范围半径, length=往前偏移长度}
		"""
		entityId = self.mEntityId
		pos = engineApiGas.GetEntityFootPos(entityId)
		if not pos:
			return
		# 获取范围实体
		if "radius" in cfg:
			x, y, z = pos
			if "length" in cfg:
				length = cfg["length"]
				rot = engineApiGas.GetEntityRot(entityId)
				offset = commonApiMgr.GetOffsetByRot((0, rot[1]), length)
				x += offset[0]
				z += offset[2]
			radius = cfg["radius"]
			startPos = (x - radius, y, z - radius)
			endPos = (x + radius, y + radius, z + radius)
			entityList = engineApiGas.GetEntitiesInSquareArea(startPos, endPos, self.mEntityObj.GetDimension())
			# 对实体造成伤害
			if engineApiGas:
				damage = self.mEntityObj.GetAttackDamage()
				if "cause" in cfg:
					cause = cfg["cause"]
				else:
					cause = minecraftEnum.ActorDamageCause.EntityAttack
				customTag = None
				if "customTag" in cfg:
					customTag = cfg["customTag"]
				for entity in entityList:
					if self.mEntityObj.IsCanHit(entity):
						engineApiGas.Hurt(entity, entityId, damage, cause, customTag=customTag)
		pass
	
	# endregion
