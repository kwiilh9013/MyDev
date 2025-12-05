# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.blocks.blockBase import BlockBase
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()

_ReviveTickTime = 1.0

class BlockTombStone(BlockBase):
	"""墓碑逻辑类"""

	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		super(BlockTombStone, self).__init__(severHandler, playerId, blockName, pos, dimension, param)
		self._leftTime = 0
		self._identifier = None
		self._rot = (0, 0)
		self.ReadBlockData()
		self._timer = engineApiGas.AddRepeatTimer(_ReviveTickTime, self.UpdateReviveTimer)

	def SetReviveData(self, identifier, leftTime, rot):
		self._identifier = identifier
		self._leftTime = leftTime
		self._rot = rot
		self.SaveBlockData()
		if self._timer:
			engineApiGas.CancelTimer(self._timer)
			self._timer = None
		self._timer = engineApiGas.AddRepeatTimer(_ReviveTickTime, self.UpdateReviveTimer)

	def UpdateReviveTimer(self):
		if self._leftTime > 0:
			if self._identifier is not None and (int(self._leftTime) % 10 == 0 or self._leftTime < 30):
				self.mServer.BroadcastToAllClient('ShowBlockInfo', {
					'pos': self.mPos,
					'dim': self.mDimension,
					'type': 'followHud',
					'active': True,
					'offset': (0.5, 1.6, 0.5),
					'msg': '§l%s §r还剩§l%d§r秒复活' % (engineApiGas.GetChinese("entity.{}.name".format(self._identifier)), int(self._leftTime))
				})
			self._leftTime -= _ReviveTickTime
			if self._leftTime <= 0:
				self.DoRevive()
			else:
				self.SaveBlockData()
		else:
			engineApiGas.CancelTimer(self._timer)
			self._timer = None
			self.SaveBlockData()

	def DoRevive(self):
		if self._identifier is not None:
			self.mServer.CreateEngineEntityByTypeStr(self._identifier, self.mPos, tuple(self._rot), self.mDimension)
			self._identifier = None
		self.mServer.BroadcastToAllClient('ShowBlockInfo', {
			'pos': self.mPos,
			'dim': self.mDimension,
			'type': 'followHud',
			'active': False,
		})


	def Destroy(self, remove=False):
		if remove:
			if self._identifier is not None:
				engineApiGas.AddTimer(0, self.DelayReplace)
			return
		super(BlockTombStone, self).Destroy(remove)
		if self._timer:
			engineApiGas.CancelTimer(self._timer)
			self._timer = None
		self.mServer.BroadcastToAllClient('ShowBlockInfo', {
			'pos': self.mPos,
			'dim': self.mDimension,
			'type': 'followHud',
			'active': False,
		})

	def DelayReplace(self):
		if engineApiGas.SetBlockNew(self.mPos, {'name': self.mBlockName}, dimensionId=self.mDimension):
			engineApiGas.SetBlockStates(self.mPos, {'direction': ((self._rot[1] + 360) // 90) % 4}, self.mDimension)
		self.SavePlayerId()
		self.SaveBlockData()

	# region 事件
	# endregion

	def SaveBlockData(self):
		blockData = self.mBlockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[itemsConfig.BlockEntityDataKey]
			if data:
				data["leftTime"] = self._leftTime
				data["identifier"] = self._identifier
				data["rot"] = self._rot
				blockData[itemsConfig.BlockEntityDataKey] = data

	def ReadBlockData(self):
		blockData = self.mBlockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[itemsConfig.BlockEntityDataKey]
			if data:
				self._leftTime = data.get('leftTime', 0)
				self._identifier = data.get('identifier', None)
				self._rot = data.get('rot', (0, 0))
