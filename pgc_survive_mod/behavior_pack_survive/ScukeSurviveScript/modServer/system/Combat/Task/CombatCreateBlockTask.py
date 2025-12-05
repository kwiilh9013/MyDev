# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.TaskBase import TaskBase
from ScukeSurviveScript.modServer.system.Combat.BaseClass.ContextBase import ContextBase
import math


class CombatCreateBlockTask(TaskBase):
    def __init__(self, skill):
        super(CombatCreateBlockTask, self).__init__(skill)

    def OnTaskStart(self):
        skillBasicContext = ContextBase.GetContextByClassName(self.context, "SkillBasicContext")
        pos = skillBasicContext.source_entity_foot_pos

        blockStateComp = self.compFactory.CreateBlockState(self.engineApi.GetLevelId())
        auxValue = blockStateComp.GetBlockAuxValueFromStates("minecraft:wool", { 'color': 'orange' })
        blockDict = {
            'name': 'minecraft:wool',
            'aux': auxValue
        }
        blockInfoComp = self.compFactory.CreateBlockInfo(self.engineApi.GetLevelId())
        blockInfoComp.SetBlockNew((math.floor(pos[0]), math.floor(pos[1]), math.floor(pos[2])), blockDict, 0, 0, True)
