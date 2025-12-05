# -*- coding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig

EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType


class AttrClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(AttrClientSystem, self).__init__(namespace, systemName)
		self._sprinting = False
		self._playerComp = None

	def Update(self):
		if self._playerComp:
			sprinting = self._playerComp.isSprinting()
			if self._sprinting != sprinting:
				data = {
					"playerId": clientApi.GetLocalPlayerId(),
					'sprinting': sprinting
				}
				self.BroadcastEvent('OnSprintingChanged', data)
				self.NotifyToServer('OnSprintingChanged', data)
				self._sprinting = sprinting

	@EngineEvent()
	def UiInitFinished(self, args):
		playerId = clientApi.GetLocalPlayerId()
		self._playerComp = clientApi.GetEngineCompFactory().CreatePlayer(playerId)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.LivingServerSystem)
	def OnApplyLivingStateAttr(self, data):
		ui = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
		if not ui:
			return
		ui.DebugUpdateAttr(data)
