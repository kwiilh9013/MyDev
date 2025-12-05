# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server.entity.component.componentBase import ComponentBase


class PassiveComponentBase(ComponentBase):
	"""被动类 组件基类"""
	def __init__(self, entityObj, config):
		super(PassiveComponentBase, self).__init__(entityObj, config)
		self.mIsTrigger = False
		"""当前是否触发"""
		pass


	def IsCanTrigger(self):
		"""被动是否可以触发"""
		# 如果有触发条件，则需重写该方法
		return True
	
	def OnTrigger(self):
		"""触发被动"""
		self.mIsTrigger = True
		# 子类重写该方法
		pass
	
	def OnCancelTrigger(self):
		"""取消被动"""
		self.mIsTrigger = False
		# 子类重写该方法
		pass
	
	def IsTrigger(self):
		"""当前是否触发"""
		return self.mIsTrigger
	