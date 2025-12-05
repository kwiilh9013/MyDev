# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modCommon.cfg.electric import electricClassConfig
from ScukeSurviveScript.modCommon.defines import electricEnum
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ElectricServerSystem(BaseServerSystem):
	"""电力系统 服务端"""
	def __init__(self, namespace, systemName):
		super(ElectricServerSystem, self).__init__(namespace, systemName)

		# 电器对象列表: {(dim, pos): obj}
		self._electricObjDict = {}

		self._eventFunctions = {
		}

		# Instance.mEventMgr.RegisterEvent(eventConfig.DetonateExplodeBlockEvent, self.SubscriptDetonateExplodeBlockEvent)
		pass

	def Destroy(self):
		super(ElectricServerSystem, self).Destroy()
		# Instance.mEventMgr.UnRegisterEvent(eventConfig.DetonateExplodeBlockEvent, self.SubscriptDetonateExplodeBlockEvent)
		for obj in self._electricObjDict.values():
			obj.Destroy()
		self._electricObjDict.clear()
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
				self.CreateElectricObj(blockName, pos, dimension)
				pass
		pass

	@EngineEvent()
	def EntityPlaceBlockAfterServerEvent(self, args):
		"""实体摆放方块事件"""
		fullName = args.get("fullName")
		dimension = args.get("dimensionId")
		pos = (args.get("x"), args.get("y"), args.get("z"))
		self.CreateElectricObj(fullName, pos, dimension)
		pass

	@EngineEvent()
	def ServerItemUseOnEvent(self, args):
		"""对方块使用物品事件"""
		blockName = args.get("blockName")
		clazz = electricClassConfig.GetElectricClass(blockName)
		if clazz and blockName != electricEnum.ElectricEnum.SpikeTrap:
			# 地刺不会执行逻辑
			args["ret"] = True
		pass

	@EngineEvent()
	def PistonActionServerEvent(self, args):
		"""活塞推动方块事件"""
		dimensionId = args.get("dimensionId")
		blockList = args.get("blockList")
		if blockList and args.get("cancel") is not True:
			# 如果是电器设备方块，则取消推动
			for block in blockList:
				isCancel = False
				for key, obj in self._electricObjDict.iteritems():
					if key[0] == dimensionId and key[1] == tuple(block):
						isCancel = True
						args["cancel"] = True
						break
				if isCancel:
					break
		pass
	# endregion


	# region 创建对象
	def CreateElectricObj(self, blockName, pos, dimension):
		"""创建电器对象"""
		clazz = electricClassConfig.GetElectricClass(blockName)
		if clazz:
			key = (dimension, pos)
			obj = self._electricObjDict.get(key)
			if not obj:
				blockObj = clazz(self, blockName, pos, dimension)
				self._electricObjDict[key] = blockObj
				self.GetElecticWorkState(dimension,pos)
		pass

	def ClearElectricObjDict(self, pos, dimension):
		"""清除方块对象字典数据，由方块对象调用"""
		key = (dimension, pos)
		self._electricObjDict.pop(key, None)
		pass

	# endregion

	# region 获取电器工作状态
	def GetElecticWorkState(self, dimension, pos):
		"""获取指定维度和位置的电器工作状态"""
		key = (dimension, pos)
		obj = self._electricObjDict.get(key, None)
		if obj:
			return obj.mWorkState
		return False
	# endregion