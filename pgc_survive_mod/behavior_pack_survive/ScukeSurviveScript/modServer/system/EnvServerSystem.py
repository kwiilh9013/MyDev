# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.equipmentAttrConfig import Config as EquipmentConfig
from ScukeSurviveScript.modCommon.cfg.buildingAttrConfig import Config as BuildingConfig
from ScukeSurviveScript.modServer.tasks.boxCheckTask import BoxCheckTask

DeltaFrame = 30

def _BoxCheckPreprocess(config):
	maxRadius = 0
	for key, building in config.iteritems():
		radius = building['radius']
		if radius > maxRadius:
			maxRadius = radius
	return maxRadius

EnvHeatSourceBoxCheckMaxRadius = _BoxCheckPreprocess(BuildingConfig)

def _Combine(fromDic, result):
	ret = fromDic
	if result is None:
		return ret
	for k in ret:
		if k in result:
			ret[k] += result[k]
	return ret

class EnvServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(EnvServerSystem, self).__init__(namespace, systemName)
		self._tickFrame = 0
		self._currentPhaseEnv = None
		self._playerWeatherEnv = {}
		self._playerEnv = {}
		self._playerBoxCheckTask = {}
		self._blockInfoComp = serverApi.GetEngineCompFactory().CreateBlockInfo(self.mLevelId)
		self.__electricSystem__ = None

	@property
	def _electricSystem(self):
		if not self.__electricSystem__:
			self.__electricSystem__ = serverApi.GetSystem(modConfig.ModNameSpace,
													  modConfig.ServerSystemEnum.ElectricServerSystem)
		return self.__electricSystem__


	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, args):
		pass

	@EngineEvent()
	def AddServerPlayerEvent(self, data):
		playerId = data['id']
		self.UpdatePlayerEnvironment(playerId)

	@EngineEvent()
	def PlayerRespawnFinishServerEvent(self, args):
		playerId = args['playerId']
		self.UpdatePlayerEnvironment(playerId)

	@EngineEvent()
	def PlayerDieEvent(self, args):
		eid = args['id']
		if eid in self._playerEnv:
			del self._playerEnv[eid]
			del self._playerBoxCheckTask[eid]


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnInitPhaseConfig(self, args):
		self._ApplyPhaseEnvConfig(args)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnApplyPhaseConfig(self, args):
		self._ApplyPhaseEnvConfig(args)

	def _ApplyPhaseEnvConfig(self, args):
		self._currentPhaseEnv = args
		#self.logger.debug('ApplyPhaseEnv %r' % self._currentPhaseEnv)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnWeatherUpdate(self, args):
		playerId = args['playerId']
		config = args.get('config', None)
		if config and args.get('snowing', False):
			if 'snowing' in config:
				config = config['snowing']
		self._playerWeatherEnv[playerId] = config

	def Update(self):
		if self._tickFrame == 0:
			self.UpdateEnvironment()
		self._tickFrame = (self._tickFrame + 1) % DeltaFrame
		self.UpdateBoxCheckTask()

	def UpdateEnvironment(self):
		for eid in self._playerEnv:
			self.UpdatePlayerEnvironment(eid)

	def UpdateBoxCheckTask(self):
		for eid, task in self._playerBoxCheckTask.iteritems():
			task.Tick()

	def UpdatePlayerEnvironment(self, eid):
		if eid not in self._playerEnv:
			self._playerEnv[eid] = {
				'biomeName': None,
				'dim': None,
				'phaseEnv': None,
				'biomeEnv': None,
				'heatSourceEnv': None,
				'entitiesEnv': None,
				'equipmentEnv': None,
			}
			self._playerBoxCheckTask[eid] = BoxCheckTask(eid, self._BuildingCheckFilter, self._BuildingCheckCompleted)

		pos = engineApiGas.GetEntityPos(eid)
		# 如果实体死亡，则pos为None
		if pos:
			dim = engineApiGas.GetEntityDimensionId(eid)
			biomeName = engineApiGas.GetBiomeName(pos, dim)
			prevEnv = self._playerEnv[eid]
			envDict = {
				'biomeName': biomeName,
				'dim': dim,
				'phaseEnv': self.GetPhaseEnvInfo(eid),
				'biomeEnv': self.GetPhaseBiomeEnvInfo(biomeName),
				'heatSourceEnv': prevEnv['heatSourceEnv'],
				'entitiesEnv': self.GetEntitiesEnvInfo(eid, pos),
				'equipmentEnv': self.GetEquipmentEnvInfo(eid),
			}
			self._playerEnv[eid] = envDict
			self.GetHeatSourceEnvInfo(eid, pos, dim)
			self.NotifyEnvStateUpdate(eid)

	def GetPhaseEnvInfo(self, playerId):
		ret = {
			'temperature': 0,
			'radiation': 0,
		}
		ret = _Combine(ret, self._currentPhaseEnv)
		weatherEnv = self._playerWeatherEnv.get(playerId, None)
		ret = _Combine(ret, weatherEnv)
		return ret

	def GetPhaseBiomeEnvInfo(self, biomeName):
		if not self._currentPhaseEnv:
			return None

		if 'biomes' not in self._currentPhaseEnv:
			return None
		ret = {
			'temperature': 0,
			'radiation': 0,
		}
		biomesConfig = self._currentPhaseEnv['biomes']
		if biomeName not in biomesConfig:
			if 'default' not in biomesConfig:
				return None
			return _Combine(ret, biomesConfig['default'])
		return _Combine(ret, biomesConfig[biomeName])

	def GetHeatSourceEnvInfo(self, eid, pos, dim):
		if eid not in self._playerBoxCheckTask:
			return
		boxCheckTask = self._playerBoxCheckTask[eid]
		boxCheckTask.Start(dim, pos, EnvHeatSourceBoxCheckMaxRadius, 100)

	def _BuildingCheckFilter(self, pos, block):
		blockName = block['name']
		return blockName in BuildingConfig

	def _BuildingCheckCompleted(self, eid, result):
		if eid not in self._playerEnv:
			return
		dim = self._playerEnv[eid]['dim']
		pos = engineApiGas.GetEntityFootPos(eid)
		if not pos:
			return
		pos = MathUtils.TupleFloor2Int(pos)
		buildingMap = {}
		for blockResult in result:
			block = blockResult['block']
			blockName = block['name']
			config = BuildingConfig[blockName]
			if 'extinguished' in config:
				info = engineApiGas.GetBlockStates(blockResult['pos'])
				if not info or 'extinguished' not in info or info['extinguished'] != config['extinguished']:
					continue
			if 'aux' in config:
				if 'aux' not in block or block['aux'] != config['aux']:
					continue
			if 'electric' in config:
				if not self._electricSystem.GetElecticWorkState(dim, blockResult['pos']):
					continue
			radius = config.get('radius', -1)
			if radius < 0:
				if pos != blockResult['pos']:
					if blockName == 'minecraft:water':
						liquidBlockDict = self._blockInfoComp.GetLiquidBlock(pos, dim)
						if liquidBlockDict is None or liquidBlockDict['name'] != blockName:
							continue
					else:
						continue
			else:
				dX = abs(pos[0] - blockResult['pos'][0])
				dY = abs(pos[1] - blockResult['pos'][1])
				dZ = abs(pos[2] - blockResult['pos'][2])
				if dX > radius or dY > radius or dZ > radius:
					continue
			buildingMap[blockName] = config
		temperature = [0, 0]
		ret = {
			'radiation': 0,
			'shelter': 0,
		}
		for building in buildingMap.itervalues():
			if 'temperature' in building:
				t = building['temperature']
				if t < 0 and t < temperature[0]:
					temperature[0] = t
				if t > 0 and t > temperature[1]:
					temperature[1] = t
			ret = _Combine(ret, building)
		ret['temperature'] = temperature[0] + temperature[1]
		self._playerEnv[eid]['heatSourceEnv'] = ret

	def GetEntitiesEnvInfo(self, eid, pos):
		maxRadius = EnvHeatSourceBoxCheckMaxRadius
		entities = engineApiGas.GetEntitiesAround(eid, maxRadius, True)
		rideEntity = engineApiGas.GetEntityRider(eid)
		if rideEntity != '-1' and rideEntity not in entities:
			entities.append(rideEntity)
		entitiesMap = {}
		for entityId in entities:
			comp = serverApi.GetEngineCompFactory().CreateEngineType(entityId)
			identifier = comp.GetEngineTypeStr()
			if identifier not in BuildingConfig:
				continue
			config = BuildingConfig[identifier]
			if 'ride' in config and config['ride']:
				if rideEntity != entityId:
					continue
			entitiesMap[identifier] = config
		ret = {
			'temperature': 0,
			'radiation': 0,
			'shelter': 0,
		}
		for building in entitiesMap.itervalues():
			ret = _Combine(ret, building)
		return ret

	def GetEquipmentEnvInfo(self, eid):
		ret = {
			'temperature': 0,
			'radiation': 0,
			'heatResistance': 0,
			'coldResistance': 0,
			'radiationResistance': 0,
		}
		carried = engineApiGas.GetPlayerAllItems(eid, serverApi.GetMinecraftEnum().ItemPosType.CARRIED)
		ret = self._CombineEquipmentEnvInfo(carried, ret, 'carry')
		offhand = engineApiGas.GetPlayerAllItems(eid, serverApi.GetMinecraftEnum().ItemPosType.OFFHAND)
		ret = self._CombineEquipmentEnvInfo(offhand, ret, 'carry')
		armor = engineApiGas.GetPlayerAllItems(eid, serverApi.GetMinecraftEnum().ItemPosType.ARMOR)
		ret = self._CombineEquipmentEnvInfo(armor, ret, 'equipment')
		return ret

	def _CombineEquipmentEnvInfo(self, items, info, flag=None):
		ret = info
		for item in items:
			if not item:
				continue
			itemName = item['newItemName']
			if itemName in EquipmentConfig:
				if flag is not None:
					if flag not in EquipmentConfig[itemName]:
						continue
				ret = _Combine(ret, EquipmentConfig[itemName])
		return ret

	def GetEntityEnvInfo(self, eid):
		if not eid in self._playerEnv:
			return None
		info = self._playerEnv[eid]
		ret = {
			'biomeName': info['biomeName'],
			'dim': info['dim'],
			'temperature': 0,
			'radiation': 0,
			'heatResistance': 0,
			'coldResistance': 0,
			'radiationResistance': 0,
			'shelter': 0
		}
		ret = _Combine(ret, info['phaseEnv'])
		ret = _Combine(ret, info['biomeEnv'])
		ret = _Combine(ret, info['heatSourceEnv'])
		ret = _Combine(ret, info['entitiesEnv'])
		ret = _Combine(ret, info['equipmentEnv'])
		return ret

	def NotifyEnvStateUpdate(self, eid):
		if eid not in self._playerEnv:
			return
		self.NotifyToClient(eid, 'OnEnvStateUpdate', self._playerEnv[eid])
