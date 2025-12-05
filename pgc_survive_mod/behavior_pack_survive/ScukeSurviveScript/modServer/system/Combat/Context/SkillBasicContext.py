# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.ContextBase import ContextBase


class SkillBasicContext(ContextBase):
    def __init__(self, up_Context=None):
        super(SkillBasicContext, self).__init__(up_Context)

        self.skill_id = None
        self.source_entity_id = None
        self.target_entity_id = None
        self.source_entity_pos = None
        self.source_entity_foot_pos = None
        self.source_entity_rot = None

