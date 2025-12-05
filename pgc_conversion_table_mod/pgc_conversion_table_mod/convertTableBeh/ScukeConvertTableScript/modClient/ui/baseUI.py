from ScukeConvertTableScript.ScukeCore.client.ui.baseUI import BaseUI
from ScukeConvertTableScript.modCommon import modConfig
import mod.client.extraClientApi as clientApi
import time
from ScukeConvertTableScript.ScukeCore.common.api.commonApiMgr import DeepCopy
from ScukeConvertTableScript.ScukeCore.client import engineApiGac
from ScukeConvertTableScript.ScukeCore.common.api import itemApi
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.ScukeCore.client.ui.utils import uiUtils
from ScukeConvertTableScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeConvertTableScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent


class ModBaseUI(BaseUI, CommonEventRegister):
	def __init__(self, namespace, name, param):
		BaseUI.__init__(self, namespace, name, param)
		self._clientSystem = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
		CommonEventRegister.__init__(self, self._clientSystem)
		self._inited = False
		self._mTick0 = 0
		self._listenEvents = {}

	@property
	def Inited(self):
		return self._inited

	def Create(self):
		self._inited = True

	def Destroy(self):
		BaseUI.Destroy(self)
		CommonEventRegister.OnDestroy(self)
		for key, event in self._listenEvents.iteritems():
			self._clientSystem.UnListenForEvent(event[0], event[1], event[2], event[3], event[4], event[5])
		self._listenEvents.clear()
		self._clientSystem = None
