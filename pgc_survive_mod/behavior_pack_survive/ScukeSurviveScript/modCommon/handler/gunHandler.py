# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.handler.lerpHandler import LerpHandler
from ScukeSurviveScript.modCommon.handler.weaponHandler import WeaponHandler


class GunHandler(WeaponHandler):
	def __init__(self, eid, config, validClipCount, extraId=None):
		super(GunHandler, self).__init__(eid, config, extraId)

		self._zoomTime = 0
		self._zoomState = False
		self._shootTime = 0
		self._keyUpShootTime = 0
		self._shootBulletTime = 0
		self._reloadTime = 0
		self._kickTime = 0
		self._kickCastTime = 0
		self._shootClip = 0
		self._currentClip = 0
		self._shootPoint = (0, 0, 0)
		self._shootDirect = (0, 0, 0)

		self._validClipCount = 0

		self._recoilVertical = None
		self._recoilFov = None
		self._scatter = None
		self._zoomFov = None

		# reload
		self.InitReload(config['reload'], validClipCount)
		# zoom
		self.InitZoom(config['zoom'])
		# recoil
		self.InitRecoil(config['recoil'])
		# scatter
		self.InitScatter(config['scatter'])
		# 蓄力
		self._charge = config.get('charge', None)
		self._chargeCoef = 1.0
		self._chargeTime = 0.0
		self._chargeLevel = 0

	@property
	def Clip(self):
		return self._currentClip

	@property
	def MaxClip(self):
		return self._config['reload']['clip']

	@property
	def ClipItemCount(self):
		return self._validClipCount

	@property
	def ChargeInfo(self):
		return {
			'time': self._chargeTime,
			'level': self._chargeLevel,
			'coef': self._chargeCoef,
		}

	@property
	def ScatterAngle(self):
		if self._scatter:
			return self._scatter.Current
		return 0

	@property
	def ReloadingTime(self):
		return self._reloadTime, self._config['reload']['duration']

	def SetClip(self, clip):
		if clip < 0:
			clip = 0
		if clip > self.MaxClip:
			clip = self.MaxClip
		self._currentClip = clip

	def SetValidClipCount(self, count):
		count = count * self.MaxClip  # 单物品弹夹
		changed = self._validClipCount != count
		self._validClipCount = count
		return changed

	def KeyDown(self, time):
		if self.IsShooting():
			return False
		if self.CheckKeyDownWaiting(time):
			return False
		if self._currentClip == 0:
			return False
		self._keyDownTime = time
		self._keyUpTime = 0
		self.ResetRecoil()
		self.CalcChargeInfo(0)
		return True

	def CheckKeyDownWaiting(self, time):
		config = self._config
		keyDownMinGap = config['keyDownMinGap'] * 1000
		if time - self._shootTime < keyDownMinGap:
			return True
		shootGap = self._config['shootGap'] * 1000
		if time - self._shootTime < shootGap:
			return True
		zoomTime = config['zoomTime'] * 1000
		if time - self._zoomTime < zoomTime:
			return True
		reloadTime = config['reload']['duration'] * 1000
		if time - self._reloadTime < reloadTime:
			return True
		kickTime = config['kick']['duration'] * 1000
		if time - self._kickTime < kickTime:
			return True

		return False

	def KeyUp(self, time):
		if not self.IsShooting():
			return False
		if time - self._keyDownTime < 100:
			return False
		self._keyUpTime = time
		config = self._config
		if config['shootType'] == 'keyUp':
			self._keyUpShootTime = time
		return True

	def IsZooming(self):
		return self._zoomState

	def IsZoomMoving(self):
		return self._zoomTime > 0

	def IsShooting(self):
		return self.IsUsing()

	def IsUsing(self):
		return super(GunHandler, self).IsUsing() or (self._keyUpShootTime > 0)

	def WaitingShootBegin(self, time):
		deltaTime = time - self._keyDownTime
		return self._keyDownTime > 0 and self._keyUpTime < self._keyDownTime and deltaTime < self._config[
			'shootDelay'] * 1000

	def IsReloading(self):
		return self._reloadTime > 0

	def IsKicking(self):
		return self._kickTime > 0

	def UpdateGunShoot(self, time):
		config = self._config

		if self.IsReloading() or self._currentClip == 0:
			return
		if not self.IsShooting():
			return
		if self.WaitingShootBegin(time):
			return

		shootClip = config['shootClip']
		shootType = config['shootType']
		shootGap = config['shootGap'] * 1000
		keyDownTime = self._keyDownTime
		keyUpTime = self._keyUpTime
		shootTime = self._shootTime
		needShoot = False
		if shootType == 'keyDown':
			if shootTime < keyDownTime:
				shootTime = keyDownTime
				needShoot = True  # 按下立刻Shoot
			deltaTime = time - shootTime
			if deltaTime >= shootGap:
				shootTime += shootGap
				needShoot = True
		elif shootType == 'keyUp':
			if self._keyUpShootTime > 0:
				self.CalcChargeInfo(self._keyUpShootTime - keyDownTime)
				shootTime = self._keyUpShootTime
				needShoot = True
				self._keyUpShootTime = 0
			elif keyUpTime == 0 and keyDownTime > 0:
				self.CalcChargeInfo(time - keyDownTime)
		if needShoot:
			self._shootTime = shootTime
			self._shootClip = shootClip

	def CalcChargeInfo(self, deltaTime):
		self._chargeTime = 0.0
		self._chargeCoef = 1.0
		self._chargeLevel = 0
		t = 0
		if self._charge:
			self._chargeTime = deltaTime
			levels = self._charge['levels']
			for level in levels:
				if deltaTime > t:
					self._chargeLevel += 1
					self._chargeCoef = level['coef']
				else:
					break
				t += level['time']*1000

	def InitRecoil(self, recoilConfig):
		duration = recoilConfig['duration']
		backDuration = recoilConfig['backDuration']
		if not self._recoilVertical:
			self._recoilVertical = LerpHandler(recoilConfig['angle'], duration, backDuration, recoilConfig['maxAngle'])
		else:
			self._recoilVertical.ResetParams(recoilConfig['angle'], duration, backDuration, recoilConfig['maxAngle'])
		if not self._recoilFov:
			self._recoilFov = LerpHandler(recoilConfig['fov'], duration, backDuration, recoilConfig['maxFov'])
		else:
			self._recoilFov.ResetParams(recoilConfig['fov'], duration, backDuration, recoilConfig['maxFov'])


	def ResetRecoil(self):
		if self._recoilVertical:
			self._recoilVertical.Reset()

	def InitZoom(self, zoomConfig):
		duration = zoomConfig['fovDuration']
		backDuration = duration
		self._zoomFov = LerpHandler(-zoomConfig['fovModify'], duration, backDuration)

	def InitReload(self, reloadConfig, validClipCount):
		self._validClipCount = validClipCount * reloadConfig['clip']  # 单物品弹夹
		self._currentClip = 0

	def InitScatter(self, scatterConfig):
		duration = 0.0
		backDuration = scatterConfig['backDuration']
		max = scatterConfig['max']
		self._scatter = LerpHandler(scatterConfig['angle'], duration, backDuration, max)


	def UpdateGunRecoil(self, time, dTime, shootBullet):
		movedAngleV = 0.0
		if self._recoilVertical:
			movedAngleV = self._recoilVertical.Update(time, dTime, shootBullet)
		movedKick = 0.0
		if self._recoilFov:
			movedKick = self._recoilFov.Update(time, dTime, shootBullet)
		return (movedAngleV, 0, movedKick)

	def UpdateGunScatter(self, time, dTime, shootBullet):
		movedScatter = 0.0
		if self._scatter:
			movedScatter = self._scatter.Update(time, dTime, shootBullet)
		return movedScatter

	def UpdateGunZoom(self, time, dTime):
		movedZoomFov = 0.0
		if self._zoomFov:
			movedZoomFov = self._zoomFov.Update(time, dTime, False, False)
		zoomTime = self._config['zoomTime'] * 1000
		if time - self._zoomTime > zoomTime:
			self._zoomTime = 0
		return movedZoomFov

	def UpdateGunReload(self, time, dTime):
		reloadConfig = self._config['reload']
		reloadDuration = reloadConfig['duration'] * 1000
		maxClip = min(self._validClipCount, reloadConfig['clip'])
		if self._currentClip == 0 and maxClip == 0:
			return True, False

		reloadCompleted = False
		deltaTime = time - self._reloadTime
		if self._reloadTime > 0 and deltaTime >= reloadDuration:
			self._reloadTime = 0
			self._currentClip = maxClip
			reloadCompleted = True

		return self._currentClip == 0 and self._reloadTime == 0, reloadCompleted

	def UpdateGunKick(self, time, dTime):
		kickConfig = self._config['kick']
		kickDuration = kickConfig['duration'] * 1000
		kickCast = kickConfig['cast'] * 1000
		kickCompleted = False
		kickAttack = False
		deltaTime = time - self._kickTime

		if self._kickTime > 0 and deltaTime >= kickCast and self._kickCastTime == 0:
			self._kickCastTime = time
			kickAttack = True

		if self._kickTime > 0 and deltaTime >= kickDuration:
			self._kickTime = 0
			self._kickCastTime = 0
			kickCompleted = True

		return kickAttack, kickCompleted

	def UpdateGunShootBullet(self, time):
		needShootClip = self._shootClip
		if needShootClip > 0:
			eid = self._eid
			config = self._config
			self._shootClip = needShootClip - 1
			self._currentClip = self._currentClip - 1
			return {
				'eid': eid,
				'config': config['shootEffect']
			}

		return None

	def SetZoomActive(self, time, active):
		if self.CheckKeyDownWaiting(time):
			return False
		if self.IsShooting():  # 瞄准时如果正在射击需要强制停止
			self.KeyUp(time)
			return False
		self._zoomTime = time
		self._zoomState = active
		config = self._config
		if active:
			self.InitRecoil(config['zoom']['recoil'])
			if self._zoomFov:
				self._zoomFov.Reset()
				self._zoomFov.Update(time, 0, True, False, 1)
		else:
			self.InitRecoil(config['recoil'])
			if self._zoomFov:
				self._zoomFov.Update(time, 0, False, False, -1)
		return True

	def Reload(self, time):
		if self.IsShooting():  # 正在射击无法触发
			return False
		if self._validClipCount <= 0:
			return False
		if self.CheckKeyDownWaiting(time):
			return False
		self._reloadTime = time
		return True

	def Kick(self, time):
		if self.IsShooting():  # 正在射击无法触发
			return False
		if self.CheckKeyDownWaiting(time):
			return False
		self._kickTime = time
		self._kickCastTime = 0
		return True

	def DoScatter(self, direction):
		import random
		import math
		from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, MathUtils
		scatter = self.ScatterAngle
		if scatter <= 0 or scatter >= 90:
			return direction
		r = math.tan(math.radians(scatter)) * random.random()
		angle = math.radians(360) * random.random()
		temp = Vector3(math.cos(angle) * r, math.sin(angle) * r, 1.0)
		temp.Normalize()
		forward = Vector3(direction)
		rot = MathUtils.LookDirection(forward)
		ret = rot * temp
		ret.Normalize()
		return ret.ToTuple()

	def GetRestoreRecoil(self):
		movedAngleV = 0.0
		if self._recoilVertical:
			movedAngleV = self._recoilVertical.GetRestore()
		movedKick = 0.0
		if self._recoilFov:
			movedKick = self._recoilFov.GetRestore()
		return (movedAngleV, 0, movedKick)

	def GetRestoreZoom(self):
		movedZoomFov = 0.0
		if self._zoomFov:
			movedZoomFov = self._zoomFov.GetRestore()
		return movedZoomFov
