# -*- coding: utf-8 -*-
import time

import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum
from ScukeSurviveScript.modCommon.cfg.livingConfig import Config as LivingConfig
CompFactory = serverApi.GetEngineCompFactory()

class LivingServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(LivingServerSystem, self).__init__(namespace, systemName)
		self.__attrSystem__ = None
		self.__envSystem__ = None
		self.__buffSystem__ = None
		self._playerLivingState = {}

	@property
	def _attrSystem(self):
		if not self.__attrSystem__:
			self.__attrSystem__ = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.AttrServerSystem)
		return self.__attrSystem__

	@property
	def _buffSystem(self):
		if not self.__buffSystem__:
			self.__buffSystem__ = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuffServerSystem)
		return self.__buffSystem__

	@property
	def _envSystem(self):
		if not self.__envSystem__:
			self.__envSystem__ = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.EnvServerSystem)
		return self.__envSystem__

	@AddonEvent(modConfig.ModName, modConfig.ClientSystemEnum.ClientSystem)
	def OnUiInitFinishedEvent(self, data):
		playerId = data['playerId']
		self.UpdateEntityLivingState(playerId, True)

	@EngineEvent()
	def PlayerRespawnFinishServerEvent(self, args):
		playerId = args['playerId']
		self.UpdateEntityLivingState(playerId, True)

	@EngineEvent()
	def PlayerDieEvent(self, args):
		eid = args['id']
		if eid in self._playerLivingState:
			del self._playerLivingState[eid]

	def GetEnvInfo(self, eid):
		return self._envSystem.GetEntityEnvInfo(eid)

	def Update(self):
		for eid in self._playerLivingState:
			self.UpdateEntityLivingState(eid)

	def UpdateEntityLivingState(self, eid, forceNotify=False):
		curTime = time.time()
		ret = {
			'__radiationUpdated__': 0,
			AttributeEnum.Temperature: 0,
			AttributeEnum.Radiation: self._attrSystem.GetAttr(eid, AttributeEnum.Radiation),
			AttributeEnum.HeatResistance: 0,
			AttributeEnum.ColdResistance: 0,
			AttributeEnum.RadiationResistance: 0,
		}
		if eid not in self._playerLivingState:
			self._playerLivingState[eid] = ret
			return  # Wait for next

		envInfo = self.GetEnvInfo(eid)
		if not envInfo:
			return
		inShelter = envInfo['shelter'] > 0
		changed = False
		prev = self._playerLivingState[eid]
		# 辐射计算
		bodyRadiationResistance = self._attrSystem.GetAttr(eid, AttributeEnum.BodyRadiationResistance)
		radiationAbsorption = self._attrSystem.GetAttr(eid, AttributeEnum.RadiationAbsorption)
		ret[AttributeEnum.RadiationResistance] += envInfo['radiationResistance']
		lastTime = prev['__radiationUpdated__']
		if curTime - lastTime >= LivingConfig['radiationInterval']:
			changed = True
			ret['__radiationUpdated__'] = curTime
			radiation = 0
			if not inShelter:
				radiation += envInfo['radiation']
			realRadiation = max(0, radiation - (ret[AttributeEnum.RadiationResistance] + bodyRadiationResistance))
			ret[AttributeEnum.Radiation] += realRadiation
			# 避免数值一直增长
			fakeMaxRadiation = radiationAbsorption
			if ret[AttributeEnum.Radiation] > fakeMaxRadiation:
				ret[AttributeEnum.Radiation] = fakeMaxRadiation + 1
		else:
			ret['__radiationUpdated__'] = lastTime
		# 温度计算
		comp = CompFactory.CreateAttr(eid)
		isOnFire = comp.IsEntityOnFire()
		bodyTemp = self._attrSystem.GetAttr(eid, AttributeEnum.BodyTemp)
		ret[AttributeEnum.Temperature] = bodyTemp
		bodyHeatResistance = self._attrSystem.GetAttr(eid, AttributeEnum.BodyHeatResistance)
		bodyColdResistance = self._attrSystem.GetAttr(eid, AttributeEnum.BodyColdResistance)
		if not inShelter:
			ret[AttributeEnum.Temperature] += envInfo['temperature']
		ret[AttributeEnum.HeatResistance] += envInfo['heatResistance']
		ret[AttributeEnum.ColdResistance] += envInfo['coldResistance']
		if isOnFire and ret[AttributeEnum.Temperature] < 0:
			ret[AttributeEnum.Temperature] = 0
		temp = ret[AttributeEnum.Temperature]
		heatResistanceTemp = LivingConfig['heatResistanceToTemp'] * (ret[AttributeEnum.HeatResistance] + bodyHeatResistance)
		coldResistanceTemp = LivingConfig['coldResistanceToTemp'] * (ret[AttributeEnum.ColdResistance] + bodyColdResistance)
		ret['__feeling_temp__'] = temp
		tempInfo = {
			'temp': temp,
			'heatResistanceTemp': heatResistanceTemp,
			'coldResistanceTemp': coldResistanceTemp,
			'radiation': ret[AttributeEnum.Radiation],
			'radiationAbsorption': radiationAbsorption,
		}
		if temp > LivingConfig['bodyTempMax']:
			temp += heatResistanceTemp
			temp = max(temp, LivingConfig['bodyTempMin'])
		if temp < LivingConfig['bodyTempMin']:
			temp += coldResistanceTemp
			temp = min(temp, LivingConfig['bodyTempMax'])
		ret[AttributeEnum.Temperature] = temp
		for key in ret:
			if not key.startswith('_') and ret[key] != prev[key]:
				changed = True
				break
		self._playerLivingState[eid] = ret
		if changed:
			self.ApplyLivingStateAttr(eid)
			self.LivingChecking(eid)
		if changed or forceNotify:
			self.NotifyLivingStateAttr(eid, tempInfo)

	def Get(self, eid):
		if eid not in self._playerLivingState:
			return None
		return self._playerLivingState[eid]

	def LivingChecking(self, eid):
		prevBuffs = self._buffSystem.GetAllBuffs(eid)
		checking = LivingConfig['livingChecking']
		buffMap = {}
		livingBuffs = {}
		removed = []
		added = []
		for checkItem in checking:
			attrType = checkItem['type']
			compareValue = checkItem['value']
			op = checkItem['op']
			attrValue = self._attrSystem.GetAttr(eid, attrType)
			if isinstance(compareValue, str):
				compareValue = self._attrSystem.GetAttr(eid, compareValue)
			passed = False
			if op == '<' and attrValue < compareValue:
				passed = True
			if op == '<=' and attrValue <= compareValue:
				passed = True
			if op == '>' and attrValue > compareValue:
				passed = True
			if op == '>=' and attrValue >= compareValue:
				passed = True
			for buff in checkItem['buffs']:
				livingBuffs[buff] = True
				if passed:
					if buff not in buffMap:
						buffMap[buff] = True
						if buff not in prevBuffs:
							added.append(buff)
		for buffState in prevBuffs:
			existBuff = buffState['type']
			if existBuff in livingBuffs and existBuff not in buffMap:
				removed.append(existBuff)
		if len(removed) > 0 or len(added) > 0:
			effectComp = CompFactory.CreateEffect(eid)
			for removeBuff in removed:
				effectComp.RemoveEffectFromEntity(removeBuff)
			for addBuff in added:
				effectComp.AddEffectToEntity(addBuff, 99999, 0, True)



	def ApplyLivingStateAttr(self, eid):
		livingState = self.Get(eid)
		if not livingState:
			return False
		# Set attrs
		for key, value in livingState.iteritems():
			if key.startswith('_'):
				continue
			self._attrSystem.SetAttr(eid, key, value, False)
		self._attrSystem.FlushEntityAttrsData(eid)

	def NotifyLivingStateAttr(self, eid, tempInfo):
		livingState = self.Get(eid)
		if not livingState:
			return
		notify = {
			AttributeEnum.BodyTemp: 0,
			AttributeEnum.BodyHeatResistance: 0,
			AttributeEnum.BodyColdResistance: 0,
			AttributeEnum.BodyRadiationResistance: 0,
			AttributeEnum.Temperature: 0,
			AttributeEnum.Radiation: 0,
			AttributeEnum.HeatResistance: 0,
			AttributeEnum.ColdResistance: 0,
			AttributeEnum.RadiationResistance: 0,
			AttributeEnum.RadiationAbsorption: 0,
		}
		for attrType in notify:
			notify[attrType] = self._attrSystem.GetAttr(eid, attrType)
		notify['tempInfo'] = tempInfo
		self.NotifyToClient(eid, 'OnApplyLivingStateAttr', notify)
