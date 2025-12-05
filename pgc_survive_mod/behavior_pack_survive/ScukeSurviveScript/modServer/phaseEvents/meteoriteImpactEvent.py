# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modServer.phaseEvents.phaseEvent import PhaseEvent
from ScukeSurviveScript.modCommon.cfg.phaseEvent.meteoriteImpact import MeteoriteReplaceBlocks
import mod.server.extraServerApi as serverApi
import random


class MeteoriteImpactEvent(PhaseEvent):
	def __init__(self, system, name, eventStateChangedCall=None):
		super(MeteoriteImpactEvent, self).__init__(system, name, eventStateChangedCall)
		self._spawnTime = 0
		# 生成陨石timer
		self._placeTimer = None
		self._placeDictList = []
		self._blockComp = serverApi.GetEngineCompFactory().CreateBlockInfo(self._system.mLevelId)

	def Destroy(self):
		if self._placeTimer:
			engineApiGas.CancelTimer(self._placeTimer)
			self._placeTimer = None
		return super(MeteoriteImpactEvent, self).Destroy()

	def EventUpdate(self, days, daytime):
		daytime = (days-self._days) * 24000 + daytime
		if daytime > self._spawnTime:
			intervalRange = self.Config['spawnInterval']
			interval = random.randint(intervalRange[0], intervalRange[1])
			self._spawnTime = daytime + interval
			players = self._system.GetPlayers()
			meteorites = self.Config['meteorites']
			spawnArea = self.Config['spawnArea']
			spawnHeight = self.Config['spawnHeight']
			spawnDir = self.Config['spawnDir']
			for playerId in players:
				dim = engineApiGas.GetEntityDimensionId(playerId)
				if dim != 0:  # 只在主世界生成
					continue
				centerPos = engineApiGas.GetEntityFootPos(playerId)
				if centerPos:
					self.SpawnMeteorite(meteorites, spawnArea, spawnHeight, spawnDir, centerPos)

	def OnStateChange(self, state, days, daytime):
		self._spawnTime = 0

	def SpawnMeteorite(self, meteorites, xzSize, yRange, spawnDir, centerPos):
		r = random.random() * 100.0
		rn = 0
		identifier = None
		for k, v in meteorites.iteritems():
			rn += v
			if r <= rn:
				identifier = k
				break
		if identifier is None:
			return
		rx = random.randint(-xzSize[0], xzSize[0])
		rz = random.randint(-xzSize[1], xzSize[1])
		ry = random.randint(yRange[0], yRange[1])
		centerPos = (centerPos[0], 0, centerPos[2])
		pos = (rx, ry, rz)
		pos = MathUtils.TupleAdd(pos, centerPos)
		eid = self._system.CreateEngineEntityByTypeStr(identifier, pos, serverApi.GetRotFromDir(spawnDir), 0)
		if eid:
			info = {
				'identifier': identifier,
				'eid': eid,
				'pos': pos
			}
			self._system.BroadcastToAllClient('OnMeteoriteSapwn', info)

	@EngineEvent()
	def ProjectileDoHitEffectEvent(self, args):
		eid = args['id']
		identifier = engineApiGas.GetEngineTypeStr(eid)
		if identifier and identifier.startswith('scuke_survive:meteorite_'):
			hitPos = (args['x'], args['y'], args['z'])
			self._system.BroadcastToAllClient('OnMeteoriteHit', {
				'eid': eid,
				'pos': hitPos
			})

			# 生成陨石矿石
			dimension = engineApiGas.GetEntityDimensionId(eid)
			self.TryPlaceYttriumOre(dimension, hitPos)
		pass

	def TryPlaceYttriumOre(self, dimension, pos):
		"""尝试在范围内生成陨石矿石"""
		if not self.Config:
			return

		oreCfg = self.Config.get("oreData", {})
		if oreCfg:
			count = oreCfg.get("count", 0)
			if type(count) == tuple:
				# 随机数量
				count = random.randint(count[0], count[1])
			if count > 0:
				self._placeDictList.append({"dimension": dimension, "pos": pos, "count": count})
				# 启动timer
				if not self._placeTimer:
					self._placeTimer = engineApiGas.AddRepeatTimer(oreCfg.get("cd", 0.25), self.PlaceYttriumOreTimer)
		pass

	def PlaceYttriumOreTimer(self):
		"""生成陨石矿石timer"""
		if len(self._placeDictList) > 0:
			oreCfg = self.Config.get("oreData", {})
			val = self._placeDictList[0]
			if val.get("count") > 0:
				val["count"] -= 1
				# 随机位置
				range = oreCfg.get("range", 0)
				if range > 0:
					pos = (
						val["pos"][0] - random.randint(-range, range),
						val["pos"][2] - random.randint(-range, range)
					)
				else:
					pos = (val["pos"][0], val["pos"][2])
				height = self._blockComp.GetTopBlockHeight(pos)
				if height is None:
					height = int(val["pos"][1])
				else:
					height = int(height)
				pos = (int(pos[0]), height, int(pos[1]))
				# 判断方块是否可生成
				dim = val["dimension"]
				block = self._blockComp.GetBlockNew(pos, dim)
				# 如果是原版方块、且硬度低于2，则可替换
				if block:
					blockName = block.get("name", "")
					canPlace = False
					if blockName in MeteoriteReplaceBlocks:
						canPlace = True
					elif blockName.startswith("minecraft:") and "shulker_box" not in blockName:
						# 潜影盒硬度是2，需要排除
						info = self._blockComp.GetBlockBasicInfo(blockName)
						if info and info.get("destroyTime", 0) > 0 and info.get("hardness", 0) <= 2:
							canPlace = True
					if canPlace:
						# 生成方块
						self._blockComp.SetBlockNew(pos, oreCfg["block"], 1, dim, updateNeighbors=False)
			else:
				self._placeDictList.pop(0)
		else:
			engineApiGas.CancelTimer(self._placeTimer)
			self._placeTimer = None
		pass
