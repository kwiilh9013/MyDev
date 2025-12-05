# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.Context.SkillBasicContext import SkillBasicContext


class CDProcessor(object):
    def __init__(self, skillMgr):
        super(CDProcessor, self).__init__()

        self.skillMgr = skillMgr

        self.entityCDInfo = {}

    def __del__(self):
        self.entityCDInfo = None

    def CanDoSkill(self, entityId, skillId):
        if entityId not in self.entityCDInfo:
            return True

        if skillId in self.entityCDInfo[entityId]:
            return False

    def Update(self, context):
        basicContext = SkillBasicContext.GetContextByClassName(context, "SkillBasicContext")
        if basicContext:
            entityId = basicContext.source_entity_id

