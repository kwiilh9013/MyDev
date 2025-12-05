# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.display.weaponAnimator import WeaponAnimatorController, RegisterParam

CompFactory = clientApi.GetEngineCompFactory()


# 注册状态参数
RegisterParam('scuke_survive_melee_taking')
RegisterParam('scuke_survive_melee_begin')
RegisterParam('scuke_survive_melee_attack')
RegisterParam('scuke_survive_melee_end')
RegisterParam('scuke_survive_melee_break')
RegisterParam('scuke_survive_melee_using')
RegisterParam('scuke_survive_melee_combo')
RegisterParam('scuke_survive_melee_level')

# 可互斥状态参数
ConflictParams = [
	'scuke_survive_melee_taking',
	'scuke_survive_melee_begin',
	'scuke_survive_melee_attack',
	'scuke_survive_melee_end',
	'scuke_survive_melee_break',
]

class MeleeAnimatorController(WeaponAnimatorController):
	def __init__(self, eid, identifier, animatorConfig):
		super(MeleeAnimatorController, self).__init__(eid, identifier, animatorConfig, {
			'scuke_survive_melee_taking': 0,
			'scuke_survive_melee_begin': 0,
			'scuke_survive_melee_attack': 0,
			'scuke_survive_melee_end': 0,
			'scuke_survive_melee_break': 0,
			'scuke_survive_melee_using': 0,
			'scuke_survive_melee_combo': 0,
		}, ConflictParams)

		self._changeToIdleTimer = None

	def MeleeTaking(self, takingTime):
		self.SetParam('scuke_survive_melee_taking', 1)
		self.DelayChangeToIdle(takingTime)

	def MeleeBegin(self):
		self.SetParam('scuke_survive_melee_using', 1)
		self.SetParamOnlyOne('scuke_survive_melee_begin', 1)

	def MeleeCast(self, combo, level=0):
		self.SetParamOnlyOne('scuke_survive_melee_attack', combo)
		self.SetParam('scuke_survive_melee_level', level)
		self.DelayChangeToIdle(0.01)

	def MeleeEnd(self):
		self.SetParamOnlyOne('scuke_survive_melee_end', 1)
		self.DelayChangeToIdle(0.01)
		self.SetParam('scuke_survive_melee_using', 0)


	def DelayChangeToIdle(self, delay):
		if self._changeToIdleTimer:
			engineApiGac.CancelTimer(self._changeToIdleTimer)
		self._changeToIdleTimer = engineApiGac.AddTimer(delay, self.ChangeToIdle)

	def ChangeToIdle(self):
		self.SetParam('scuke_survive_melee_taking', 0)
		self.SetParam('scuke_survive_melee_begin', 0)
		self.SetParam('scuke_survive_melee_attack', 0)
		self.SetParam('scuke_survive_melee_end', 0)
		self.SetParam('scuke_survive_melee_break', 0)

		self._changeToIdleTimer = None

	def MeleeBreak(self):
		self.SetParamOnlyOne('scuke_survive_melee_break', 1)
