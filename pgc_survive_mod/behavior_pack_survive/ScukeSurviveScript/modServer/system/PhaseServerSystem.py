# -*- encoding: utf-8 -*-
import random
import time
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.phaseServerData import PhaseServerData
from ScukeSurviveScript.modServer.manager.singletonGas import Instance

from ScukeSurviveScript.modCommon import modConfig
import ScukeSurviveScript.modCommon.cfg.phaseConfig as PhaseConfig
from ScukeSurviveScript.modCommon.cfg.phaseEvent.bloodMoon import BloodMoon, BloodMoonIntervalDays
from ScukeSurviveScript.modCommon.cfg.phaseEvent.meteoriteImpact import MeteoriteImpact, MeteoriteRain
from ScukeSurviveScript.modCommon.cfg.phaseEvent.npcTrader import NpcTrader, TraderIntervalDays
from ScukeSurviveScript.modCommon.cfg.phaseEvent.mobSpawn import MobSpawn
from ScukeSurviveScript.modCommon.cfg.weatherEvent.snowStorm import SnowStorm
from ScukeSurviveScript.modCommon.cfg.weatherEvent.moderateSnow import ModerateSnow
from ScukeSurviveScript.modCommon.cfg.weatherEvent.rain import Rain
from ScukeSurviveScript.modCommon.cfg.weatherEvent.thunder import Thunder
from ScukeSurviveScript.modServer.phaseEvents.meteoriteImpactEvent import MeteoriteImpactEvent
from ScukeSurviveScript.modServer.phaseEvents.mobSpawnEvent import MobSpawnEvent
from ScukeSurviveScript.modServer.phaseEvents.npcTraderEvent import NpcTraderEvent
from ScukeSurviveScript.modServer.phaseEvents.phaseEvent import PhaseEvent
from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum, GetBossList
from ScukeSurviveScript.modServer.phaseEvents.weatherRainEvent import WeatherRainEvent
from ScukeSurviveScript.modServer.phaseEvents.weatherSnowEvent import WeatherSnowEvent
from ScukeSurviveScript.modCommon.defines.phaseEventEnum import PhaseEventEnum, PhaseWeatherEventEnum



OneDayMinutes = 20.0
DayFrameCount = 24000
OneSecondFrame = 20.0
OneSecondUpdate = 30.0
UpdateTimeMs = 1000.0 / OneSecondUpdate

PhaseEventConfigDict = {
	PhaseEventEnum.BloodMoon: BloodMoon,
	PhaseEventEnum.MeteoriteImpact: MeteoriteImpact,
	PhaseEventEnum.MeteoriteRain: MeteoriteRain,
	PhaseEventEnum.NPCTrader: NpcTrader,
	PhaseEventEnum.MobSpawn: MobSpawn,
}

WeatherTickFrame = 30
WeatherEventConfigDict = {
	PhaseWeatherEventEnum.SnowStorm: SnowStorm,
	PhaseWeatherEventEnum.ModerateSnow: ModerateSnow,
	PhaseWeatherEventEnum.Rain: Rain,
	PhaseWeatherEventEnum.Thunder: Thunder,
}

class PhaseServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(PhaseServerSystem, self).__init__(namespace, systemName)
		self._tick = 0
		self._isReady = False
		self._passedTime = 0
		self._passedDays = 0
		self._frameScale = 0
		self._phaseConfig = None
		self._phaseLeftDays = 0
		self._phaseDays = 0
		self._nextPhaseDays = 0
		self._keyPointPhaseConfig = None
		self._players = []
		# 生成策略
		self._spawnerConfig = None
		self._spawnerTimerCoef = 1.0
		# 生成设置
		self._S_spawnerTimerCoef = 1.0
		self._S_spawnerLimitCoef = 1.0
		self._S_daySpeedCoef = 1.0
		self._S_eventPlaceCoef = 1.0

		self._phaseData = self.GetPhaseData()
		self._weatherComp = serverApi.GetEngineCompFactory().CreateWeather(self.mLevelId)

		# 怪物数量，仅统计本mod的怪物（非boss）
		self._monsterDict = {}
		self._bossDict = {}
		# 生成怪的时间值
		self._spawnMonsterTime = time.time()
		# 生成怪的timer
		self._spawnMonsterTimer = None
		self._spawnMonsterPool = []

		# Init timeScale
		self._startTime = int(self._phaseData['startTime'])
		self._passedTime = engineApiGas.GetTime() - self._startTime
		if self._passedTime < 0:
			self._passedTime = 0
			self._startTime = int(engineApiGas.GetTime() / DayFrameCount) * DayFrameCount
			self._phaseData['startTime'] = self._startTime
			self.FlushPhaseData()
		self._passedDays = int(self._passedTime / DayFrameCount)
		self._phaseDaysEnded = self._passedDays + 1 > PhaseConfig.EndDays
		self._frameScale = (OneDayMinutes / PhaseConfig.OneDayMinutes) * (OneSecondFrame / OneSecondUpdate)
		# 事件
		self._events = {
			PhaseEventEnum.BloodMoon: PhaseEvent(self, PhaseEventEnum.BloodMoon, self.ActiveBloodMoon),
			PhaseEventEnum.MeteoriteImpact: MeteoriteImpactEvent(self, PhaseEventEnum.MeteoriteImpact, self.ActiveMeteoriteImpact),
			PhaseEventEnum.MeteoriteRain: MeteoriteImpactEvent(self, PhaseEventEnum.MeteoriteRain, self.ActiveMeteoriteRain),
			PhaseEventEnum.NPCTrader: NpcTraderEvent(self, PhaseEventEnum.NPCTrader),
			PhaseEventEnum.MobSpawn: MobSpawnEvent(self, PhaseEventEnum.MobSpawn),
		}
		self._eventsConfig = {}
		for key in self._events:
			self._eventsConfig[key] = None
		# 天气事件
		self._weathers = {
			PhaseWeatherEventEnum.SnowStorm: WeatherSnowEvent(self, PhaseWeatherEventEnum.SnowStorm, self.ActiveWeather),
			PhaseWeatherEventEnum.ModerateSnow: WeatherSnowEvent(self, PhaseWeatherEventEnum.ModerateSnow, self.ActiveWeather),
			PhaseWeatherEventEnum.Rain: WeatherRainEvent(self, PhaseWeatherEventEnum.Rain, self.ActiveWeather),
			PhaseWeatherEventEnum.Thunder: WeatherRainEvent(self, PhaseWeatherEventEnum.Thunder, self.ActiveWeather),
		}
		self._weathersConfig = {}
		for key in self._weathers:
			self._weathersConfig[key] = None
		# PhaseConfig
		self.NextPhase()
		# BloodMoon TODO 血月状态要保存，从存档读取
		self.TryPlaceEventToday()

	def Destroy(self):
		super(PhaseServerSystem, self).Destroy()
		for obj in self._events.values():
			obj.Destroy()
		self._events.clear()
		for obj in self._weathers.values():
			obj.Destroy()
		self._weathers.clear()

	@property
	def Days(self):
		return self._passedDays + 1

	@property
	def PhaseDays(self):
		return self._phaseDays + 1

	@property
	def NextPhaseDays(self):
		return self._nextPhaseDays + 1

	@property
	def LeftDays(self):
		return self._phaseLeftDays + 1

	@property
	def PhaseConfig(self):
		return self._phaseConfig

	def GetPlayers(self):
		return self._players

	def GetPhaseData(self):
		data = Instance.mDatasetManager.GetLevelData('phase')
		if not data:
			data = DatasetObj.Build(PhaseServerData)
			data['startTime'] = int(engineApiGas.GetTime() / DayFrameCount) * DayFrameCount
			Instance.mDatasetManager.SetLevelData('phase', data)
		else:
			data = DatasetObj.Format(PhaseServerData, data)
		return data

	def FlushPhaseData(self):
		Instance.mDatasetManager.SetLevelData('phase', self._phaseData)

	def LoadPhaseConfig(self, days):
		phaseRet = None
		keyPointPhase = None
		leftDays = -1
		for config in PhaseConfig.Phases:
			if config['days'] <= days and leftDays < 0:
				phaseRet = config
			keyPoint = config.get('keyPoint', False)
			if keyPoint and config['days'] - days >= 0:
				leftDays = config['days'] - days
				keyPointPhase = config
				break
		curPhaseTag = ''
		phaseDays = 0
		nextPhaseDays = 0
		for config in PhaseConfig.Phases:
			if config['days'] <= days:
				if curPhaseTag != config['tag']:
					phaseDays = config['days']
					curPhaseTag = config['tag']
			else:
				if curPhaseTag != config['tag']:
					nextPhaseDays = config['days'] - 1
					break
		return phaseRet, leftDays, keyPointPhase, max(0, days-phaseDays), max(0, nextPhaseDays-days)-1

	def LoadPhaseEventConfig(self, days, name):
		ret = None
		configs = PhaseEventConfigDict[name]
		for config in configs:
			if config['days'] <= days:
				ret = config
			else:
				break
		return ret

	def LoadWeatherEventConfig(self, days, name):
		ret = None
		configs = WeatherEventConfigDict[name]
		for config in configs:
			if config['days'] <= days:
				ret = config
			else:
				break
		return ret

	def NextPhase(self):
		days = self.Days
		phase, leftDays, keyPointPhase, phaseDays, nextPhaseDays = self.LoadPhaseConfig(days)
		if not phase:
			self.logger.warning('Days: %d, phase config not exist! Nothing applied.', days)
			return
		if self._phaseConfig != phase:
			self.PhaseConfigChanged(self._phaseConfig, phase)
			self._phaseConfig = phase
		self._phaseLeftDays = leftDays
		self._keyPointPhaseConfig = keyPointPhase
		self._phaseDays = phaseDays
		self._nextPhaseDays = nextPhaseDays

		for eventName in self._events:
			self._eventsConfig[eventName] = self.LoadPhaseEventConfig(days, eventName)
		for weatherName in self._weathers:
			self._weathersConfig[weatherName] = self.LoadWeatherEventConfig(days, weatherName)

	def Update(self):
		if not self._isReady:
			return
		lastDay = self._passedDays
		passedTime = engineApiGas.GetTime() - self._startTime
		if passedTime < 0:
			passedTime = 0  # 强制避免异常
		# 时间倍率
		curOnDayMinutes = PhaseConfig.OneDayMinutes / self._S_daySpeedCoef
		frameScale = self._frameScale * self._S_daySpeedCoef

		if abs(curOnDayMinutes - OneDayMinutes) > 0.01:
			if abs(passedTime - self._passedTime) < frameScale * 5:
				passedTime = self._passedTime + frameScale
		days = int(passedTime / DayFrameCount)

		if days + 1 > PhaseConfig.EndDays:
			if not self._phaseDaysEnded:
				self.PhaseDaysEnded()
				self._phaseDaysEnded = True

		self._passedTime = passedTime
		if abs(curOnDayMinutes - OneDayMinutes) > 0.01:
			engineApiGas.SetTime(self._startTime + int(self._passedTime))

		if days != lastDay:
			self._passedDays = days
			self.PhaseDaysChanged()
			
		self.UpdateWeathers()
		self.UpdatePhaseEvent()

		self._tick += 1

	def PhaseDaysChanged(self):
		self.NextPhase()
		self.TryPlaceEventToday()
		self.NotifyPhaseInfo()
		self.BroadcastEvent('OnDayChanged', {
			'days': self.Days
		})

	def _BuildNotifyPhaseInfo(self, config):
		return {
			'days': config['days'],
			'desc': config['desc'],
			'tag': config['tag'],
			'temperature': config.get('temperature', 0),
			'radiation': config.get('radiation', 0),
		}

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnPlayerOutShelter(self, args):
		# 玩家出避难所后重新弹一次
		playerId = args['playerId']
		self.NotifyPhaseInfo(playerId)

	def NotifyPhaseInfo(self, targetId = None):
		phaseInfo = self._BuildNotifyPhaseInfo(self.PhaseConfig)
		keyPointPhase = None
		if self._keyPointPhaseConfig:
			keyPointPhase = self._BuildNotifyPhaseInfo(self._keyPointPhaseConfig)
		info = {
			'days': self.Days,
			'phaseDays': self.PhaseDays,
			'nextPhaseDays': self.NextPhaseDays,
			'leftDays': self.LeftDays,
			'phase': phaseInfo,
			'keyPointPhase': keyPointPhase
		}
		if targetId:
			self.NotifyToClient(targetId, 'OnUpdatePhaseInfo', info)
		else:
			self.BroadcastToAllClient('OnUpdatePhaseInfo', info)

	def PhaseDaysEnded(self):
		self.logger.info('PhaseDaysEnded %d', self.Days)
		self._phaseData['endDays'] = self.Days
		self.FlushPhaseData()

	def PhaseConfigChanged(self, prev, cur):
		if not prev:
			self.InitPhaseConfig(cur)
			return
		# self.UndoPhaseConfig(prev)
		self.ApplyPhaseConfig(cur)

	def UndoPhaseConfig(self, phaseConfig):
		pass

	def InitPhaseConfig(self, phaseConfig):
		self.BroadcastEvent('OnInitPhaseConfig', phaseConfig)
		self.ResetSpawnerStrategy(phaseConfig)

	def ApplyPhaseConfig(self, phaseConfig):
		self.BroadcastEvent('OnApplyPhaseConfig', phaseConfig)
		self.ResetSpawnerStrategy(phaseConfig)


	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, args):
		self.NotifyPhaseInfo(args['playerId'])
		self._isReady = True
		playerId = args['playerId']
		if playerId not in self._players:
			self._players.append(playerId)

	@EngineEvent()
	def DelServerPlayerEvent(self, args):
		playerId = args['id']
		if playerId in self._players:
			self._players.remove(playerId)

	def ResetSpawnerStrategy(self, phaseConfig, overrideSpawner=None, coef = 0.0):
		if not phaseConfig:
			return
		if 'spawner' not in phaseConfig:
			self._spawnerConfig = None
			self._spawnerTimerCoef = 1.0
			return
		spawner = phaseConfig['spawner'].copy()
		if overrideSpawner is not None:
			# 血月的config是倍率
			for key, value in overrideSpawner.iteritems():
				spawnerVal = spawner.get(key)
				if spawnerVal:
					spawner[key] = spawnerVal * value
			# 重置刷新间隔
			spawner.pop("perMinuteGenCD", None)
			# spawner = overrideSpawner
		self._spawnerConfig = spawner
		self._spawnerTimerCoef = (1.0 + coef)
		print 'ResetSpawnerStrategy', spawner, overrideSpawner, self._spawnerTimerCoef

	def TryPlaceEventToday(self):
		if not self._phaseConfig:
			return
		events = self._phaseConfig.get('events', None)
		if events is None:
			return
		days = self.Days
		daytime = engineApiGas.GetTime() % DayFrameCount
		
		placeEvents = events.copy()
		# 血月固定触发
		if days % BloodMoonIntervalDays == 0:
			placeEvents[PhaseEventEnum.BloodMoon] = 100
		# 商人事件，固定触发
		if days % TraderIntervalDays == 0:
			placeEvents[PhaseEventEnum.NPCTrader] = 100
		# 概率系数
		for eventName in placeEvents:
			placeEvents[eventName] *= self._S_eventPlaceCoef
		for eventName in placeEvents:
			if eventName not in self._events:
				continue
			event = self._events[eventName]
			config = self._eventsConfig[eventName]
			forcePlace = False
			if forcePlace or event.TryPlace(days, daytime, placeEvents, config):
				event.Place(days, daytime, config)
				#print '_____ PlacePhaseEvent', eventName, event.StartTime, event.EndTime

	def TryPlaceWeatherEvent(self):
		if not self._phaseConfig:
			return
		weathers = self._phaseConfig.get('weathers', None)
		if weathers is None:
			return
		for weatherEvent in self._weathers.itervalues():
			if weatherEvent.Active:
				return
		# 天气同时只能有一个
		days = self.Days
		daytime = engineApiGas.GetTime() % DayFrameCount
		for weatherName in weathers:
			weatherEvent = self._weathers[weatherName]
			config = self._weathersConfig[weatherName]
			if weatherEvent.TryPlace(days, daytime, weathers, config):
				weatherEvent.Place(days, daytime, config, True)
				print 'PlaceWeatherEvent', weatherName, weatherEvent.StartTime, weatherEvent.EndTime
				return

	def UpdateWeathers(self):
		if self._tick % WeatherTickFrame == 0:
			self.TryPlaceWeatherEvent()
			isThunder = self._weatherComp.IsThunder()
			isRaining = isThunder or self._weatherComp.IsRaining()
			eventThunder = self._weathers[PhaseWeatherEventEnum.Thunder].Active
			eventRaining = eventThunder or self._weathers[PhaseWeatherEventEnum.Rain].Active
			if isRaining and not eventRaining:
				self._weatherComp.SetRaining(0, 10000)
			if isThunder and not eventThunder:
				self._weatherComp.SetThunder(0, 10000)
			daytime = engineApiGas.GetTime() % DayFrameCount
			if not isThunder and eventThunder:
				self._weathers[PhaseWeatherEventEnum.Thunder].Remove(self.Days, daytime)
			elif not isRaining and eventRaining:
				self._weathers[PhaseWeatherEventEnum.Rain].Remove(self.Days, daytime)


	def UpdatePhaseEvent(self):
		days = self.Days
		daytime = engineApiGas.GetTime() % DayFrameCount
		dirty = False
		for event in self._events.itervalues():
			temp = event.Update(days, daytime)
			if temp is not None:
				dirty = True
		for event in self._weathers.itervalues():
			temp = event.Update(days, daytime)
			if temp is not None:
				dirty = True
		# Event 特定的效果
		spawnerSpeedUp = 0
		if dirty:
			overrideSpawner = None
			# 加速生成
			for event in self._events.itervalues():
				if not event.Active or event.Config is None:
					continue
				config = event.Config
				if event.Name == 'bloodMoon':
					overrideSpawner = config.get('spawner', None)
				if 'spawnerSpeedUp' in config:
					spawnerSpeedUp += config['spawnerSpeedUp'] / 100.0
			# 天气加速
			for weather in self._weathers.itervalues():
				if not weather.Active or weather.Config is None:
					continue
				config = weather.Config
				if 'spawnerSpeedUp' in config:
					spawnerSpeedUp += config['spawnerSpeedUp'] / 100.0
			self.ResetSpawnerStrategy(self._phaseConfig, overrideSpawner, spawnerSpeedUp)

	@EngineEvent()
	def PlayerTrySleepServerEvent(self, args):
		playerId = args['playerId']
		# 处于事件激活期间不允许睡觉
		for event in self._events.itervalues():
			if event.Active and event.Config.get('forbidSleep', False):
				args['cancel'] = True
				dim = engineApiGas.GetEntityDimensionId(playerId)
				pos = engineApiGas.GetEntityPos(playerId)
				if pos:
					engineApiGas.SetPlayerRespawnPos(playerId, pos, dim)
				engineApiGas.NotifyOneMessage(playerId, '§c%s 无法入睡， 重生点已设置' % event.Config['name'])
				return

	def ActiveBloodMoon(self, phaseEvent, state):
		config = phaseEvent.Config
		if not config:
			return
		info = {'state': state}
		if 'desc' in config:
			info['desc'] = config['desc']
		self.BroadcastToAllClient('OnBloodMoonUpdate', info)
		print 'ActiveBloodMoon', state

	def ActiveMeteoriteImpact(self, phaseEvent, state):
		config = phaseEvent.Config
		if not config:
			return
		info = {'state': state}
		if 'desc' in config:
			info['desc'] = config['desc']
		self.BroadcastToAllClient('OnMeteoriteImpactUpdate', info)
		print 'ActiveMeteoriteImpact', state

	def ActiveMeteoriteRain(self, phaseEvent, state):
		print 'ActiveMeteoriteRain', state

	# region 怪物刷新
	@EngineEvent()
	def AddEntityServerEvent(self, args):
		"""添加实体事件"""
		entityId = args.get("id")
		engineTypeStr = args.get("engineTypeStr")
		if engineTypeStr in GetBossList():
			self._bossDict[entityId] = True
		elif PhaseConfig.IsSelfMonster(engineTypeStr):
			self._monsterDict[entityId] = True
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体移除事件"""
		entityId = args.get("id")
		self._bossDict.pop(entityId, None)
		self._monsterDict.pop(entityId, None)
		pass

	@EngineEvent()
	def ServerSpawnMobEvent(self, args):
		"""生成生物事件"""
		identifier = args.get("identifier")
		cancel = args.get("cancel")
		# 分为在地表刷新和在地底刷新
		if cancel is not True and (identifier == MonsterEnum.ZombieNormal or identifier == MonsterEnum.ZombieBaby):
			# 如果是自然刷新出的普通僵尸，则取消刷新，并通过代码生成
			args["cancel"] = True
			pos = (args.get("x"), args.get("y"), args.get("z"))
			dimension = args.get("dimensionId")
			self.TrySpawnMob(dimension, pos)
		pass

	def TrySpawnMob(self, dimension, pos, rot=None):
		"""尝试生成实体"""
		if not self._spawnerConfig:
			return
		# 判断数量上限
		curTime = time.time()
		mobLimit = self._spawnerConfig.get("mobLimit")
		if not mobLimit or self.GetMonsterTotalCount() < mobLimit * self._S_spawnerLimitCoef:
			if self._spawnerConfig.get("perMinuteGen"):
				# 计算生成CD = 数量 / 60.0
				perMinuteGenCD = self._spawnerConfig.get("perMinuteGenCD")
				if perMinuteGenCD is None:
					perMinuteGen = self._spawnerConfig.get("perMinuteGen")
					perMinuteGenCD = 60.0 / perMinuteGen
					self._spawnerConfig["perMinuteGenCD"] = perMinuteGenCD
				# 加速
				perMinuteGenCD /= self._spawnerTimerCoef
				perMinuteGenCD /= self._S_spawnerTimerCoef
				# 插值逻辑：根据上一次触发的时间，计算本次应当生成的数量
				timeCD = curTime - self._spawnMonsterTime
				# 对CD做限制，否则会出现这种情况：如果这段时间内没刷怪（如传送到其他维度），则下次触发时，会刷新这一段时间缺失的怪
				timeCD = min(timeCD, 60)
				spawnNum = timeCD // perMinuteGenCD
				if spawnNum > 0:
					# 更新时间
					self._spawnMonsterTime = curTime
					# 生成多个
					if rot is None:
						rot = (0, 0)
					self._spawnMonsterPool.append([dimension, pos, rot, spawnNum])
					if not self._spawnMonsterTimer:
						self._spawnMonsterTimer = engineApiGas.AddRepeatTimer(0.5, self.DelaySpawnMonsterTimer)
					# print("___________ TrySpawnMob curLen=", len(self._monsterDict) + spawnNum, "perMinuteGenCD=", perMinuteGenCD, "perMinuteGen=", self._spawnerConfig.get("perMinuteGen"), "mobLimit", mobLimit, self._S_spawnerLimitCoef)
				# else:
				# 	# CD没到，不生成，也不更新时间
				# 	pass
		else:
			# 达到上限、或者其他情况，则仅更新时间，以免cd越叠越大
			self._spawnMonsterTime = curTime
		pass

	def DelaySpawnMonsterTimer(self):
		"""延时生成怪物timer"""
		if len(self._spawnMonsterPool) > 0:
			val = self._spawnMonsterPool[0]
			if val[3] > 0:
				self.SetSpawnMonster(val[0], val[1], val[2])
				val[3] -= 1
				if val[3] <= 0:
					self._spawnMonsterPool.pop(0)
		pass

	def SetSpawnMonster(self, dimension, pos, rot):
		"""设置生成怪物"""
		# 随机怪物类型
		mobs = self._phaseConfig["mobs"]
		# 计算刷怪的权重（如果有缓存，直接获取缓存）
		totalMobsWeight = self._phaseConfig.get('totalMobsWeight')
		if totalMobsWeight is None:
			# 计算总权重
			totalMobsWeight = 0
			for val in mobs:
				totalMobsWeight += val['probability']
			self._phaseConfig['totalMobsWeight'] = totalMobsWeight
		# 按照权重随机
		rdm = random.randint(1, totalMobsWeight)
		spawnMobConfig = None
		currentWeight = 0
		bossCount = self.GetBossTotalCount()
		for val in mobs:
			currentWeight += val.get('probability', 0)
			if rdm <= currentWeight:
				# 如果是boss，则额外判断数量上限，如果到达上限，则改成刷其他小怪
				if val.get('type') in GetBossList() and bossCount >= PhaseConfig.BossLimit:
					continue
				else:
					spawnMobConfig = val
					break
		# 生成
		if spawnMobConfig:
			abilities = self._spawnerConfig.get('abilities', [])
			healthCoef = self._spawnerConfig.get('healthCoef', 1.0)
			damageCoef = self._spawnerConfig.get('damageCoef', 1.0)
			speedCoef = self._spawnerConfig.get('speedCoef', 1.0)
			armorCoef = self._spawnerConfig.get('armorCoef', 1.0)
			self.BroadcastEvent("OnPhaseSpawnMob", {
				"config": spawnMobConfig,
				"args": {
					"abilities": abilities,
					"healthCoef": healthCoef,
					"damageCoef": damageCoef,
					"speedCoef": speedCoef,
					"armorCoef": armorCoef,
					"pos": pos,
					"rot": rot,
					"dim": dimension
				},
			})
			# print("____________ SetSpawnMonster", spawnMobConfig["type"])
		pass

	def SetSpawnMonsterFromAttrRatio(self, engineTypeStr, dimension, pos, rot, healthCoef=1, damageCoef=1, speedCoef=1, armorCoef=1):
		"""生成指定的怪物, 需应用天数的加成、以及自带的加成"""
		# 获取当前天数的属性加成
		abilities = self._spawnerConfig.get('abilities', [])
		dayHealthCoef = self._spawnerConfig.get('healthCoef', 1.0)
		dayDamageCoef = self._spawnerConfig.get('damageCoef', 1.0)
		daySpeedCoef = self._spawnerConfig.get('speedCoef', 1.0)
		dayArmorCoef = self._spawnerConfig.get('armorCoef', 1.0)
		self.BroadcastEvent("OnPhaseSpawnMob", {
			"config": {"type": engineTypeStr},
			"args": {
				"abilities": abilities,
				"healthCoef": dayHealthCoef * healthCoef,
				"damageCoef": dayDamageCoef * damageCoef,
				"speedCoef": daySpeedCoef * speedCoef,
				"armorCoef": dayArmorCoef * armorCoef,
				"pos": pos,
				"rot": rot,
				"dim": dimension
			},
		})
		pass

	def GetMonsterTotalCount(self):
		"""获取怪物总数"""
		return len(self._monsterDict) + len(self._bossDict)
	
	def GetBossTotalCount(self):
		"""获取boss总数"""
		count = 0
		for entityId in self._bossDict.keys():
			pos = engineApiGas.GetEntityPos(entityId)
			if pos:
				count += 1
		return count
	# endregion

	def ActiveWeather(self, weatherEvent, state):
		print 'ActiveWeather', weatherEvent.Name, state


	def _PlaceEvent(self, eventName):
		daytime = engineApiGas.GetTime() % DayFrameCount
		if eventName not in self._events:
			for event in self._events.itervalues():
				if event.Active:
					event.Remove(self.Days, daytime)
			return
		config = self._eventsConfig[eventName]
		self._events[eventName].Place(self.Days, daytime, config, True)


	def _PlaceWeather(self, weatherName):
		daytime = engineApiGas.GetTime() % DayFrameCount
		for weather in self._weathers.itervalues():
			if weather.Active:
				weather.Remove(self.Days, daytime)
		if weatherName not in self._weathersConfig:
			return
		config = self._weathersConfig[weatherName]
		self._weathers[weatherName].Place(self.Days, daytime, config, True)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnJumpToNextPhase(self, args):
		curTime = engineApiGas.GetTime()
		jumpTime = curTime + self.LeftDays * DayFrameCount
		engineApiGas.SetTime(jumpTime)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnEscapeFailed(self, args):
		self._PlaceEvent(PhaseEventEnum.MeteoriteRain)
