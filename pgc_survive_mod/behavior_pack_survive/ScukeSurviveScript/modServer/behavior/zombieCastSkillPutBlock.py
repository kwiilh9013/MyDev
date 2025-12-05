# -*- encoding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from mod.common.utils.mcmath import Vector3
from math import floor, sqrt
CustomGoalCls = serverApi.GetCustomGoalCls()
CompFactory = serverApi.GetEngineCompFactory()


class ZombieCastSkillPutBlock(CustomGoalCls):
	def __init__(self, entityId, argsJson):
		CustomGoalCls.__init__(self, entityId, argsJson)

		self.mEntityId = entityId
		self.mTimeCounter = 0

		self.mDimensionId = CompFactory.CreateDimension(self.mEntityId).GetEntityDimensionId()

	def CanUse(self):
		if self._HasTarget() and self._IsTargetAlive() \
				and (abs(self._GetHeightDifferenceWithTarget()) >= 2.0 or self._CheckPathAheadForFooting()):
			return True
		return False

	def CanContinueToUse(self):
		return self.CanUse()

	def CanBeInterrupted(self):
		return True

	def Start(self):
		self.mTimeCounter = 0

	def Stop(self):
		pass

	def Tick(self):
		self.mTimeCounter += 1
		perSec = self.mTimeCounter % 20 == 0
		if perSec:
			self._PutBlockToTarget()

	def _HasTarget(self):
		# 是否有仇恨目标
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

	# 检查与目标之间是否存在高度差
	def _GetHeightDifferenceWithTarget(self):
		comp = CompFactory.CreateAction(self.mEntityId)
		targetId = comp.GetAttackTarget()
		if targetId != '-1':
			rider = CompFactory.CreateRide(targetId).GetEntityRider()
			if rider != '-1':  # 如果乘骑，使用乘骑物的entity坐标
				targetId = rider
		targetPos = CompFactory.CreatePos(targetId).GetFootPos()
		selfPos = CompFactory.CreatePos(self.mEntityId).GetFootPos()
		return targetPos[1] - selfPos[1]

	# 获取与目标水平方向上的距离
	def _GetHorizontalDifferenceWithTarget(self):
		comp = CompFactory.CreateAction(self.mEntityId)
		targetId = comp.GetAttackTarget()

		targetPos = CompFactory.CreatePos(targetId).GetFootPos()
		selfPos = CompFactory.CreatePos(self.mEntityId).GetFootPos()
		return sqrt((targetPos[0] - selfPos[0]) ** 2 + (targetPos[2] - selfPos[2]) ** 2)

	# 检查前往目标的路径，脚下是否有路
	def _CheckPathAheadForFooting(self):
		blockInfoComp = CompFactory.CreateBlockInfo(self.mEntityId)
		aheadBlockPos = self._GetPathAheadForFootingBlockPos()
		blockDict = blockInfoComp.GetBlockNew(aheadBlockPos, self.mDimensionId)
		return not blockDict or blockDict['name'] == 'minecraft:air'

	def _GetPathAheadForFootingBlockPos(self):
		comp = CompFactory.CreateAction(self.mEntityId)
		targetId = comp.GetAttackTarget()

		targetPosX, targetPosY, targetPosZ = CompFactory.CreatePos(targetId).GetFootPos()
		entityPosX, entityPosY, entityPosZ = CompFactory.CreatePos(self.mEntityId).GetFootPos()
		# 去掉 y 方向上的不同，因为我们是要检测的是目标前方脚下一格的位置
		diff = Vector3(targetPosX - entityPosX, 0, targetPosZ - entityPosZ).Normalized()
		result = (entityPosX + diff[0], entityPosY - 0.5, entityPosZ + diff[2])
		result = tuple(map(int, map(floor, result)))  # 把实体坐标转换成方块坐标
		FootResult = tuple(
			map(int, map(floor, (entityPosX + diff[0] * 0.1, entityPosY - 0.5, entityPosZ + diff[2] * 0.1))))
		if FootResult[0] == result[0] and FootResult[2] == result[2]:
			result = (entityPosX + diff[0] * 2, entityPosY - 0.5, entityPosZ + diff[2] * 2)
			result = tuple(map(int, map(floor, result)))  # 把实体坐标转换成方块坐标
		return result

	# 向目标搭建搭建方块
	def _PutBlockToTarget(self):
		if self._GetHeightDifferenceWithTarget() >= 1.0:
			# 第一种情况：存在高度差，那么就需要实体自己跳一下，然后在脚下搭建一个方块
			self._JumpAndPutBlockOnFoot()
		elif self._GetHeightDifferenceWithTarget() <= -1.0:
			self._DestroyBlockOnFoot()
		else:
			# 第二种情况：那就是在前方搭建一个方块
			self._PutBlockToAheadFoot()

	def _JumpAndPutBlockOnFoot(self):
		resBlockPos = CompFactory.CreatePos(self.mEntityId).GetFootPos()
		resBlockPos = tuple(map(int, map(floor, resBlockPos)))  # 把实体坐标转换成方块坐标
		# 先把自己弹起来
		actionComp = CompFactory.CreateAction(self.mEntityId)
		actionComp.SetMobKnockback(0, 0, 0.65, 0.65, 1)

		# 需要等待实体跳起来之后再放置方块
		# print "Put Block", resBlockPos
		CompFactory.CreateGame(self.mEntityId).AddTimer(0.3, self._PutBlock, resBlockPos, True)

	def _DestroyBlockOnFoot(self):
		resBlockPos = CompFactory.CreatePos(self.mEntityId).GetFootPos()
		resBlockPos = (resBlockPos[0], resBlockPos[1]-0.5, resBlockPos[2])

		aroundBlocks = []
		aroundBlocks.append(tuple(map(int, map(floor, resBlockPos))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0] + 0.4, resBlockPos[1], resBlockPos[2])))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0] - 0.4, resBlockPos[1], resBlockPos[2])))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0], resBlockPos[1], resBlockPos[2] + 0.4)))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0], resBlockPos[1], resBlockPos[2] - 0.4)))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0] + 0.4, resBlockPos[1], resBlockPos[2] + 0.4)))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0] + 0.4, resBlockPos[1], resBlockPos[2] - 0.4)))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0] - 0.4, resBlockPos[1], resBlockPos[2] + 0.4)))))
		aroundBlocks.append(tuple(map(int, map(floor, (resBlockPos[0] - 0.4, resBlockPos[1], resBlockPos[2] - 0.4)))))
		for block in aroundBlocks:
			self._PutBlock(block, False)


	def _PutBlockToAheadFoot(self):
		resBlockPos = self._GetPathAheadForFootingBlockPos()
		# print "Put Block Ahead"
		self._PutBlock(resBlockPos, True)

	def _PutBlock(self, resBlockPos, bPutorDestroy=True):
		if bPutorDestroy:
			CompFactory.CreateBlockInfo(self.mEntityId).SetBlockNew(resBlockPos, {'name': "minecraft:oak_log"}, 0,
																	self.mDimensionId)
		else:
			CompFactory.CreateBlockInfo(self.mEntityId).SetBlockNew(resBlockPos, {'name': 'minecraft:air'}, 1,
																	self.mDimensionId)