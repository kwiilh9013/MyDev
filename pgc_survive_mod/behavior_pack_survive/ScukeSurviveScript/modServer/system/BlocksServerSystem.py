# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modCommon.cfg.items import itemsClassConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BlocksServerSystem(BaseServerSystem):
	"""方块 服务端"""
	def __init__(self, namespace, systemName):
		super(BlocksServerSystem, self).__init__(namespace, systemName)

		# 监听方块破坏的列表，用于防止重复监听
		self._listenRemoveBlocks = []
		# 方块对象列表: {(dim, pos): obj}
		self._blockObjDict = {}

		self._blockComp = compFactory.CreateBlockInfo(self.mLevelId)

		self._eventFunctions = {
			"detonate_block": self.SetDetonateBlocks
		}

		Instance.mEventMgr.RegisterEvent(eventConfig.DetonateExplodeBlockEvent, self.SubscriptDetonateExplodeBlockEvent)
		pass

	def Destroy(self):
		super(BlocksServerSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.DetonateExplodeBlockEvent, self.SubscriptDetonateExplodeBlockEvent)
		for obj in self._blockObjDict.values():
			obj.Destroy()
		self._blockObjDict.clear()
		self._listenRemoveBlocks = None
		pass

	# region 事件
	@EngineEvent()
	def ChunkLoadedServerEvent(self, args):
		"""区块加载事件"""
		dimension = args.get("dimension")
		blockEntities = args.get("blockEntities")
		# 格式: [{blockName, posX, posY, posZ}]
		if blockEntities:
			# 过滤方块实体，创建逻辑对象
			for blockEntity in blockEntities:
				blockName = blockEntity.get("blockName")
				pos = (blockEntity.get("posX"), blockEntity.get("posY"), blockEntity.get("posZ"))
				self.CreateBlockObj(None, blockName, pos, dimension)
				pass
		pass

	@EngineEvent()
	def EntityPlaceBlockAfterServerEvent(self, args):
		"""实体摆放方块事件"""
		entityId = args.get("entityId")
		fullName = args.get("fullName")
		dimension = args.get("dimensionId")
		pos = (args.get("x"), args.get("y"), args.get("z"))
		# 对特殊的方块进行转换，比如定时炸弹
		if fullName in itemsConfig.SpecialBlockDict:
			face = args["face"]
			fullName = itemsConfig.SpecialBlockDict[fullName][face]

			def _wait():
				blockDict = {"name": fullName, "aux": args["auxData"]}
				self._blockComp.SetBlockNew(pos, blockDict, 0, dimension)
				self.PlaceFunctionalBlockAfter(entityId, fullName, pos, dimension)
			engineApiGas.AddTimer(0.00, _wait)
		else:
			self.PlaceFunctionalBlockAfter(entityId, fullName, pos, dimension)

	@EngineEvent()
	def ProjectileDoHitEffectEvent(self, args):
		"""抛射物碰撞事件"""
		projectileId = args.get("id")
		hitTargetType = args.get("hitTargetType")
		if hitTargetType == "BLOCK":
			# 获取方块id
			pos = (args.get("blockPosX"), args.get("blockPosY"), args.get("blockPosZ"))
			dimension = engineApiGas.GetEntityDimensionId(projectileId)
			engineComp = compFactory.CreateEngineType(projectileId)
			engineTypeStr = engineComp.GetEngineTypeStr()
			canDetonate = itemsConfig.IsDetonateProjectileType(engineTypeStr)
			if canDetonate:
				if engineTypeStr == itemsConfig.Arrow:
					# 额外判断是否着火
					canDetonate = engineApiGas.IsEntityOnFire(projectileId)
				if canDetonate:
					# 引爆
					srcId = args.get("srcId")
					info = {
						"cause": "fire_projectile", "pos": pos, "dimension": dimension, "playerId": srcId,
					}
					self.SetDetonateBlocks(info)
		pass

	@EngineEvent()
	def PistonActionServerEvent(self, args):
		"""活塞推动方块事件"""
		dimensionId = args.get("dimensionId")
		blockList = args.get("blockList")
		if blockList and args.get("cancel") is not True:
			# 如果是有代码逻辑的方块，则取消推动
			for block in blockList:
				isCancel = False
				for key, obj in self._blockObjDict.iteritems():
					if key[0] == dimensionId and key[1] == tuple(block):
						isCancel = True
						args["cancel"] = True
						break
				if isCancel:
					break
		pass

	def SubscriptDetonateExplodeBlockEvent(self, args):
		"""引爆方块事件，订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region 引爆器
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.BlocksClientSystem)
	def C4BombIgniteEvent(self, args):
		pid = args["igniter"]
		item = engineApiGas.GetPlayerItem(pid, 2, 0)
		if item and item["newItemName"] == itemsConfig.ItemsNameEnum.C4Detonator:
			comp = compFactory.CreateItem(pid)
			dur = comp.GetItemDurability(2, 0) - 10
			if dur <= 10:
				comp.SetPlayerAllItems({(2, 0): {}})
				return
			comp.SetItemDurability(2, 0, dur)
	# endregion

	# region 方块爆炸
	def SetDetonateBlocks(self, args):
		"""设置方块爆炸"""
		# 获取方块id
		pos = args.get("pos")
		dimension = args.get("dimension")
		blockName = engineApiGas.GetBlockName(pos, dimension)
		cfg = itemsConfig.GetFunctionalBlockConfig(blockName)
		if cfg:
			# 判断引爆类型
			cause = args.get("cause")
			if cause in cfg.get("cause", []):
				playerId = args.get("playerId")
				playerList = serverApi.GetPlayerList()
				if playerId not in playerList:
					# 随机一位玩家
					playerId = playerList[0]
				# 清除方块自身
				block = self._blockComp.GetBlockNew(pos, dimension)
				if block and block.get("name") == blockName:
					self._blockComp.SetBlockNew(pos, itemsConfig.AirBlockDict, 0, dimension)
					# 执行爆炸逻辑
					radius = cfg.get("explode_radius")
					fire = cfg.get("fire")
					breaks = cfg.get("breaks")
					serverApiMgr.CreateExplosion(playerId, playerId, pos, radius, fire, breaks)
		pass
	# endregion


	# region 创建对象
	def CreateBlockObj(self, playerId, blockName, pos, dimension):
		"""创建方块对象"""
		clazz = itemsClassConfig.GetItemsClass(blockName)
		if clazz:
			# 监听方块破坏
			if blockName not in self._listenRemoveBlocks:
				self._listenRemoveBlocks.append(blockName)
				self._blockComp.ListenOnBlockRemoveEvent(blockName, True)
			# 创建对象
			key = (dimension, pos)
			obj = self._blockObjDict.get(key)
			if not obj:
				blockObj = clazz(self, playerId, blockName, pos, dimension)
				self._blockObjDict[key] = blockObj
				obj = blockObj
			return obj
		return None

	def ClearBlockObjDict(self, pos, dimension):
		"""清除方块对象字典数据，由方块对象调用"""
		key = (dimension, pos)
		self._blockObjDict.pop(key, None)
		pass
	# endregion

	# region 摆放功能方块
	def PlaceFunctionalBlockAfter(self, playerId, blockName, pos, dimension):
		"""摆放方块"""
		cfg = itemsConfig.GetFunctionalBlockConfig(blockName)
		if cfg:
			# 创建对象
			return self.CreateBlockObj(playerId, blockName, pos, dimension)
		return None
	# endregion
