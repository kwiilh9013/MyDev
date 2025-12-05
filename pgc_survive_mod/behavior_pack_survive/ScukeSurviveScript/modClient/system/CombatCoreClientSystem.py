# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent

from ScukeSurviveScript.modCommon import modConfig


class CombatCoreClientSystem(BaseClientSystem):
    def __init__(self, namespace, systemName):
        super(CombatCoreClientSystem, self).__init__(namespace, systemName)

    def RequestCastSkill(self, entityId, skillId):
        self.NotifyToServer('RequestCastSkill', {'entityId': entityId, 'skillId': skillId})
