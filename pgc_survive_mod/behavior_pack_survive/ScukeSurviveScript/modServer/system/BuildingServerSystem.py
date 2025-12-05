# -*- coding: utf-8 -*-
import math
import random
import time

from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.buildingServerData import BuildingServerData, BuildingState, \
	BuildingTaskState, BuildingPosMarkerTaskState
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig, eventConfig
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon.cfg.buildingConfig import GetConfig as GetBuildingConfig
from ScukeSurviveScript.modCommon.cfg.buildingPlaceConfig import TransMarkerPos, GetMarkerPos, GetStructNameBase, InverseMarkerPos
from ScukeSurviveScript.modCommon.cfg.buildingPlaceConfig import Config as LargeBuildingConfig
from ScukeSurviveScript.modCommon.cfg.buildingPlaceConfig import GetMarkerConfig as GetBuildingMarkerConfig
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_old_booster import Config as Scuke_oldBooster
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_planet_booster import Config as Scuke_planetBooster

CompFactory = serverApi.GetEngineCompFactory()

ListenStructureFeatureList = [
]

AutoEngineEffectBuildings = {
	Scuke_planetBooster['identifier']: 'scuke_survive:pos3'
}

ShelterBornIdentifier = 'scuke_survive:@shelter_born'
ShelterArea = [
	{'pos': (419, 0, 190), 'face': 0},
	{'pos': (451, 26, 206), 'face': 0},
]

class BuildingTask(object):
	def __init__(self, uid, config, dim, pos, rot=0, startIndex=0):
		self._dim = dim
		self._config = config
		self._index = startIndex
		self._total = len(config['structures'])
		self._pos = pos
		self._tickCount = 0
		self._tickStep = 2
		self._uid = uid
		self._rot = rot
		self._areaUid = 'area_'+str(self._uid)

		self._levelId = serverApi.GetLevelId()
		self._gameComp = CompFactory.CreateGame(self._levelId)
		self._chunckComp = CompFactory.CreateChunkSource(self._levelId)
		halfSize = MathUtils.TupleFloor2Int(MathUtils.TupleMul(config['size'], 0.5))
		padding = (80, 0, 80)
		minPos = MathUtils.TupleSub(MathUtils.TupleSub(pos, halfSize), padding)
		maxPos = MathUtils.TupleAdd(MathUtils.TupleAdd(pos, halfSize), padding)
		self._chunckComp.SetAddArea(self._areaUid, dim, minPos, maxPos)

	@property
	def Uid(self):
		return self._uid

	@property
	def State(self):
		ret = DatasetObj.Build(BuildingTaskState)
		ret['uid'] = self._uid
		ret['dim'] = self._dim
		ret['total'] = self._total
		ret['pos'] = self._pos
		ret['index'] = self._index
		ret['rot'] = self._rot
		ret['identifier'] = self._config['identifier']
		return ret

	def BuildPart(self, part):
		pos = MathUtils.TupleAdd(self._pos, part['pos'])
		name = modConfig.ModNameSpace+':'+part['mcs']
		ret = self._gameComp.PlaceStructure(None, pos, name, self._dim, self._rot)
		print 'PlaceStructure', pos, name, ret
		return ret

	def Update(self):
		if self._index < 0:
			return False
		if self._index > -1 and self._index == self._total:
			self.OnBuildCompleted()
			return True
		dirty = False
		if self._tickCount == 0:
			structures = self._config['structures']
			self.BuildPart(structures[self._index])
			self._index += 1
			dirty = True
		self._tickCount = (self._tickCount + 1) % self._tickStep
		return dirty

	def OnBuildCompleted(self):
		self._index = -1
		self._chunckComp.DeleteArea(self._areaUid)

	@property
	def Completed(self):
		return self._index == -1

class BuildingPosMarkerTask(object):
	def __init__(self, system, dim, identifier, pos, rot, size, markerConfig=None):
		self._system = system
		self._dim = dim
		self._pos = pos
		self._rot = rot
		self._size = size
		self._id = identifier
		self._chunkComp = CompFactory.CreateChunkSource(system.mLevelId)
		self._blockInfoComp = CompFactory.CreateBlockInfo(system.mLevelId)
		if markerConfig is None:
			markerConfig = GetBuildingMarkerConfig(identifier)
			if markerConfig is None:
				structNameBase = GetStructNameBase(identifier)
				markerConfig = GetBuildingMarkerConfig(structNameBase)
		# 刷新距离：默认24，用于刷怪
		self._spawnDistance = markerConfig.get('spawnDistance', 24)
		# 用于生成npc、方块等
		self._spawnLongDistance = min(self._spawnDistance, 64)
		# 区块大小，默认16
		chunkBlockSize = markerConfig.get('chunkSize', 16) + 0.0
		self._center = markerConfig['center']
		self._detectArea = []
		self._spawnMarkersMap = {}
		x_n = int(math.ceil(size[0]/chunkBlockSize))
		z_n = int(math.ceil(size[2]/chunkBlockSize))
		chunkSize = (chunkBlockSize, 0, chunkBlockSize)
		chunkSize = MathUtils.RotByFace(chunkSize, self._rot)
		offsetPos = MathUtils.TupleSub(pos, MathUtils.RotByFace(self._center, self._rot))
		for i in range(0, x_n):
			for j in range(0, z_n):
				dp = (offsetPos[0] + i * chunkSize[0], offsetPos[2] + j * chunkSize[2])
				self._detectArea.append({
					'pos': dp,
					'inited': False,
					'markers': []
				})
		overSizeArea = {}
		markers = markerConfig['posMarkers']
		for marker in markers:
			if not self.IsValidAutoSpawnMarker(marker['id']):
				continue
			p = marker['pos']
			uid = '%s_%d_%d_%d' % (marker['id'], p[0], p[1], p[2])
			self._spawnMarkersMap[uid] = False
			x = int(p[0] / chunkBlockSize)
			z = int(p[2] / chunkBlockSize)
			index = x * z_n + z
			area = None
			if x < 0 or x >= x_n or z < 0 or z >= z_n:
				if index not in overSizeArea:
					dp = (offsetPos[0] + x * chunkSize[0], offsetPos[2] + z * chunkSize[2])
					overSizeArea[index] = {
						'pos': dp,
						'inited': False,
						'markers': []
					}
				area = overSizeArea[index]
			else:
				area = self._detectArea[index]
			area['markers'].append(marker)
			# 根据生成类型，添加判断距离
			if not area.get("spawnDistance"):
				dist = self._spawnDistance
				if marker['id'] != modConfig.MonsterPoolIdentifierPrefix:
					dist = self._spawnLongDistance
				area["spawnDistance"] = dist
		for area in overSizeArea.itervalues():
			self._detectArea.append(area)
		self._blockComp = CompFactory.CreateBlockInfo(self._system.mLevelId)
		pass

	def IsValidAutoSpawnMarker(self, identifier):
		if identifier == modConfig.MonsterPoolIdentifierPrefix:
			return True
		if identifier == modConfig.ChestIdentifierPrefix:
			return True
		if identifier.startswith(modConfig.NPCIdentifierPrefix):
			return True
		if identifier == 'scuke_survive:base_car_broken':
			return True
		return False

	@property
	def State(self):
		ret = DatasetObj.Build(BuildingPosMarkerTaskState)
		ret['id'] = self._id
		ret['pos'] = self._pos
		ret['rot'] = self._rot
		ret['dim'] = self._dim
		ret['size'] = self._size
		ret['sp'] = self._spawnMarkersMap
		return ret

	def SetState(self, state):
		sp = state['sp']
		for uid in sp:
			if uid in self._spawnMarkersMap:
				self._spawnMarkersMap[uid] = sp[uid]

	def Update(self, playerPos):
		pPos = (playerPos[0], playerPos[2])
		dirty = False
		for area in self._detectArea:
			if area['inited']:
				continue
			p = area['pos']
			p0 = (p[0], 0, p[1])
			p1 = (p[0]+15, 0, p[1]+15)
			blockInfo = self._blockInfoComp.GetBlockNew((p[0], -63, p[1]), self._dim)
			loaded = blockInfo['name'] != 'minecraft:air' or self._chunkComp.CheckChunkState(self._dim, p0) or self._chunkComp.CheckChunkState(
				self._dim, p1)
			if not loaded:
				continue
			dp = MathUtils.TupleSub(pPos, p)
			dis = MathUtils.TupleLength(dp)
			markers = area['markers']
			if len(markers) <= 0:
				area['inited'] = True
				dirty = True
				continue
			# 刷怪距离调近一些，不然没等玩家靠近，怪就被刷新掉了
			spawnDist = area.get('spawnDistance', self._spawnDistance)
			if dis < spawnDist:
				dirty = True
				spawnMarkers = []
				for marker in markers:
					p = marker['pos']
					uid = '%s_%d_%d_%d' % (marker['id'], p[0], p[1], p[2])
					if uid not in self._spawnMarkersMap or self._spawnMarkersMap[uid]:
						continue
					ret = False
					identifier = marker.get('id')
					pos, face = TransMarkerPos(self._pos, self._rot, self._center, marker)
					if identifier == modConfig.MonsterPoolIdentifierPrefix:
						# 怪物池中随机
						ret = self.PlaceBuildingEntityByPool(self._dim, marker, pos, face)
					elif identifier == modConfig.ChestIdentifierPrefix:
						# 箱子
						ret = self.PlaceBuildingChest(self._dim, marker, pos, face)
					elif identifier.startswith(modConfig.NPCIdentifierPrefix):
						# NPC 放置
						ret = self.PlaceBuildingEntity(self._dim, identifier, pos, face)
					elif identifier == "scuke_survive:base_car_broken":
						# 损坏的基地车
						ret = self.PlaceBuildingEntity(self._dim, identifier, pos, face)
					self._spawnMarkersMap[uid] = ret
					if ret:
						spawnMarkers.append(marker)
					# print("__________ BuildingPosMarkerTask set markers", p, markers)
				for marker in spawnMarkers:
					markers.remove(marker)
				area['inited'] = len(markers) <= 0
		return dirty

	def PlaceBuildingChest(self, dim, marker, pos, face):
		"""生成奖励箱"""
		ret = False
		# 随机抽取
		weight = self.GetMakerPoolTotalWight(marker, key='chest_pool')
		if weight:
			rdm = random.randint(1, weight)
			currentWeight = 0
			for identifier, val in marker['chest_pool'].iteritems():
				currentWeight += val.get('weight', 0)
				if rdm <= currentWeight:
					# 生成方块
					ret = self._blockComp.SetBlockNew(pos, {"name": identifier, "aux": face}, 0, dim, updateNeighbors=False)
					# 设置奖励箱（如果是奖励箱）
					if ret and val.get('loot_table'):
						self._blockComp.SetChestLootTable(pos, dim, val['loot_table'], isIgnoreSpilt=val.get('isIgnore_spilt', False))
					return ret
		return ret

	def PlaceBuildingEntity(self, dim, identifier, pos, face):
		footPos = MathUtils.TupleAdd(pos, (0.5, 0.0, 0.5))
		rot = (0, face * 90)
		eid = self._system.CreateEngineEntityByTypeStr(identifier, footPos, rot, dim)
		if eid:
			comp = CompFactory.CreateEntityEvent(eid)
			comp.TriggerCustomEvent(eid, 'scuke_survive:on_npc_spawn')
			comp = CompFactory.CreateEntityDefinitions(eid)
			comp.SetSitting(True)
			return True
		else:
			self._system.logger.warning('PlaceBuildingEntity failed. %s %s %r %r %d' % (self._id, identifier, footPos, rot, dim))
		return False

	def PlaceBuildingEntityByPool(self, dim, marker, pos, face):
		"""在实体池中随机选择一个实体生成"""
		footPos = MathUtils.TupleAdd(pos, (0.5, 0.0, 0.5))
		rot = (0, face * 90)
		# 随机抽取
		weight = self.GetMakerPoolTotalWight(marker)
		if weight:
			rdm = random.randint(1, weight)
			currentWeight = 0
			for identifier, val in marker['entity_pool'].iteritems():
				currentWeight += val.get('weight', 0)
				if rdm <= currentWeight:
					count = val.get("count", 1)
					# print("__________ PlaceBuildingEntityByPool", pos, identifier)
					ret = False
					for i in xrange(count):
						eid = self._system.CreateEngineEntityByTypeStr(identifier, footPos, rot, dim)
						if not eid:
							self._system.logger.warning('PlaceBuildingEntityByPool failed. %s %s %r %r %d' % (self._id, identifier, footPos, rot, dim))
						else:
							ret = True
					return ret
		return False
	
	def GetMakerPoolTotalWight(self, posMaker, key='entity_pool'):
		"""获取池的总权重"""
		totalWeight = posMaker.get('totalWeight')
		if totalWeight is None:
			# 计算总权重
			totalWeight = 0
			if posMaker.get(key):
				for key, val in posMaker[key].iteritems():
					totalWeight += val['weight']
				posMaker['totalWeight'] = totalWeight
		return totalWeight

	@property
	def Completed(self):
		completedCount = 0
		for state in self._spawnMarkersMap.itervalues():
			if state:
				completedCount += 1
		return completedCount == len(self._spawnMarkersMap)

	@property
	def Uid(self):
		return '%d_%s_%r' % (self._dim, self._id, self._pos)


class BuildingServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(BuildingServerSystem, self).__init__(namespace, systemName)
		self._chunckComp = CompFactory.CreateChunkSource(self.mLevelId)
		self._gameComp = CompFactory.CreateGame(self.mLevelId)
		self._buildingTasks = []
		self._buildingsData = self.GetBuildingsData()
		self._firstInit = len(self.GetBuildingById(ShelterBornIdentifier, 0)) <= 0
		self._buildingPosMarkerTasks = []
		self._players = []
		self._playersAdded = []
		self._playersWaitBorn = []
		self._readyToBuilding = False
		self._shelterBorn = None
		self._placingShelter = False
		self._chunkLoadRequests = []
		self._placeStructureRequests = []
		self.__areaSystem__ = None
		# 注册特征生成事件
		comp = CompFactory.CreateFeature(self.mLevelId)
		for i in ListenStructureFeatureList:
			comp.AddNeteaseFeatureWhiteList(i)
		# 遍历所有组，如果是非结构池类型，则进行注册
		for key, groupVal in LargeBuildingConfig.iteritems():
			for featureName, val in groupVal.get("pools", {}).iteritems():
				cfg = GetBuildingMarkerConfig(featureName)
				# 只有是规则生成、有生成实体的需求，才进行注册
				if cfg and cfg.get("is_feature_rule") and len(cfg.get("posMarkers", [])) > 0:
					# if val.get("try_cancel") is True:
					# 	# 需监听所有structure，用于取消生成
					# 	# 根据size，生成所有structure的id，并进行监听
					# 	size = cfg.get("size")
					# 	nameBase = cfg.get("structure_name_base")
					# 	if size and nameBase:
					# 		for x in xrange(size[0] // 16 + 1):
					# 			for z in xrange(size[2] // 16 + 1):
					# 				name = "{}_{}_{}".format(nameBase, hex(x)[2:], hex(z)[2:])
					# 				comp.AddNeteaseFeatureWhiteList(name)
					# 	else:
					# 		comp.AddNeteaseFeatureWhiteList(cfg['identifier'])
					# 		print("__________ ERROR BuildingServerSystem __init__ AddNeteaseFeatureWhiteList size config is None")
					# else:
					# 	comp.AddNeteaseFeatureWhiteList(cfg['identifier'])
					comp.AddNeteaseFeatureWhiteList(cfg['identifier'])
			pass

		for state in self._buildingsData['buildingTasks']:
			self._buildingTasks.append(
				BuildingTask(
					state['uid'],
					GetBuildingConfig(state['identifier']),
					state['dim'],
					state['pos'],
					state['rot'],
					state['index'],
				))
		for state in self._buildingsData['buildingPosMarkerTasks']:
			config = GetBuildingMarkerConfig(state['id'])
			if config is None:
				continue
			markerTast = BuildingPosMarkerTask(
				self,
				state['dim'],
				state['id'],
				state['pos'],
				state['rot'],
				state['size'],
			)
			markerTast.SetState(state)
			self._buildingPosMarkerTasks.append(markerTast)
		#self.logger.debug('BuildingsData %r' % self._buildingsData)
		self.BroadcastEvent('OnUpdateBuildingsInfo', {
			'buildings': self._buildingsData['buildings']
		})

		self._updateTimer = None

	@property
	def _areaSystem(self):
		if not self.__areaSystem__:
			self.__areaSystem__ = serverApi.GetSystem(modConfig.ModNameSpace,
													  modConfig.ServerSystemEnum.AreaServerSystem)
		return self.__areaSystem__

	def Destroy(self):
		if self._updateTimer:
			engineApiGas.CancelTimer(self._updateTimer)
		return super(BuildingServerSystem, self).Destroy()

	def GetAllBuildings(self):
		return self._buildingsData['buildings']

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, args):
		self._readyToBuilding = True
		playerId = args['playerId']
		if playerId not in self._players:
			self._players.append(playerId)
			engineApiGas.AddTimer(0.1, self._DelaySendBuildings, playerId)
			# 已经点燃的引擎特效
			for building in self._buildingsData['buildings']:
				if building['identifier'] in AutoEngineEffectBuildings:
					if not building['data'].get('activated', False):
						continue
					self.EmitEngineEffect(building, AutoEngineEffectBuildings[building['identifier']], playerId)
			if self._shelterBorn:
				if not self._placingShelter:
					self.NotifyShelterBorn(playerId, self._shelterBorn)
				else:
					self._playersWaitBorn.append(playerId)
			else:
				haveSetShelter = playerId in self._buildingsData['shelterBorn']
				if haveSetShelter:
					self.NotifyToClient(playerId, 'OnLoadCompleted', {
						'outShelter': playerId in self._buildingsData['outShelter']
					})
				else:
					buildings = self.GetBuildingById(ShelterBornIdentifier, 0)
					bornInfo = None
					if len(buildings) > 0:
						bornInfo = buildings[0]
					if bornInfo:
						self.NotifyShelterBorn(playerId, bornInfo)
					else:
						self.logger.error('Not init ShelterBorn!')
						self.NotifyToClient(playerId, 'OnLoadCompleted', {
							'outShelter': playerId in self._buildingsData['outShelter']
						})
			self.TryAddPlayerOutShelterDetect(playerId)
		# 更新频率
		if self._updateTimer is None:
			self._updateTimer = engineApiGas.AddRepeatTimer(1, self.UpdateTimer)

	def NotifyShelterBorn(self, playerId, bornInfo):
		# print 'NotifyShelterBorn', playerId
		pos = bornInfo['pos']
		rot = bornInfo['rot']
		dim = bornInfo['dim']
		engineApiGas.StopEntityRiding(playerId)
		engineApiGas.SetEntityPos(playerId, pos)
		engineApiGas.SetEntityRot(playerId, (0, rot))
		comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
		ret = comp.SetPlayerRespawnPos(pos, dim)
		info = {
			'playerId': playerId,
			'pos': pos,
			'rot': rot,
			'dim': dim
		}
		engineApiGas.SpawnItemToPlayerInv(playerId, {
			'itemName': 'scuke_survive:game_introduce_book',
			'count': 1
		}, 1)
		self.NotifyToClient(playerId, 'OnShelterBorn', info)
		self.BroadcastEvent('OnShelterBorn', info)
		self._buildingsData['shelterBorn'].append(playerId)
		self.FlushBuildingsData()

	def TryAddPlayerOutShelterDetect(self, playerId):
		if playerId in self._buildingsData['outShelter']:
			return
		dim = 0
		identifier = Scuke_oldBooster['identifier']
		buildings = self.GetBuildingById(identifier, 0)
		if len(buildings) <= 0:
			self.logger.error('Not init OldBooster!')
			return
		building = buildings[0]
		config = GetBuildingMarkerConfig(identifier)
		m0, _ = TransMarkerPos(building['pos'], building['rot'], config['center'], ShelterArea[0])
		m1, _ = TransMarkerPos(building['pos'], building['rot'], config['center'], ShelterArea[1])
		minPos = tuple(min(a, b) for a, b in zip(m0, m1))
		maxPos = tuple(max(a, b) for a, b in zip(m0, m1))
		self._areaSystem.AddAreaDetect('outShelter%s' % playerId, dim, minPos, maxPos, playerId, None, self.OnPlayerOutShelter)

	def OnPlayerOutShelter(self, item):
		playerId = item['eid']
		state = item['state']
		self._areaSystem.RemoveAreaDetect(item['uid'])
		self._buildingsData['outShelter'].append(playerId)
		self.FlushBuildingsData()
		self.BroadcastEvent('OnPlayerOutShelter', {'playerId': playerId})

	@EngineEvent()
	def AddServerPlayerEvent(self, args):
		playerId = args['id']
		if playerId not in self._playersAdded:
			if len(self._playersAdded) <= 0 and self._firstInit:
				engineApiGas.SetEntityPos(playerId, (0, 64, 0))
				bindIdentifier = Scuke_oldBooster['identifier']
				buildings = self.GetBuildingById(bindIdentifier, 0)
				if len(buildings) > 0:
					self.TryPlaceMoreBuilding(bindIdentifier)
			self._playersAdded.append(playerId)

	def _DelaySendBuildings(self, playerId):
		self.NotifyToClient(playerId, 'OnUpdateBuildingsInfo', {
			'buildings': self._buildingsData['buildings']
		})

	@EngineEvent()
	def DelServerPlayerEvent(self, args):
		playerId = args['id']
		if playerId in self._players:
			self._players.remove(playerId)
		if playerId in self._playersAdded:
			self._playersAdded.remove(playerId)

	def Update(self):
		if not self._readyToBuilding:
			return
		self.HandleShelterBorn()
		self.HandlePlaceStructureRequests()
		self.HandleChunkLoadRequests()

	def UpdateTimer(self):
		if not self._readyToBuilding:
			return
		flush = False
		# 分块建筑代码生成
		dirty = len(self._buildingTasks) != len(self._buildingsData['buildingTasks'])
		i = 0
		while i < len(self._buildingTasks):
			task = self._buildingTasks[i]
			dirty = dirty or task.Update()
			if task.Completed:
				self._buildingTasks.pop(i)
				continue
			i += 1
		if dirty:
			newStates = []
			for task in self._buildingTasks:
				newStates.append(task.State)
			self._buildingsData['buildingTasks'] = newStates
			flush = True
		# 建筑位置标记检测和生成
		playerPos = []
		for pid in self._players:
			pos = engineApiGas.GetEntityFootPos(pid)
			if pos:
				playerPos.append(pos)
		dirty = len(self._buildingPosMarkerTasks) != len(self._buildingsData['buildingPosMarkerTasks'])
		i = 0
		while i < len(self._buildingPosMarkerTasks):
			task = self._buildingPosMarkerTasks[i]
			for pos in playerPos:
				dirty = dirty or task.Update(pos)
			if task.Completed:
				self._buildingPosMarkerTasks.pop(i)
				continue
			i += 1
		if dirty:
			newStates = []
			for task in self._buildingPosMarkerTasks:
				newStates.append(task.State)
			self._buildingsData['buildingPosMarkerTasks'] = newStates
			flush = True
		if flush:
			self.FlushBuildingsData()


	def GetBuildingsData(self):
		buildingsDataKey = 'buildings'
		data = Instance.mDatasetManager.GetLevelData(buildingsDataKey)
		if not data:
			data = DatasetObj.Build(BuildingServerData)
			Instance.mDatasetManager.SetLevelData(buildingsDataKey, data)
		else:
			data = DatasetObj.Format(BuildingServerData, data)
		return data

	def GetUid(self, flush=True):
		uid = self._buildingsData['uid']
		self._buildingsData['uid'] = uid + 1
		if flush:
			self.FlushBuildingsData()
		return uid

	def UpdateBuildingTaskState(self, task, flush=True):
		buildingTasks = self._buildingsData['buildingTasks']
		i = 0
		ret = False
		while i < len(buildingTasks):
			item = buildingTasks[i]
			if item['uid'] == task.Uid:
				state = task.State
				if state['index'] > -1:
					buildingTasks[i] = state
				else:
					buildingTasks.pop(i)
				ret = True
				break
			i += 1
		if not ret:
			buildingTasks.append(task.State)
			ret = True
		if flush:
			self.FlushBuildingsData()
		return ret

	def AddBuildingState(self, dim, pos, rot, identifier, size, group='', flush=True, structNameBase=None):
		buildings = self._buildingsData['buildings']
		data = DatasetObj.Build(BuildingState)
		data['dim'] = dim
		data['pos'] = pos
		data['rot'] = rot
		data['identifier'] = identifier
		data['group'] = group
		data['size'] = size
		buildings.append(data)
		#print('AddBuildingState', data)
		if structNameBase is None:
			structNameBase = GetStructNameBase(identifier)
		markerConfig = GetBuildingMarkerConfig(structNameBase)
		# print('________ AddBuildingState marker', identifier, structNameBase, markerConfig)
		if markerConfig and len(markerConfig['posMarkers']) > 0:
			tempTask = BuildingPosMarkerTask(self, dim, identifier, pos, rot, size, markerConfig=markerConfig)
			curTaskUid = tempTask.Uid
			found = False
			for task in self._buildingPosMarkerTasks:
				if task.Uid == curTaskUid:
					found = True
					break
			if not found:
				self._buildingPosMarkerTasks.append(tempTask)
		engineApiGas.AddTimer(0.1, self._NotifyBuildingState, data)
		if flush:
			self.FlushBuildingsData()
		'''
		if addArea:
			key = identifier+str(pos)
			_size = (size[0], 0, size[2])
			halfSize = MathUtils.TupleFloor2Int(MathUtils.TupleMul(_size, 0.5))
			padding = (80, 0, 80)
			minPos = MathUtils.TupleSub(MathUtils.TupleSub(pos, halfSize), padding)
			maxPos = MathUtils.TupleAdd(MathUtils.TupleAdd(pos, halfSize), padding)
			maxPos = MathUtils.TupleAdd(maxPos, (0, size[1], 0))
			ret = self._chunckComp.SetAddArea(key, dim, minPos, maxPos)
			print 'SetAddArea', ret, minPos, maxPos
		'''
		return True

	def _NotifyBuildingState(self, data):
		self.BroadcastEvent('OnUpdateBuildingsInfo', {
			'buildings': [data]
		})
		self.BroadcastToAllClient('OnUpdateBuildingsInfo', {
			'buildings': [data]
		})

	def GetBuildingById(self, identifier, dim):
		buildings = self._buildingsData['buildings']
		ret = []
		for building in buildings:
			if building['identifier'] == identifier and dim == building['dim']:
				ret.append({
					'dim': building['dim'],
					'pos': building['pos'],
					'rot': building['rot'],
					'identifier': building['identifier'],
					'group': building['group'],
					'data': building['data'],
				})
		return ret

	def GetBuildingByGroup(self, group, dim):
		buildings = self._buildingsData['buildings']
		ret = []
		for building in buildings:
			if building['group'] == group and dim == building['dim']:
				ret.append({
					'dim': building['dim'],
					'pos': building['pos'],
					'identifier': building['identifier'],
					'group': building['group'],
					'data': building['data'],
				})
		return ret

	def GenBuilding(self, identifier, dim, pos, rot=0):
		config = GetBuildingConfig(identifier)
		if config is None:
			return False
		uid = self.GetUid()
		self._buildingTasks.append(BuildingTask(uid, config, dim, pos, rot))
		return True

	def FlushBuildingsData(self):
		buildingsDataKey = 'buildings'
		Instance.mDatasetManager.SetLevelData(buildingsDataKey, self._buildingsData)

	def GetLargeBuildingGroup(self, poolName):
		for group, config in LargeBuildingConfig.iteritems():
			if poolName in config['pools']:
				return config
		return None

	@EngineEvent()
	def PlaceNeteaseStructureFeatureEvent(self, args):
		# print('PlaceNeteaseStructureFeatureEvent', args)
		structureName = args['structureName']
		dim = args['dimensionId']
		x = args['x']
		y = args['y']
		z = args['z']
		pos = (x, y, z)
		rot = 0  # TODO

		# 生成拦截：将structure转换为中心池的structure，再进行判断逻辑
		nameList = structureName.rsplit('_', 2)
		structNameBase = nameList[0]
		chunkX = int(nameList[1], 16)
		chunkZ = int(nameList[2], 16)

		buildingGroup = self.GetLargeBuildingGroup(structNameBase)
		if not buildingGroup:
			return
		makerConfig = GetBuildingMarkerConfig(structNameBase)
		center = makerConfig['center']
		centerPos = (x - chunkX * 16 + center[0], y, z - chunkZ * 16 + center[2])
		centerStructName = makerConfig.get('identifier')
		ret = self.CheckPlaceValidByNeteaseStructure(structNameBase, centerStructName, buildingGroup, centerPos, dim)
		if not ret:
			if ret is False:
				args['cancel'] = True
				#print 'PlaceNeteaseStructureFeatureEvent', structNameBase, 'cancel'
				# print("__________ PlaceNeteaseStructureFeatureEvent can place", structureName)
			# else:
			# 	self.TryPlaceMoreBuilding(structureName)
			return
		
		# 只有中心池才往下执行
		if structureName == makerConfig['identifier']:
			groupName = buildingGroup['name']
			size = makerConfig['size']
			self.AddBuildingState(dim, pos, rot, structureName, size, groupName, True, structNameBase=structNameBase)
			self.TryPlaceMoreBuilding(structureName)

	def CheckPlaceValidByNeteaseStructure(self, structNameBase, centerStructName, buildingGroup, pos, dim):
		"""仅用于普通结构特征生成的判断，结构池类不走这里的判断"""
		# 发动机改成定点生成，不需要再做拦截
		return True
		# # 只需要判断和行星发动机的位置
		# buildingTest = buildingGroup['pools'][structNameBase]
		# mode = buildingTest['mode']
		# buildings = self.GetBuildingById(centerStructName, dim)

		# # 自身策略
		# if mode == 'singleton':
		# 	if len(buildings) > 0:
		# 		return False
		
		# # 限制数量
		# if mode == 'limit_count':
		# 	# 如果该建筑是已生成的建筑，则仍可以生成；而如果是未生成的，则判断总数，如果超过了限制数量，则返回False
		# 	isSpawn = False
		# 	for build in buildings:
		# 		if build.get('pos') == pos:
		# 			isSpawn = True
		# 			break
		# 	if isSpawn is False and len(buildings) >= buildingTest['limit_count']:
		# 		return False
		
		# # 和行星发动机组的策略
		# maxDis = buildingGroup.get('planetBooster_distance')
		# if maxDis:
		# 	groupName = 'planetBooster'
		# 	vPos = Vector3(pos[0], 0, pos[2])
		# 	buildings = self.GetBuildingByGroup(groupName, dim)
		# 	for building in buildings:
		# 		p = building['pos']
		# 		vXZ = Vector3(p[0], 0, p[2])
		# 		dis = (vXZ - vPos).Length()
		# 		if dis < maxDis:
		# 			return False
		return True

	# @EngineEvent()
	# def PlaceNeteaseLargeFeatureServerEvent(self, args):
	# 	#print('TryPlaceNeteaseLargeFeatureServerEvent', args)
	# 	dim = args['dimensionId']
	# 	poolName = args['centerPool']
	# 	pos = args['pos']
	# 	pos = (pos[0], -256, pos[1])
	# 	rot = args['rot']
	# 	buildingGroup = self.GetLargeBuildingGroup(poolName)
	# 	if not buildingGroup:
	# 		return
	# 	ret = self.CheckPlaceValid(buildingGroup, poolName, pos, dim)
	# 	if not ret:
	# 		if ret is False:
	# 			args['cancel'] = True
	# 		else:
	# 			self.TryPlaceMoreBuilding(poolName)
	# 		return
	# 	groupName = buildingGroup['name']
	# 	buildingConfig = buildingGroup['pools'][poolName]
	# 	# 注意：该事件触发极早，在此时获取地表方块，会返回None
	# 	y = buildingConfig.get('y')
	# 	if y is None:
	# 		# 报错
	# 		print("============= ERROR PlaceNeteaseLargeFeatureServerEvent config y is None. feature={}".format(poolName))
	# 		return
	# 	size = buildingConfig['size']
	# 	self.AddBuildingState(dim, (pos[0], y, pos[2]), rot, poolName, size, groupName, True, structNameBase=poolName)
	# 	self.TryPlaceMoreBuilding(poolName)

	def TryPlaceMoreBuilding(self, identifier):
		# 特定建筑生成
		if identifier == Scuke_oldBooster['identifier']:
			self.PlaceShelter()

	def CheckPlaceValid(self, buildingGroup, identifier, pos, dim):
		"""用于结构池feature的拦截检测"""
		buildingTest = buildingGroup['pools'][identifier]
		mode = buildingTest['mode']
		buildings = self.GetBuildingById(identifier, dim)
		# 是否已存在
		for building in buildings:
			ePos = building['pos']
			if ePos[0] == pos[0] and ePos[2] == pos[2] and (pos[1] == -256 or ePos[2] == pos[1]):
				print 'Keeping PlaceFeature...', identifier, ePos
				return None
		# 自身策略
		if mode == 'singleton':
			if len(buildings) > 0:
				return False
		elif mode == 'outter':
			checkTargets = buildingTest['targets_radius']
			checkPos = (pos[0], pos[2])
			for _id in checkTargets:
				radius = checkTargets[_id]
				_buildings = self.GetBuildingById(_id, dim)
				for building in _buildings:
					_pos = building['pos']
					_pos = (_pos[0], _pos[2])
					_delta = MathUtils.TupleSub(_pos, checkPos)
					if MathUtils.TupleLength(_delta) < radius:
						return False
		elif mode == 'after':
			afterTarget = buildingTest['after']
			_buildings = self.GetBuildingById(afterTarget, dim)
			if len(_buildings) <= 0:
				return False
		# 组间策略
		groupMode = buildingGroup['mode']
		groupName = buildingGroup['name']
		if groupMode == 'distance':
			maxDis = buildingGroup['distance']
			vPos = Vector3(pos[0], 0, pos[2])
			buildings = self.GetBuildingByGroup(groupName, dim)
			for building in buildings:
				p = building['pos']
				vXZ = Vector3(p[0], 0, p[2])
				dis = (vXZ - vPos).Length()
				if dis < maxDis:
					return False
		return True

	def SetBuildingData(self, identifier, dim, pos, name, value, flush=True):
		buildings = self._buildingsData['buildings']
		for building in buildings:
			curPos = building['pos']
			if building['identifier'] == identifier and dim == building['dim'] and curPos == pos:
				data = building['data']
				data[name] = value
				# 处理新增点燃特效
				if identifier in AutoEngineEffectBuildings and name == 'activated' and value:
					self.EmitEngineEffect(building, AutoEngineEffectBuildings[identifier])

		if flush:
			self.FlushBuildingsData()

	def EmitEngineEffect(self, buildingInfo, posMarkerKey, playerId = None):
		pos, face = GetMarkerPos(buildingInfo['identifier'], buildingInfo['pos'], buildingInfo['rot'], posMarkerKey)
		info = {
			"stage": "engine",
			"dimension": buildingInfo['dim'],
			"pos": pos,
		}
		if playerId is None:
			self.SendMsgToAllClient(eventConfig.EffectPlayEvent, info)
		else:
			self.SendMsgToClient(playerId, eventConfig.EffectPlayEvent, info)

	def PlaceShelter(self):
		dim = 0
		buildings = self.GetBuildingById(ShelterBornIdentifier, dim)
		if len(buildings) > 0:
			self.logger.warning('Repeat PlaceShelter! Ignore!')
			return
		bindIdentifier = Scuke_oldBooster['identifier']
		buildings = self.GetBuildingById(bindIdentifier, dim)
		if len(buildings) <= 0:
			return
		bindBuilding = buildings[0]
		pos = bindBuilding['pos']
		rot = bindBuilding['rot']
		# 出生点设置
		bornPos, bornFace = GetMarkerPos(bindIdentifier, pos, rot, 'scuke_survive:pos2')
		bornPos = MathUtils.TupleAdd(bornPos, (0, 1, 0))
		self._shelterBorn = {
			'pos': bornPos,
			'rot': bornFace*90,
			'dim': dim,
		}
		self._placingShelter = True
		self.AddChunkLoadRequest(dim, bornPos, (32, 32, 32))
		self.BroadcastEvent('OnPlaceShelter', self._shelterBorn)

	@EngineEvent()
	def DamageEvent(self, args):
		if not self._placingShelter:
			return
		# 避难所出生时免伤
		entityId = args['entityId']
		if entityId in self._playersAdded:
			args['damage'] = 0
			args['knock'] = False
			args['ignite'] = False

	def AddPlaceStructureRequest(self, identifier, dim, pos, rot, size):
		info = {
			'identifier': identifier,
			'dim': dim,
			'pos': pos,
			'rot': rot,
			'size': size,
			'time': time.time(),
		}
		halfSize = MathUtils.TupleFloor2Int(MathUtils.TupleMul(size, 0.5))
		padding = (80, 0, 80)
		minPos = MathUtils.TupleSub(MathUtils.TupleSub(pos, halfSize), padding)
		maxPos = MathUtils.TupleAdd(MathUtils.TupleAdd(pos, halfSize), padding)
		self._chunckComp.SetAddArea(identifier, dim, minPos, maxPos)
		chunks = []
		x = size[0]//16
		z = size[2]//16
		px = pos[0]//16
		pz = pos[2]//16
		for i in range(-x, x+1):
			for j in range(-z, z+1):
				chunks.append(((px + i) * 16, pos[1], (pz + j) * 16))
		info['chunks'] = chunks
		self._placeStructureRequests.append(info)

	def AddChunkLoadRequest(self, dim, pos, size):
		info = {
			'dim': dim,
			'pos': pos,
			'time': time.time(),
		}
		chunks = []
		x = size[0] // 16
		z = size[2] // 16
		px = pos[0] // 16
		pz = pos[2] // 16
		for i in range(-x, x + 1):
			for j in range(-z, z + 1):
				chunks.append(((px + i) * 16, pos[1], (pz + j) * 16))
		info['chunks'] = chunks
		self._chunkLoadRequests.append(info)

	def HandleShelterBorn(self):
		if not self._placingShelter:
			return
		if self._shelterBorn is not None:
			pos = self._shelterBorn['pos']
			rot = self._shelterBorn['rot']
			dim = self._shelterBorn['dim']
			for playerId in self._playersAdded:
				engineApiGas.SetEntityPos(playerId, pos)
				engineApiGas.SetEntityRot(playerId, (0, rot))
				if not self._shelterBorn.get('inited', False):
					engineApiGas.StopEntityRiding(playerId)
					comp = serverApi.GetEngineCompFactory().CreatePlayer(playerId)
					ret = comp.SetPlayerRespawnPos(pos, dim)
					print 'SetShelterBornPos', playerId, pos, ret, rot
			self._shelterBorn['inited'] = True
		if ((self._placeStructureRequests is None or len(self._placeStructureRequests) <= 0)
				and (self._chunkLoadRequests is None or len(self._chunkLoadRequests) <= 0)):
			# 全部放置结束才停止设置坐标，避免放置途中被挤出
			self._placingShelter = False
			self.AddBuildingState(self._shelterBorn['dim'], self._shelterBorn['pos'], self._shelterBorn['rot'], ShelterBornIdentifier, (32, 32, 32))
			for playerId in self._playersWaitBorn:
				self.NotifyShelterBorn(playerId, self._shelterBorn)


	def HandlePlaceStructureRequests(self):
		if self._placeStructureRequests and len(self._placeStructureRequests) > 0:
			removed = []
			for request in self._placeStructureRequests:
				identifier = request['identifier']
				dim = request['dim']
				size = request['size']
				pos = request['pos']
				rot = request['rot']
				addTime = request['time']
				chunks = request['chunks']
				loaded = True
				for cPos in chunks:
					if not self._chunckComp.CheckChunkState(dim, cPos):
						loaded = False
						break
				if not loaded:
					if time.time() - addTime < 10:  # timeout
						continue
					else:
						self.logger.error('ChunkLoad timeout %r', request)
					continue
				ret = self._gameComp.PlaceStructure(None, pos, identifier, dim, rot)
				print 'PlaceStructure', identifier, dim, pos, rot, ret
				if ret:
					self.AddBuildingState(dim, pos, rot, identifier, size)
					removed.append(request)
				self._chunckComp.DeleteArea(identifier)
			for item in removed:
				self._placeStructureRequests.remove(item)

	def HandleChunkLoadRequests(self):
		if self._chunkLoadRequests and len(self._chunkLoadRequests) > 0:
			removed = []
			for request in self._chunkLoadRequests:
				dim = request['dim']
				chunks = request['chunks']
				addTime = request['time']
				loaded = True
				for cPos in chunks:
					if not self._chunckComp.CheckChunkState(dim, cPos):
						loaded = False
						break
				if not loaded:
					if time.time() - addTime < 10:  # timeout
						continue
					else:
						self.logger.error('ChunkLoad timeout %r', request)
				removed.append(request)
			for item in removed:
				self._chunkLoadRequests.remove(item)
