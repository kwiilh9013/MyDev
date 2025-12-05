# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.TaskBase import TaskBase


class CombatDashTask(TaskBase):
    def __init__(self, skill):
        super(CombatDashTask, self).__init__(skill)

    def OnTaskStart(self):
        self.rotComp = self.compFactory.CreateRot(self.GetCasterId())
        self.motionComp = self.compFactory.CreateActorMotion(self.GetCasterId())

    def OnTaskUpdate(self, frame):
        if self.dir == "face":
            rot = self.rotComp.GetRot()
            x,y,z = self.engineApi.GetDirFromRot(rot)
            self.motionComp.SetPlayerMotion((x*self.speed, y*self.speed, z*self.speed))
        elif self.dir == "up":
            self.motionComp.SetPlayerMotion((0, self.speed, 0))
