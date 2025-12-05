from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.ui.baseWidget import BaseWidget
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils


class SafeAreaWidget(BaseWidget):

	def __init__(self, baseUI, path, contentPath):
		super(SafeAreaWidget, self).__init__(baseUI, path)
		self._container = self.GetBaseUIControl('')
		self._contentContainer = self.GetBaseUIControl(contentPath)

	def UpdatePos(self, pos):
		outSize = self._container.GetSize()
		contentSize = self._contentContainer.GetSize()
		offset = self._container.GetPosition()
		deltaPos = MathUtils.TupleSub(pos, offset)
		validPos = [deltaPos[0], deltaPos[1]]

		for i in range(0, 2):
			curPos = deltaPos[i]
			leftSize = outSize[i] - curPos
			while contentSize[i] > leftSize and curPos > 0:
				curPos -= 0.1 * contentSize[i]
				leftSize = outSize[i] - curPos
			if curPos > 0:
				validPos[i] = curPos
		if validPos[0] > 0 and validPos[1] > 0:
			self._contentContainer.SetPosition((validPos[0], validPos[1]))
			return True
		return False