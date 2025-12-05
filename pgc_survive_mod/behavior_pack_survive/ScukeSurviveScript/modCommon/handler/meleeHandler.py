# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.handler.lerpHandler import LerpHandler
from ScukeSurviveScript.modCommon.handler.weaponHandler import WeaponHandler


class MeleeHandler(WeaponHandler):
	def __init__(self, eid, config, extraId=None):
		super(MeleeHandler, self).__init__(eid, config, extraId)
		self._combo = 0
		self._nextMeleeTime = 0
		self._meleeStartTime = 0
		self._meleeCast = False
		self._meleeEndTime = 0
		self._meleeConfig = None
		self._keyUpAttack = None
		self._level = 0
		self._recoilFov = None
		self._keyUpCast = False
		self._takingPassed = 0

	@property
	def Combo(self):
		return self._combo

	@property
	def Level(self):
		return self._level

	def KeyDown(self, time):
		if self.IsUsing():
			return False
		if self.CheckKeyDownWaiting(time):
			return False
		self._keyDownTime = time
		self._nextMeleeTime = time
		self._meleeStartTime = 0
		self._meleeCast = False
		self._meleeConfig = None
		self._keyUpAttack = None
		self._keyUpTime = 0
		return True

	def CheckKeyDownWaiting(self, time):
		config = self._config
		if time - self._nextMeleeTime < 0 or time - self._meleeEndTime < 0:
			return True
		if self._takingPassed < config['takingTime'] * 1000:
			return True
		if self._keyUpAttack:
			return True
		return False

	def WaitingMeleeBegin(self, time):
		deltaTime = time - self._keyDownTime
		return self._keyDownTime > 0 and self._keyUpTime < self._keyDownTime and deltaTime < self._config['meleeDelay'] * 1000

	def UpdateMelee(self, time, dTime):
		config = self._config
		if self._takingPassed < config['takingTime'] * 1000:
			self._takingPassed += dTime
		if not self.IsUsing():
			# 冷却时间到combo从0开始
			if self._meleeCast and self._combo > 0 and time - self._meleeEndTime >= config['cooldownTime'] * 1000:
				self._combo = 0
				self._level = 0
			if self._combo < 0:
				self._combo = -self._combo
				return self._meleeConfig
			return None
		if self.WaitingMeleeBegin(time):
			self._nextMeleeTime = time
			return None
		changeToNext = time >= self._nextMeleeTime and self._combo >= 0
		if changeToNext:
			meleeEffects = config['meleeEffects']
			total = len(meleeEffects)
			self._combo += 1
			if self._combo > total:
				self._combo = self._combo % total
			self._meleeConfig = self.GetMelee(self._combo)
			if not self._meleeConfig:
				self._combo = 0
			else:
				self._meleeStartTime = time
				self._meleeCast = False
				type = self._meleeConfig['type']
				if type == 'emit' or type == 'loop':
					self._nextMeleeTime += self._meleeConfig['duration'] * 1000
				elif type == 'charge':
					self._combo = -self._combo  # 负数标记为等待

		if changeToNext:
			if self._meleeConfig:
				self._keyUpCast = self._meleeConfig['type'] == 'charge'
				if 'recoil' in self._meleeConfig:
					self.SetRecoil(self._meleeConfig['recoil'])
			return self._meleeConfig

		return None

	def UpdateMeleeAttack(self, time):
		attack = None
		config = self._meleeConfig
		if not config:
			return None
		startTime = self._meleeStartTime
		if startTime > 0 and not self._meleeCast:
			type = config['type']
			dTime = time - startTime
			if type == 'emit' or type == 'loop':
				attack = self.UpdateMeleeEmit(config, time, dTime)
			elif type == 'charge':
				self._keyUpAttack = self.UpdateMeleeCharge(config, time, dTime)
				self._level = 0 if 'level' not in self._keyUpAttack else self._keyUpAttack['level']

		if not self.IsUsing() and self._keyUpAttack:
			startTime = self._keyUpTime
			dTime = time - startTime
			attack = self.UpdateMeleeEmit(config, time, dTime, self._keyUpAttack)

		if attack:
			self._level = 0 if 'level' not in attack else attack['level']
			self._keyUpAttack = None
			self._meleeCast = True
			self._meleeEndTime = startTime + config['duration'] * 1000
			return {
				'eid': self._eid,
				'config': attack,
				'level': self._level,
				'combo': self._combo,
				'castTime': time - startTime,
				'meleeTime': time - self._meleeStartTime,
			}

		return None

	def UpdateMeleeEmit(self, config, time, dTime, attack=None):
		castTime = config['cast'] * 1000
		if dTime >= castTime:
			return attack if attack else config['attack']
		return None

	def UpdateMeleeCharge(self, config, time, dTime):
		return self._GetMeleeChargeAttack(config, dTime)

	def _GetMeleeChargeAttack(self, config, dTime):
		levels = config['levels']
		attacks = config['attacks']
		ret = None
		for l in range(0, len(levels)):
			ltime = levels[l] * 1000
			ret = attacks[l]
			if dTime <= ltime:
				break
		return ret

	def GetMelee(self, combo):
		config = self._config
		meleeEffects = config['meleeEffects']
		if combo <= 0 or combo > len(meleeEffects):
			return None
		return meleeEffects[combo-1]

	def GetMeleeAttack(self, combo, castTime, meleeTime):
		meleeConfig = self.GetMelee(combo)
		if meleeConfig['type'] == 'charge':
			return self._GetMeleeChargeAttack(meleeConfig, meleeTime - castTime)
		return meleeConfig['attack']

	def KeyUp(self, time):
		if not self.IsUsing():
			return False
		if time - self._keyDownTime < 200:
			return False
		self._keyUpTime = time
		return True

	def SetRecoil(self, recoilConfig):
		duration = recoilConfig['duration']
		backDuration = recoilConfig['backDuration']
		maxValue = None
		if 'maxFov' in recoilConfig:
			maxValue = recoilConfig['maxFov']
		newRecoilFov = LerpHandler(recoilConfig['fov'], duration, backDuration, maxValue)
		if self._recoilFov and self._recoilFov.Current != 0:
			return
		self._recoilFov = newRecoilFov

	def UpdateMeleeRecoilFov(self, time, dTime, active):
		keyDown = self._keyDownTime > self._keyUpTime
		movedKick = 0.0
		if self._recoilFov:
			if self._keyUpCast:
				movedKick = self._recoilFov.Update(time, dTime, active and keyDown, False, 1 if keyDown else -1)
			else:
				movedKick = self._recoilFov.Update(time, dTime, active)
		return movedKick

	def GetRestoreRecoilFov(self):
		movedKick = 0.0
		if self._recoilFov:
			movedKick = self._recoilFov.GetRestore()
		return movedKick
