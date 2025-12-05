# -*- coding: utf-8 -*-
import random
import time
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBase


HealthAttrEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH

class SpawnMobsWavesBattlePhase(BattlePhaseBase):
	def __init__(self, battleEvent, config, data):
		super(SpawnMobsWavesBattlePhase, self).__init__(battleEvent, config, data)
		self._wavesData = None
		self._startTime = 0
		self._duration = self.GetConfigValue('duration')
		self._aliveTargets = self.GetConfigValue('targets')
		self._faceTargetPos = battleEvent.Center
		self._events = self.GetConfigValue('events')
		self._waves = self.GetConfigValue('waves')



	def OnStart(self):
		super(SpawnMobsWavesBattlePhase, self).OnStart()
		self._startTime = time.time()
		self._wavesData = []
		for waveConfig in self._waves:
			areasConfig = waveConfig['areas']
			spawnAreas = []
			for areaConfig in areasConfig:
				pos = self.TransPos(areaConfig['pos'])
				spawner = {
					'pos': pos,
					'range': areaConfig['range'],
					'interval': areaConfig['interval'],
					'count': areaConfig['count'],
					'mobs': areaConfig['mobs'],
					'_lastTime': 0.0,
				}
				spawnAreas.append(spawner)
			waveOffset = waveConfig['offset']
			waveDuration = waveConfig['duration']
			self._wavesData.append({
				'offset': waveOffset,
				'duration': waveDuration,
				'spawnAreas': spawnAreas,
				'state': False
			})

	def OnWaveAreaUpdate(self, t, spawnAreas):
		for spawner in spawnAreas:
			interval = spawner['interval']
			lastTime = spawner['_lastTime']
			if t - lastTime >= interval:
				self.SpawnMobs(spawner)
				lastTime += interval
				spawner['_lastTime'] = lastTime

	def OnUpdate(self):
		ret = super(SpawnMobsWavesBattlePhase, self).OnUpdate()
		t = time.time()
		deltaTime = t - self._startTime
		for wave in self._wavesData:
			spawnAreas = wave['spawnAreas']
			state = 0.0 <= deltaTime - wave['offset'] < wave['duration']
			if state != wave['state']:
				if state:
					for spawner in spawnAreas:
						spawner['_lastTime'] = t - spawner['interval']
				wave['state'] = state
			if state:
				self.OnWaveAreaUpdate(t, spawnAreas)
		endPhase = deltaTime >= self._duration
		if self._aliveTargets is not None:
			aliveCount = 0
			for eid in self._aliveTargets:
				health = engineApiGas.GetAttrValue(eid, HealthAttrEnum)
				if health > 0:
					aliveCount += 1
			if aliveCount <= 0:
				endPhase = True
		if endPhase:
			self._startTime = -1
		return ret

	def SpawnMobs(self, spawner):
		created = 0
		spawnRange = spawner['range']
		footPos = (spawner['pos'])
		count = spawner['count']
		mobs = spawner['mobs']
		dim = 0  # 默认主世界
		eventHandler = self._battleEvent.EventHandler
		targetPos = self._faceTargetPos
		while created < count:
			i = 0
			while i < 2:  # 尝试生成次数
				x = int(footPos[0] + random.randint(-spawnRange[0], spawnRange[0]))
				z = int(footPos[2] + random.randint(-spawnRange[2], spawnRange[2]))
				y = int(footPos[1])
				offsetY = y - spawnRange[1]
				yRanges = engineApiGas.GetValidYRanges(dim, x, y, z, spawnRange[1], 3)
				minYDis = -1
				minYRange = None
				for range in yRanges:
					dis = abs(range[0] - offsetY)
					if minYDis < 0 or dis < minYDis:
						minYDis = dis
						minYRange = range
				if minYRange is not None:
					pos = (x, minYRange[0], z)
					dir = MathUtils.TupleSub(targetPos, pos)
					rot = serverApi.GetRotFromDir(dir)
					eid = eventHandler.CreateEngineEntityByTypeStr(self.GetMobIdentifier(mobs), pos, rot, dim)
					if eid and eid != '-1':
						if self._events:  # 触发实体行为事件
							for event in self._events:
								engineApiGas.TriggerCustomEvent(eid, event)
						# 强制设定目标
						# engineApiGas.SetAttackTarget(eid, self.GetClosestTarget(pos))
					break
				i += 1
			created += 1

	def GetMobIdentifier(self, mobs):
		totalMobsWeight = mobs.get('_totalMobsWeight', None)
		if totalMobsWeight is None:
			totalMobsWeight = 0
			for weight in mobs.itervalues():
				totalMobsWeight += weight
			mobs['_totalMobsWeight'] = totalMobsWeight
		rdm = random.randint(1, totalMobsWeight)
		currentWeight = 0
		ret = None
		for identifier, weight in mobs.iteritems():
			if identifier.startswith('_'):
				continue
			currentWeight += weight
			ret = identifier
			if rdm <= currentWeight:
				break
		return ret

	def GetClosestTarget(self, pos):
		minDis = -1
		target = None
		for eid in self._aliveTargets:
			health = engineApiGas.GetAttrValue(eid, HealthAttrEnum)
			if health > 0:
				dis = MathUtils.TupleLength(MathUtils.TupleSub(engineApiGas.GetEntityPos(eid), pos))
				if minDis < 0 or minDis > dis:
					minDis = dis
					target = eid
		players = self._battleEvent.Players
		for eid in players:
			health = engineApiGas.GetAttrValue(eid, HealthAttrEnum)
			if health > 0:
				dis = MathUtils.TupleLength(MathUtils.TupleSub(engineApiGas.GetEntityPos(eid), pos))
				if minDis < 0 or minDis > dis:
					minDis = dis
					target = eid
		return target

	def Completed(self):
		return self._startTime < 0

	def OnOutRange(self):
		for eid in self._aliveTargets:
			health = engineApiGas.GetAttrValue(eid, HealthAttrEnum)
			if health > 0:
				engineApiGas.KillEntity(eid)