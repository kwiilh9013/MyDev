# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.buffConfig import Config as BuffConfig
CompFactory = clientApi.GetEngineCompFactory()


class BuffClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(BuffClientSystem, self).__init__(namespace, systemName)
		self.__displaySystem__ = None

	@property
	def _displaySystem(self):
		if not self.__displaySystem__:
			self.__displaySystem__ = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.DisplayClientSystem)
		return self.__displaySystem__

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuffServerSystem)
	def OnBuffAdded(self, data):
		buffState = data
		buffType = buffState['type']
		if buffType not in BuffConfig:
			return
		config = BuffConfig[buffType]
		if 'display' not in config:
			return
		displayConfig = config['display']
		eid = buffState['eid']
		for keyName in displayConfig:
			self._displaySystem.AddDisplayByStr(eid, keyName, False)
		self._displaySystem.UpdateDisplay(eid)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuffServerSystem)
	def OnBuffRemoved(self, data):
		buffState = data
		buffType = buffState['type']
		if buffType not in BuffConfig:
			return
		config = BuffConfig[buffType]
		if 'display' not in config:
			return
		displayConfig = config['display']
		eid = buffState['eid']
		for keyName in displayConfig:
			self._displaySystem.RemoveDisplayByStr(eid, keyName, False)
		self._displaySystem.UpdateDisplay(eid)