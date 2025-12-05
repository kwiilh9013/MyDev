# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi


class EditorServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(EditorServerSystem, self).__init__(namespace, systemName)

	@EngineEvent()
	def LoadServerAddonScriptsAfter(self, args):
		pass

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, data):
		pass

	@EngineEvent()
	def PlaceNeteaseLargeFeatureServerEvent(self, args):
		args['cancel'] = True

	@EngineEvent()
	def PlaceNeteaseStructureFeatureEvent(self, args):
		args['cancel'] = True