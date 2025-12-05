# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.ContextBase import ContextBase


class TestNextContext(ContextBase):
    def __init__(self, up_Context=None):
        super(TestNextContext, self).__init__(up_Context)

        self.modify = False