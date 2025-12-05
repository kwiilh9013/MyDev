# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
import ScukeSurviveScript.modCommon.cfg.illustration.illustrateMergeCfg as Illustrate
import mod.server.extraServerApi as serverApi
LEVEL_ID = serverApi.GetLevelId()
CMD = serverApi.GetEngineCompFactory().CreateCommand(LEVEL_ID).SetCommand
WORLD = serverApi.GetEngineCompFactory().CreateGame(LEVEL_ID)
MOB_TYPE = serverApi.GetEngineCompFactory().CreateEngineType
CreatingItem = serverApi.GetEngineCompFactory().CreateItem
CreatingExtraData = serverApi.GetEngineCompFactory().CreateExtraData


class IllustrateServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(IllustrateServerSystem, self).__init__(namespace, systemName)
		self._unlockServer = None
		self._memoryList = []
		# 玩家已解锁图鉴列表: {plrId: list}
		self._hasUnlockDict = {}
		self.GetSystem()

	def Update(self):
		pass

	def GetSystem(self):
		Dict = Illustrate.GetAllData()
		valueList = Dict.values()
		mergeList = reduce(lambda x, y: x + y, valueList)
		for i in mergeList:
			if i and type(i) == dict and "id" in i:
				self._memoryList.append(i['id'])

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.IllustrateClientSystem)
	def func3(self, args):
		pass

	@EngineEvent()
	def ClientLoadAddonsFinishServerEvent(self, args):
		pid = args['playerId']
		self._hasUnlockDict.update({pid: []})
		Data = CreatingExtraData(pid).GetExtraData("scukeSurviveIllustrateUnlockData")
		if Data and type(Data) == list:
			self._hasUnlockDict.update({pid: Data})
		self.NotifyToClient(pid, "UpdateUnlockList", {"list": self._hasUnlockDict[pid]})

	@EngineEvent()
	def InventoryItemChangedServerEvent(self, args):
		pid = args['playerId']
		oldItem, newItem = args['oldItemDict'], args['newItemDict']
		if newItem and newItem['newItemName']:
			Name = newItem['newItemName']
			if Name in self._memoryList:
				if pid not in self._hasUnlockDict:
					self.ClientLoadAddonsFinishServerEvent({'playerId': pid})
					return
				if Name not in self._hasUnlockDict[pid]:
					self.NotifyToClient(pid, "UnlockIllustrate", {"name": Name, "type": "item"})
					self._hasUnlockDict[pid].append(Name)

	@EngineEvent()
	def DamageEvent(self, args):
		plrList = serverApi.GetPlayerList()
		if args['srcId'] and args['srcId'] in plrList:
			pid = args['srcId']
			TypeStr = MOB_TYPE(args['entityId']).GetEngineTypeStr()
			if TypeStr in self._memoryList:
				if pid not in self._hasUnlockDict:
					self.ClientLoadAddonsFinishServerEvent({'playerId': pid})
					return
				if TypeStr not in self._hasUnlockDict[pid]:
					self.NotifyToClient(pid, "UnlockIllustrate", {"name": TypeStr, "type": "mob"})
					self._hasUnlockDict[pid].append(TypeStr)

	@EngineEvent()
	def PlayerLeftMessageServerEvent(self, args):
		pid = args['id']
		if pid in self._hasUnlockDict:
			CreatingExtraData(pid).SetExtraData("scukeSurviveIllustrateUnlockData", self._hasUnlockDict[pid])
			CreatingExtraData(pid).SaveExtraData()

	@EngineEvent()
	def PlayerIntendLeaveServerEvent(self, args):
		self.PlayerLeftMessageServerEvent({'id': args['playerId']})

