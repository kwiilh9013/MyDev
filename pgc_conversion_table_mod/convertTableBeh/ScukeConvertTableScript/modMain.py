# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from mod.common.mod import Mod
from ScukeConvertTableScript.modCommon import modConfig


@Mod.Binding(name=modConfig.ModName, version=modConfig.ModVersion)
class ScriptSurvive(object):

	@Mod.InitServer()
	def ScriptSurviveServerInit(self):
		from ScukeConvertTableScript.ScukeCore.server import engineApiGas
		print("===== init mod server =====")
		ServerSystemList = modConfig.ServerSystemList
		if engineApiGas.IsEditorMode():
			ServerSystemList = modConfig.EditorServerSystemList
		for systemName in ServerSystemList:
			serverApi.RegisterSystem(
				modConfig.ModNameSpace,
				systemName,
				"%s.%s.%s" % (modConfig.ServerSystemPath, systemName, systemName))

	@Mod.DestroyServer()
	def ScriptSurviveServerDestroy(self):
		pass

	@Mod.InitClient()
	def ScriptSurviveClientInit(self):
		for systemName in modConfig.ClientSystemList:
			clientApi.RegisterSystem(
				modConfig.ModNameSpace,
				systemName,
				"%s.%s.%s" % (modConfig.ClientSystemPath, systemName, systemName))

	@Mod.DestroyClient()
	def ScriptSurviveClientDestroy(self):
		pass
