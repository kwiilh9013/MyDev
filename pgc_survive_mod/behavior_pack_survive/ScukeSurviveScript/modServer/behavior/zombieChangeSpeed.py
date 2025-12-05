# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from mod.common.utils.mcmath import Vector3
from math import floor, sqrt
CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()


class ZombieChangeSpeed(CustomGoalCls):
    def __init__(self, entityId, argsJson):
        CustomGoalCls.__init__(self, entityId, argsJson)

        self.mEntityId = entityId
        self.mTargetID = '-1'
        self.baseSpeed = None
        self._initSpeed = False

    def CanUse(self):
        targetId = self._GetTarget()
        if targetId != '-1' and targetId != self.mTargetID:
            self.mTargetID = targetId
            return True
        if targetId == '-1' and self.mTargetID != '-1':
            self.mTargetID = targetId
            return True
        return False

    def CanContinueToUse(self):
        return False

    def CanBeInterrupted(self):
        return False

    def Start(self):
        # Phase会修改速度，时序问题不能在behavior init的时候拿速度
        if not self._initSpeed:
            attrComp = serverApi.GetEngineCompFactory().CreateAttr(self.mEntityId)
            self.baseSpeed = attrComp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.SPEED)
            self._initSpeed = True

        attrComp = serverApi.GetEngineCompFactory().CreateAttr(self.mEntityId)

        tagComp = serverApi.GetEngineCompFactory().CreateTag(self.mTargetID)
        tagList = tagComp.GetEntityTags()

        if self.mTargetID == '-1':
            attrComp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.SPEED, self.baseSpeed)
            return

        if "Highlight" in tagList:
            attrComp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.SPEED, self.baseSpeed * 1.5)
        elif "Attractor" in tagList:
            attrComp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.SPEED, self.baseSpeed * 2.0)
        else:
            attrComp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.SPEED, self.baseSpeed)

    def Stop(self):
        pass

    def Tick(self):
        pass

    def _GetTarget(self):
        # 是否有仇恨目标
        comp = CompFactory.CreateAction(self.mEntityId)
        targetId = comp.GetAttackTarget()
        return targetId
