# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()


class GameRenderTickUI(clientApi.GetScreenNodeCls()):
	"""游戏渲染tickUI 实现；当界面不是主界面时，tick会停止"""
	def __init__(self, namespace, name, param):
		super(GameRenderTickUI, self).__init__(namespace, name, param)
		self._client = param.get("client")
		pass

	def Destroy(self):
		pass

	def Create(self):
		pass

	@ViewBinder.binding(ViewBinder.BF_BindString, "#main.gametick")
	def OnGameTick(self):
		# 广播事件
		if self._client:
			self._client.OnGameRenderTick()
		pass
