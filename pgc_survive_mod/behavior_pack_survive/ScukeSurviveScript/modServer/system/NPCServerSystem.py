# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class NPCServerSystem(BaseServerSystem):
	"""NPC 服务端"""
	def __init__(self, namespace, systemName):
		super(NPCServerSystem, self).__init__(namespace, systemName)

		pass

	def Destroy(self):
		super(NPCServerSystem, self).Destroy()
		pass
