# -*- encoding: utf-8 -*-
import math
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, MathUtils
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.damageTagEnum import DamageTagEnum
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.defines.projectileEnum import ProjectileEnum

CompFactory = serverApi.GetEngineCompFactory()
HitscanFilter = serverApi.GetMinecraftEnum().RayFilterType.BothEntitiesAndBlock
IgnoreBlockEntity = [
	'minecraft:item',
	'minecraft:xp_orb',
	'minecraft:water',
	'minecraft:tallgrass',
	'minecraft:double_plant',
	'minecraft:yellow_flower',
	'minecraft:red_flower',
]

BreakBlockList = [
	"scuke_survive:items_oil_drum_small",
	"scuke_survive:items_oil_drum_large",
]


class BulletServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(BulletServerSystem, self).__init__(namespace, systemName)
		self._shootBulletMap = {}
		self._bulletSpawnSummonMap = {}
		self._currentExplosion = None
		self._currentExplosionPid = '-1'
		self._breakingBlock = False
		self._recoverDurability = 0
		self._damageSystem = None
		self._gameComp = serverApi.GetEngineCompFactory().CreateGame(self.mLevelId)
		self._blockInfoComp = serverApi.GetEngineCompFactory().CreateBlockInfo(self.mLevelId)
		self._attrSystem = None
		self._meleeAttackSystem = None
		# setting
		self._S_damageCoef = 1.0
		self._S_blockBreaking = True

	# DEBUG
	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnClientGunTest(self, data):
		eid = data['playerId']
		pass

	def CreateClip(self, eid, identify, args):
		count = 1
		if 'count' in args:
			count = args['count']
		while count > 0:
			c = min(count, 64)
			itemDic = {
				'itemName': identify,
				'count': c,
				'showInHand': False,  # 重要！！！
			}
			if eid != '-1':
				engineApiGas.SpawnItemToPlayerInv(eid, itemDic)
			else:
				engineApiGas.SpawnItemToLevel(itemDic, args['position'])
			count -= c


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunShootBullet(self, args):
		eid = args['eid']
		config = args['config']
		position = args['position']
		direction = args['direction']
		self.Create(eid, config, position, direction, args)

	def Create(self, fromEid, config, position, direction, data):
		if not self._attrSystem:
			self._attrSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		if not self._meleeAttackSystem:
			self._meleeAttackSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
		ret = None
		self.BeginDamageRecord(fromEid)
		shootEffectType = config['type']
		chargeLevel = data.get('chargeLevel', 0) - 1
		if shootEffectType == 'level' and 0 <= chargeLevel < len(config['levels']):
			ret = self.Create(fromEid, config['levels'][chargeLevel], position, direction, data)
		if shootEffectType == 'hitscan':
			ret = self.CreateHitscan(fromEid, config, position, direction, data)
		elif shootEffectType == 'projectile':
			ret = self.CreateProjectile(fromEid, config, position, direction, data)
		elif shootEffectType == 'shot':
			forward = Vector3(direction)
			shotRot = MathUtils.LookDirection(forward)

			angle = config['angle']
			count = config['count']
			layerCount = int(math.sqrt(count)) + 1
			layerAngleStep = angle / layerCount
			remainCount = count
			layerData = []
			curLayerAngle = 0
			for i in range(1, layerCount):
				cur = i * i
				if remainCount - cur < 0:
					cur = remainCount
				if i == layerCount - 1 and remainCount > cur:
					cur = remainCount
				r = math.tan(math.radians(curLayerAngle))
				curLayerDir = self._BuildShotLayerDir(shotRot, cur, r, i)
				remainCount -= cur
				curLayerAngle += layerAngleStep
				layerData.append(curLayerDir)
			if remainCount > 0:
				self.logger.error('shot bullet remainCount > 0')
			for i in range(len(layerData)):
				for j in range(len(layerData[i])):
					self.CreateHitscan(fromEid, config, position, layerData[i][j], data)
		elif shootEffectType == 'laser':
			ret = self.CreateLaser(fromEid, config, position, direction, data)
		self.EndDamageRecord()
		return ret

	def _BuildShotLayerDir(self, shotRot, count, r, layer):
		angleStep = 360 / count
		curAngle = angleStep / 2 * (layer % 2)
		curLayerDir = []
		for j in range(1, count + 1):
			curAngle = (curAngle + angleStep) % 360
			x = math.cos(math.radians(curAngle)) * r
			y = math.sin(math.radians(curAngle)) * r
			_dir = Vector3(x, y, 1.0)
			_dir.Normalize()
			_dir = shotRot * _dir
			curLayerDir.append(_dir.ToTuple())
		return curLayerDir

	def CreateLaser(self, fromEid, config, position, direction, data):
		eid = fromEid  # 无实体
		self.Add(fromEid, eid, config, position, direction, data)
		laserSize = config['size']
		laserSplitSize = config['splitSize']
		distance = config['distance']
		distanceSize = int(distance / laserSplitSize)
		laserSize = (laserSize[0], laserSize[1], distanceSize)
		bullet = self.Get(eid)
		targets = self._meleeAttackSystem.BoxDetect(fromEid, bullet['dim'], position, direction, laserSize, (0, 0, distanceSize/2.0), laserSplitSize)
		if not targets or len(targets) <= 0:
			bullet['endPosition'] = MathUtils.TupleAddMul(position, direction, distance)
			bullet['endDirection'] = direction
			self.OnDead(bullet)
		else:
			minBlockDis = -1
			minTargetDis = -1
			closetTarget = None
			closetBlock = None
			fromPos = Vector3(position)
			dir = Vector3(direction)
			for target in targets:
				p = Vector3(target['x'], target['y'], target['z'])
				temp = p - fromPos
				dis = Vector3.Dot(temp, dir)
				if target['type'] == 'Entity':
					if minTargetDis < 0 or dis < minTargetDis:
						minTargetDis = dis
						closetTarget = target
				else:
					if minBlockDis < 0 or dis < minBlockDis:
						minBlockDis = dis
						closetBlock = target
			endTarget = closetTarget
			if endTarget is None:
				endTarget = closetBlock
			endPos = Vector3(endTarget['x'], endTarget['y'], endTarget['z'])
			t = Vector3.Dot(endPos-fromPos, dir)
			endPos = fromPos + t * dir
			if endTarget:
				hit = {
					'srcId': eid,
					'targetId': endTarget['entityId'],
					'x': endPos.x,
					'y': endPos.y,
					'z': endPos.z,
					'hitFace': self.GetHitFace(MathUtils.TupleMul(direction, -1)),
				}
				if 'blockPosX' in endTarget:
					hit['blockPosX'] = endTarget['blockPosX']
					hit['blockPosY'] = endTarget['blockPosY']
					hit['blockPosZ'] = endTarget['blockPosZ']
				self.OnHit(eid, hit)
				self.DestroyBullet(eid)
			else:
				bullet['endPosition'] = endPos.ToTuple()
				bullet['endDirection'] = direction
				self.OnDead(bullet)
		return None


	def CreateHitscan(self, fromEid, config, position, direction, data):
		eid = fromEid  # 无实体
		self.Add(fromEid, eid, config, position, direction, data)
		distance = config['distance']
		bullet = self.Get(eid)
		target = self.DoHitscan(eid, position, direction, distance, bullet['dim'])
		if not target:
			bullet['endPosition'] = MathUtils.TupleAddMul(position, direction, distance)
			bullet['endDirection'] = direction
			self.OnDead(bullet)
		else:
			self.OnHit(eid, target)
			self.DestroyBullet(eid)

		return None

	def DoHitscan(self, eid, position, direction, dis, dim):
		targets = serverApi.getEntitiesOrBlockFromRay(dim, position, direction, dis, True, HitscanFilter)
		if targets and len(targets) > 0:
			for target in targets:
				type = target['type']
				identifier = target['identifier']
				if identifier in IgnoreBlockEntity:
					continue
				if type == 'Block' and self.IsIgnoreBlock(target['pos'], dim):
					continue
				if 'hitPos' not in target:
					if 'pos' in target:
						target['hitPos'] = target['pos']
					elif 'entityId' in target:
						target['hitPos'] = engineApiGas.GetEntityPos(target['entityId'])
					else:
						# print 'getEntitiesOrBlockFromRay', target
						self.logger.warning('getEntitiesOrBlockFromRay not support hitPos')
						return None
				hitPos = target['hitPos']
				id = '-1'

				if type == 'Entity':
					id = target['entityId']
					if id == eid:
						continue
					if not self._gameComp.IsEntityAlive(id):
						continue
				ret = {
					'srcId': eid,
					'targetId': id,
					'x': hitPos[0], 'y': hitPos[1], 'z': hitPos[2],
					'hitFace': self.GetHitFace(MathUtils.TupleMul(direction, -1)),
				}
				if 'pos' in target:
					blockPos = target['pos']
					ret['blockPosX'] = blockPos[0]
					ret['blockPosY'] = blockPos[1]
					ret['blockPosZ'] = blockPos[2]
				# 单独针对电磁弹做处理
				if identifier == ProjectileEnum.EMMissile:
					# 如果是电磁弹，则直接销毁
					self.DestroyEntity(target['entityId'])
				return ret
		return None

	def IsIgnoreBlock(self, pos, dim):
		comp = self._blockInfoComp
		blockDict = comp.GetBlockCollision(pos, dim)
		if not blockDict:
			return True
		size = MathUtils.TupleSub(blockDict['max'], blockDict['min'])
		return max(size) <= 0

	def GetHitFace(self, direction):
		# TODO 朝向转FaceId
		return 0

	def IsWeakness(self, eid, pos):
		typeComp = CompFactory.CreateEngineType(eid)
		EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType
		if typeComp.GetEngineType() != EntityTypeEnum.Mob:
			return False
		identifier = typeComp.GetEngineTypeStr()
		if not identifier.startswith(modConfig.ModNameSpace):
			return False
		if 'zombie' in identifier:
			collider = CompFactory.CreateCollisionBox(eid)
			footPos = engineApiGas.GetEntityFootPos(eid)
			size = collider.GetSize()
			dY = pos[1] - footPos[1]
			return dY / size[1] > 0.7

		return False

	def CreateProjectile(self, fromEid, config, position, direction, data):
		comp = CompFactory.CreateProjectile(fromEid)
		id = config['identifier']
		param = {
			'position': position,
			'direction': direction,
		}
		if 'gravity' in config:
			param['gravity'] = config['gravity']
		if 'power' in config:
			param['power'] = config['power']
		eid = comp.CreateProjectileEntity(fromEid, id, param)
		if eid == '-1':
			return None
		self.Add(fromEid, eid, config, position, direction, data)
		self.BroadcastToAllClient('OnBulletEntityCreated', {
			'fromId': fromEid,
			'eid': eid
		})
		return eid

	def Add(self, fromId, eid, config, position, direction, data):
		dim = engineApiGas.GetEntityDimensionId(eid)
		# 根据玩家的属性，计算叠加的枪械伤害值
		damageParam = {}
		if self._attrSystem:
			gunDamage = self._attrSystem.GetAttr(fromId, "GunDamage")
			if gunDamage is None:
				gunDamage = 0
			damageParam = {
				"_coef": self._S_damageCoef,
				"_chargeCoef": data.get('chargeCoef', 1.0),
				"GunDamage": gunDamage,
			}
		self._shootBulletMap[eid] = {
			'fromId': fromId,
			'eid': eid,
			'dim': dim,
			'config': config,
			'spawnTime': time.time(),
			'position': position,
			'direction': direction,
			'damageParam': damageParam,
			'level': data.get('chargeLevel', 0)
		}

	def Get(self, eid):
		if eid in self._shootBulletMap:
			return self._shootBulletMap[eid]
		return None

	def Remove(self, eid):
		if eid in self._shootBulletMap:
			del self._shootBulletMap[eid]

	def DestroyBullet(self, eid):
		bullet = self.Get(eid)
		if not bullet:
			return
		if bullet['fromId'] != bullet['eid']:
			engineApiGas.KillEntity(eid)
			self.BroadcastToAllClient('OnBulletEntityDestroy', {
				'fromId': bullet['fromId'],
				'eid': bullet['eid'],
			})
		self.Remove(eid)

	def Update(self):
		# 生命周期维护
		curTime = time.time()
		destroyBullets = []
		for bullet in self._shootBulletMap.values():
			deltaTime = curTime - bullet['spawnTime']
			lifeTime = bullet['config']['lifeTime']
			if deltaTime > lifeTime:
				eid = bullet['eid']
				bullet['endPosition'] = engineApiGas.GetEntityPos(eid)
				bullet['endDirection'] = serverApi.GetDirFromRot(engineApiGas.GetEntityRot(eid))
				destroyBullets.append(bullet)

		for bullet in destroyBullets:
			self.OnDead(bullet)

	'''
	SpawnProjectileServerEvent
	ProjectileDoHitEffectEvent
	'''

	@EngineEvent()
	def ProjectileDoHitEffectEvent(self, args):
		eid = args['id']
		self.OnHit(eid, args)

	def OnHit(self, eid, hitInfo):
		# TODO 可添加检查是否碰撞 hitInfo['cancel'] = True
		bullet = self.Get(eid)
		if not bullet:
			return
		fromId = str(hitInfo['srcId'])
		targetId = str(hitInfo['targetId'])
		if targetId == fromId:
			hitInfo['cancel'] = True
			return
		hit = {
			'x': hitInfo['x'],
			'y': hitInfo['y'],
			'z': hitInfo['z'],
			'dim': bullet['dim'],
			'hitFace': hitInfo['hitFace'],
			'weakness': self.IsWeakness(targetId, (hitInfo['x'], hitInfo['y'], hitInfo['z']))
		}
		if targetId == '-1':
			blockPos = (hitInfo['blockPosX'], hitInfo['blockPosY'], hitInfo['blockPosZ'])
			if self.CheckBlockBreakable(fromId, bullet, blockPos):
				self.BreakBlock(fromId, blockPos, bullet['dim'])
		isProjectile = fromId != eid
		if isProjectile:
			self.BeginDamageRecord(fromId)
		self.DoHitEffect(fromId, eid, [targetId], [hit], bullet)
		if isProjectile:
			self.EndDamageRecord()
			engineApiGas.AddTimer(0, self.DestroyBullet, eid)
			#self.DestroyBullet(eid)

	def OnDead(self, bullet):
		endPos = bullet['endPosition']
		endDir = bullet['endDirection']
		self.BroadcastToAllClient('OnHitEnd', {
			'fromId': bullet['fromId'],
			'eid': bullet['eid'],
			'endPosition': endPos,
			'endDirection': endDir,
			'level': bullet['level']
		})
		# TODO 添加子弹非碰撞销毁效果

		self.DestroyBullet(bullet['eid'])

	def DoHitEffect(self, fromEid, eid, targets, hits, bullet):
		self.BroadcastToAllClient('OnHitTargets', {
			'fromId': fromEid,
			'targets': targets,
			'hits': hits,
			'level': bullet['level']
		})
		for (targetId, hit) in zip(targets, hits):
			self.ApplyHitEffect(fromEid, targetId, bullet, hit)

	def BeginDamageRecord(self, pid):
		self.BroadcastEvent('OnBeginBulletDamageRecord', {'fromId': pid})

	def AppendDamageRecord(self, info):
		self.BroadcastEvent('OnAppendBulletDamageRecord', info)

	def EndDamageRecord(self):
		self.BroadcastEvent('OnEndBulletDamageRecord', {})

	def ApplyHitEffect(self, fromEid, toEid, bullet, hit):
		config = bullet['config']
		hitEffect = config['hitEffect']
		self._ApplyHitEffect(fromEid, toEid, bullet, hit, hitEffect)

	def _ApplyHitEffect(self, fromEid, toEid, bullet, hit, hitEffect):
		type = hitEffect['type']
		if type == 'damage':
			# TODO 伤害按距离衰减等需求
			damageParam = bullet['damageParam']
			self.ApplyDamageEffect(fromEid, toEid, hitEffect, hit, damageParam)
		elif type == 'explosion':
			self.ApplyExplosionEffect(fromEid, bullet, hit)
		elif type == 'spawn':
			self.ApplySpawnEntity(fromEid, toEid, bullet, hitEffect, hit)
		elif type == 'array':
			hits = hitEffect['hits']
			for item in hits:
				self._ApplyHitEffect(fromEid, toEid, bullet, hit, item)

	def ApplySpawnEntity(self, fromEid, toEid, bullet, hitEffect, hit):
		import random
		pos = (hit['x'], hit['y'], hit['z'])
		rot = serverApi.GetRotFromDir(bullet['direction'])
		mob = hitEffect['identifier']
		if fromEid not in self._bulletSpawnSummonMap:
			self._bulletSpawnSummonMap[fromEid] = []
		if not self.CheckSpawnSummonCondition(fromEid, mob, hitEffect):
			return
		for i in range(0, hitEffect['count']):
			pos_ = pos
			if i > 0:
				pos_ = MathUtils.TupleAdd(pos, (random.random() - 0.5, random.random() - 0.5, random.random() - 0.5))
			summonEid = self.CreateEngineEntityByTypeStr(
				mob,
				pos_,
				rot,
				hit['dim'],
				False)
			if summonEid != '-1':
				self._bulletSpawnSummonMap[fromEid].append({
					'eid': summonEid,
					'identifier': mob
				})
				comp = CompFactory.CreateActorOwner(summonEid)
				comp.SetEntityOwner(fromEid)
				#CompFactory.CreatePlayer(summonEid).OpenPlayerHitMobDetection()

	def GetSpawnSummonAlive(self, eid, summonIdentifier):
		summons = self._bulletSpawnSummonMap[eid]
		i = 0
		ret = []
		while i < len(summons):
			item = summons[i]
			if self._gameComp.IsEntityAlive(item['eid']):
				i += 1
				if item['identifier'] == summonIdentifier:
					ret.append(item['eid'])
			else:
				summons.pop(i)
		return ret

	def CheckSpawnSummonCondition(self, eid, summonIdentifier, hitEffect):
		return True

	def ApplyExplosionEffect(self, fromEid, bullet, hit):
		config = bullet['config']
		hitEffect = config['hitEffect']
		radius = hitEffect['radius']
		fire = hitEffect['fire']
		breaks = hitEffect['breaks']
		pos = (hit['x'], hit['y'], hit['z'])
		self._currentExplosion = hitEffect
		self._currentExplosionPid = fromEid
		serverApiMgr.CreateExplosion(bullet['eid'], fromEid, pos, radius, fire, breaks)
		self._currentExplosion = None
		self._currentExplosionPid = '-1'

	@EngineEvent()
	def DamageEvent(self, args):
		if self._currentExplosionPid == args['srcId']:
			if engineApiGas.GetEntityRider(args['srcId']) == args['entityId']:
				args['damage'] = 0

	@EngineEvent()
	def ExplosionServerEvent(self, args):
		if not self._currentExplosion or 'addonDamage' not in self._currentExplosion:
			return
		if not self._S_blockBreaking:
			blocks = args['blocks']
			for block in blocks:
				block[3] = True
		addonDamage = self._currentExplosion['addonDamage']
		victims = args['victims']
		for eid in victims:
			if eid == self._currentExplosionPid:
				continue
			pos = engineApiGas.GetEntityPos(eid)
			if not pos:
				continue
			self.ApplyDamageEffect(self._currentExplosionPid, eid, {
				'damage': addonDamage
			}, {
				'x': pos[0],
				'y': pos[1] + 1,
				'z': pos[2],
				'weakness': False,
			})

	def ApplyDamageEffect(self, fromEid, toEid, hitEffect, hit, damageParam={}):
		if not self._damageSystem:
			self._damageSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.DamageServerSystem)
		if not self._damageSystem:
			return
		self._damageSystem.ApplyDamageEffect(fromEid, toEid, hitEffect, hit, self.AppendDamageRecord, damageParam=damageParam, damageType=DamageTagEnum.Bullet)

	def CheckBlockBreakable(self, fromEid, bullet, pos):
		dim = bullet['dim']
		block = engineApiGas.GetBlock(pos, dim)
		if block and block.get("name") in BreakBlockList:
			return True
		if not self._S_blockBreaking:
			return False
		if 'hardness' not in bullet['config']:
			return False
		hardness = bullet['config']['hardness']
		blockInfo = engineApiGas.GetBlockBasicInfo(block['name'])
		if blockInfo and 'destroyTime' in blockInfo and blockInfo['destroyTime'] >= 0:
			return round(hardness, 2) >= round(blockInfo['destroyTime'], 2)
		return False


	def BreakBlock(self, fromEid, pos, dim):
		# 先尝试引爆方块
		info = {"stage": "detonate_block", "cause": "gun", "pos": pos, "dimension": dim, "playerId": fromEid,}
		Instance.mEventMgr.NotifyEvent(eventConfig.DetonateExplodeBlockEvent, info)
		# 再执行破坏逻辑
		self._breakingBlock = True
		blockInfo = engineApiGas.GetBlock(pos, dim)
		engineApiGas.SetBlockNew(pos, {'name': 'minecraft:air'}, 1, dim)
		self.BroadcastEvent('BulletBreakingBlock', {
			'playerId': fromEid,
			'fullName': blockInfo['name'],
			'auxData': blockInfo['aux'],
			'dimensionId': dim,
			'x': pos[0],
			'y': pos[1],
			'z': pos[2],
		})
		self._breakingBlock = False

	@EngineEvent()
	def ServerPlayerTryDestroyBlockEvent(self, args):
		if self._breakingBlock:
			args['spawnResources'] = False


	@EngineEvent()
	def ItemDurabilityChangedServerEvent(self, args):
		if self._recoverDurability > 0:
			return
		if self._breakingBlock:
			playerId = args['entityId']
			keepValue = args['durabilityBefore']
			self._recoverDurability = keepValue
			engineApiGas.AddTimer(0, self.DelayRecoverDurability, playerId)

	def DelayRecoverDurability(self, playerId):
		comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
		comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, self._recoverDurability)
		self._recoverDurability = 0
