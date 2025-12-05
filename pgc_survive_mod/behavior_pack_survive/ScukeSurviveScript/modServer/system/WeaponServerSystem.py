# -*- encoding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum

CompFactory = serverApi.GetEngineCompFactory()


class WeaponServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(WeaponServerSystem, self).__init__(namespace, systemName)
		self._time = 0
		self._playerWeaponMap = {}
		self._entityWeaponMap = {}
		self._offhandItemMap = {}
		self._takeTasks = []
		self._removeTasks = []
		self._S_enableModifyAttr = True
		self.__attrSystem__ = None

		self._tempUids = set()

	@property
	def _attrSystem(self):
		if not self.__attrSystem__:
			self.__attrSystem__ = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		return self.__attrSystem__


	def IsWeapon(self, identifier):
		for prefix in modConfig.WeaponIdentifierPrefixes:
			if identifier.startswith(prefix):
				return True
		return False

	@EngineEvent()
	def AddServerPlayerEvent(self, data):
		playerId = data['id']
		self._attrSystem.SetAttr(playerId, AttributeEnum.Speed, 0.1)

	def DelayTake(self, eid, weapon, data=None):
		self._takeTasks.append({
			'eid': eid,
			'handler': weapon,
			'data': data
		})

	def DelayRemove(self, eid):
		self._removeTasks.append({
			'eid': eid,
		})

	def DoDelayTakeTask(self):
		if len(self._takeTasks) > 0:
			args = self._takeTasks.pop(0)
			self.Take(args['eid'], args['handler'], args['data'])

	def DoDelayRemoveTask(self):
		if len(self._removeTasks) > 0:
			args = self._removeTasks.pop(0)
			self.Remove(args['eid'])

	def Take(self, eid, weapon, data=None):
		self._playerWeaponMap[eid] = weapon
		typeComp = CompFactory.CreateEngineType(eid)
		typeIdentifier = typeComp.GetEngineTypeStr()
		if typeIdentifier != 'minecraft:player':
			self._entityWeaponMap[eid] = weapon
		if self._S_enableModifyAttr:
			self.ModifyCarryAttr(eid, True)
		self.CheckOffhandAndDrop(eid)

	def Get(self, eid):
		if eid in self._playerWeaponMap:
			return self._playerWeaponMap[eid]
		return None

	def Remove(self, eid):
		if eid in self._playerWeaponMap:
			if self._S_enableModifyAttr:
				self.ModifyCarryAttr(eid, False)
			if eid in self._offhandItemMap:
				self.ReTakeOffhandItem(eid)
			del self._playerWeaponMap[eid]

		typeComp = CompFactory.CreateEngineType(eid)
		typeIdentifier = typeComp.GetEngineTypeStr()
		if typeIdentifier != 'minecraft:player':
			if eid in self._entityWeaponMap:
				del self._entityWeaponMap[eid]

	def GetWeaponData(self, extraId):
		return Instance.mDatasetManager.GetLevelData(extraId)

	def ResetWeaponItemData(self, playerId, exId):
		comp = CompFactory.CreateItem(playerId)
		comp.ChangePlayerItemTipsAndExtraId(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, extraId=exId)

	def SetWeaponData(self, extraId, weaponData):
		Instance.mDatasetManager.SetLevelData(extraId, weaponData)


	@EngineEvent()
	def PlayerDieEvent(self, args):
		self.DelayRemove(args['id'])

	@EngineEvent()
	def MobDieEvent(self, args):
		self.DelayRemove(args['id'])

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.AttrClientSystem)
	def OnSprintingChanged(self, data):
		playerId = data['playerId']
		sprinting = data['sprinting']
		weapon = self.Get(playerId)
		if not weapon:
			return
		weapon.SetSprinting(sprinting)

	def ModifyCarryAttr(self, eid, carryState):
		weapon = self.Get(eid)
		if not weapon:
			return
		config = weapon.Config
		carrySpeed = config['carrySpeed']
		attrSystem = self._attrSystem
		if not attrSystem:
			return
		speed = self._attrSystem.GetAttr(eid, AttributeEnum.Speed)
		if carryState:
			speed += carrySpeed
		else:
			speed -= carrySpeed
		attrSystem.SetAttr(eid, AttributeEnum.Speed, speed)

	def ModifyAllPlayersCarryAttr(self, carryState):
		for eid in self._playerWeaponMap:
			self.ModifyCarryAttr(eid, carryState)

	def GetClipItemCount(self, eid, clipIdentifier):
		itemComp = CompFactory.CreateItem(eid)
		allItems = itemComp.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
		totalCount = 0
		for slotPos, itemDict in enumerate(allItems):
			if itemDict and itemDict['itemName'] == clipIdentifier:
				item_count = itemDict['count']
				totalCount += item_count

		return totalCount

	def ReduceWeaponClipItem(self, eid, clipIdentifier, count):
		itemComp = CompFactory.CreateItem(eid)
		allItems = itemComp.GetPlayerAllItems(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
		remainingCount = count
		for slotPos, itemDict in enumerate(allItems):
			if itemDict and itemDict['itemName'] == clipIdentifier:
				item_count = itemDict['count']
				if item_count >= remainingCount:
					itemComp.SetInvItemNum(slotPos, item_count - remainingCount)
					return True
				else:
					itemComp.SetInvItemNum(slotPos, 0)
					remainingCount -= item_count

		return False

	@EngineEvent()
	def OnOffhandItemChangedServerEvent(self, args):
		playerId = args['playerId']
		current = args['newItemDict']
		if current:
			engineApiGas.AddTimer(0, self.CheckOffhandAndDrop, playerId)

	def CanUseOffhand(self, playerId):
		return True

	def OnForceDropOffhand(self, args):
		pass

	def CheckOffhandAndDrop(self, playerId, item=None):
		if not item:
			current = engineApiGas.GetEntityItem(playerId, serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, 0, True)
		else:
			current = item
		if not current:
			return
		if self.CanUseOffhand(playerId):
			return
		self.ClearOffhand(playerId)
		dic = {
			'newItemName': current['newItemName'],
			'itemName': current['itemName'],
			'count': current['count'],
			'enchantData': current['enchantData'],
			'durability': current['durability'],
			'customTips': current['customTips'],
			'extraId': current['extraId'],
			'newAuxValue': current['newAuxValue'],
			'modEnchantData': current['modEnchantData'],
			'auxValue': current['auxValue'],
		}
		if 'userData' in current:
			dic['userData'] = current['userData']
		engineApiGas.SpawnItemToPlayerInv(playerId, dic)
		self._offhandItemMap[playerId] = current
		self.OnForceDropOffhand({'playerId': playerId, 'oldItemDict': current})

	def GetItemUniqueKey(self, itemDit):
		keys = [
			'durability',
			'enchantData',
			'modEnchantData',
			'auxValue',
			'newAuxValue',
			'itemName',
			'newItemName',
			'modId',
			'modItemId',
			'customTips'
		]
		key = ''
		for keyItem in keys:
			if keyItem in itemDit:
				key += str(itemDit[keyItem])
		return key

	def ReTakeOffhandItem(self, playerId):
		offhandItem = self._offhandItemMap[playerId]
		del self._offhandItemMap[playerId]
		allItems = engineApiGas.GetPlayerAllItems(playerId, serverApi.GetMinecraftEnum().ItemPosType.INVENTORY)
		keyOffhand = self.GetItemUniqueKey(offhandItem)
		comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
		for i in range(0, len(allItems)):
			item = allItems[i]
			if item is None:
				continue
			if item['itemName'] == offhandItem['itemName']:
				keyItem = self.GetItemUniqueKey(item)
				if keyItem == keyOffhand:
					if comp.SetInvItemNum(i,0):
						comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, item, 0)
					return

	def ClearOffhand(self, playerId):
		comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
		comp.SetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.OFFHAND, None, 0)

	def GetEntityCameraPosAndDir(self, eid):
		pos = MathUtils.TupleAdd(engineApiGas.GetEntityPos(eid), (0, 1.8, 0))
		dir = serverApi.GetDirFromRot(engineApiGas.GetEntityRot(eid))
		pos = MathUtils.TupleAddMul(pos, dir, 0.5)
		return pos, dir
