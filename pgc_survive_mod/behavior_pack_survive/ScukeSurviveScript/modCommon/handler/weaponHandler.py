
class WeaponHandler(object):
	def __init__(self, eid, config, extraId=None):
		self._eid = eid
		self._extraId = extraId
		self._isSprinting = False
		self._config = config
		self._keyDownTime = 0
		self._keyUpTime = 0

	@property
	def Eid(self):
		return self._eid

	@property
	def ExtraId(self):
		return self._extraId

	@property
	def Config(self):
		return self._config

	@property
	def Sprinting(self):
		return self._isSprinting

	def SetSprinting(self, state):
		self._isSprinting = state

	def KeyDown(self, time):
		return False

	def KeyUp(self, time):
		return False

	def IsUsing(self):
		return self._keyDownTime > 0 and self._keyUpTime < self._keyDownTime
