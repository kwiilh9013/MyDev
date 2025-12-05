# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.TaskBase import TaskBase
from ScukeSurviveScript.modServer.system.Combat.BaseClass.ContextBase import ContextBase
TaskDirectory = "ScukeSurviveScript.modServer.system.Combat.Task."


class SkillBase(object):
    def __init__(self, system, context):
        super(SkillBase, self).__init__()

        self.system = system
        self.engineApi = system.engineApi
        self.compFactory = self.engineApi.GetEngineCompFactory()
        self.context = context

        self.task_list = set()
        self.active_task = set()

        self.timeline = None
        self.skill_config = None
        self.skill_id = 0
        self.name = ''

    def InitSkill(self, skill_config):
        self.skill_config = skill_config
        print "[CombatSystem] InitSkill", skill_config
        self.skill_id = skill_config['skill_id']
        self.name = skill_config['name']

        timeline_config = skill_config['timeline']
        self.timeline = self.system.GetTimelineManager().CreateTimeline(timeline_config['total_frame'], 0,
            lambda: self.OnSkillStart(), lambda frame: self.OnSkillUpdate(frame), lambda: self.OnSkillEnd())

        task_config = timeline_config['task_list']
        if task_config:
            for task_item in task_config:
                task_class_str = task_item['class']
                task_params = task_item['params']
                task_start_frame = task_item['start_frame']
                task_end_frame = task_item['end_frame']
                task_class_name = "Combat"+task_class_str+"Task"
                task_class_module = None  # importlib.import_module(TaskDirectory+task_class_name)

                task_class = getattr(task_class_module, task_class_name)
                task = task_class(self)
                task.InitTask(self.timeline, False, task_start_frame, task_end_frame, task_params or {})
                self.task_list.add(task)

    def DoSkill(self):
        self.timeline.start()

    def OnSkillStart(self):
        print "[CombatSystem] OnSkillStart", self.name
        pass

    def OnSkillUpdate(self, frame):
        for task in self.active_task:
            task.OnTaskUpdate(frame)

    def OnSkillEnd(self):
        print "[CombatSystem] OnSkillEnd", self.name
        for task in self.task_list:
            del task
        skillBasicContext = ContextBase.GetContextByClassName(self.context, "SkillBasicContext")
        self.system.GetSkillServerMgr().SkillFinish(skillBasicContext.source_entity_id)

    def GetCasterId(self):
        skillBasicContext = ContextBase.GetContextByClassName(self.context, "SkillBasicContext")
        return skillBasicContext.source_entity_id
