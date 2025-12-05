# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi


class AreaServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(AreaServerSystem, self).__init__(namespace, systemName)
		self._detectAreas = {}
		self._updateTimer = engineApiGas.AddRepeatTimer(1, self.UpdateTimer)

	def AddAreaDetect(self, uid, dim, minPos, maxPos, eid, inCallback=None, outCallback=None):
		item = {
			'uid': uid,
			'dim': dim,
			'minPos': minPos,
			'maxPos': maxPos,
			'eid': eid,
			'inCallback': inCallback,
			'outCallback': outCallback,
			'state': False,
		}
		self._detectAreas[uid] = item

	def RemoveAreaDetect(self, uid):
		if uid in self._detectAreas:
			del self._detectAreas[uid]

	def UpdateTimer(self):
		dirtyItems = []
		for item in self._detectAreas.itervalues():
			prevState = item['state']
			state = False
			eid = item['eid']
			dim = item['dim']
			minPos = item['minPos']
			maxPos = item['maxPos']
			cDim = engineApiGas.GetEntityDimensionId(eid)
			if cDim == dim:
				pos = engineApiGas.GetEntityFootPos(eid)
				state = pos is not None and (minPos[0] < pos[0] < maxPos[0]) and (minPos[1] < pos[1] < maxPos[1]) and (minPos[2] < pos[2] < maxPos[2])
			if state != prevState:
				item['state'] = state
				dirtyItems.append(item)
		for item in dirtyItems:
			state = item['state']
			inCallback = item['inCallback']
			outCallback = item['outCallback']
			if state and inCallback:
				inCallback(item)
			if not state and outCallback:
				outCallback(item)

	def Destroy(self):
		super(AreaServerSystem, self).Destroy()
		if self._updateTimer:
			engineApiGas.CancelTimer(self._updateTimer)