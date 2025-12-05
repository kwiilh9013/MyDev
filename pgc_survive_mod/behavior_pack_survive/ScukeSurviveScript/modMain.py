# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from mod.common.mod import Mod
from .modCommon import modConfig
from .gameRenderTick import gameRenderTickConfig
from .cameraEffect import cameraEffectConfig

GlobalClientSystemConfig = [
	gameRenderTickConfig,
	cameraEffectConfig
]

@Mod.Binding(name=modConfig.ModName, version=modConfig.ModVersion)
class ScriptSurvive(object):

	@Mod.InitServer()
	def ScriptSurviveServerInit(self):
		from .ScukeCore.server import engineApiGas
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
		# 注册全局system（如果没有注册，此模组才注册，保证只会有一个system），需要先于其他system注册
		for config in GlobalClientSystemConfig:
			if clientApi.GetSystem(config.SystemNameSpace, config.SystemName):
				continue
			clientApi.RegisterSystem(config.SystemNameSpace, config.SystemName, config.SystemPath)

		for systemName in modConfig.ClientSystemList:
			clientApi.RegisterSystem(
				modConfig.ModNameSpace,
				systemName,
				"%s.%s.%s" % (modConfig.ClientSystemPath, systemName, systemName))

	@Mod.DestroyClient()
	def ScriptSurviveClientDestroy(self):
		pass
