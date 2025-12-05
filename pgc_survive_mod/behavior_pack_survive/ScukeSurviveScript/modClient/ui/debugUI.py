# -*- encoding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.common import config
from ScukeSurviveScript.ScukeCore.client.ui.baseUI import BaseUI


class GMDebugUI(BaseUI):
	def __init__(self, namespace, name, param):
		super(GMDebugUI, self).__init__(namespace, name, param)

	def Create(self):
		pass

	def OnClickDebugBtnC(self, *args, **kwargs):
		pass

	def OnClickDebugBtnS(self, *args, **kwargs):
		pass
