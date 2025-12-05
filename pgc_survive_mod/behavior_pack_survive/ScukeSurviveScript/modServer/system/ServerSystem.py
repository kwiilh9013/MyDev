# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import disassembleConfig, itemEMCConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas
import mod.server.extraServerApi as serverApi


class ServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(ServerSystem, self).__init__(namespace, systemName)
		self.Init()
		self.InitManager()
		self._cmdFunctions = {
			"/phase": self.PhaseCmd,
			"/attr": self.AttrCmd,
			"/event": self.EventCmd,
		}

	@EngineEvent()
	def LoadServerAddonScriptsAfter(self, args):
		"""加载服务端脚本完成事件"""
		# 在此做初始化逻辑
		# 自动合堆设置，当前版本该接口对爆炸破坏的掉落物不生效，可以开着，对玩家体验不会有什么影响
		gameComp = serverApi.GetEngineCompFactory().CreateGame(self.mLevelId)
		gameComp.SetMergeSpawnItemRadius(5.0)
		# 关闭客户端区块生成功能
		chunkComp = serverApi.GetEngineCompFactory().CreateChunkSource(self.mLevelId)
		chunkComp.OpenClientChunkGeneration(False)

		# 注册拆解台配方
		dusassenbleMod = "ScukeDisassembleMod"
		disassembleRecipesSystem = serverApi.GetSystem(dusassenbleMod, "{}RecipesServerSystem".format(dusassenbleMod))
		if disassembleRecipesSystem:
			DisassembleRecipes = disassembleConfig.GetDisassembleRecipes()
			for itemName in DisassembleRecipes:
				disassembleRecipesSystem.AddModRecipes(itemName, [DisassembleRecipes[itemName]])

		def LinkConversionTableEmcServer():
			# 注册EMC转换桌物品的EMC值
			ServerName = "LinkServer"
			modNameSpace = "scuke_convert_table"
			conversionTableLinkServer = serverApi.GetSystem(modNameSpace, ServerName)
			if conversionTableLinkServer:
				surviveItemEmc = itemEMCConfig.ItemsEMC
				conversionTableLinkServer.LinkEmcData("【惊变·星球生存】", surviveItemEmc)
		engineApiGas.AddTimer(3.0, LinkConversionTableEmcServer)
			
		pass

	# @AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	# def OnUiInitFinishedEvent(self, data):
	# 	pass

	def Init(self):
		pass

	def InitManager(self):
		from ScukeSurviveScript.modServer.manager.serverMgrList import ServerManagerList
		import re
		strinfo = re.compile(r'Gas$')
		for mgrCls in ServerManagerList:
			mgr = mgrCls(self)
			setattr(Instance, "m" + strinfo.sub("", mgrCls.__name__), mgr)

	def Update(self):
		Instance.mDatasetManager.FlushLevelData()

	# @EngineEvent()
	# def WillTeleportToServerEvent(self, args):
	# 	self.NotifyToClient(args['entityId'], 'OnWillTeleportToServerEvent', args)

	@EngineEvent()
	def CommandEvent(self, args):
		playerId = args.get("entityId")
		# 返回的cmd带有/
		command = args.get("command")
		cmdParam = command.split(" ")
		func = self._cmdFunctions.get(cmdParam[0])
		if func:
			args["cancel"] = True
			func(playerId, cmdParam)
			return
		if len(cmdParam) == 2 and cmdParam[0] == '/weather' and cmdParam[1] == 'clear':
			phaseSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PhaseServerSystem)
			phaseSystem._PlaceWeather(None)

	def PhaseCmd(self, playerId, cmdParam):
		"""阶段相关指令"""
		phaseSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PhaseServerSystem)
		lens = len(cmdParam)
		if lens == 3 and cmdParam[1] == "event":
			phaseSystem._PlaceEvent(cmdParam[2])
		if lens == 3 and cmdParam[1] == "weather":
			phaseSystem._PlaceWeather(cmdParam[2])

	def AttrCmd(self, playerId, cmdParam):
		"""属性相关指令"""
		attrSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		lens = len(cmdParam)
		if lens == 3:
			attrSystem.SetAttr(playerId, cmdParam[1], float(cmdParam[2]))

	def EventCmd(self, playerId, cmdParam):
		"""事件相关指令"""
		sys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.RandomEventServerSystem)
		lens = len(cmdParam)
		if lens == 2:
			sys.TriggerEvent(cmdParam[1], playerId)

