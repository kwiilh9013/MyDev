# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.items.foodsLogic import FoodsLogic
from ScukeSurviveScript.modServer.items.projectileLogic import ProjectileLogic
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ItemsServerSystem(BaseServerSystem):
	"""物品道具 服务端"""
	def __init__(self, namespace, systemName):
		super(ItemsServerSystem, self).__init__(namespace, systemName)

		self._eventFunctions = {
		}

		pass

	def Destroy(self):
		super(ItemsServerSystem, self).Destroy()
		pass

	# region 事件
	# @EngineEvent()
	# def LoadServerAddonScriptsAfter(self, args=None):
	# 	"""加载服务端脚本后事件"""
	# 	pass

	@EngineEvent()
	def AddServerPlayerEvent(self, args):
		"""玩家登录事件"""
		playerId = args.get("id")
		# 创建对象逻辑
		self.CreateFoodsLogicObj(playerId)
		self.CreateProjectileLogicObj(playerId)
		pass

	# @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.BuildStructClientSystem)
	# def BuildStructEvent(self, args):
	# 	"""一键建造事件"""
	# 	stage = args.get("stage")
	# 	func = self._eventFunctions.get(stage)
	# 	if func:
	# 		func(args)
	# 	pass
	# endregion
	

	# region 创建对象
	def CreateFoodsLogicObj(self, playerId):
		"""创建食物逻辑对象"""
		obj = FoodsLogic(self, playerId)
		return obj

	def CreateProjectileLogicObj(self, playerId):
		"""创建射击逻辑对象"""
		obj = ProjectileLogic(self, playerId)
		return obj

	# endregion
