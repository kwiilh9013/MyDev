# -*- coding: utf-8 -*-
from ScukeConvertTableScript.ScukeCore.common import config
from ScukeConvertTableScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeConvertTableScript.modServer.manager.singletonGas import Instance
from ScukeConvertTableScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi


class ServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(ServerSystem, self).__init__(namespace, systemName)
		self.Init()
		self.InitManager()

	def Init(self):
		pass

	def InitManager(self):
		from ScukeConvertTableScript.modServer.manager.serverMgrList import ServerManagerList
		import re
		strinfo = re.compile(r'Gas$')
		for mgrCls in ServerManagerList:
			mgr = mgrCls(self)
			setattr(Instance, "m" + strinfo.sub("", mgrCls.__name__), mgr)

	def Update(self):
		Instance.mDatasetManager.FlushLevelData()



