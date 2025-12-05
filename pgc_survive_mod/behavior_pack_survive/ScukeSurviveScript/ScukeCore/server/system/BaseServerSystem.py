import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.log.logMetaClass import LogMetaClass
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server import engineApiGas

ServerSystem = serverApi.GetServerSystemCls()

class BaseServerSystem(ServerSystem, CommonEventRegister):
	__metaclass__ = LogMetaClass

	def __init__(self, namespace, systemName):
		ServerSystem.__init__(self, namespace, systemName)
		CommonEventRegister.__init__(self, self)

		self.mLevelId = serverApi.GetLevelId()
		"""levelid"""
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
