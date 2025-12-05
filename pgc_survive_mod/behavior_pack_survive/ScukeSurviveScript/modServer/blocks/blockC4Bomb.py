# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modServer.blocks.blockBase import BlockBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BlockC4Bomb(BlockBase):
	"""定时炸弹方块逻辑类"""
	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		super(BlockC4Bomb, self).__init__(severHandler, playerId, blockName, pos, dimension, param)
		engineApiGas.SetCommand("/playsound scuke_survive.block.time_bomb_build @a ~ ~ ~", self.mPlayerId, False)
		self.activeBoom = False
		self.activeChainBoom = True
		if self.mPlayerId:
			severHandler.NotifyToClient(self.mPlayerId, eventConfig.C4BombPlaceEvent, {"blockData": (pos, dimension)})
			bag = engineApiGas.GetPlayerAllItems(self.mPlayerId, 0)
			if "scuke_survive:c4_detonator" not in str(bag):
				engineApiGas.SetPopupNotice("", "需要手持C4 引爆器进行引爆")

	def Destroy(self, remove=False):
		if self.mPlayerId:
			self.SendMsgToClient(self.mPlayerId, eventConfig.C4BombRemoveEvent, {"blockData": (self.mPos, self.mDimension)})
		super(BlockC4Bomb, self).Destroy(remove)

	@EngineEvent()
	def ServerPlayerTryDestroyBlockEvent(self, args):
		if args["dimensionId"] == self.mDimension and (args["x"], args["y"], args["z"]) == self.mPos:
			if args["playerId"] != self.mPlayerId and args["fullName"] == self.mBlockName:
				args["cancel"] = True
				engineApiGas.NotifyOneMessage(args["playerId"], "§c你无法挖掘别人的炸弹")
				return

	@EngineEvent()
	def ExplosionServerEvent(self, args):
		thisData = [self.mPos[0], self.mPos[1], self.mPos[2], False]
		# 判定定时炸弹是否被爆炸破坏，如果是，先取消被炸掉，再触发一次爆炸
		Bool = thisData in args["blocks"] and True
		if Bool and not self.activeBoom and self.activeChainBoom:
			self.activeBoom = True
			v = args["blocks"].index(thisData)
			args["blocks"][v][3] = True
			engineApiGas.AddTimer(0.3, self.SetDetonateBlocks)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.BlocksClientSystem)
	def C4BombIgniteEvent(self, args):
		pid = args["igniter"]
		dim = args["dim"]
		if pid != self.mPlayerId and self.mPlayerId is not None: return
		if dim != self.mDimension: return
		dist = sum((a - b)**2 for a, b in zip(self.mPos, engineApiGas.GetEntityPos(pid)))
		if dist < 2500:
			self.SetDetonateBlocks()

	def DetectIsThisBlock(self, dim, pos, pid, blockName=None):
		if self.mPos != pos: return False
		if self.mDimension != dim: return False
		if blockName and self.mBlockName != blockName: return False
		if self.mPlayerId != pid:
			if self.mPlayerId is None:
				self.mPlayerId = pid
				return True
			engineApiGas.NotifyOneMessage(pid, "§c这个炸弹不属于你")
			return False
		return True

	def SetDetonateBlocks(self):
		"""设置方块爆炸"""
		engineApiGas.SetCommand("/playsound scuke_survive.block.time_bomb_boom @a %s %s %s" % self.mPos)
		playerList = serverApi.GetPlayerList()
		if self.mPlayerId not in playerList:
			# 随机一位玩家
			self.mPlayerId = playerList[0]
		# 执行爆炸逻辑
		radius = self.mCfg.get("explode_radius")
		fire = self.mCfg.get("fire")
		breaks = self.mCfg.get("breaks")
		# 后清除方块自身（否则可能会先销毁对象，导致无法往后执行逻辑）
		blockComp = compFactory.CreateBlockInfo(self.mLevelId)
		blockComp.SetBlockNew(self.mPos, itemsConfig.AirBlockDict, 0, self.mDimension)
		engineApiGas.AddTimer(0.05, serverApiMgr.CreateExplosion, self.mPlayerId, self.mPlayerId, self.mPos, radius, fire, breaks)

