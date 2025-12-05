# -*- encoding: utf-8 -*-
import random
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modServer.randomEvents.randomEventBase import RandomEventBase
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon.cfg.randomEvent.spawnEntityConfig import GetSpawnEngineTypeStr, SpawnDistance
from ScukeSurviveScript.ScukeCore.server import engineApiGas
compFactory = serverApi.GetEngineCompFactory()


class SpawnEntityEvent(RandomEventBase):
	"""生成实体类 事件"""
	
	# region 生命周期、事件
	def Start(self):
		super(SpawnEntityEvent, self).Start()
		# 在目标前方附近，生成实体
		phaseSys = self.mSystem.GetPhaseSys()
		if not phaseSys:
			return
		
		targetPos = self.GetTargetPos()
		pos = self.GetSpawnPos(targetPos)
		if pos:
			# 生成怪物
			engineStr = GetSpawnEngineTypeStr(self.mEventType)
			if engineStr:
				phaseSys.SetSpawnMonsterFromAttrRatio(engineStr, self.mDimension, pos, (0, 0))

		# 结束事件
		self.End()
		pass

	def GetSpawnPos(self, targetPos):
		"""获取抛射物生成位置"""
		distance = SpawnDistance
		# 从目标正面发射过来
		rot = self.GetTargetRot()
		if not rot:
			return None
		rot = rot[1] + random.uniform(-45, 45)
		offset = commonApiMgr.GetNextPosByRot(targetPos, (0, rot), distance)
		y = engineApiGas.GetTopBlockHeight((offset[0], offset[2]), self.mDimension)
		if not y:
			return None
		return (offset[0], y + 1, offset[2])
