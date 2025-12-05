# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3
from ScukeSurviveScript.ScukeCore.server import engineApiGas

CompFactory = serverApi.GetEngineCompFactory()
DefaultHurtCD = 10

class DamageServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(DamageServerSystem, self).__init__(namespace, systemName)
		self._currentDamageEid = '-1'
		self._currentDamageSource = None
		self._currentRecordContext = None
		self._recordStackCount = 0
		self._damageRecords = []
		self._gameComp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnBeginBulletDamageRecord(self, args):
		self._gameComp.SetHurtCD(0)
		self.BeginDamageRecord(args['fromId'], 'gun')

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnAppendBulletDamageRecord(self, args):
		if self._currentDamageEid != args['fromId']:
			return
		self._currentRecordContext = {
			'damage': args['damage'],
			'eid': args['eid'],
			'pos': args['pos'],
			'critical': args['critical'],
			'dead': args['to'] == 0,
		}

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnEndBulletDamageRecord(self, args):
		self.EndDamageRecord()
		self._gameComp.SetHurtCD(DefaultHurtCD)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
	def OnBeginMeleeDamageRecord(self, args):
		self._gameComp.SetHurtCD(0)
		self.BeginDamageRecord(args['fromId'], 'melee')

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
	def OnAppendMeleeDamageRecord(self, args):
		if self._currentDamageEid != args['fromId']:
			return
		self._currentRecordContext = {
			'damage': args['damage'],
			'eid': args['eid'],
			'pos': args['pos'],
			'critical': args['critical'],
			'dead': args['to'] == 0,
		}

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
	def OnEndMeleeDamageRecord(self, args):
		self.EndDamageRecord()
		self._gameComp.SetHurtCD(DefaultHurtCD)

	@EngineEvent()
	def HealthChangeServerEvent(self, args):
		damage = args['from'] - args['to']
		eid = args['entityId']
		if self._currentRecordContext:
			info = self._currentRecordContext
			info['damage'] = damage
			info['dead'] = args['to'] <= 0
			self._damageRecords.append(info)
			self._currentRecordContext = None
			return
		info = {'damage': damage, 'eid': eid, 'pos': engineApiGas.GetEntityPos(eid), 'dead': args['to'] == 0}
		self.NotifyDamage('-1', [info])


	def NotifyDamage(self, fromId, damages, source=None):
		self.NotifyToClient(fromId, 'OnHealthDamage', {
			'fromId': fromId,
			'source': source,
			'damages': damages
		})

	def BeginDamageRecord(self, eid, source=None):
		if self._currentDamageEid != eid:
			self._currentDamageEid = eid
			self._currentDamageSource = source
			del self._damageRecords[:]
			self._recordStackCount = 0
		else:
			self._recordStackCount += 1


	def EndDamageRecord(self):
		if self._currentDamageEid == '-1':
			return
		self._recordStackCount -= 1
		if self._recordStackCount > 0:
			return
		if len(self._damageRecords) > 0:
			self.NotifyDamage(self._currentDamageEid, self._damageRecords, self._currentDamageSource)
		self._currentDamageEid = '-1'
		self._currentDamageSource = None


	def ApplyDamageEffect(self, fromEid, toEid, hitEffect, hit, recordFunc=None, useHurt=False, damageParam=None, damageType=None):
		if toEid == '-1':
			return
		if engineApiGas.GetEntityRider(fromEid) == toEid:
			return
		pos = (hit['x'], hit['y'], hit['z'])
		critical = False if 'weakness' not in hit else hit['weakness']
		knock = False if 'knock' not in hitEffect else hitEffect['knock']
		if knock and knock > 0:
			curPos = engineApiGas.GetEntityPos(fromEid)
			collisionComp = CompFactory.CreateCollisionBox(toEid)
			cSize = collisionComp.GetSize()
			rSize = MathUtils.Clamp(MathUtils.TupleLength(cSize)/2.0, 1.0, 10.0)
			knock *= 1.0 / (rSize*rSize)
			motionComp = CompFactory.CreateActorMotion(toEid)
			dir = Vector3(MathUtils.TupleSub(pos, curPos)).Normalized() + Vector3.Up()
			dir.Normalize()
			motion = (dir * knock).ToTuple()
			motionComp.SetMotion(motion)
			self.BroadcastToAllClient('OnDamageKnock', {
				'fromId': fromEid,
				'toId': toEid,
				'motion': motion,
			})
		# 根据传递进来的伤害参数，叠加伤害
		damage = hitEffect['damage']
		if critical and 'critical' in hitEffect:
			damage = hitEffect['critical']
		coef = 1.0
		if damageParam:
			if '_coef' in damageParam:
				coef *= damageParam['_coef']
			if '_chargeCoef' in damageParam:
				coef *= damageParam['_chargeCoef']
		damage = int(coef * damage)
		if damageParam:
			for key in damageParam:
				if key.startswith('_'):
					continue
				damage += damageParam[key]
			damage = int(damage)
		attrComp = CompFactory.CreateAttr(toEid)
		healthEnum = serverApi.GetMinecraftEnum().AttrType.HEALTH
		curHealth = attrComp.GetAttrValue(healthEnum)
		afterHealth = curHealth - damage
		if afterHealth < 0:
			afterHealth = 0
		# TODO PreDamageEvent
		if recordFunc:
			recordFunc({
				'fromId': fromEid,
				'eid': toEid,
				'damage': damage,
				'critical': critical,
				'pos': pos,
				'to': afterHealth
			})
		# identifier = CompFactory.CreateEngineType(toEid).GetEngineTypeStr()
		# 对原版生物使用Hurt
		#if not identifier.startswith(modConfig.ModNameSpace):
		# 这里useHurt为True，所以将代码改一下
		# useHurt = True
		# if useHurt:
		hurtComp = CompFactory.CreateHurt(toEid)
		actorDamageCause = serverApi.GetMinecraftEnum().ActorDamageCause
		damageCause = actorDamageCause.EntityAttack
		if damageType is not None:
			damageCause = actorDamageCause.Custom
		hurtComp.Hurt(damage, damageCause, fromEid, knocked=False, customTag=damageType)  # 无法同时多次调用
		# else:
		# 	attrComp.SetAttrValue(healthEnum, afterHealth)



	def ApplyEffects(self, fromEid, eid, effects):
		mcEffectTypeEnum = serverApi.GetMinecraftEnum().EffectType
		for effect in effects:
			type = effect['type']
			mcEffectType = getattr(mcEffectTypeEnum, type, None)
			if mcEffectType == None:
				continue
			duration = effect['duration']
			amplifier = effect['amplifier']
			if not engineApiGas.AddEffectToEntity(eid, mcEffectType, duration, amplifier):
				self.logger.warning('ApplyEffects Failed %s %f %f', type, duration, amplifier)
