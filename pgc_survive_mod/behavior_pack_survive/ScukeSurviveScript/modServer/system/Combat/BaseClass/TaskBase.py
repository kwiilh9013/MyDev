# -*- coding: utf-8 -*-


class TaskBase(object):
    def __init__(self, skill):
        super(TaskBase, self).__init__()

        self.skill = skill
        self.context = skill.context
        self.system = skill.system
        self.engineApi = self.system.engineApi
        self.compFactory = self.engineApi.GetEngineCompFactory()
        self.timeline = None
        self.bSingleFrame = False
        self.StartFrame = 0
        self.EndFrame = 0

    def InitTask(self, timeline, bSingleFrame=False, StartFrame=0, EndFrame=0, params={}):
        self.timeline = timeline
        self.bSingleFrame = bSingleFrame
        self.StartFrame = StartFrame
        self.EndFrame = EndFrame
        self.timeline.add_node(self.StartFrame, lambda: self.BaseOnTaskStart())
        self.timeline.add_node(self.EndFrame, lambda: self.BaseOnTaskEnd())
        for (key, value) in params.items():
            setattr(self, key, value)

    def BaseOnTaskStart(self):
        print '[CombatSystem] TaskBase BaseOnTaskStart'
        self.skill.active_task.add(self)
        self.OnTaskStart()

    def BaseOnTaskEnd(self):
        print '[CombatSystem] TaskBase BaseOnTaskEnd'
        self.skill.active_task.discard(self)
        self.OnTaskEnd()

    def OnTaskStart(self):
        pass

    def OnTaskUpdate(self, frame):
        pass

    def OnTaskEnd(self):
        pass

    def GetCasterId(self):
        return self.skill.GetCasterId()