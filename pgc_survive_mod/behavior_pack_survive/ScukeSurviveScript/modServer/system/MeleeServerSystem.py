# -*- encoding: utf-8 -*-

import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent

from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import meleeConfig as MeleeConfig
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.ScukeCore.server import engineApiGas

from ScukeSurviveScript.modCommon.handler.meleeHandler import MeleeHandler
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modServer.system.WeaponServerSystem import WeaponServerSystem

CompFactory = serverApi.GetEngineCompFactory()

OneSecondUpdate = 30.0
UpdateTimeMs = 1000.0 / OneSecondUpdate


class MeleeServerSystem(WeaponServerSystem):

	def __init__(self, namespace, systemName):
		super(MeleeServerSystem, self).__init__(namespace, systemName)
		self._meleeAttackFlag = False
		self._S_ignoreDurability = False

	def CreateMelee(self, eid, identify, args):
		gunDataKey = Instance.mDatasetManager.BuildKey('melee')
		itemDic = {
			'itemName': identify,
			'count': 1,
			'extraId': gunDataKey,
			'showInHand': False,  # 重要！！！
		}
		ret = False
		if eid != '-1':
			ret = engineApiGas.SpawnItemToPlayerInv(eid, itemDic)
		else:
			ret = engineApiGas.SpawnItemToLevel(itemDic, args['position'])
		if ret:
			Instance.mDatasetManager.SetLevelData(gunDataKey, {
				'clip': 0,
				'identifier': identify
			})

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, args):
		self.NotifyCurrentTakeMelee(args['playerId'])

	def NotifyCurrentTakeMelee(self, playerId):
		for eid, melee in self._playerWeaponMap.iteritems():
			self.NotifyToClient(playerId, 'OnTakeMelee', {
				'playerId': eid,
				'identifier': melee.Config['identifier'],
			})

	def Take(self, eid, weapon, data=None):
		config = weapon.Config
		self.BroadcastToAllClient('OnTakeMelee', {
			'playerId': eid,
			'identifier': config['identifier'],
		})
		super(MeleeServerSystem, self).Take(eid, weapon, data)

	def Remove(self, eid):
		melee = self.Get(eid)
		if melee:
			config = melee.Config
			self.BroadcastToAllClient('OnRemoveMelee', {
				'playerId': eid,
				'identifier': config['identifier']
			})
		super(MeleeServerSystem, self).Remove(eid)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
	def OnMeleeBegin(self, data):
		eid = data['playerId']
		melee = self.Get(eid)
		if not melee:
			return
		if data.get('ai', False):
			melee.KeyDown(self._time)
		self.BroadcastToAllClient('OnMeleeBegin', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
	def OnMeleeCast(self, data):
		eid = data['playerId']
		melee = self.Get(eid)
		if not melee:
			return
		self.BroadcastToAllClient('OnMeleeCast', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
	def OnMeleeAttack(self, data):
		eid = data['playerId']
		combo = data['combo']
		meleeTime = data['meleeTime']
		castTime = data['castTime']
		melee = self.Get(eid)
		if not melee:
			return
		attack = melee.GetMeleeAttack(combo, castTime, meleeTime)
		self._meleeAttackFlag = eid
		self.BroadcastEvent('OnMeleeAttack', {
			'eid': eid,
			'attack': attack,
			'position': data['position'],
			'direction': data['direction'],
		})
		self._meleeAttackFlag = None


	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
	def OnMeleeEnd(self, data):
		eid = data['playerId']
		melee = self.Get(eid)
		if not melee:
			return
		if data.get('ai', False):
			melee.KeyUp(self._time)
		self.BroadcastToAllClient('OnMeleeEnd', data)


	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.MeleeClientSystem)
	def OnMeleeKick(self, data):
		eid = data['playerId']
		melee = self.Get(eid)
		if not melee:
			return
		# TODO Melee kick damage
		self.BroadcastToAllClient('OnMeleeKick', data)

	@EngineEvent()
	def OnCarriedNewItemChangedServerEvent(self, args):
		itemName = args['newItemName']
		oldItemName = args['oldItemName']
		eid = args['playerId']
		# 装备
		if oldItemName.startswith(MeleeConfig.MeleeIdentifierPrefix):
			self.Remove(eid)
		if not itemName.startswith(MeleeConfig.MeleeIdentifierPrefix):
			return
		rider = engineApiGas.GetEntityRider(eid)
		if rider != '-1':
			riderIdentifier = engineApiGas.GetEngineTypeStr(rider)
			if riderIdentifier in MeleeConfig.ForbidTakeMeleeRides:
				return
		config = MeleeConfig.GetConfig(itemName)
		if not config:
			return
		item = args['newItemDict']
		extraId = item['extraId']
		meleeData = self.GetWeaponData(extraId)
		self.DelayTake(eid, MeleeHandler(eid, config, extraId), meleeData)


	@EngineEvent()
	def PlayerRespawnFinishServerEvent(self, args):
		eid = args['playerId']
		type = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
		item = serverApi.GetEngineCompFactory().CreateItem(eid).GetPlayerItem(type)
		if not item:
			return
		itemName = item['newItemName']
		if not itemName.startswith(MeleeConfig.MeleeIdentifierPrefix):
			return
		config = MeleeConfig.GetConfig(itemName)
		if not config:
			return
		extraId = item['extraId']
		meleeData = self.GetWeaponData(extraId)
		self.Take(eid, MeleeHandler(eid, config, extraId), meleeData)

	def Update(self):
		self.DoDelayTakeTask()

		dTime = UpdateTimeMs
		time = self._time + dTime
		for weapon in self._entityWeaponMap.itervalues():
			self.UpdateWeapon(weapon, time, dTime)
		self._time = time

		self.DoDelayRemoveTask()

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
	def OnMeleeAttackTargets(self, args):
		fromId = args['fromId']
		if fromId == self._meleeAttackFlag:
			for target in args['targets']:
				if target['type'] == 'Block':
					continue
				self.ReduceDurability(fromId)
				return

	def ReduceDurability(self, eid, value=1):
		if self._S_ignoreDurability:
			return
		gameComp = serverApi.GetEngineCompFactory().CreateGame(eid)
		if gameComp.GetPlayerGameType(eid) == serverApi.GetMinecraftEnum().GameType.Creative:
			return
		posType = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
		carried = engineApiGas.GetPlayerItem(eid, posType, 0)
		if carried is None:
			return
		itemName = carried['newItemName']
		if itemName.startswith(MeleeConfig.MeleeIdentifierPrefix):
			durability = max(carried['durability'] - value, 1)
			if durability > 0:
				engineApiGas.SetItemDurability(eid, posType, 0, durability)
				if durability <= 1:
					# 武器没耐久（锁1点），则修改命名
					engineApiGas.AddTimer(0.05, serverApiMgr.SetItemCustomNameSuffix, eid, itemName, '§c(已损坏)')
			# if durability == 0:
			# 	self.NotifyToClient(eid, 'OnMeleeBreak', {
			# 		'playerId': eid,
			# 		'identifier': itemName,
			# 	})
			# 	engineApiGas.SpawnItemToPlayerCarried(eid,  {'itemName': 'minecraft:air', 'count': 1})

	@EngineEvent(10)
	def EntityStopRidingEvent(self, args):
		eid = args['id']
		riderId = args['rideId']
		posType = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
		carried = engineApiGas.GetPlayerItem(eid, posType, 0)
		if carried is None:
			return
		itemName = carried['newItemName']
		if not itemName.startswith(MeleeConfig.MeleeIdentifierPrefix):
			return
		handler = self.Get(eid)
		if handler is None:
			config = MeleeConfig.GetConfig(itemName)
			if not config:
				return
			extraId = carried['extraId']
			meleeData = self.GetWeaponData(extraId)
			self.Take(eid, MeleeHandler(eid, config, extraId), meleeData)

	@EngineEvent(10)
	def EntityStartRidingEvent(self, args):
		eid = args['id']
		riderId = args['rideId']
		riderIdentifier = engineApiGas.GetEngineTypeStr(riderId)
		if riderIdentifier not in MeleeConfig.ForbidTakeMeleeRides:
			return
		posType = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
		carried = engineApiGas.GetPlayerItem(eid, posType, 0)
		if carried is None:
			return
		itemName = carried['newItemName']
		if not itemName.startswith(MeleeConfig.MeleeIdentifierPrefix):
			return
		handler = self.Get(eid)
		if handler:
			self.Remove(eid)

	
	# region 实体ai
	def OnAttackKeyDownByAI(self, args):
		"""模拟近战按钮按下"""
		eid = args['id']
		self.OnMeleeBegin({
			'playerId': eid,
			'ai': True
		})

	def OnAttackKeyUpByAI(self, args):
		"""模拟近战按钮抬起"""
		eid = args['id']
		self.OnMeleeEnd({
			'playerId': eid,
			'ai': True
		})
	
	def EntityTake(self, eid, item):
		itemName = item['newItemName']
		config = MeleeConfig.GetConfig(itemName)
		if not config:
			return
		extraId = item['extraId']
		meleeData = self.GetWeaponData(extraId)
		self.DelayTake(eid, MeleeHandler(eid, config, extraId), meleeData)
	# endregion

	def UpdateWeapon(self, melee, time, dTime):
		castMelee = melee.UpdateMelee(time, dTime)
		if castMelee:
			self.DoMeleeCast(melee, castMelee)
		attack = melee.UpdateMeleeAttack(time)
		if attack:
			self.DoMeleeAttack(melee, attack)
		# recoilFov = melee.UpdateMeleeRecoilFov(time, dTime, castMelee is not None)

	def DoMeleeCast(self, handler, castMelee):
		self.OnMeleeCast({
			'playerId': handler.Eid,
			'identifier': handler.Config['identifier'],
			'combo': handler.Combo,
			'level': handler.Level,
			'ai': True,
		})


	def DoMeleeAttack(self, handler, meleeAttack):
		pos, dir = self.GetEntityCameraPosAndDir(handler.Eid)
		self.OnMeleeAttack({
			'playerId': handler.Eid,
			'identifier': handler.Config['identifier'],
			'position': pos,
			'direction': dir,
			'combo': meleeAttack['combo'],
			'castTime': meleeAttack['castTime'],
			'meleeTime': meleeAttack['meleeTime'],
			'ai': True,
		})