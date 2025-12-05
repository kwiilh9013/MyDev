# -*- coding: UTF-8 -*-
from ScukeSurviveScript.ScukeCore.server.entity.entityBase import EntityBase
from ScukeSurviveScript.modCommon.cfg.entity.entityAIConfig import GetEntityConfig
from ScukeSurviveScript.modCommon.eventConfig import EntityEffectEvent


class GameEntityBase(EntityBase):
	"""boss 瞬杀者"""
	def __init__(self, server, entityId, engineTypeStr):
		# 获取config，设置参数
		config = GetEntityConfig(engineTypeStr)
		super(GameEntityBase, self).__init__(server, entityId, engineTypeStr, config)
		# 消息事件名
		self.mEventName = EntityEffectEvent
		pass
