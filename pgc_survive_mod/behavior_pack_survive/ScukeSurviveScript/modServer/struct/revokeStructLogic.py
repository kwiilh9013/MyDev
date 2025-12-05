# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.modCommon.cfg.struct import buildStructConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class RevokeStructLogic(CommonEventRegister):
	"""撤销建筑逻辑 服务端"""
	def __init__(self, severHandler, playerId, structId, startPos, rotate, height=None):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		self._playerId = playerId
		self._startPos = startPos

		# 建筑数据
		structCfg = buildStructConfig.GetStructPaletteDict(structId)
		if not structCfg:
			self.Destroy()
			return
		
		volume = structCfg.get("volume", (1, 1, 1))
		# 计算结束位置
		self._endPos = self.GetEndPos(self._startPos, volume, rotate)
		# 如果是正在建造中的，则会传递height，则按照height来撤销
		if height is not None:
			self._endPos = (self._endPos[0], self._startPos[1] + height, self._endPos[2])

		# 所在维度
		self._dimension = engineApiGas.GetEntityDimensionId(self._playerId)

		self.cmdComp = compFactory.CreateCommand(self._levelId)
		
		# 封装指令集：每次只设置几层方块，分多次设置完
		self._cmdList = []
		height = self._startPos[1]
		while height <= self._endPos[1]:
			nextHeight = min(height + 3, self._endPos[1])
			cmd = "/fill {} {} {} {} {} {} air".format(self._startPos[0], height, self._startPos[2], self._endPos[0], nextHeight, self._endPos[2])
			self._cmdList.append(cmd)
			height = nextHeight + 1

		# 启动timer，开始撤销建筑
		self._revokeTimer = engineApiGas.AddRepeatTimer(0.1, self.RevokeStructTimer)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self._server = None
		if self._revokeTimer:
			engineApiGas.CancelTimer(self._revokeTimer)
			self._revokeTimer = None
		# 清除对象自己
		del self
		pass

	def RevokeStructTimer(self):
		"""tick撤销建筑"""
		if len(self._cmdList) > 0:
			cmd = self._cmdList.pop(0)
			self.cmdComp.SetCommand(cmd, self._playerId, True)
		else:
			# 结束逻辑
			self.Destroy()
		pass

	def GetEndPos(self, startPos, volume, rotate):
		"""获取建筑结束位置"""
		# 根据体积大小，获取结束位置
		offset = [volume[1] - 1, volume[2] - 1, volume[0] - 1]
		offset[0], offset[2] = self.GetXZByRotate(offset[0], offset[2], rotate)
		endPos = (
			startPos[0] + offset[0],
			startPos[1] + offset[1],
			startPos[2] + offset[2]
		)
		return endPos
	
	def GetXZByRotate(self, x, z, rot):
		"""根据旋转角度，获取新的位置，角度需是-90、0、90、180"""
		if rot == 90:
			# 交换位置、z取反
			x, z = -z, x
		elif rot == 180:
			# 取反
			x, z = -x, -z
		elif rot == -90:
			# 交换位置、x取反
			x, z = z, -x
		return x, z
