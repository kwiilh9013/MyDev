# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.display.weaponAnimator import WeaponAnimatorController, RegisterParam

CompFactory = clientApi.GetEngineCompFactory()

# 注册状态参数
RegisterParam('scuke_survive_gun_zoomin')
RegisterParam('scuke_survive_gun_zoom')
RegisterParam('scuke_survive_gun_zoomout')
RegisterParam('scuke_survive_gun_shoot_begin')
RegisterParam('scuke_survive_gun_shoot_bullet')
RegisterParam('scuke_survive_gun_shoot_end')
RegisterParam('scuke_survive_gun_shoot_break')
RegisterParam('scuke_survive_gun_reload')
RegisterParam('scuke_survive_gun_shooting')
RegisterParam('scuke_survive_gun_shooting_hold')
RegisterParam('scuke_survive_gun_kick')
RegisterParam('scuke_survive_gun_walk')
RegisterParam('scuke_survive_gun_walk_exit')
RegisterParam('scuke_survive_gun_sprint')
RegisterParam('scuke_survive_gun_sprint_exit')
RegisterParam('scuke_survive_gun_pick_exit')

# 可互斥状态参数
ConflictParams = [
	'scuke_survive_gun_shoot_begin',
	'scuke_survive_gun_shoot_bullet',
	'scuke_survive_gun_shoot_end',
	'scuke_survive_gun_shoot_break',
	'scuke_survive_gun_reload',
	'scuke_survive_gun_kick',
	'scuke_survive_gun_walk',
	'scuke_survive_gun_sprint',
]


class GunAnimatorController(WeaponAnimatorController):
	def __init__(self, eid, identifier, animatorConfig):
		super(GunAnimatorController, self).__init__(eid, identifier, animatorConfig, {
			'scuke_survive_gun_shoot_begin': 0,
			'scuke_survive_gun_shoot_bullet': 0,
			'scuke_survive_gun_shoot_end': 0,
			'scuke_survive_gun_shoot_break': 0,
			'scuke_survive_gun_reload': 0,
			'scuke_survive_gun_shooting': 0,
		}, ConflictParams)

		self._zoom = False
		self._zoomTime = 0

		self._changeToIdleTimer = None
		self._changeToZoomTimer = None
		self._changeToReloadTimer = None
		self._resetMovingExitTimer = None
		self._shootingHoldExitTimer = None

	def SetZoomTime(self, zoomTime):
		self._zoomTime = zoomTime

	def ZoomIn(self):
		self.ExitShootingHold()
		self._zoom = True
		self.SetParam('scuke_survive_gun_zoomin', 1)
		self.DelaySetZoom(self._zoomTime - 0.05, 1)
		self.SetParam('scuke_survive_gun_shooting', 0)
		self.ExitMoving()

	def ZoomOut(self):
		self.ExitShootingHold()
		self._zoom = False
		self.SetParam('scuke_survive_gun_zoomout', 1)
		self.DelaySetZoom(self._zoomTime - 0.05, 0)
		self.SetParam('scuke_survive_gun_shooting', 0)
		self.ExitMoving()

	def BeginShoot(self):
		self.SetParam('scuke_survive_gun_shooting', 1)
		self.SetParamOnlyOne('scuke_survive_gun_shoot_begin', 1)
		self.DelayChangeToIdle(0.01)
		self.ExitMoving()

	def ShootBullet(self):
		self.BeginShootingHold()
		self.SetParamOnlyOne('scuke_survive_gun_shoot_bullet', 1)
		self.DelayChangeToIdle(0.01)
		self.ExitMoving()

	def EndShoot(self):
		self.BeginShootingHold()
		self.SetParamOnlyOne('scuke_survive_gun_shoot_end', 1)
		self.DelayChangeToIdle(0.01)
		self.SetParam('scuke_survive_gun_shooting', 0)
		self.ExitMoving()

	def Reload(self):
		self.ExitShootingHold()
		self.SetParamOnlyOne('scuke_survive_gun_reload', 1)
		self.DelayChangeToIdle(0.01)
		self.SetParam('scuke_survive_gun_shooting', 0)
		self.ExitMoving()

	def Kick(self):
		self.ExitShootingHold()
		self.SetParamOnlyOne('scuke_survive_gun_kick', 1)
		self.DelayChangeToIdle(0.01)
		self.SetParam('scuke_survive_gun_shooting', 0)
		self.ExitMoving()

	def ExitMoving(self):
		self.SetParam('scuke_survive_gun_walk_exit', 1)
		self.SetParam('scuke_survive_gun_sprint_exit', 1)
		self.SetParam('scuke_survive_gun_pick_exit', 1)
		self.DelayResetMoving(0.01)

	def SetWalking(self, state):
		self.SetParam('scuke_survive_gun_walk', 1 if state else 0)

	def SetSprinting(self, state):
		self.ExitShootingHold()
		self.SetParam('scuke_survive_gun_sprint', 1 if state else 0)

	def DelaySetZoom(self, delay, state):
		if self._changeToZoomTimer:
			engineApiGac.CancelTimer(self._changeToZoomTimer)
		self._changeToZoomTimer = engineApiGac.AddTimer(delay, self.ChangeZoomState, state)

	def DelaySetReload(self, delay, state):
		if self._changeToReloadTimer:
			engineApiGac.CancelTimer(self._changeToReloadTimer)
		self._changeToReloadTimer = engineApiGac.AddTimer(delay, self.ChangeZoomState, state)

	def DelayChangeToIdle(self, delay):
		if self._changeToIdleTimer:
			engineApiGac.CancelTimer(self._changeToIdleTimer)
		self._changeToIdleTimer = engineApiGac.AddTimer(delay, self.ChangeToIdle)

	def DelayResetMoving(self, delay):
		if self._resetMovingExitTimer:
			engineApiGac.CancelTimer(self._resetMovingExitTimer)
		self._resetMovingExitTimer = engineApiGac.AddTimer(delay, self.ResetDownLayer)

	def DelayExitShootingHold(self, delay):
		if self._shootingHoldExitTimer:
			engineApiGac.CancelTimer(self._shootingHoldExitTimer)
		self._shootingHoldExitTimer = engineApiGac.AddTimer(delay, self.ExitShootingHold, False)

	def ResetDownLayer(self):
		self.SetParam('scuke_survive_gun_walk_exit', 0)
		self.SetParam('scuke_survive_gun_sprint_exit', 0)
		self.SetParam('scuke_survive_gun_pick_exit', 0)
		self._resetMovingExitTimer = None

	def BeginShootingHold(self):
		self.SetParam('scuke_survive_gun_shooting_hold', 1)
		self.DelayExitShootingHold(5.0)

	def ExitShootingHold(self, rightNow=True):
		if rightNow:
			if self._shootingHoldExitTimer:
				engineApiGac.CancelTimer(self._shootingHoldExitTimer)
		self.SetParam('scuke_survive_gun_shooting_hold', 0)
		self._shootingHoldExitTimer = None

	def ChangeToIdle(self):
		self.SetParam('scuke_survive_gun_shoot_begin', 0)
		self.SetParam('scuke_survive_gun_shoot_bullet', 0)
		self.SetParam('scuke_survive_gun_shoot_end', 0)
		self.SetParam('scuke_survive_gun_shoot_break', 0)
		self.SetParam('scuke_survive_gun_reload', 0)
		self.SetParam('scuke_survive_gun_kick', 0)

		self._changeToIdleTimer = None

	def ChangeZoomState(self, state):
		self.SetParam('scuke_survive_gun_zoomin', 0)
		self.SetParam('scuke_survive_gun_zoomout', 0)
		self.SetParam('scuke_survive_gun_zoom', state)
		self._changeToZoomTimer = None

	def ChangeReloadState(self, state):
		self.SetParam('scuke_survive_gun_reload', state)
		self._changeToReloadTimer = None

	def BreakShoot(self):
		self.SetParamOnlyOne('scuke_survive_gun_shoot_break', 1)

