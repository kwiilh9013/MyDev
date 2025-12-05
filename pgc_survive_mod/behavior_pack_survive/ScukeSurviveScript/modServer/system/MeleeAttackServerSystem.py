# -*- encoding: utf-8 -*-
import math

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, MathUtils
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.damageTagEnum import DamageTagEnum

CompFactory = serverApi.GetEngineCompFactory()
RaycastFilter = serverApi.GetMinecraftEnum().RayFilterType.BothEntitiesAndBlock
IgnoreBlockEntity = [
	'minecraft:item',
	'minecraft:xp_orb',
	'minecraft:water',
	'minecraft:tallgrass',
	'minecraft:double_plant',
	'minecraft:yellow_flower',
	'minecraft:red_flower',
]


class MeleeAttackServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(MeleeAttackServerSystem, self).__init__(namespace, systemName)
		self._currentExplosion = None
		self._currentExplosionPid = '-1'
		self._damageSystem = None
		self._attrSystem = None
		self._blockInfoComp = CompFactory.CreateBlockInfo(self.mLevelId)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunMeleeAttack(self, args):
		eid = args['eid']
		config = args['attack']
		position = args['position']
		direction = args['direction']
		self.Create(eid, config, position, direction)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnMeleeAttack(self, args):
		eid = args['eid']
		config = args['attack']
		position = args['position']
		direction = args['direction']
		self.Create(eid, config, position, direction)

	def Create(self, fromEid, config, position, direction):
		self.BeginDamageRecord(fromEid)
		dim = engineApiGas.GetEntityDimensionId(fromEid)
		shapeConfig = config['shape']
		shapeType = shapeConfig['type']
		targets = None
		if shapeType == 'box':
			size = shapeConfig['size']
			offset = (0, 0, 0) if 'offset' not in shapeConfig else shapeConfig['offset']
			targets = self.BoxDetect(fromEid, dim, position, direction, size, offset)

		if targets and len(targets) > 0:
			self.BroadcastEvent('OnMeleeAttackTargets', {
				'fromId': fromEid,
				'targets': targets,
			})
			self.BroadcastToAllClient('OnHitTargets', {
				'fromId': fromEid,
				'targets': targets,
			})
			for target in targets:
				eid = target['entityId']
				self.ApplyAttack(fromEid, eid, config, target)

		self.EndDamageRecord()

	def BeginDamageRecord(self, pid):
		self.BroadcastEvent('OnBeginMeleeDamageRecord', {'fromId': pid})

	def AppendDamageRecord(self, info):
		self.BroadcastEvent('OnAppendMeleeDamageRecord', info)

	def EndDamageRecord(self):
		self.BroadcastEvent('OnEndMeleeDamageRecord', {})


	def ApplyAttack(self, fromEid, toEid, attackConfig, hit):
		effects = attackConfig['effects']
		# 根据玩家的属性，计算叠加的枪械伤害值
		damageParam = {}
		if not self._attrSystem:
			self._attrSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		if self._attrSystem:
			meleeDamage = self._attrSystem.GetAttr(fromEid, "MeleeDamage")
			if meleeDamage is None:
				meleeDamage = 0
			damageParam = {
				"MeleeDamage": meleeDamage,
			}
		self.ApplyDamageEffect(fromEid, toEid, attackConfig, hit, damageParam)

	def ApplyDamageEffect(self, fromEid, toEid, effect, hit, damageParam={}):
		if not self._damageSystem:
			self._damageSystem = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.DamageServerSystem)
		if not self._damageSystem:
			return

		self._damageSystem.ApplyDamageEffect(fromEid, toEid, effect, hit, self.AppendDamageRecord, damageParam=damageParam)


	def BoxDetect(self, fromEid, dim, position, direction, size, offset, splitSize=1.0):
		halfSize = tuple(a/2.0*splitSize for a in size)
		offset = MathUtils.TupleMul(offset, splitSize)
		pos = Vector3(position)
		dir = Vector3(direction)
		rot = MathUtils.LookDirection(dir)
		center = pos + rot * Vector3(offset)
		start = center - rot * Vector3(halfSize)
		up = rot * (Vector3.Up() * splitSize)
		right = rot * (Vector3.Right() * splitSize)
		x = size[0]
		y = size[1]
		dis = size[2]
		splitedX = range(0, x)
		splitedY = range(0, y)
		p = start
		targetsMap = {}
		for i in splitedX:
			q = p
			for j in splitedY:
				self.__SplitDetect(fromEid, dim, q, right, up, direction, dis, targetsMap, splitSize)
				q += up
			p += right
		return targetsMap.values()

	def __SplitDetect(self, fromEid, dim, pos, right, up, direction, dis, detectMap, splitSize=1.0):
		split = 2
		d = splitSize / split
		offsetDis = d / 2
		p = pos
		p += up * offsetDis
		p += right * offsetDis
		splited = range(0, split)
		for i in splited:
			q = p
			for j in splited:
				blocks = self.__Raycast(fromEid, dim, q.ToTuple(), direction, dis, False)
				if blocks and len(blocks) > 0:
					for block in blocks:
						key = block['entityId']
						if key == '-1':
							key = '%d_%d_%d' % (block['x'], block['y'], block['z'])
						if key not in detectMap:
							detectMap[key] = block
				q += up * d
			p += right * d

	def __Raycast(self, fromEid, dim, position, direction, dis, isThrouth=False, filter=RaycastFilter, ignoreBlockEntity = IgnoreBlockEntity):
		targets = serverApi.getEntitiesOrBlockFromRay(dim, position, direction, dis, True, filter)
		if targets and len(targets) > 0:
			ret = []
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
						print 'getEntitiesOrBlockFromRay not support hitPos', target
						continue
				hitPos = target['hitPos']
				if 'pos' in target:
					hitPos = target['pos']
				id = '-1'
				if type == 'Entity':
					id = target['entityId']
					if id == fromEid:
						continue
				info = {
					'entityId': id,
					'identifier': identifier,
					'type': type,
					'x': hitPos[0], 'y': hitPos[1], 'z': hitPos[2],
				}
				if 'pos' in target:
					blockPos = target['pos']
					info['blockPosX'] = blockPos[0]
					info['blockPosY'] = blockPos[1]
					info['blockPosZ'] = blockPos[2]
				ret.append(info)
				if not isThrouth:
					return ret
			return ret
		return None

	def IsIgnoreBlock(self, pos, dim):
		comp = self._blockInfoComp
		blockDict = comp.GetBlockCollision(pos, dim)
		if not blockDict:
			return True
		size = MathUtils.TupleSub(blockDict['max'], blockDict['min'])
		return max(size) <= 0
