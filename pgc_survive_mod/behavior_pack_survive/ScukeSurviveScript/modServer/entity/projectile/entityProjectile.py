# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityProjectile(EntityBase):
	"""抛射物 实体对象"""
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(EntityProjectile, self).__init__(severHandler, entityId, engineTypeStr, param)
		
		pass

	def Destroy(self):
		super(EntityProjectile, self).Destroy()
		pass
	
	# region 事件
	# endregion

	# region 逻辑入口
	# endregion
