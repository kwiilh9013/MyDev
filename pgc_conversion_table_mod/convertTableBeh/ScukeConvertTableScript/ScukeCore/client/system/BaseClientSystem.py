# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeConvertTableScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister

ClientSystem = clientApi.GetClientSystemCls()


class BaseClientSystem(ClientSystem, CommonEventRegister):
	def __init__(self, namespace, systemName):
		ClientSystem.__init__(self, namespace, systemName)
		CommonEventRegister.__init__(self, self)
		
		self.mLevelId = clientApi.GetLevelId()
		"""levelId"""
		self.mPlayerId = clientApi.GetLocalPlayerId()
		"""本地玩家id"""

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
