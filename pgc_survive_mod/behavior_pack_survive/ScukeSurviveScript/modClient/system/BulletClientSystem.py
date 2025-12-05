# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.modClient.display.weaponParticle import WeaponParticleController
from ScukeSurviveScript.modCommon import modConfig

CompFactory = clientApi.GetEngineCompFactory()


class BulletClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(BulletClientSystem, self).__init__(namespace, systemName)
		self._bulletEntityRecord = {}

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnClientBulletEntityCreated(self, args):
		eid = args['eid']
		config = args['config']
		if 'display' not in config:
			return
		if eid in self._bulletEntityRecord:
			self._bulletEntityRecord[eid] = args
			self.InitBulletEntity(eid)
		else:
			self._bulletEntityRecord[eid] = args


	def InitBulletEntity(self, eid):
		if eid in self._bulletEntityRecord:
			data = self._bulletEntityRecord[eid]
			config = data['config']
			displayConfig = config['display']
			if 'particle' in displayConfig:
				WeaponParticleController(eid, displayConfig['particle'])
			del self._bulletEntityRecord[eid]

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		self.InitBulletEntity(args['id'])

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnClientBulletEntityDestroy(self, args):
		eid = args['eid']
		if eid in self._bulletEntityRecord:
			del self._bulletEntityRecord[eid]
