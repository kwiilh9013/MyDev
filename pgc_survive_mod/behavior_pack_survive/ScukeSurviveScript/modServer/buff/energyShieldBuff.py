# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3
from ScukeSurviveScript.modServer.buff.buff import Buff

filters = {
	"all_of": [
		{"test": "is_family", "subject": "other", "operator": "equals", "value": "mob"},
		{"test": "is_family", "subject": "other", "operator": "not", "value": "npc"},
	]
}

CompFactory = serverApi.GetEngineCompFactory()

HurtEnum = serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack
EngineNamespace = serverApi.GetEngineNamespace()
EngineSystem = serverApi.GetEngineSystemName()

class EnergyShieldBuff(Buff):
	def __init__(self, eid, state, duration=-1, amplifier=0, attrSystem=None, eventHanlder=None):
		super(EnergyShieldBuff, self).__init__(eid, state, duration, amplifier, attrSystem, eventHanlder)
		self._radius = int(state.get('radius', 4))
		self._power = state.get('power', 1.0)
		self._totalEnergy = state.get('energy', 99999.0)
		self._energyReduce = state.get('energy_reduce', 1.0)
		self._energyUsed = state.get('_energy_used', 0.0)
		self._gameComp = CompFactory.CreateGame(eid)
		self._posComp = CompFactory.CreatePos(eid)
		self._hurtComp = CompFactory.CreateHurt(eid)
		self._dimComp = CompFactory.CreateDimension(eid)
		self._fbxEntity = None
		self._fbxPosComp = None
		self._fbxCreateTimer = engineApiGas.AddRepeatTimer(0.1, self.TryCreateFbxEntity)
		self._fbxPosSyncTimer = engineApiGas.AddRepeatTimer(0.05, self.OnUpdateFbxEntityPos)
		self.TryCreateFbxEntity()

	def TryCreateFbxEntity(self):
		if self._fbxEntity is None:
			self._fbxEntity = self._eventHandler.CreateEngineEntityByTypeStr('scuke_survive:fbx_entity', self._posComp.GetFootPos(), (0, 0), self._dimComp.GetEntityDimensionId())
		if self._fbxEntity is not None:
			actionComp = CompFactory.CreateAction(self._fbxEntity)
			actionComp.SetAttackTarget(self._eid)
			self._fbxPosComp = CompFactory.CreatePos(self._fbxEntity)
			engineApiGas.CancelTimer(self._fbxCreateTimer)
			self._fbxCreateTimer = None

	def OnAdded(self):
		super(EnergyShieldBuff, self).OnAdded()
		engineApiGas.AddTimer(0.1, self.NotifySheildInfo)
		self._eventHandler.ListenForEvent(EngineNamespace, EngineSystem, 'HealthChangeBeforeServerEvent', self,
										  self.HealthChangeBeforeServerEvent, priority=10)
		self._eventHandler.ListenForEvent(EngineNamespace, EngineSystem, 'DamageEvent', self,
										  self.DamageEvent, priority=10)

	def OnRemoved(self):
		super(EnergyShieldBuff, self).OnRemoved()
		self._eventHandler.DestroyEntity(self._fbxEntity)
		if self._fbxPosSyncTimer:
			engineApiGas.CancelTimer(self._fbxPosSyncTimer)
			self._fbxPosSyncTimer = None
		if self._fbxCreateTimer:
			engineApiGas.CancelTimer(self._fbxCreateTimer)
			self._fbxCreateTimer = None

		self._eventHandler.UnListenForEvent(EngineNamespace, EngineSystem, 'HealthChangeBeforeServerEvent', self,
										  self.HealthChangeBeforeServerEvent, priority=10)
		self._eventHandler.UnListenForEvent(EngineNamespace, EngineSystem, 'DamageEvent', self,
										  self.DamageEvent, priority=10)

	def OnUpdateFbxEntityPos(self):
		if self._fbxPosComp is None:
			return
		self._fbxPosComp.SetFootPos(self._posComp.GetFootPos())


	def Tick(self, tickTime):
		buffEnd, active = super(EnergyShieldBuff, self).Tick(tickTime)
		if active:
			last = self._energyUsed
			eid = self._eid
			# 检测范围怪物，施加击飞，扣除能量
			mobs = self._gameComp.GetEntitiesAround(eid, self._radius, filters)
			if mobs and len(mobs) > 0:
				knock = self._power
				curPos = self._posComp.GetPos()
				for entityId in mobs:
					collisionComp = CompFactory.CreateCollisionBox(entityId)
					cSize = collisionComp.GetSize()
					rSize = MathUtils.Clamp(MathUtils.TupleLength(cSize) / 2.0, 1.0, 10.0)
					k = MathUtils.Clamp(rSize * rSize, 0.5, 10.0)  # 系数调整
					motionComp = CompFactory.CreateActorMotion(entityId)
					pos = CompFactory.CreatePos(entityId).GetPos()
					if pos is not None:
						delta = MathUtils.TupleSub(pos, curPos)
						dir = Vector3((delta[0], 0, delta[2])).Normalized()+Vector3.Up()*0.2
						dir.Normalize()
						motion = (dir * knock).ToTuple()
						if motionComp.SetMotion(motion):
							self._energyUsed += self._energyReduce * k  # 使用能量和体型有关，越大消耗越多
			if self._energyUsed != last:
				self.NotifySheildInfo()
		if self._totalEnergy - self._energyUsed <= 0:
			buffEnd = True
		return buffEnd, active


	@property
	def State(self):
		ret = super(EnergyShieldBuff, self).State
		ret['_energy_used'] = self._energyUsed
		return ret

	def NotifySheildInfo(self):
		if self._eventHandler:
			data = {
				'eid': self._eid,
				'total': self._totalEnergy,
				'used': self._energyUsed,
				'fbxEid': self._fbxEntity,
			}
			self._eventHandler.BroadcastToAllClient('OnEnergySheildInfo', data)

	def DamageEvent(self, args):
		entityId = args['entityId']
		damage = args['damage']
		if entityId == self._fbxEntity:
			args['damage'] = 0
			return
		if entityId != self._eid:
			return
		if damage > 0 and self._energyUsed < self._totalEnergy:
			args['damage'] = 0
			self._energyUsed += damage

			self.NotifySheildInfo()

	def HealthChangeBeforeServerEvent(self, args):
		entityId = args['entityId']
		if entityId == self._fbxEntity:
			args['cancel'] = True
			return
		if entityId != self._eid:
			return
		damage = args['from'] - args['to']
		if damage > 0 and self._energyUsed < self._totalEnergy:
			args['cancel'] = True
			self._energyUsed += damage
			self.NotifySheildInfo()
