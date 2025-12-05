# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.entity.enum.actionEnum import ActionEnum
from ScukeSurviveScript.ScukeCore.server.entity.component.activeComponentBase import ActiveComponentBase
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
minecraftEnum = serverApi.GetMinecraftEnum()


class TeleportComp(ActiveComponentBase):
	"""瞬移 组件"""
	def __init__(self, entityObj, config):
		super(TeleportComp, self).__init__(entityObj, config)
		pass
	
	# region Actions
	@AddActionMapping(ActionEnum.TeleportToTarget)
	def TeleportToTarget(self, cfg):
		"""
		传送到目标附近
			cfg = {max_dist=每次传送最大距离, target_min_dist=和目标最小距离(以防挨太近)}
		"""
		entityId = self.mEntityId
		pos = engineApiGas.GetEntityFootPos(entityId)
		if not pos:
			return
		# 获取目标位置
		# 计算和目标的距离
		# 如果距离大于max_dist, 则仅传送max_dist
		targetId = self.mEntityObj.GetAttackTargetId()
		if not targetId:
			return
		tpos = engineApiGas.GetEntityPos(targetId)
		dist = commonApiMgr.GetDistanceXZSqrt(pos, tpos)
		if "max_dist" in cfg:
			# 有最大距离限制
			if dist > cfg["max_dist"]:
				dist = cfg["max_dist"]
			else:
				dist = dist - cfg.get("target_min_dist", 0)
		else:
			# 传送到目标前方一点
			dist = dist - cfg.get("target_min_dist", 1)
		newPos = commonApiMgr.VectorLerpLength(pos, tpos, dist)
		# 防止卡方块里
		# 设置新位置
		engineApiGas.SetEntityPos(entityId, newPos)
		pass
	
	# endregion
