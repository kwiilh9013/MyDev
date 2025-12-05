from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.ui.baseWidget import BaseWidget


class ToggleGroupWidget(BaseWidget):

	def __init__(self, baseUI, path, toggleBtns, unique=False, initState=None, caller=None):
		super(ToggleGroupWidget, self).__init__(baseUI, path)
		self._toggles = []
		self._togglesValue = []
		self._index = -1
		self._caller = None
		self._uniqueMode = unique
		for i in range(0, len(toggleBtns)):
			togglePath = toggleBtns[i]
			ctrl = self.GetBaseUIControl(togglePath).asButton()
			ctrl.AddTouchEventParams({"isSwallow":True})
			def _selectFunc(index):
				return lambda (args): self.SetIndex(index)
			ctrl.SetButtonTouchUpCallback(_selectFunc(i))
			self._toggles.append({
				'default': ctrl.GetChildByName('default').asImage(),
				'selected': ctrl.GetChildByName('selected').asImage(),
			})
			self._togglesValue.append(False)
		if initState and len(initState) > 0:
			i = 0
			while i < len(initState):
				active = initState[i]
				toggleItem = self._toggles[i]
				self._SetBtnState(toggleItem, 'selected' if active else 'default')
				self._togglesValue[i] = active
				i += 1
			while i < len(self._toggles):
				active = False
				toggleItem = self._toggles[i]
				self._SetBtnState(toggleItem, 'selected' if active else 'default')
				self._togglesValue[i] = active
				i += 1
		self._caller = caller

	def SetIndex(self, index, state=None, notify=True):
		indexes = []
		last = self._index
		if self._uniqueMode:
			if state is None:
				state = True
			if last == index:
				return
			if not state:
				return
			for i in range(0, len(self._toggles)):
				toggleItem = self._toggles[i]
				active = i == index
				self._SetBtnState(toggleItem, 'selected' if active else 'default')
				self._togglesValue[i] = active

			self._index = index
			indexes.append(index)
		else:
			if state is None:
				state = not self._togglesValue[index]
			for i in range(0, len(self._toggles)):
				toggleItem = self._toggles[i]
				if i == index:
					self._SetBtnState(toggleItem, 'selected' if state else 'default')
					self._togglesValue[index] = state
				if self._togglesValue[i]:
					indexes.append(i)
		if notify and self._caller:
			self._caller(indexes)


	def _SetBtnState(self, btn, state):
		for key, img in btn.iteritems():
			img.SetAlpha(1 if key == state else 0)
			img.SetVisible(key == state)

	def GetStates(self):
		return list(self._togglesValue)

	def SetStates(self, states):
		i = 0
		indexes = []
		while i < len(states):
			active = states[i]
			toggleItem = self._toggles[i]
			self._SetBtnState(toggleItem, 'selected' if active else 'default')
			self._togglesValue[i] = active
			if active:
				indexes.append(i)
			i += 1
		while i < len(self._toggles):
			active = False
			toggleItem = self._toggles[i]
			self._SetBtnState(toggleItem, 'selected' if active else 'default')
			self._togglesValue[i] = active
			if active:
				indexes.append(i)
			i += 1

		if self._caller:
			self._caller(indexes)
