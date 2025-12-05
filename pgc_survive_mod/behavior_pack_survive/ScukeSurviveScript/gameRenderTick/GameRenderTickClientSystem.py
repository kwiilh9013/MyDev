# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..ScukeCore.utils.eventWrapper import EngineEvent
from ..ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ..modCommon import modConfig
import gameRenderTickConfig


class GameRenderTickClientSystem(BaseClientSystem):
	""" 渲染帧 客户端，多个mod间只存在一个"""
	def __init__(self, namespace, systemName):
		super(GameRenderTickClientSystem, self).__init__(namespace, systemName)
		# 订阅的回调方法
		self.mEventDict = None
		self._updateMode = False
		self._tick = 0
		self._tickDict = {"tick": self._tick}
		pass
	
	@EngineEvent(priority=5)
	def UiInitFinished(self, args=None):
		# 初始化renderTick的UI
		clientApi.RegisterUI(modConfig.ModNameSpace, gameRenderTickConfig.UIKey, gameRenderTickConfig.UIClassPath, gameRenderTickConfig.UINamespace)
		clientApi.CreateUI(modConfig.ModNameSpace, gameRenderTickConfig.UIKey, {"isHud": 1, "client": self})
		pass

	@EngineEvent()
	def PushScreenEvent(self, args):
		if args['screenDef'] != '':
			self._updateMode = True

	@EngineEvent()
	def PopScreenAfterClientEvent(self, args):
		if args['screenDef'] == 'hud.hud_screen':
			self._updateMode = False

	def Update(self):
		if self._updateMode:
			self.OnGameRenderTick()

	# region api
	def OnGameRenderTick(self):
		self._tick += 1
		self._tickDict["tick"] = self._tick
		args = self._tickDict
		"""渲染帧事件，由UI调用"""
		# 调用订阅的回调方法
		if self.mEventDict:
			for func in self.mEventDict:
				# 迭代期间注销订阅，会报错：Set changed size during iteration
				try:
					func(*args)
				except Exception as e:
					# 将报错信息输出到日志中，但不阻止程序运行
					import traceback
					from ScukeAHSScript.ScukeCore.common.log import log
					log.logerror(traceback.format_exc())
		pass


	def RegisterEvent(self, func):
		"""
		订阅渲染帧事件，传入函数实例
		:param func: function
		"""
		if self.mEventDict is None:
			self.mEventDict = set()
		self.mEventDict.add(func)

	def UnRegisterEvent(self, func):
		"""
		取消订阅渲染帧事件，传入函数实例
		:param func: function
		"""
		if self.mEventDict:
			self.mEventDict.discard(func)
		pass
	# endregion
