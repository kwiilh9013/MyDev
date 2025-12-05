# -*- encoding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import gunConfig as GunConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.gunServerData import GunServerData
from ScukeSurviveScript.modCommon.handler.gunHandler import GunHandler
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modServer.system.WeaponServerSystem import WeaponServerSystem

CompFactory = serverApi.GetEngineCompFactory()

OneSecondUpdate = 30.0
UpdateTimeMs = 1000.0 / OneSecondUpdate


class GunServerSystem(WeaponServerSystem):

	def __init__(self, namespace, systemName):
		super(GunServerSystem, self).__init__(namespace, systemName)
		self._takeTasks = []
		self._meleeAttackFlag = None
		self._S_infiniteClip = False
		self._S_ignoreDurability = False

	def CreateGun(self, eid, identify, args):
		gunDataKey = Instance.mDatasetManager.BuildKey('gun')
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
		self.NotifyCurrentTakeGun(args['playerId'])

	def NotifyCurrentTakeGun(self, playerId):
		for eid, gun in self._playerWeaponMap.iteritems():
			self.NotifyToClient(playerId, 'OnTakeGun', {
				'playerId': eid,
				'identifier': gun.Config['identifier'],
				'clip': gun.Clip,
			})

	def Take(self, eid, weapon, data=None):
		config = weapon.Config
		gunClip = 0 if not data else data['clip']
		weapon.SetClip(gunClip)
		self.BroadcastToAllClient('OnTakeGun', {
			'playerId': eid,
			'identifier': config['identifier'],
			'clip': gunClip,
		})
		super(GunServerSystem, self).Take(eid, weapon, data)


	def Remove(self, eid, force=False):
		gun = self.Get(eid)
		if gun:
			config = gun.Config
			self.BroadcastToAllClient('OnRemoveGun', {
				'playerId': eid,
				'identifier': config['identifier'],
				'force': force
			})
		super(GunServerSystem, self).Remove(eid)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunShootBegin(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		if data.get('ai', False):
			gun.KeyDown(self._time)
		self.BroadcastToAllClient('OnGunShootBegin', data)


	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunShootBullet(self, data):
		# TODO Check data['clip']
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		self.BroadcastEvent('OnGunShootBullet', {
			'eid': eid,
			'config': gun.Config['shootEffect'],
			'position': data['position'],
			'direction': data['direction'],
			'chargeCoef': data['charge']['coef'],
			'chargeLevel': data['charge']['level'],
		})
		if 'clip' in data:
			gun.SetClip(data['clip'])
			gunData = self.GetWeaponData(gun.ExtraId)
			if gunData:
				gunData['clip'] = data['clip']
				self.SetWeaponData(gun.ExtraId, gunData)

		self.BroadcastToAllClient('OnGunShootBullet', data)
		self.ReduceDurability(eid)


	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunShootEnd(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		if data.get('ai', False):
			gun.KeyUp(self._time)
		self.BroadcastToAllClient('OnGunShootEnd', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunReloadBegin(self, data):
		# TODO Check data['clip']
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		clipItem = gun.Config['clipIdentifier']
		if not data.get('ai', False):  # 非AI才检查ClipItem
			if self.GetClipItemCount(eid, clipItem) <= 0:
				self.logger.warning('Reload ClipItem %s not enough, %d', clipItem, 1)
				return
		if 'clip' in data:
			gunData = self.GetWeaponData(gun.ExtraId)
			if gunData:
				gunData['clip'] = data['clip']
				self.SetWeaponData(gun.ExtraId, gunData)

		self.BroadcastToAllClient('OnGunReloadBegin', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunReloadEnd(self, data):
		# TODO Check data['clip']
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		if not data.get('ai', False):  # 非AI才检查ClipItem
			clipItem = gun.Config['clipIdentifier']
			if not self.ReduceWeaponClipItem(eid, clipItem, 1):
				self.logger.warning('Reload ClipItem %s not enough, %d', clipItem, 1)
				return
		if 'clip' in data:
			gunData = self.GetWeaponData(gun.ExtraId)
			if gunData:
				gunData['clip'] = data['clip']
				self.SetWeaponData(gun.ExtraId, gunData)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunKick(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		#TODO Check valid
		self.BroadcastToAllClient('OnGunKick', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunKickAttack(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		if 'kick' not in gun.Config or 'attack' not in gun.Config['kick']:
			return
		self._meleeAttackFlag = eid
		self.BroadcastEvent('OnGunMeleeAttack', {
			'eid': eid,
			'attack': gun.Config['kick']['attack'],
			'position': data['position'],
			'direction': data['direction'],
		})
		self._meleeAttackFlag = None

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunZoomIn(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		self.BroadcastToAllClient('OnGunZoomIn', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunZoomOut(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		self.BroadcastToAllClient('OnGunZoomOut', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunWalking(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		self.BroadcastToAllClient('OnGunWalking', data)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.GunClientSystem)
	def OnGunSprinting(self, data):
		eid = data['playerId']
		gun = self.Get(eid)
		if not gun:
			return
		self.BroadcastToAllClient('OnGunSprinting', data)

	@EngineEvent()
	def OnCarriedNewItemChangedServerEvent(self, args):
		itemName = args['newItemName']
		oldItemName = args['oldItemName']
		eid = args['playerId']
		# 装备
		if oldItemName.startswith(GunConfig.GunIdentifierPrefix):
			self.Remove(eid)
		if not itemName.startswith(GunConfig.GunIdentifierPrefix):
			return
		rider = engineApiGas.GetEntityRider(eid)
		if rider != '-1':
			riderIdentifier = engineApiGas.GetEngineTypeStr(rider)
			if riderIdentifier in GunConfig.ForbidTakeGunRides:
				return
		config = GunConfig.GetConfig(itemName)
		if not config:
			return
		item = args['newItemDict']
		extraId = item['extraId']
		gunData = self.GetWeaponData(extraId)
		if gunData is None:
			extraId = Instance.mDatasetManager.BuildKey('gun')
			self.ResetWeaponItemData(eid, extraId)
			gunData = DatasetObj.Build(GunServerData)
			gunData['identifier'] = itemName
			gunData['clip'] = config['reload']['clip']
			self.SetWeaponData(extraId, gunData)
		else:
			gunData = DatasetObj.Format(GunServerData, gunData)
		self.DelayTake(eid, GunHandler(eid, config, self.GetClipItemCount(eid, config['clipIdentifier']), extraId), gunData)


	@EngineEvent()
	def PlayerRespawnFinishServerEvent(self, args):
		eid = args['playerId']
		type = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
		item = serverApi.GetEngineCompFactory().CreateItem(eid).GetPlayerItem(type)
		if not item:
			return
		itemName = item['newItemName']
		if not itemName.startswith(GunConfig.GunIdentifierPrefix):
			return
		config = GunConfig.GetConfig(itemName)
		if not config:
			return
		extraId = item['extraId']
		gunData = self.GetWeaponData(extraId)
		self.Take(eid, GunHandler(eid, config, self.GetClipItemCount(eid, config['clipIdentifier']), extraId), gunData)


	def CanUseOffhand(self, playerId):
		gun = self.Get(playerId)
		if not gun:
			return True
		if gun.Config['gripType'] == 'oneHand':
			return True
		return False

	def OnForceDropOffhand(self, args):
		playerId = args['playerId']
		self.NotifyToClient(playerId, 'OnForceDropOffhand', {'oldItemDict':args['oldItemDict']})


	def Update(self):
		self.DoDelayTakeTask()

		dTime = UpdateTimeMs
		time = self._time + dTime
		for weapon in self._entityWeaponMap.itervalues():
			self.UpdateWeapon(weapon, time, dTime)
		self._time = time

		self.DoDelayRemoveTask()

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
		if itemName.startswith(GunConfig.GunIdentifierPrefix):
			# 锁1点耐久
			durability = max(carried['durability'] - value, 1)
			if durability > 0:
				engineApiGas.SetItemDurability(eid, posType, 0, durability)
				if durability <= 1:
					# 武器没耐久（锁1点），则修改命名
					engineApiGas.AddTimer(0.05, serverApiMgr.SetItemCustomNameSuffix, eid, itemName, '§c(已损坏)')
			# if durability == 0:
			# 	self.NotifyToClient(eid, 'OnGunBreak', {
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
		if not itemName.startswith(GunConfig.GunIdentifierPrefix):
			return
		handler = self.Get(eid)
		if handler is None:
			config = GunConfig.GetConfig(itemName)
			if not config:
				return
			extraId = carried['extraId']
			gunData = self.GetWeaponData(extraId)
			self.Take(eid, GunHandler(eid, config, self.GetClipItemCount(eid, config['clipIdentifier']), extraId),
					  gunData)


	@EngineEvent(10)
	def EntityStartRidingEvent(self, args):
		eid = args['id']
		riderId = args['rideId']
		riderIdentifier = engineApiGas.GetEngineTypeStr(riderId)
		if riderIdentifier not in GunConfig.ForbidTakeGunRides:
			return
		posType = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
		carried = engineApiGas.GetPlayerItem(eid, posType, 0)
		if carried is None:
			return
		itemName = carried['newItemName']
		if not itemName.startswith(GunConfig.GunIdentifierPrefix):
			return
		handler = self.Get(eid)
		if handler:
			self.Remove(eid, True)

	def GetClipItemCount(self, eid, clipIdentifier):
		count = super(GunServerSystem, self).GetClipItemCount(eid, clipIdentifier)
		if self._S_infiniteClip and count <= 0:
			count = 1
		return count

	def ReduceWeaponClipItem(self, eid, clipIdentifier, count):
		if self._S_infiniteClip:
			return True
		return super(GunServerSystem, self).ReduceWeaponClipItem(eid, clipIdentifier, count)

	def EntityTake(self, eid, item, validClip = 1):
		itemName = item['newItemName']
		config = GunConfig.GetConfig(itemName)
		if not config:
			return
		extraId = item['extraId']
		gunData = self.GetWeaponData(extraId)
		if gunData is None:
			extraId = Instance.mDatasetManager.BuildKey('gun')
			self.ResetWeaponItemData(eid, extraId)
			gunData = DatasetObj.Build(GunServerData)
			gunData['identifier'] = itemName
			gunData['clip'] = config['reload']['clip']
			self.SetWeaponData(extraId, gunData)
		else:
			gunData = DatasetObj.Format(GunServerData, gunData)
		self.DelayTake(eid, GunHandler(eid, config, validClip, extraId), gunData)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
	def OnMeleeAttackTargets(self, args):
		fromId = args['fromId']
		if fromId == self._meleeAttackFlag:
			for target in args['targets']:
				if target['type'] == 'Block':
					continue
				self.ReduceDurability(fromId, 10)
				return

	# region 实体ai
	def OnShootKeyDownByAI(self, args):
		"""模拟射击按钮按下"""
		eid = args['id']
		self.OnGunShootBegin({
			'playerId': eid,
			'ai': True
		})

	def OnShootKeyUpByAI(self, args):
		"""模拟射击按钮松开"""
		eid = args['id']
		self.OnGunShootEnd({
			'playerId': eid,
			'ai': True
		})

	def OnReloadKeyDonwByAI(self, args):
		"""模拟换弹按钮按下"""
		eid = args['id']
		handler = self.Get(eid)
		self.Reload(handler)

	def OnMeleeKeyDownByAI(self, args):
		"""模拟枪械近战按钮按下"""
		eid = args['id']
		handler = self.Get(eid)
		self.Kick(handler)
	# endregion


	def UpdateWeapon(self, gun, time, dTime):
		needReload, reloadCompleted = gun.UpdateGunReload(time, dTime)
		kickAttack, kickCompleted = gun.UpdateGunKick(time, dTime)
		if kickAttack:
			self.DoKickAttack(gun)
		gun.UpdateGunShoot(time)
		bullet = gun.UpdateGunShootBullet(time)
		shootBullet = bullet is not None
		if shootBullet:
			self.DoShootBullet(gun, bullet)
		# recoil = gun.UpdateGunRecoil(time, dTime, shootBullet)
		# scatter = gun.UpdateGunScatter(time, dTime, shootBullet)
		# zoom = gun.UpdateGunZoom(time, dTime)
		if needReload:
			self.Reload(gun, True)
		if reloadCompleted:
			self.ReloadEnd(gun)

	def Reload(self, handler, auto=False):
		if not handler:
			return
		if not handler.Reload(self._time):
			return
		self.OnGunReloadBegin({
			'playerId': handler.Eid,
			'clip': handler.Clip,
			'ai': True
		})

	def ReloadEnd(self, handler):
		self.OnGunReloadEnd({
			'playerId': handler.Eid,
			'clip': handler.Clip,
			'ai': True
		})

	def Kick(self, handler):
		if not handler:
			return
		if not handler.Kick(self._time):
			return
		self.OnGunKick({
			'playerId': handler.Eid,
			'ai': True
		})


	def DoKickAttack(self, handler):
		pos, dir = self.GetEntityCameraPosAndDir(handler.Eid)
		self.OnGunKickAttack({
			'playerId': handler.Eid,
			'position': pos,
			'direction': dir,
			'ai': True
		})

	def DoShootBullet(self, handler, bullet):
		pos, dir = self.GetEntityCameraPosAndDir(handler.Eid)
		self.OnGunShootBullet({
			'playerId': handler.Eid,
			'identifier': handler.Config['identifier'],
			'position': pos,
			'direction': dir,
			'clip': handler.Clip,
			'charge': handler.ChargeInfo,
			'ai': True
		})
