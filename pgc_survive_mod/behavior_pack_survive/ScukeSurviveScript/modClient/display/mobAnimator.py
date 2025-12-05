# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3

CompFactory = clientApi.GetEngineCompFactory()

def RegisterParam(name, defaultValue=0):
	key = 'query.mod.' + name
	comp = CompFactory.CreateQueryVariable(clientApi.GetLevelId())
	comp.Register(key, defaultValue)


RegisterParam('hurt_time')
RegisterParam('hurt_duration')
RegisterParam('hurt_direction')

class MobAnimatorController(object):
	def __init__(self, eid, identifier):
		self._eid = eid
		self._identifier = identifier
		self._queryVariableComp = CompFactory.CreateQueryVariable(eid)

		self.SetParam('hurt_duration', 3)  # 0.3

	def SetHurt(self, fromPos, level=1.0):
		cur = self._queryVariableComp.GetMolangValue('query.time_stamp')
		pos = engineApiGac.GetEntityPos(self._eid)
		dir = Vector3()
		if pos and fromPos:
			forward = Vector3(engineApiGac.GetDirFromRot(engineApiGac.GetRot(self._eid)))
			rot0 = MathUtils.LookDirection(forward)
			d = MathUtils.TupleSub(pos, fromPos)
			rot1 = MathUtils.LookDirection(Vector3(d[0], 0, d[2]))
			rot = MathUtils.InverseRot(rot0) * rot1
			dir = rot * Vector3.Forward()
		self.SetParam('hurt_direction', dir.z * 30 * level)
		self.SetParam('hurt_time', cur)

	def SetParam(self, name, value):
		self._queryVariableComp.Set('query.mod.' + name, value)
