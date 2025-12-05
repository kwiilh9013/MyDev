# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac

CompFactory = clientApi.GetEngineCompFactory()

class WeaponSoundController(object):
	def __init__(self, eid, soundConfig):
		self._eid = eid
		self._config = soundConfig
		self._audio = CompFactory.CreateCustomAudio(clientApi.GetLevelId())
		self._playedSounds = {}
		comp = CompFactory.CreateActorRender(eid)
		for k, v in soundConfig.iteritems():
			comp.AddPlayerSoundEffect(k, v)


	def Play(self, eid, sKeyName, position, loop=False, volume=1.0, pitch=1.0, index=-1):
		if sKeyName not in self._config:
			return
		sound = self._config[sKeyName]
		pos = position
		bindId = None
		if not pos:
			bindId = eid
			pos = engineApiGac.GetEntityPos(eid)
		if pos:
			musicId = self._audio.PlayCustomMusic(sound, pos, volume, pitch, loop, bindId)
			self._playedSounds[sKeyName] = musicId
