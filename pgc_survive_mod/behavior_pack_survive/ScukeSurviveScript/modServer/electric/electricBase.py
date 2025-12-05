# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.cfg.electric import electricConfig
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ElectricBase(CommonEventRegister):
	"""电器逻辑 基类"""
	def __init__(self, severHandler, blockName, pos, dimension, param={}):
		CommonEventRegister.__init__(self, severHandler)
		self.mServer = severHandler
		self.mLevelId = self.mServer.mLevelId
		self.mBlockName = blockName
		self.mPos = pos
		self.mDimension = dimension
		
		# 获取config，设置参数
		self.mCfg = electricConfig.GetElectricConfig(blockName)

		# 开启、关闭状态
		self.mWorkState = False

		# 唯一的key，用于服务端、客户端校验是否是同一个方块
		self.mKey = "{}{}{}{}{}".format(self.mBlockName.replace(modConfig.ModNameSpace + ":electric_", ""), self.mDimension, self.mPos[0], self.mPos[1], self.mPos[2])
		self.mKey = self.mKey.replace("_", "")
		
		self.mBlockDataComp = compFactory.CreateBlockEntityData(self.mLevelId)
		pass

	def Destroy(self, breaks=False):
		CommonEventRegister.OnDestroy(self)
		# 存储数据
		if breaks is False:
			self.SaveBlockData()
		if self.mServer:
			self.mServer.ClearElectricObjDict(self.mPos, self.mDimension)
		self.mServer = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def DestroyBlockEvent(self, args):
		"""方块销毁事件"""
		blockName = args.get("fullName")
		dimension = args.get("dimensionId")
		pos = (args.get("x"), args.get("y"), args.get("z"))
		if blockName == self.mBlockName and dimension == self.mDimension and pos == self.mPos:
			self.Destroy(breaks=True)
		pass
	# endregion

	def SendUIInfo(self, info):
		"""发送UI信息到附近玩家的客户端"""
		playerList = serverApiMgr.GetNearbyPlayerList(self.mDimension, self.mPos, 16)
		self.SendMsgToMultiClient(playerList, eventConfig.ElectricEvent, info)
		pass

	# region 数据存储
	def LoadBlockData(self):
		"""加载方块数据"""
		data = None
		blockData = self.mBlockDataComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[electricConfig.BlockEntityDataKey]
			if not data:
				data = {}
		# 由子类重写
		pass

	def SaveBlockData(self):
		"""保存方块数据"""
		# 由子类重写
		pass

	def GetDataObj(self):
		"""获取数据对象"""
		blockData = self.mBlockDataComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[electricConfig.BlockEntityDataKey]
			if not data:
				data = {}
			return data
		return None
	# endregion
