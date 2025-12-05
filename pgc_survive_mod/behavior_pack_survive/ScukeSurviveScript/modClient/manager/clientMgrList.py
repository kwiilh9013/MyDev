# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modClient.manager.uiManagerGac import UIManagerGac
from ScukeSurviveScript.ScukeCore.common.manager.eventManager import EventMgr
from ...gameRenderTick import gameRenderTickConfig
import mod.client.extraClientApi as clientApi

from ...modCommon.eventConfig import GameTickSubscribeEvent


class EventMgrWrap(EventMgr):
	__identify__ = 'EventMgr'

	def __init__(self, handler=None):
		super(EventMgrWrap, self).__init__(handler)
		self._gameRenderTickSys = clientApi.GetSystem(gameRenderTickConfig.SystemNameSpace,
													  gameRenderTickConfig.SystemName)

	def RegisterEvent(self, eventId, func):
		if self._gameRenderTickSys and eventId == GameTickSubscribeEvent:
			self._gameRenderTickSys.RegisterEvent(func)
			return
		super(EventMgrWrap, self).RegisterEvent(eventId, func)

	def UnRegisterEvent(self, eventId, func):
		if self._gameRenderTickSys and eventId == GameTickSubscribeEvent:
			self._gameRenderTickSys.UnRegisterEvent(func)
			return
		super(EventMgrWrap, self).UnRegisterEvent(eventId, func)


ClientManagerList = [
	UIManagerGac,
	EventMgrWrap,
]
