# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon.eventConfig import FullScreenUIEvent
compFactory = clientApi.GetEngineCompFactory()


"""
控制类效果，仅针对玩家
"""


class CtrlBuilder(object):
	__bindingObj__ = {}

	@staticmethod
	def BindingClass(name, cls):
		"""构建类的映射"""
		CtrlBuilder.__bindingObj__[name] = cls

	@staticmethod
	def CreateObj(eventHandler, eid, config):
		"""创建对象"""
		tType = config['type']
		if tType not in CtrlBuilder.__bindingObj__:
			return None
		cls = CtrlBuilder.__bindingObj__[tType]
		return cls(eventHandler, eid, config)


class CancelPlayerCtrl(object):
	"""取消玩家操作"""
	def __init__(self, eventHandler, eid, config):
		self._eid = eid
		self._eventHandler = eventHandler
		self._cancelMove = config.get("cancel_move", False)
		self._cancelDrag = config.get("cancel_drag", False)
		self._cancelJump = config.get("cancel_jump", False)
		self._cancelBlocks = config.get("cancel_blocks", False)
		self._cancelUI = config.get("cancel_ui_response", False)

		self._motionComp = compFactory.CreateActorMotion(self._eid)
		self._operationComp = compFactory.CreateOperation(self._eventHandler.mLevelId)

		# 移动
		if self._cancelMove:
			self._motionComp.LockInputVector((0, 0))
		# 跳跃
		if self._cancelJump:
			self._operationComp.SetCanJump(False)
			self._operationComp.SetCanInair(False)
		# 拖动屏幕
		if self._cancelDrag:
			self._operationComp.SetCanDrag(False)
		# 方块交互
		if self._cancelBlocks:
			clientApi.SetResponse(False)
		# 屏蔽自定义UI
		if self._cancelUI:
			info = {"stage": "ui_response", "state": True}
			Instance.mEventMgr.NotifyEvent(FullScreenUIEvent, info)
		pass

	# 需在 DisplayClientSystem.UpdateDisplay中开启
	# def OnUpdate(self):
	# 	pass

	def OnDestroy(self):
		# 恢复操作
		# 移动
		if self._cancelMove:
			self._motionComp.UnlockInputVector()
		if self._cancelJump:
			self._operationComp.SetCanJump(True)
			self._operationComp.SetCanInair(True)
		if self._cancelDrag:
			self._operationComp.SetCanDrag(True)
		if self._cancelUI:
			clientApi.SetResponse(True)
		if self._cancelUI:
			info = {"stage": "ui_response", "state": False}
			Instance.mEventMgr.NotifyEvent(FullScreenUIEvent, info)
		pass
