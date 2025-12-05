# -*- coding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.display.armorAnimator import ArmorAnimatorController
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import modConfig
import ScukeSurviveScript.modCommon.cfg.armorConfig as ArmorConfig



class ArmorClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(ArmorClientSystem, self).__init__(namespace, systemName)
		self._isReady = False
		self._armorDisplayMap = {}

	def Add(self, eid, identifier, config):
		displayConfig = config['display']
		typeName = config['type']
		if eid not in self._armorDisplayMap:
			self._armorDisplayMap[eid] = {}
		self._armorDisplayMap[eid][typeName] = {
			'identifier': identifier,
			'config': displayConfig,
			'id': config['id'],
			'level': config['level'],
		}

	def Get(self, eid, typeName=None):
		if eid in self._armorDisplayMap:
			if typeName is None:
				return self._armorDisplayMap[eid]
			return self._armorDisplayMap[eid].get(typeName, None)
		return None

	def Remove(self, eid, typeName=None):
		ret = None
		if eid in self._armorDisplayMap:
			if typeName is None:
				del self._armorDisplayMap[eid]
			elif typeName in self._armorDisplayMap[eid]:
				ret = self._armorDisplayMap[eid][typeName]
				del self._armorDisplayMap[eid][typeName]
				if len(self._armorDisplayMap[eid]) == 0:
					del self._armorDisplayMap[eid]
		return ret

	@EngineEvent()
	def UiInitFinished(self, args):
		self._isReady = True
		eid = clientApi.GetLocalPlayerId()
		if self.Get(eid):
			self.ActiveAllArmor(eid)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.ArmorServerSystem)
	def OnTakeArmor(self, data):
		identifier = data['identifier']
		playerId = data['playerId']
		config = ArmorConfig.GetConfig(identifier)
		if not config:
			return
		self.Add(playerId, identifier, config)
		if self._isReady:
			self.SetArmorDisplay(playerId, config['type'])

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.ArmorServerSystem)
	def OnTakeArmors(self, data):
		identifiers = data['identifiers']
		playerId = data['playerId']
		for identifier in identifiers:
			self.OnTakeArmor({
				'playerId': playerId,
				'identifier': identifier,
			})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.ArmorServerSystem)
	def OnRemoveArmor(self, data):
		identifier = data['identifier']
		playerId = data['playerId']
		config = ArmorConfig.GetConfig(identifier)
		self.RemoveArmorDisplay(playerId, config['type'])
		self.Remove(playerId, config['type'])

	def GetArmorAnimator(self, playerId, aid):
		displays = self.Get(playerId)
		isEmpty = True
		for typeName in displays:
			display = displays[typeName]
			animator = display.get('animator', None)
			if animator:
				isEmpty = False
				if animator.ArmorId == aid:
					return animator, isEmpty
		return None, isEmpty

	def ActiveAllArmor(self, playerId):
		displays = self.Get(playerId)
		keys = displays.keys()
		for typeName in keys:
			self.SetArmorDisplay(playerId, typeName)

	def SetArmorDisplay(self, playerId, typeName):
		display = self.Get(playerId, typeName)
		if not display:
			return
		aid = display['id']
		identifier = display['identifier']
		config = display['config']
		animator, isEmpty = self.GetArmorAnimator(playerId, aid)
		if not animator:
			animator = ArmorAnimatorController(playerId, identifier, aid, config['animator'], isEmpty)
			display['animator'] = animator
		animator.SetPartActive(typeName, True, display['config']['animator'])

	def RemoveArmorDisplay(self, playerId, typeName):
		display = self.Get(playerId, typeName)
		if not display:
			return
		aid = display['id']
		animator = display['animator']
		animator.SetPartActive(typeName, False, display['config'])
		del display['animator']
		_animator, isEmpty = self.GetArmorAnimator(playerId, aid)
		if _animator is None:
			animator.Reset()
