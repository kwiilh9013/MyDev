# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.blocks.blockBase import BlockBase
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BlockLandmine(BlockBase):
	"""地雷逻辑类"""
	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		super(BlockLandmine, self).__init__(severHandler, playerId, blockName, pos, dimension, param)
		pass

	def Destroy(self, remove=False):
		super(BlockLandmine, self).Destroy(remove)
		pass
	
	# region 事件
	@EngineEvent()
	def StepOnBlockServerEvent(self, args):
		"""实体移动到实心方块事件"""
		entityId = args.get("entityId")
		# 对摆放的玩家不造成伤害
		if entityId != self.mPlayerId:
			blockName = args.get("blockName")
			if blockName == self.mBlockName:
				dimension = args.get("dimensionId")
				pos = (args.get("blockX"), args.get("blockY"), args.get("blockZ"))
				if dimension == self.mDimension and pos == self.mPos:
					# 有实体踩到方块
					# 爆炸
					self.SetDetonateBlocks(entityId)
		pass
	# endregion

	def SetDetonateBlocks(self, entityId):
		"""设置方块爆炸"""
		# 判断实体是否有血量，如果有，就进行爆炸
		attrComp = compFactory.CreateAttr(entityId)
		health = attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
		if health > 0:
			if not self.IsCheck(entityId):
				return
			playerList = serverApi.GetPlayerList()
			if self.mPlayerId not in playerList:
				# 随机一位玩家
				self.mPlayerId = playerList[0]
			# 执行爆炸逻辑
			radius = self.mCfg.get("explode_radius")
			fire = self.mCfg.get("fire")
			breaks = self.mCfg.get("breaks")
			serverApiMgr.CreateExplosion(self.mPlayerId, self.mPlayerId, self.mPos, radius, fire, breaks)
			# 后清除方块自身（否则可能会先销毁对象，导致无法往后执行逻辑）
			blockComp = compFactory.CreateBlockInfo(self.mLevelId)
			blockComp.SetBlockNew(self.mPos, itemsConfig.AirBlockDict, 0, self.mDimension)
		pass
