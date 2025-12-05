# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.TaskBase import TaskBase
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas


class CombatHitFrameTask(TaskBase):
    def __init__(self, skill):
        super(CombatHitFrameTask, self).__init__(skill)

    def OnTaskStart(self):
        posComp = self.compFactory.CreatePos(self.GetCasterId())
        rotComp = self.compFactory.CreateRot(self.GetCasterId())
        rot = rotComp.GetRot()
        x, y, z = self.engineApi.GetDirFromRot(rot)
        startPos = posComp.GetPos()

        dim = engineApiGas.GetEntityDimensionId(self.GetCasterId())
        targets = serverApi.getEntitiesOrBlockFromRay(dim, startPos, (x, y, z), self.length, serverApi.GetMinecraftEnum().RayFilterType.OnlyEntities)

        targetId = None
        if targets and len(targets) > 0:
            for target in targets:
                type = target['type']
                entityId = target['entityId']

                if type == 'Entity':
                    targetId = entityId

        comp = serverApi.GetEngineCompFactory().CreatePlayer(self.GetCasterId())
        comp.PlayerAttackEntity(targetId)
