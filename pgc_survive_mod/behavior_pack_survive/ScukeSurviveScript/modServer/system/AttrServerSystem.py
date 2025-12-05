# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modCommon.defines.dataset.attrServerData import AttrServerData
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj

from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum

MinecrafatEnum = serverApi.GetMinecraftEnum()
MCAttrTypeEnum = MinecrafatEnum.AttrType
MCDamageCauseTypeEnum = MinecrafatEnum.ActorDamageCause

EffectAmplifierConfig = {
	'speed': 0.2,
	'slowness': -0.15,
	'player_sprint': 0.3,
}

AutoKeepAttrs = [
	AttributeEnum.Radiation,
]

ForbidAttrWhenEntityDead = [
	AttributeEnum.Health,
	AttributeEnum.MaxHealth,
]

class AttrServerSystem(BaseServerSystem):
	def __init__(self, namespace, systemName):
		super(AttrServerSystem, self).__init__(namespace, systemName)
		self._entitySpeed = {}
		self._playerSprint = {}
		self._entityAttrs = {}
		self._players = []
		self._gameComp = serverApi.GetEngineCompFactory().CreateGame(self.mLevelId)
		AttributeEnum.Binding(AttributeEnum.Health, MCAttrTypeEnum.HEALTH)
		AttributeEnum.Binding(AttributeEnum.Speed, MCAttrTypeEnum.SPEED)
		AttributeEnum.Binding(AttributeEnum.Damage, MCAttrTypeEnum.DAMAGE)
		AttributeEnum.Binding(AttributeEnum.UnderwaterSpeed, MCAttrTypeEnum.UNDERWATER_SPEED)
		AttributeEnum.Binding(AttributeEnum.Hunger, MCAttrTypeEnum.HUNGER)
		AttributeEnum.Binding(AttributeEnum.Saturation, MCAttrTypeEnum.SATURATION)
		AttributeEnum.Binding(AttributeEnum.Absorption, MCAttrTypeEnum.ABSORPTION)
		AttributeEnum.Binding(AttributeEnum.LavaSpeed, MCAttrTypeEnum.LAVA_SPEED)
		AttributeEnum.Binding(AttributeEnum.Luck, MCAttrTypeEnum.LUCK)
		AttributeEnum.Binding(AttributeEnum.FollowRange, MCAttrTypeEnum.FOLLOW_RANGE)
		AttributeEnum.Binding(AttributeEnum.KnockbackResistance, MCAttrTypeEnum.KNOCKBACK_RESISTANCE)
		AttributeEnum.Binding(AttributeEnum.JumpStrength, MCAttrTypeEnum.JUMP_STRENGTH)
		AttributeEnum.Binding(AttributeEnum.Armor, MCAttrTypeEnum.ARMOR)

		AttributeEnum.Binding(AttributeEnum.MaxHealth, MCAttrTypeEnum.HEALTH, True)
		# 范围限制
		AttributeEnum.SetRange(AttributeEnum.Radiation, (0, 9999999))
		AttributeEnum.SetRange(AttributeEnum.ColdResistance, (0, 9999999))
		AttributeEnum.SetRange(AttributeEnum.HeatResistance, (0, 9999999))
		AttributeEnum.SetRange(AttributeEnum.RadiationResistance, (0, 9999999))
		AttributeEnum.SetRange(AttributeEnum.BodyColdResistance, (0, 9999999))
		AttributeEnum.SetRange(AttributeEnum.BodyHeatResistance, (0, 9999999))
		AttributeEnum.SetRange(AttributeEnum.BodyRadiationResistance, (0, 9999999))

		# 设置system
		self._settingSys = None

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.AttrClientSystem)
	def OnSprintingChanged(self, data):
		eid = data['playerId']
		self._playerSprint[eid] = data['sprinting']
		self._UpdatePlayerSpeedRecord(eid, True)

	@EngineEvent()
	def AddEffectServerEvent(self, args):
		eid = args['entityId']
		self._UpdatePlayerSpeedRecord(eid, True)

	@EngineEvent()
	def PlayerDieEvent(self, args):
		eid = args['id']
		self.SetAttr(eid, AttributeEnum.Radiation, 0)

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, data):
		playerId = data['playerId']
		if playerId in self._players:
			return
		self._players.append(playerId)
		self.AddDamageResistance(playerId, 10)

	@EngineEvent()
	def PlayerRespawnFinishServerEvent(self, args):
		"""玩家复活完毕事件"""
		# 出生保护：复活后获得10秒保护效果（防御buff）
		playerId = args.get('playerId')
		self.AddDamageResistance(playerId, 10)

	def AddDamageResistance(self, playerId, duration):
		if self._settingSys is None:
			self._settingSys = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.SettingServerSystem)
		if self._settingSys and self._settingSys.IsRespawnProtect():
			engineApiGas.AddEffectToEntity(playerId, MinecrafatEnum.EffectType.DAMAGE_RESISTANCE, duration, 32767, False)

	@EngineEvent()
	def RefreshEffectServerEvent(self, args):
		eid = args['entityId']
		self._UpdatePlayerSpeedRecord(eid, True)

	@EngineEvent()
	def RemoveEffectServerEvent(self, args):
		eid = args['entityId']
		self._UpdatePlayerSpeedRecord(eid, True)

	@EngineEvent()
	def AddServerPlayerEvent(self, data):
		playerId = data['id']
		self._playerSprint[playerId] = False
		self._entitySpeed[playerId] = {
			'value': self.GetAttr(playerId, AttributeEnum.Speed),
			'buffs': self._GetSpeedBuffs(playerId),
		}
		attrs = self.GetEntityAttrsData(playerId)
		self._entityAttrs[playerId] = attrs
		self.logger.debug('Player %r Attrs: %r' % (playerId, attrs))

	def GetEntityAttrsData(self, eid):
		data = Instance.mDatasetManager.GetEntityData(eid, 'attrs')
		if data is None:
			data = DatasetObj.Build(AttrServerData)
			Instance.mDatasetManager.SetEntityData(eid, 'attrs', data)
		else:
			orgData = DatasetObj.Build(AttrServerData)
			data = DatasetObj.Format(AttrServerData, data)
			for attrKey in data:
				if attrKey not in AutoKeepAttrs:
					data[attrKey] = orgData[attrKey]
		return data

	def FlushEntityAttrsData(self, eid):
		attrs = self.Get(eid)
		if not attrs:
			return False
		return Instance.mDatasetManager.SetEntityData(eid, 'attrs', attrs)

	def Update(self):
		for eid in self._entitySpeed:
			self._UpdatePlayerSpeedRecord(eid)

	def Get(self, eid):
		if eid in self._entityAttrs:
			return self._entityAttrs[eid]
		return None

	def GetAttr(self, eid, attrType, original=False):
		mcType = None
		isMax = False
		mcTypeItem = AttributeEnum.GetMCAttrType(attrType)
		if mcTypeItem:
			mcType = mcTypeItem['type']
			isMax = mcTypeItem['isMax']
		ret = None
		if mcType is not None:
			if isMax:
				ret = engineApiGas.GetAttrMaxValue(eid, mcType)
			else:
				ret = engineApiGas.GetAttrValue(eid, mcType)
		else:
			attrs = self.Get(eid)
			if not attrs or attrType not in attrs:
				return ret
			ret = attrs[attrType]
		if original:
			return ret
		# 处理Speed
		if attrType == AttributeEnum.Speed:
			if eid not in self._entitySpeed:
				return ret
			item = self._entitySpeed[eid]
			ret = item['value']
			buffs = item['buffs']
			ret = self._DoEffectsValue(ret, buffs, True)
		return ret

	def SetAttr(self, eid, attrType, value, flush=True):
		mcType = None
		isMax = False
		mcTypeItem = AttributeEnum.GetMCAttrType(attrType)
		if mcTypeItem:
			mcType = mcTypeItem['type']
			isMax = mcTypeItem['isMax']
		value = AttributeEnum.Clamp(attrType, value)
		ret = False
		if attrType in ForbidAttrWhenEntityDead:
			if engineApiGas.GetAttrValue(eid, MCAttrTypeEnum.HEALTH) <= 0:
				return ret
		if mcType is not None:
			if isMax:
				ret = engineApiGas.SetAttrMaxValue(eid, mcType, value)
			else:
				ret = engineApiGas.SetAttrValue(eid, mcType, value)
		else:
			attrs = self.Get(eid)
			if not attrs or attrType not in attrs:
				return ret, 0.0
			attrs[attrType] = value
			ret = True
			if flush:
				self.FlushEntityAttrsData(eid)
		# 处理Speed
		if attrType == AttributeEnum.Speed:
			self._playerSprint[eid] = False
			self._ReaddEffects(eid, ['speed', 'slowness'])
			buffs = self._GetMCEffects(eid, ['speed', 'slowness'])
			newSpeed = engineApiGas.GetAttrValue(eid, mcType)
			newOrgSpeed = self._DoEffectsValue(newSpeed, buffs, True)
			if abs(newOrgSpeed - value) > 0.00001:
				self._playerSprint[eid] = True
			self._UpdatePlayerSpeedRecord(eid, True)
		return ret, value

	def ModifyAttr(self, eid, attrType, modify, flush=True):
		value = self.GetAttr(eid, attrType)
		if value is None:
			return False, 0.0
		if attrType == AttributeEnum.Health and modify < 0:  # 血量减少特殊处理
			ret = engineApiGas.Hurt(eid, eid, int(-modify), MCDamageCauseTypeEnum.Contact, False)
			return ret, modify
		ret, rv = self.SetAttr(eid, attrType, value + modify, flush)
		#self.logger.debug('ModifyAttr %r %r from %r to %r [%r]' % (eid, attrType, value, rv, modify))
		return ret, rv-value

	def _UpdatePlayerSpeedRecord(self, eid, force=False):
		if eid not in self._entitySpeed:
			return
		item = self._entitySpeed[eid]
		cur = self.GetAttr(eid, AttributeEnum.Speed, True)
		speed = item['value']
		if cur != speed or force:
			item['value'] = cur
			item['buffs'] = self._GetSpeedBuffs(eid)

	def _DoEffectsValue(self, value, buffs, undo=False):
		for buff in buffs:
			effect = buff['effectName']
			level = buff['amplifier'] + 1
			levelCoef = 0.0
			if effect in EffectAmplifierConfig:
				levelCoef = EffectAmplifierConfig[effect]
			if undo:
				value /= (1.0 + levelCoef * level)
			else:
				value *= (1.0 + levelCoef * level)
		return value

	def _ReaddEffects(self, eid, filters=None):
		buffs = self._GetMCEffects(eid, filters)
		for buff in buffs:
			engineApiGas.RemoveEffectFromEntity(eid, buff['effectName'])
		for buff in buffs:
			engineApiGas.AddEffectToEntity(eid, buff['effectName'], int(round(buff['duration'])), buff['amplifier'])

	def _GetMCEffects(self, eid, filters=None):
		allBuffs = engineApiGas.GetAllEffects(eid)
		filterBuffs = []
		if not allBuffs:
			return filterBuffs
		if not filters:
			return allBuffs
		for item in allBuffs:
			effectName = item['effectName']
			if effectName in filters and item['duration_f'] > 0:
				filterBuffs.append({
					'effectName': effectName,
					'amplifier': item['amplifier'],
					'duration': item['duration_f']
				})
		return filterBuffs


	def _GetSpeedBuffs(self, eid):
		buffs = self._GetMCEffects(eid, ['speed', 'slowness'])
		if eid in self._playerSprint and self._playerSprint[eid]:
			buffs.append({
				'effectName': 'player_sprint',
				'amplifier': 0,
				'duration': -1
			})
		return buffs
