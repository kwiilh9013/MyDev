# -*- coding: utf-8 -*-
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI

ProgressPath = "/progress_bar"


class C4BombUI(ModBaseUI):
	"""定时炸弹UI"""
	def __init__(self, namespace, name, param):
		super(C4BombUI, self).__init__(namespace, name, param)
		self.bar = None

	def Create(self):
		self.bar = self.GetBaseUIControl(ProgressPath).asProgressBar()
		self.SetBar(0)

	def SetBar(self, p, v=False):
		self.bar.SetVisible(v)
		self.bar.SetValue(p)



