# -*- encoding: utf-8 -*-


class EventMgr(object):
	def __init__(self, handler=None):
		self.mEventDict = {}    # {event_id : func}

	def RegisterEvent(self, eventId, func):
		"""
		监听事件，传入函数实例
		:param event_id: modEnum.EventId
		:param func: function
		:return:
		"""
		if eventId not in self.mEventDict:
			self.mEventDict[eventId] = set()
		self.mEventDict[eventId].add(func)

	def NotifyEvent(self, eventId, *args):
		"""
		触发事件，执行之前Register传进来的函数，调用时注意规范好eventArgs
		:param eventId: modEnum.EventId
		:param args: dict 函数参数，需要注意结合RegisterEvent确定参数内容
		:return:
		"""
		funcs = self.mEventDict.get(eventId)
		if funcs is None:
			return
		for func in funcs:
			# 迭代期间注销订阅，会报错：Set changed size during iteration
			try:
				func(*args)
			except Exception as e:
				# 将报错信息输出到日志中，但不阻止程序运行
				import traceback
				from ScukeSurviveScript.ScukeCore.common.log import log
				log.logerror(traceback.format_exc())
		pass
	
	def UnRegisterEvent(self, eventId, func):
		"""
		反监听事件，与Register一致
		:param eventId: modEnum.EventId
		:param func: function
		:return:
		"""
		if eventId in self.mEventDict:
			self.mEventDict[eventId].discard(func)
		# logger.info("UnRegisterEvent {} {}".format(eventId, func.__name__))

	def ClearOne(self, eventId):
		if eventId in self.mEventDict:
			self.mEventDict[eventId].clear()

	def Destroy(self):
		for eventId, funcSet in self.mEventDict.iteritems():
			self.mEventDict[eventId] = None
		self.mEventDict = {}