# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.modCommon.cfg.entity import entityConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityBase(CommonEventRegister):
	"""实体基类"""
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		CommonEventRegister.__init__(self, severHandler)
		self.mServer = severHandler
		self.mLevelId = self.mServer.mLevelId
		self.mEntityId = entityId
		self.mEngineTypeStr = engineTypeStr
		
		# 获取config，设置参数
		self.mCfg = entityConfig.GetEntityConfig(engineTypeStr)
		
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self.mServer = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体死亡事件"""
		entityId = args.get("id")
		if entityId == self.mEntityId:
			# 销毁
			self.Destroy()
		pass

	# endregion
