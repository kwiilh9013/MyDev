# -*- encoding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from math import floor
from mod.common.utils.mcmath import Vector3

CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()


class ZombieCastSkillBreakBlock(CustomGoalCls):
    def __init__(self, entityId, argsJson):
        CustomGoalCls.__init__(self, entityId, argsJson)
        self.mEntityId = entityId
        self.mTimeCounter = 0
        self.mTargetBlockDestroyTime = 0

    # region 继承函数
    def CanUse(self):
        if self._HasTarget() and self._IsTargetAlive() and self._HasBlockBetweenTargetAndCanDestroyBlock():
            return True
        return False

    def CanContinueToUse(self):
        return self.CanUse()

    def CanBeInterrupted(self):
        return True

    def Start(self):
        self.mTimeCounter = 0
        self._FaceToTarget()
        self._ResetDestroyTime()

    def Stop(self):
        pass

    def Tick(self):
        self.mTimeCounter += 1
        time2destroy = self.mTimeCounter >= int(self.mTargetBlockDestroyTime * 30)

        if time2destroy:
            self._DestroyFrontBlock()
            self._ResetDestroyTime()

    # endregion

    # region 类函数
    def _ResetDestroyTime(self):
        blockDict = self._GetFirstBlockFromRay()[0]
        self.mTargetBlockDestroyTime = self._GetTargetBlockDestroyTime(blockDict['identifier'])

    def _HasTarget(self):
        #是否有仇恨目标
        comp = CompFactory.CreateAction(self.mEntityId)
        targetId = comp.GetAttackTarget()
        hasTarget = targetId != "-1"
        return hasTarget

    def _IsTargetAlive(self):
        comp = CompFactory.CreateAction(self.mEntityId)
        targetId = comp.GetAttackTarget()
        comp = CompFactory.CreateGame(serverApi.GetLevelId())
        alive = comp.IsEntityAlive(targetId)
        return alive

    # 跟目标之间是否存在方块并且是否能够破坏
    def _HasBlockBetweenTargetAndCanDestroyBlock(self):
        blockDictList = self._GetFirstBlockFromRay()
        if blockDictList is None or len(blockDictList) == 0:
            return False
        blockDict = blockDictList[0]
        blockPos = blockDict['pos']
        selfPos = CompFactory.CreatePos(self.mEntityId).GetFootPos()
        distance2block = (Vector3(blockPos) - Vector3(selfPos)).Length()
        if distance2block > 2:
            # 2 是手长，也就是只有够得到的方块才能够被破坏
            return False
            # 还需要检测手上的物品是否能够破坏掉方块
        destroyTotalTime = self._GetTargetBlockDestroyTime(blockDict['identifier'])
        canDestroy = destroyTotalTime > 0
        return canDestroy

    def _GetTargetBlockDestroyTime(self, blockIdentifier):
        blockInfoComp = CompFactory.CreateBlockInfo(self.mEntityId)
        carriedItem = CompFactory.CreateItem(self.mEntityId).GetEntityItem(
            serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        totalTime = blockInfoComp.GetDestroyTotalTime(blockIdentifier,
                                                      None if not carriedItem else carriedItem['itemName'])
        return totalTime

    # 面向目标
    def _FaceToTarget(self):
        comp = CompFactory.CreateAction(self.mEntityId)
        targetId = comp.GetAttackTarget()
        targetPosX, targetPosY, targetPosZ = CompFactory.CreatePos(targetId).GetFootPos()
        entityPosX, entityPosY, entityPosZ = CompFactory.CreatePos(self.mEntityId).GetFootPos()
        diffPos = (targetPosX - entityPosX, targetPosY - entityPosY, targetPosZ - entityPosZ)
        CompFactory.CreateRot(self.mEntityId).SetRot(serverApi.GetRotFromDir(diffPos))

    # 破坏生物面前的方块
    def _DestroyFrontBlock(self):
        blockDictList = self._GetFirstBlockFromRay()
        if blockDictList:
            blockDict = blockDictList[0]
            blockPos = blockDict['pos']
            blockInfoComp = CompFactory.CreateBlockInfo(self.mEntityId)
            dimensionId = CompFactory.CreateDimension(self.mEntityId).GetEntityDimensionId()
            destroyTotalTime = self._GetTargetBlockDestroyTime(blockDict['identifier'])
            if destroyTotalTime > 0:
                blockInfoComp.SetBlockNew(blockPos, {'name': 'minecraft:air'}, 1, dimensionId)

    # 获得视线范围内第一个方块信息
    def _GetFirstBlockFromRay(self):
        dimensionId = CompFactory.CreateDimension(self.mEntityId).GetEntityDimensionId()
        comp = CompFactory.CreateAction(self.mEntityId)
        targetId = comp.GetAttackTarget()
        targetPosX, targetPosY, targetPosZ = CompFactory.CreatePos(targetId).GetFootPos()
        entityPosX, entityPosY, entityPosZ = CompFactory.CreatePos(self.mEntityId).GetFootPos()

        # 这里获取碰撞箱的高度，因为 FootPos 是从脚底开始计算的坐标，这里加上碰撞箱 -0.2 模拟的是头部眼睛的高度
        _, collisionBoxHeight = CompFactory.CreateCollisionBox(self.mEntityId).GetSize()
        _, targetCollisionBoxHeight = CompFactory.CreateCollisionBox(targetId).GetSize()

        targetPosY = targetPosY + targetCollisionBoxHeight - 0.2
        entityPosY = entityPosY + collisionBoxHeight - 0.2

        rot = (targetPosX - entityPosX, targetPosY - entityPosY, targetPosZ - entityPosZ)
        distance = int(Vector3(rot).Length() - 1)   # 这个地方用小数会非常卡，所以取一个 int，主要是防止射线击穿实体

        blockDictList = serverApi.getEntitiesOrBlockFromRay(
            dimensionId, (entityPosX, entityPosY, entityPosZ), rot, distance, False,
            serverApi.GetMinecraftEnum().RayFilterType.OnlyBlocks
        )

        return blockDictList