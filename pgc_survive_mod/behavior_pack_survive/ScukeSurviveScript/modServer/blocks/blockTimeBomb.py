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


class BlockTimeBomb(BlockBase):
	"""定时炸弹方块逻辑类"""
	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		super(BlockTimeBomb, self).__init__(severHandler, playerId, blockName, pos, dimension, param)
		self.hasDestroy = False
		self.totalTime = 0
		self.leftTime = 0
		self.clickTime = 0
		self.activeBoom = False
		# 倒计时是否存盘，如果开启，重进地图后，倒计时继续，否则取消倒计时
		self.saveLeftTime = True
		engineApiGas.AddTimer(1.0, self.Timer)
		if self.saveLeftTime:
			self.LoadBlockdata()
		# 是否启动连锁爆炸，即如果多个定时炸弹在附近，一个爆炸后会引起其他的一起爆炸
		self.activeChainBoom = True
		engineApiGas.SetCommand("/playsound scuke_survive.block.time_bomb_build @a ~ ~ ~", self.mPlayerId, False)

	def Destroy(self, remove=False):
		self.hasDestroy = True
		self.SaveBlockData()
		super(BlockTimeBomb, self).Destroy(remove)

	@EngineEvent()
	def ServerItemUseOnEvent(self, args):
		"""对方块使用物品事件"""
		blockName = args.get("blockName")
		if blockName == self.mBlockName:
			pos = (args["x"], args["y"], args["z"])
			if pos == self.mPos:
				pid = args["entityId"]
				s = compFactory.CreatePlayer(pid).isSneaking()
				if not s:
					args["ret"] = True

	@EngineEvent()
	def ServerBlockUseEvent(self, args):
		if not self.DetectIsThisBlock(args["dimensionId"], (args["x"], args["y"], args["z"]), args["playerId"]):
			return
		t = time.time()
		if t - self.clickTime < 1.0:return
		self.clickTime = t
		args["cancel"] = True
		param = {"pos": self.mPos, "dim": self.mDimension, "owner": self.mPlayerId}
		self.SendMsgToClient(self.mPlayerId, eventConfig.OpenTimeBombScreenEvent, param)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.BlocksClientSystem)
	def TimeBombSetTimeEvent(self, args):
		if not self.DetectIsThisBlock(args["dim"], args["pos"], args["owner"]):
			return
		totalTime = args["totalTime"]
		self.leftTime = totalTime
		self.totalTime = totalTime
		self.SyncStatus(args["pos"], args["dim"], totalTime)

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
		Bool = thisData in args["blocks"] and (self.leftTime >= 0.5 or self.totalTime == 0)
		if Bool and not self.activeBoom and self.activeChainBoom:
			self.activeBoom = True
			v = args["blocks"].index(thisData)
			args["blocks"][v][3] = True
			engineApiGas.AddTimer(0.3, self.SetDetonateBlocks)

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

	def SyncStatus(self, pos, dim, t):
		param = {
			"stage": "set_block",
			"pos": pos,
			"dimension": dim,
			"molangValue": {
				"variable.total_time": t,
				"variable.left_time": t,
				"variable.has_set_time": 1.0
			}
		}
		Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, param)
		self.SendMsgToAllClient(eventConfig.TimeBombSyncStatusEvent, {"pos": pos, "dim": dim, "time": t})

	def Timer(self):
		self.leftTime = int(max(self.leftTime - 1, 0))
		if self.leftTime <= 0 and self.totalTime != 0:
			self.SetDetonateBlocks()
			return
		if not self.hasDestroy:
			engineApiGas.AddTimer(1.0, self.Timer)
			if self.totalTime != 0:
				self.SyncStatus(self.mPos, self.mDimension, self.leftTime)

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

	def LoadBlockdata(self):
		blockEntityComp = compFactory.CreateBlockEntityData(self.mLevelId)
		blockData = blockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[itemsConfig.BlockEntityDataKey]
			if data:
				t = data.get("leftTime")
				if t:
					self.leftTime = t
					self.totalTime = t

	def SaveBlockData(self):
		if not self.saveLeftTime:return
		blockEntityComp = compFactory.CreateBlockEntityData(self.mLevelId)
		blockData = blockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[itemsConfig.BlockEntityDataKey]
			if data:
				data["leftTime"] = self.leftTime
				blockData[itemsConfig.BlockEntityDataKey] = data
