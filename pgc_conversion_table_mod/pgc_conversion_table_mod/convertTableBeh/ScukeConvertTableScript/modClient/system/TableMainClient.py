# -*- coding: utf-8 -*-
from ScukeConvertTableScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi
from ScukeConvertTableScript.ScukeCore.client import engineApiGac
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.ScukeCore.client.localDataMgr import *
import ast


class TableMainClient(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(TableMainClient, self).__init__(namespace, systemName)
		self.emcCfgName = modConfig.ModName + "EmcGlobalCfg"
		self.cfgComp = engineApiGac.compFactory.CreateConfigClient(engineApiGac.levelId)
		self.globalEmcCfg = {}
		self.hasInit = False

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def SaveGlobalEmcConfig(self, args):
		emcData = args["data"]
		saveData = self.ConvertToStorgeData(emcData)
		self.cfgComp.SetConfigData(self.emcCfgName, {"emcData": saveData}, True)

	def LoadGlobalEmcConfig(self, args=None):
		# 加载EMC，并传递给服务端
		data = self.cfgComp.GetConfigData(self.emcCfgName, True)
		if type(data) == dict:
			data = data.get("emcData", "{}")
		emcData = self.ConvertFromStorgeData(data)
		self.NotifyToServer("LoadGlobalEmcConfig", {"pid": self.mPlayerId, "emcData": emcData})

	@EngineEvent()
	def UiInitFinished(self, args=None):
		if not self.hasInit:
			self.LoadGlobalEmcConfig()
		self.hasInit = True

	def ConvertToStorgeData(self, data):
		return str(data)

	def ConvertFromStorgeData(self, data):
		return ast.literal_eval(data)
