# -*- coding: utf-8 -*-
import math

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.defines.monsterEnum import MosterAbilityEventEnum
comp = serverApi.GetEngineCompFactory()

class MobServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(MobServerSystem, self).__init__(namespace, systemName)

	# @EngineEvent(priority=10)
	# def ServerSpawnMobEvent(self, args):
	# 	# 这边是设置不刷怪区域，需调高优先级
	# 	identifier = args['realIdentifier']
	# 	if not identifier.startswith(modConfig.ModNameSpace):
	# 		return
	# 	if identifier.startswith(modConfig.NPCIdentifierPrefix):
	# 		return
	# 	spawnPos = (int(args['x']), int(args['y']), int(args['z']))
	# 	dimensionID = args['dimensionId']
	# 	if not self.CheckCanSpawn(identifier, spawnPos, dimensionID):
	# 		args['cancel'] = True
	# 		return
	
	def CheckCanSpawn(self, identifier, spawnPos, dimensionID):
		"""判断是否能生成"""
		comp = serverApi.GetEngineCompFactory().CreateFeature(dimensionID)
		pos = comp.LocateStructureFeature(serverApi.GetMinecraftEnum().StructureFeatureType.Village, dimensionID, spawnPos)
		if not pos:
			return True
		# 村庄附近
		dis = self.DistanceSqrt((pos[0], spawnPos[1], pos[-1]), spawnPos)
		if 0 <= dis < modConfig.CheckVillageDis ** 2:
			self.logger.info("near village")
			return False
		return True

	def DistanceSqrt(self, pos1, pos2):
		if pos1 is None or pos2 is None:
			return -1
		return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnPhaseSpawnMob(self, data):
		args = data['args']
		mob = data['config']
		eid = self.CreateEngineEntityByTypeStr(
			mob['type'],
			args['pos'],
			args['rot'],
			args['dim'],
			False)
		if eid:
			#print 'OnPhaseSpawnMob', mob['type'], eid
			if 'attrs' in mob:
				self.InitMobAttributes(eid, mob['attrs'])
			if 'effects' in mob:
				self.InitMobEffects(eid, mob['effects'])
			self.SetMobAttributesCoef(eid, args)
			self.SetMobAbilities(eid, args)

	def SetMobAbilities(self, eid, args):
		abilities = args.get('abilities', None)
		if not abilities or len(abilities) <= 0:
			return
		eventComp = serverApi.GetEngineCompFactory().CreateEntityEvent(eid)
		for event in abilities:
			if event == MosterAbilityEventEnum.FireResistance:
				# 抗火，加buff
				effectComp = serverApi.GetEngineCompFactory().CreateEffect(eid)
				effectComp.AddEffectToEntity(event, 32767, 1, False)
			else:
				eventComp.TriggerCustomEvent(eid, event)
		pass

	def SetMobAttributesCoef(self, eid, args):
		mcAttrTypeEnum = serverApi.GetMinecraftEnum().AttrType
		healthCoef = args.get('healthCoef')
		speedCoef = args.get('speedCoef')
		damageCoef = args.get('damageCoef')
		armorCoef = args.get('armorCoef')
		# 血量
		self._SetMobAttributeCoef(eid, mcAttrTypeEnum.HEALTH, healthCoef)
		# 速度
		self._SetMobAttributeCoef(eid, mcAttrTypeEnum.SPEED, speedCoef, True)
		self._SetMobAttributeCoef(eid, mcAttrTypeEnum.LAVA_SPEED, speedCoef, True)
		self._SetMobAttributeCoef(eid, mcAttrTypeEnum.UNDERWATER_SPEED, speedCoef, True)
		# 伤害
		self._SetMobAttributeCoef(eid, mcAttrTypeEnum.DAMAGE, damageCoef)
		# TODO 护甲


	def _SetMobAttributeCoef(self, eid, attrType, coef, floatable = False):
		cur = engineApiGas.GetAttrMaxValue(eid, attrType)
		if cur is None:
			self.logger.warning('SetMobAttributeCoef attr %r is None' % attrType)
			return
		cur = coef * cur
		if not floatable:
			cur = int(math.ceil(cur))
		engineApiGas.SetAttrMaxValue(eid, attrType, cur)
		engineApiGas.SetAttrValue(eid, attrType, cur)

	def InitMobAttributes(self, eid, attrs):
		mcAttrTypeEnum = serverApi.GetMinecraftEnum().AttrType
		modifyAttrs = attrs.keys()
		for type in modifyAttrs:
			mcAttrType = getattr(mcAttrTypeEnum, type, None)
			if mcAttrType == None:
				continue
			newValue = attrs[type]
			if not engineApiGas.SetAttrValue(eid, mcAttrType, newValue):
				self.logger.warning('InitMobAttributes Failed %s %f', type, newValue)

	def InitMobEffects(self, eid, effects):
		mcEffectTypeEnum = serverApi.GetMinecraftEnum().EffectType
		for effect in effects:
			type = effect['type']
			mcEffectType = getattr(mcEffectTypeEnum, type, None)
			if mcEffectType == None:
				continue
			duration = effect['duration']
			amplifier = effect['amplifier']
			if not engineApiGas.AddEffectToEntity(eid, mcEffectType, duration, amplifier):
				self.logger.warning('InitMobEffects Failed %s %f %f', type, duration, amplifier)

	@EngineEvent()
	def ProjectileDoHitEffectEvent(self,args):
		id = args['id']
		projectileName = comp.CreateEngineType(id).GetEngineTypeStr()
		if projectileName == "scuke_survive:projectile_random_zombie" or projectileName == "scuke_survive:projectile_zombie" or projectileName == "scuke_survive:projectile_zombie_baby":
			comp.CreatePos(id).SetPos((args['x'],args['y']+1,args['z']))