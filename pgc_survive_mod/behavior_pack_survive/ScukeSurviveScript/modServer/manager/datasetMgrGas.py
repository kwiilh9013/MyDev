# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.manager.commonMgr import CommonManager
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon import modConfig

compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
levelDataComp = compFactory.CreateExtraData(levelId)

class DatasetManagerGas(CommonManager):
	def __init__(self, system):
		super(DatasetManagerGas, self).__init__(system)
		self._dirtyData = False
		self._levelDataset = {}
		self.InitLevelData()


	def InitLevelData(self):
		self._levelDataset = levelDataComp.GetWholeExtraData()
		key = 'uid'
		cur = self.GetLevelData(key)
		if cur is None:
			self.SetLevelData(key, 0)

	def SetLevelData(self, key, data):
		key = modConfig.ModNameSpace + '_' + key
		self._dirtyData = True
		if data is None:
			if key in self._levelDataset:
				del self._levelDataset[key]
			levelDataComp.CleanExtraData(key)
			return
		self._levelDataset[key] = data
		levelDataComp.SetExtraData(key, data, False)

	def GetLevelData(self, key):
		if key is None:
			return None
		key = modConfig.ModNameSpace + '_' + key
		if key in self._levelDataset:
			return self._levelDataset[key]
		return levelDataComp.GetExtraData(key)

	def SetEntityData(self, entityId, key, data):
		key = modConfig.ModNameSpace + '_' + key
		dataComp = compFactory.CreateExtraData(entityId)
		if not dataComp:
			return False
		if data is None:
			dataComp.CleanExtraData(key)
			return dataComp.SaveExtraData()
		return dataComp.SetExtraData(key, data, True)

	def GetEntityData(self, entityId, key):
		if key is None:
			return None
		key = modConfig.ModNameSpace + '_' + key
		dataComp = compFactory.CreateExtraData(entityId)
		if not dataComp:
			return None
		return dataComp.GetExtraData(key)

	def CreateUid(self):
		key = 'uid'
		cur = self.GetLevelData(key)
		if cur is None:
			cur = 0
		cur += 1
		self.SetLevelData(key, cur)
		return cur

	def BuildKey(self, tag=None):
		if tag:
			return '%s_%d' % (tag, self.CreateUid())
		return '%d' % (self.CreateUid())


	def FlushLevelData(self):
		if self._dirtyData:
			levelDataComp.SaveExtraData()
			self._dirtyData = False