# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common.Timeline.Timeline import Timeline


class TimelineManager(object):
    def __init__(self):
        self.nextId = 0
        self.mTimelines = {}

    def __del__(self):
        for (_, timeline) in self.mTimelines.items():
            del timeline
        self.mTimelines.clear()

    def CreateTimeline(self, end_time, start_time=0, on_start_func=None, on_update_func=None, on_finish_func=None, can_eternal_update=False):
        Id = self.nextId
        self.nextId += 1

        def wrap_on_finish_func():
            if on_finish_func:
                on_finish_func()
            if not can_eternal_update:
                self.RemoveTimeline(Id)

        timeline = Timeline(end_time, start_time, on_start_func, on_update_func, wrap_on_finish_func, can_eternal_update)
        self.mTimelines[Id] = timeline

        return timeline

    def RemoveTimeline(self, Id):
        if Id in self.mTimelines:
            del self.mTimelines[Id]

    def GetTimeline(self, Id):
        if Id in self.mTimelines:
            return self.mTimelines[Id]

    def Update(self):
        for (_, timeline) in self.mTimelines.items():
            timeline.update()