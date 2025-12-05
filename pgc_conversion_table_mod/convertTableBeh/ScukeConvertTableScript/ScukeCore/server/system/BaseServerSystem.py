import mod.server.extraServerApi as serverApi
from ScukeConvertTableScript.ScukeCore.common.log.logMetaClass import LogMetaClass
from ScukeConvertTableScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeConvertTableScript.ScukeCore.server import engineApiGas

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
