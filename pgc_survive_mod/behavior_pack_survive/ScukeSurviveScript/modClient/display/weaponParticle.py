# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, MathUtils
from ScukeSurviveScript.ScukeCore.utils.quaternion import Quaternion

TrailNodeAndRot = {
	'first': {
		'node': 'rightItem',
		'rot': (-90, 0, 0),
		'pos': (0, 0, 0)
	},
	'first_zoom': {
		'node': 'rightItem',
		'rot': (-90, 0, 0),
		'pos': (0, 0, 0)
	},
	'third': {
		'node': 'rightItem',
		'rot': (-90, 0, 0),
		'pos': (0, 0, 0)
	}
}

class WeaponParticleController(object):
	def __init__(self, eid, particleConfig):
		self._eid = eid
		self._config = particleConfig
		self._particleSystem = clientApi.GetEngineCompFactory().CreateParticleSystem(None)
		self._cameraComp = clientApi.GetEngineCompFactory().CreateCamera(eid)
		self._trailTimer = {}
		comp = clientApi.GetEngineCompFactory().CreateActorRender(eid)
		for k, v in particleConfig.iteritems():
			if not k.startswith('__'):
				comp.AddPlayerParticleEffect(k, v)
		self.Emit(eid, '__active__')

	def Emit(self, eid, fxKeyName, position=None, direction=None, index=-1):
		if fxKeyName not in self._config:
			return
		comp = self._particleSystem
		fxConfig = self._config[fxKeyName]
		if type(fxConfig) is list:
			if -1 < index < len(fxConfig):
				fxConfig = fxConfig[index]
			else:
				return
		if isinstance(fxConfig, str):
			fxName = fxConfig
		else:
			fxName = fxConfig['name']
		parId = comp.Create(fxName)
		if 'bone' in fxConfig:
			comp.BindEntity(parId, eid, fxConfig['bone'])
		else:
			comp.SetPos(parId, position)
			#rot = clientApi.GetRotFromDir(direction)
			#comp.SetRotUseZXY(parId, (rot[0], rot[1], 0))  # ignore Z

	def EmitTrail(self, fxKeyName, trailType, hitPosition, index=-1):
		if fxKeyName not in self._config:
			return
		comp = self._particleSystem
		config = self._config[fxKeyName]
		if trailType not in config:
			return

		fxConfig = config[trailType]
		fxName = fxConfig['name']
		if type(fxName) is list:
			if -1 < index < len(fxName):
				fxName = fxName[index]
			else:
				return
		fxOffset = fxConfig['offset']
		node = TrailNodeAndRot[trailType]['node']
		rot = TrailNodeAndRot[trailType]['rot']
		pos = TrailNodeAndRot[trailType]['pos']
		parId = comp.Create(fxName)
		if comp.BindEntity(parId, self._eid, node, pos, rot):
			comp.Hide(parId)
			comp.SetTimeScale(parId, 0)
			engineApiGac.AddTimer(0, self._Unbind, parId, fxName, hitPosition, fxOffset)

	def _Unbind(self, parId, fxName, hitPosition, offset):
		comp = self._particleSystem
		comp.Unbind(parId)
		comp.Show(parId)
		fromPos = Vector3(comp.GetPos(parId, False))
		hitPos = Vector3(hitPosition)
		particleRot = comp.GetRot(parId, False)
		particleRotQ = Quaternion.Euler(particleRot[0], particleRot[1], particleRot[2])
		up = Vector3(Quaternion.RotateVector(particleRotQ, (0, 1, 0)))
		right = Vector3(Quaternion.RotateVector(particleRotQ, (1, 0, 0)))
		forward = Vector3(Quaternion.RotateVector(particleRotQ, (0, 0, 1)))
		fromPos = fromPos + right * offset[0] + up * offset[1] + forward * offset[2]
		# 重新计算
		deltaPos = hitPos - fromPos
		dis = deltaPos.Length()
		direction = deltaPos / dis
		rot = Quaternion.LookDirection(direction.ToTuple(), up.ToTuple())
		comp.SetRot(parId, Quaternion.ToEuler(rot))
		if dis < 0:
			self._DestroyTrail(parId)
			return
		speed = min(dis / 0.1, 100)
		time = (dis - 1) / speed
		scale = speed / 100.0
		comp.SetTimeScale(parId, scale)
		if time < 0.05:
			time = 0
		self._trailTimer[parId] = {
			'fx': fxName,
			'timer': engineApiGac.AddTimer(time, self._DestroyTrail, parId)
		}

	def _DestroyTrail(self, parId):
		self._particleSystem.Remove(parId)
		if parId in self._trailTimer:
			del self._trailTimer[parId]
