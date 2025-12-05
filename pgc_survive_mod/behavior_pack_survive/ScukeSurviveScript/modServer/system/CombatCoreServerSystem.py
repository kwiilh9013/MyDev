# -*- encoding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modServer.system.Combat.Mgr.SkillServerMgr import SkillServerMgr
from ScukeSurviveScript.modServer.system.Combat.Mgr.TimelineServerMgr import TimelineServerMgr
from ScukeSurviveScript.modServer.system.Combat.Mgr.AttractorServerMgr import AttractorServerMgr


class CombatCoreServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(CombatCoreServerSystem, self).__init__(namespace, systemName)
		self.engineApi = serverApi
		self._TimelineManager = TimelineServerMgr()
		self._SkillServerMgr = SkillServerMgr(self)
		self._AttractorMgr = AttractorServerMgr(self)

	# Debug
	@EngineEvent()
	def ServerChatEvent(self, args):
		playerId = args['playerId']
		message = args['message']
		if str.startswith(message, "CastSkill"):
			skillId = int(message.split(' ')[1])
			self.GetSkillServerMgr().CastSkill(playerId, skillId)
			args['cancel'] = True

		if str.startswith(message, "glass"):
			itemComp = serverApi.GetEngineCompFactory().CreateItem(playerId)
			itemComp.SpawnItemToPlayerInv({'newItemName': 'minecraft:glass', 'count': 64, 'newAuxValue': 0}, playerId)

		if str.startswith(message, "Bow"):
			itemComp = serverApi.GetEngineCompFactory().CreateItem(playerId)
			itemComp.SpawnItemToPlayerInv({'newItemName': 'minecraft:bow', 'count': 1, 'newAuxValue': 0},
										  playerId)
			itemComp.SpawnItemToPlayerInv({'newItemName': 'minecraft:arrow', 'count': 64, 'newAuxValue': 0},
										  playerId)

		if str.startswith(message, "tag"):
			bAdd = int(message.split(" ")[1])
			if bAdd == 1:
				comp = serverApi.GetEngineCompFactory().CreateTag(playerId)
				comp.AddEntityTag("Attractor")
			else:
				comp = serverApi.GetEngineCompFactory().CreateTag(playerId)
				comp.RemoveEntityTag("Attractor")

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.CombatCoreClientSystem)
	def RequestCastSkill(self, data):
		entityId = data['entityId']
		skillId = data['skillId']
		print "combat server system cast skill", entityId, skillId
		self._SkillServerMgr.CastSkill(entityId, skillId)

	def Update(self):
		self._TimelineManager.Update()
		self._AttractorMgr.Update()

	def GetTimelineManager(self):
		return self._TimelineManager

	def GetSkillServerMgr(self):
		return self._SkillServerMgr
