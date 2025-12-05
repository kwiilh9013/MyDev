# -*- encoding: utf-8 -*-
import inspect
from ScukeSurviveScript.ScukeCore.common.Timeline.Timeline import Timeline
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server.entity.enum.actionEnum import ActionEnum
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
from ScukeSurviveScript.ScukeCore.server import engineApiGas


class ComponentBase(CommonEventRegister):
	"""组件基类"""
	# region 初始化
	def __init__(self, entityObj, config):
		CommonEventRegister.__init__(self, entityObj.mServer)
		# 组件相关
		self.mEntityObj = entityObj
		"""组件对应的实体对象"""
		self.mEntityId = entityObj.mEntityId
		"""实体id"""
		self.mConfig = config
		"""组件配置"""

		self.mTimeline = None
		"""timeline对象"""

		self._runState = False

		# action方法
		self._actionFunctionMapping = {}
		self._InitActionMapping()

		# 初始化timeline
		self.InitTimeline()
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self.mEntityObj = None
		if self.mTimeline:
			self.mTimeline.Destroy()
			self.mTimeline = None
		pass

	def _InitActionMapping(self):
		"""初始化动作映射, 根据装饰器添加的方法属性, 初始化mapping"""
		for _, func in inspect.getmembers(self, inspect.ismethod):
			actionType = getattr(func, "_actionType", None)
			if actionType and actionType not in self._actionFunctionMapping:
				self._actionFunctionMapping[actionType] = func
		pass
	# endregion
	
	# region 生命周期
	def InitTimeline(self):
		"""timeline逻辑的初始化"""
		if not self.mConfig:
			return
		cfg = self.mConfig
		timelienCfg = cfg.get("timeline")
		if timelienCfg:
			# 获取最大关键帧
			maxFrame = max(timelienCfg.iterkeys())
			# 创建timeline
			self.mTimeline = Timeline(maxFrame, endFunction=self.End)
			# 设置节点
			for frame, nodeCfg in timelienCfg.iteritems():
				# 如果是没有config，则跳过
				if not nodeCfg:
					continue
				nodeType = nodeCfg["type"]
				nodeFunct = self.GetActionFunction(nodeType)
				self.mTimeline.addNode(frame, nodeFunct, nodeCfg)
		pass
	
	def Start(self):
		"""组件启动时调用"""
		self._runState = True
		# timeline和actions只能执行其一
		if self.mTimeline:
			self.mTimeline.Start()
			return
		
		# 执行actions
		if "actions" in self.mConfig:
			for actionCfg in self.mConfig["actions"]:
				func = self.GetActionFunction(actionCfg["type"])
				func(actionCfg)
			self.End()
			return
		pass

	def Update(self):
		"""tick方法, 1秒30帧"""
		if self.mTimeline:
			self.mTimeline.Update()
		pass

	def End(self):
		"""组件结束时调用"""
		self._runState = False
		pass

	def GetRunState(self):
		"""获取组件运行状态"""
		return self._runState
	# endregion

	# region Actions
	def GetActionFunction(self, actionEnum):
		"""获取动作节点函数"""
		return self._actionFunctionMapping.get(actionEnum)

	@AddActionMapping(ActionEnum.SetMolang)
	def SetMolang(self, cfg):
		"""设置molang值"""
		if not cfg or "molang" not in cfg:
			return
		info = {
			"stage": "molang",
			"molang": cfg["molang"],
		}
		self.mEntityObj.SendOneMsgToAllClient(info)
		pass

	@AddActionMapping(ActionEnum.TriggerAddEvent)
	def TriggerAddEvent(self, cfg):
		"""触发行为包事件"""
		if not cfg or "event" not in cfg:
			return
		engineApiGas.TriggerCustomEvent(self.mEntityId, cfg["event"])
		pass

	@AddActionMapping(ActionEnum.ResetAttackTarget)
	def ResetAttackTarget(self, cfg):
		"""清除仇恨目标"""
		engineApiGas.ResetAttackTarget(self.mEntityId)
		pass
	# endregion

