# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent

from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.dataset.buffServerData import BuffServerData
from ScukeSurviveScript.modServer.buff.buff import BuffBuilder
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig

from ScukeSurviveScript.modCommon.cfg.buffConfig import Config as BuffConfig
from ScukeSurviveScript.modCommon.defines.buffEnum import BuffEnum
from ScukeSurviveScript.modServer.buff.energyShieldBuff import EnergyShieldBuff
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()

OneSecondUpdate = 30.0
UpdateTimeMs = 1000.0 / OneSecondUpdate

# 注册buff的处理类
BuffBuilder.BindingBuff(BuffEnum.EnergyShield, EnergyShieldBuff)
BuffBuilder.BindingBuff(BuffEnum.EnergyShieldV2, EnergyShieldBuff)
BuffBuilder.BindingBuff(BuffEnum.EnergyShieldV3, EnergyShieldBuff)


class BuffServerSystem(BaseServerSystem):
	"""
	buff系统，仅负责buff的功能逻辑
	添加buff、移除buff请用API来实现
	"""

	def __init__(self, namespace, systemName):
		super(BuffServerSystem, self).__init__(namespace, systemName)
		self._entityBuffs = {}
		self._entityBuffsObj = []
		self._entityBuffsObjMap = {}
		self._delayTask = []
		self.__attrSystem__ = None
		self._gameComp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())

	@property
	def _attrSystem(self):
		if not self.__attrSystem__:
			self.__attrSystem__ = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		return self.__attrSystem__

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, data):
		playerId = data['playerId']
		self.RegisterEntityBuffState(playerId)

	def RegisterEntityBuffState(self, eid):
		if eid in self._entityBuffsObjMap:
			return
		buffs = self.GetEntityBuffsData(eid)
		self._entityBuffs[eid] = DatasetObj.Build(BuffServerData)
		self._entityBuffsObjMap[eid] = {}
		effectComp = compFactory.CreateEffect(eid)
		addedEffects = effectComp.GetAllEffects()
		if addedEffects and len(addedEffects) > 0:  # 确保效果关联
			for effect in addedEffects:
				effectName = effect['effectName']
				duration = effect['duration']
				amplifier = effect['amplifier']
				if (not self.HasBuff(eid, effectName)) and effectName in BuffConfig:
					self.AddBuff(eid, BuffConfig[effectName], True, duration, amplifier)
		for buffState in buffs:
			left_duration = int(max(0, buffState['duration'] - (buffState['_passedTime'] / 1000.0)))
			effectComp.AddEffectToEntity(buffState['type'], left_duration, int(buffState['amplifier']), True)

		self.logger.debug('Player/Entity %r Buffs: %r' % (eid, buffs))

	@EngineEvent(10)
	def PlayerDieEvent(self, args):
		eid = args['id']
		allBuffs = self.GetAllBuffs(eid)
		for buff in allBuffs:
			engineApiGas.RemoveEffectFromEntity(eid, buff['type'])
		self.FlushEntityBuffsData(eid)

	@EngineEvent()
	def AddEffectServerEvent(self, args):
		self._DoMCEffectUpdate(args)

	@EngineEvent()
	def RefreshEffectServerEvent(self, args):
		self._DoMCEffectUpdate(args, True)

	@EngineEvent()
	def RemoveEffectServerEvent(self, args):
		entityId = args['entityId']
		effectName = args['effectName']
		self.RemoveBuff(entityId, effectName)

	def _DoMCEffectUpdate(self, args, refresh=False):
		# 处理食物
		eid = args['entityId']
		effectName = args['effectName']
		if (not self.HasBuff(eid, effectName) or refresh) and effectName in BuffConfig:
			engineApiGas.AddTimer(0, self.AddBuff, eid, BuffConfig[effectName], True, args['effectDuration'], args['effectAmplifier'])
			# self.AddBuff(eid, BuffConfig[effectName], True, args['effectDuration'], args['effectAmplifier'])

	def GetEntityBuffsData(self, eid):
		data = Instance.mDatasetManager.GetEntityData(eid, 'buffs')
		if data is None:
			# 无记录则初始化
			data = DatasetObj.Build(BuffServerData)
			Instance.mDatasetManager.SetEntityData(eid, 'buffs', data)
		else:
			data = DatasetObj.Format(BuffServerData, data)
		return data

	def FlushEntityBuffsData(self, eid):
		buffs = self._Get(eid)
		if buffs is None:
			return False
		return Instance.mDatasetManager.SetEntityData(eid, 'buffs', buffs)

	def FlushEntityBuffsState(self, eids):
		for eid in eids:
			self._entityBuffs[eid] = DatasetObj.Build(BuffServerData)
		for buff in self._entityBuffsObj:
			if buff.Eid in eids:
				self._entityBuffs[buff.Eid].append(buff.State)

	def _Get(self, eid):
		if eid in self._entityBuffs:
			return self._entityBuffs[eid]
		return None

	def GetAllBuffs(self, eid):
		ret = []
		for buff in self._entityBuffsObj:
			if buff.Eid == eid:
				ret.append(buff.State)
		return ret

	def HasBuff(self, eid, buffType):
		if eid not in self._entityBuffsObjMap:
			return False
		return buffType in self._entityBuffsObjMap[eid]

	def RemoveBuff(self, eid, buffType, flush=True):
		if eid not in self._entityBuffsObjMap:
			return False
		if buffType not in self._entityBuffsObjMap[eid]:
			return False
		buff = self._entityBuffsObjMap[eid][buffType]
		self._entityBuffsObj.remove(buff)
		if buff.NeedUndo:
			self._attrSystem.ModifyAttr(buff.Eid, buff.Attr, -buff.Modified)
		del self._entityBuffsObjMap[eid][buffType]
		self.OnBuffRemoved(buff, False)
		i = 0
		buffsState = self._entityBuffs[eid]
		while i < len(buffsState):
			buffState = buffsState[i]
			if buffState['type'] == buffType:
				buffsState.pop(i)
				break
			i += 1
		if flush:
			self.FlushEntityBuffsData(eid)
		return True

	def _GetBuffObj(self, eid, buffType):
		if eid not in self._entityBuffsObjMap:
			return None
		if buffType not in self._entityBuffsObjMap[eid]:
			return None
		return self._entityBuffsObjMap[eid][buffType]

	def GetBuff(self, eid, buffType):
		obj = self._GetBuffObj(eid, buffType)
		if obj:
			return obj.State
		return None

	def AddBuffByStr(self, eid, buffStr, flush=True, duration=-1):
		if buffStr not in BuffConfig:
			return False
		buffInfo = BuffConfig[buffStr]
		return self.AddBuff(eid, buffInfo, flush, duration)

	def AddBuff(self, eid, buffInfo, flush=True, duration=-1, amplifier=0, checkAlive=True):
		if eid not in self._entityBuffs:
			return False
		# 移除互斥buff
		effectComp = compFactory.CreateEffect(eid)
		if buffInfo.get('mutex_buff'):
			for effName in buffInfo['mutex_buff']:
				effectComp.RemoveEffectFromEntity(effName)
		if not effectComp.HasEffect(buffInfo['type']):
			self.logger.error('Must use EffectComponent to add buff! %r' % buffInfo['type'])
		buffObj = self._GetBuffObj(eid, buffInfo['type'])
		if buffObj:
			# 更新时间、等级
			buffObj.Refresh(duration, amplifier)
		else:
			buff = BuffBuilder.GetBuff(eid, buffInfo, duration=duration, amplifier=amplifier, attrSystem=self._attrSystem, eventHanlder=self)
			self._entityBuffsObjMap[eid][buff.Type] = buff
			self._entityBuffsObj.append(buff)
			self._entityBuffs[eid].append(buff.State)
			self.OnBuffAdded(buff)
		if flush:
			self.FlushEntityBuffsData(eid)
		return True

	def DelayAddBuff(self, eid, buffInfo, flush=True, duration=-1):
		self._delayTask.append({
			'eid': eid,
			'buffInfo': buffInfo,
			'flush': flush,
			'duration': duration
		})


	def Update(self):
		i = 0
		while i < len(self._delayTask):
			task = self._delayTask[i]
			if self._gameComp.IsEntityAlive(task['eid']):
				self.AddBuff(task['eid'], task['buffInfo'], task['flush'], task['duration'], False)
				self._delayTask.pop(i)
			else:
				i+=1
		i = 0
		flushBuffsEid = {}
		while i < len(self._entityBuffsObj):
			buff = self._entityBuffsObj[i]
			ended, apply = buff.Tick(UpdateTimeMs)
			if ended or apply:
				flushBuffsEid[buff.Eid] = True
			if apply:
				deltaValue = buff.ClampAttrValue()
				if deltaValue != 0:
					ret, rv = self._attrSystem.ModifyAttr(buff.Eid, buff.Attr, deltaValue)
					if ret:
						buff.Apply(rv)
			if ended:
				if buff.NeedUndo:
					self._attrSystem.ModifyAttr(buff.Eid, buff.Attr, -buff.Modified)
				self._entityBuffsObj.pop(i)
				del self._entityBuffsObjMap[buff.Eid][buff.Type]
				self.OnBuffRemoved(buff, True)
				# 主动移除对应的原生buff
				engineApiGas.RemoveEffectFromEntity(buff.Eid, buff.Type)
			else:
				i += 1

		eids = flushBuffsEid.keys()
		if len(eids) > 0:
			self.FlushEntityBuffsState(eids)
			for eid in eids:
				self.FlushEntityBuffsData(eid)

	def OnBuffAdded(self, buff):
		buff.OnAdded()
		state = buff.State
		#self.logger.debug('AddBuff %r %r' % (buff.Eid, state))
		self.BroadcastToAllClient('OnBuffAdded', state)

	def OnBuffRemoved(self, buff, ended):
		buff.OnRemoved()
		state = buff.State
		#if ended:
		#	self.logger.debug('EndedBuff %r %r' % (buff.Eid, state))
		#else:
		#	self.logger.debug('RemoveBuff %r %r' % (buff.Eid, state))
		self.BroadcastToAllClient('OnBuffRemoved', state)
