from mod.client import extraClientApi

from ScukeSurviveScript.ScukeCore.client.ui.baseUI import BaseUI
from ScukeSurviveScript.modCommon import modConfig


class ModBaseUI(BaseUI):
	def __init__(self, namespace, name, param):
		super(ModBaseUI, self).__init__(namespace, name, param)
		self._inited = False
		self._listenEvents = {}

	@property
	def Inited(self):
		return self._inited

	def Create(self):
		self._clientSystem = extraClientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
		self._inited = True

	def ListenForEvent(self, systemName, eventName, instance, func, modName=modConfig.ModNameSpace, priority=0):
		self._clientSystem.ListenForEvent(modName, systemName, eventName, instance, func, priority)
		key = '%s|%s|%s' % (modName,systemName, eventName)
		self._listenEvents[key] = (modName, systemName, eventName, instance, func, priority)

	def UnListenForEvent(self, systemName, eventName, instance, func, modName=modConfig.ModNameSpace, priority=0):
		self._clientSystem.UnListenForEvent(modName, systemName, eventName, instance, func, priority)
		key = '%s|%s|%s' % (modName,systemName, eventName)
		if key in self._listenEvents:
			del self._listenEvents[key]

	def Destroy(self):
		super(ModBaseUI, self).Destroy()
		for key, event in self._listenEvents.iteritems():
			self._clientSystem.UnListenForEvent(event[0], event[1], event[2], event[3], event[4], event[5])
		self._listenEvents.clear()
		self._clientSystem = None