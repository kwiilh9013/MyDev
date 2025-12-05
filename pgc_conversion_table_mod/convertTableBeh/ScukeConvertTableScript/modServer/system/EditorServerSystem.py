# -*- coding: utf-8 -*-
from ScukeConvertTableScript.ScukeCore.common import config
from ScukeConvertTableScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeConvertTableScript.modServer.manager.singletonGas import Instance
from ScukeConvertTableScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi


class EditorServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(EditorServerSystem, self).__init__(namespace, systemName)

	@EngineEvent()
	def LoadServerAddonScriptsAfter(self, args):
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, data):
		pass
