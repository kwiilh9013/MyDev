# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent

from ScukeSurviveScript.modCommon import modConfig
import ScukeSurviveScript.modCommon.cfg.armorConfig as ArmorConfig
from ScukeSurviveScript.modCommon.cfg.armorSuitConfig import Config as ArmorSuitConfig
import mod.server.extraServerApi as serverApi

ArmorPosType = serverApi.GetMinecraftEnum().ItemPosType.ARMOR
UpdateInterval = 30

class ArmorServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(ArmorServerSystem, self).__init__(namespace, systemName)
		self._playerArmorMap = {}
		self._players = []
		self._tick = 0

	@EngineEvent()
	def OnNewArmorExchangeServerEvent(self, args):
		slot = args['slot']
		eid = args['playerId']
		oldItemName = args['oldArmorName']
		newItemName = args['newArmorName']
		if oldItemName.startswith(ArmorConfig.ArmorIdentifierPrefix):
			self.Remove(eid, oldItemName)
		if not newItemName.startswith(ArmorConfig.ArmorIdentifierPrefix):
			return
		self.Take(eid, newItemName)

	def Take(self, eid, identifier):
		config = ArmorConfig.GetConfig(identifier)
		if not config:
			return
		if eid not in self._playerArmorMap:
			self._playerArmorMap[eid] = {}
		self._playerArmorMap[eid][identifier] = True
		self.BroadcastToAllClient('OnTakeArmor', {
			'playerId': eid,
			'identifier': identifier,
		})

	def Remove(self, eid, identifier):
		config = ArmorConfig.GetConfig(identifier)
		if not config:
			return
		if eid not in self._playerArmorMap:
			self._playerArmorMap[eid] = {}
		if identifier in self._playerArmorMap[eid]:
			self.BroadcastToAllClient('OnRemoveArmor', {
				'playerId': eid,
				'identifier': identifier
			})
			del self._playerArmorMap[eid][identifier]

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, args):
		playerId = args['playerId']
		if playerId not in self._players:
			self._players.append(playerId)
		if playerId in self._playerArmorMap:
			self.BroadcastToAllClient('OnTakeArmors', {
				'playerId': playerId,
				'identifiers': self._playerArmorMap[playerId],
			})

	def Update(self):
		if self._tick % UpdateInterval == 0:
			for playerId in self._players:
				armors = engineApiGas.GetPlayerAllItems(playerId, ArmorPosType)
				armorIds = []
				if armors and len(armors) > 0:
					for armorItem in armors:
						if not armorItem:
							continue
						itemName = armorItem['newItemName']
						armorIds.append(itemName)
				self._UpdateArmorSuitBuff(playerId, armorIds)
		self._tick += 1

	def _UpdateArmorSuitBuff(self, playerId, armors):
		effectComp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
		for armorSuit in ArmorSuitConfig:
			allArmors = armorSuit['armors']
			count = 0
			for item in armors:
				if item in allArmors:
					count += 1
				else:
					break
			active = count == len(allArmors)
			if not active:
				continue
			buffs = armorSuit['buffs']
			for buff in buffs:
				effectComp.AddEffectToEntity(buff['type'], 12, buff['amplifier'], False)
