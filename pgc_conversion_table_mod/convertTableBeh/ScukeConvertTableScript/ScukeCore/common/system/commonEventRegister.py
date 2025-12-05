# -*- coding: utf-8 -*-
import inspect

class CommonEventRegister(object):
	__INNER_ATTR__ = ["__func_list__", "__register_func_list__"]
	EngineNamespace = "Minecraft"
	EngineSystemName = "Engine"

	def __init__(self, system):
		self.__system__ = system
		self.__func_list__ = set()
		self.__register_func_list__ = set()
		self.ListenEvent()

	def OnDestroy(self):
		self.UnListenEvent()

	def ListenEvent(self):
		for _, func in inspect.getmembers(self, inspect.ismethod):
			eventName = getattr(func, "eventName", None)
			if eventName is not None:
				if eventName in self.__func_list__:
					print "[ERR]skip duplicate register event with name:", eventName
					continue
				self.__func_list__.add(eventName)
				registerByDefault = getattr(func, "registerByDefault", False)
				if not registerByDefault:
					continue
				space = getattr(func, "spaceName", None)
				if space:
					realNameSpace = space
				else:
					realNameSpace = self.EngineNamespace
				innerSystemName = getattr(func, "systemName", None)
				if innerSystemName:
					realSystemName = innerSystemName
				else:
					realSystemName = self.EngineSystemName
				self.__system__.ListenForEvent(realNameSpace, realSystemName, eventName, self, func, func.priority)
				# update register flag
				self.__register_func_list__.add(eventName)

	def UnListenEvent(self):
		for _, func in inspect.getmembers(self, inspect.ismethod):
			eventName = getattr(func, "eventName", None)
			if eventName is not None:
				if eventName not in self.__register_func_list__:
					continue
				space = getattr(func, "spaceName", None)
				if space:
					realNameSpace = space
				else:
					realNameSpace = self.EngineNamespace
				innerSystemName = getattr(func, "systemName", None)
				if innerSystemName:
					realSystemName = innerSystemName
				else:
					realSystemName = self.EngineSystemName
				self.__system__.UnListenForEvent(realNameSpace, realSystemName, eventName, self, func, func.priority)
				# update register flag
				self.__register_func_list__.discard(eventName)
	
	def __setattr__(self, name, value):
		func_list = getattr(self, "__func_list__", None)
		if func_list is not None and name in func_list:
			func = getattr(self, name)
			if value and name in self.__register_func_list__:
				return
			if value:
				self.__system__.ListenForEvent(self.EngineNamespace, self.EngineSystemName, name, self, func, func.priority)
				self.__register_func_list__.add(name)
			else:
				self.__system__.UnListenForEvent(self.EngineNamespace, self.EngineSystemName, name, self, func, func.priority)
				self.__register_func_list__.discard(name)
		else:
			if self is None: return
			if CommonEventRegister is None: return
			super(CommonEventRegister, self).__setattr__(name, value)

	def SendMsgToServer(self, msgName, args):
		"""发送消息到服务端，仅能在客户端执行"""
		# 封装参数
		data = self.__system__.CreateEventData()
		for k, v in args.items():
			data[k] = v
		# 发消息
		self.__system__.NotifyToServer(msgName, data)
		pass
	
	def SendMsgToClient(self, playerId, msgName, args):
		"""发送消息到指定的客户端，仅能在服务端执行"""
		# 封装参数
		data = self.__system__.CreateEventData()
		for k, v in args.items():
			data[k] = v
		# 发消息
		self.__system__.NotifyToClient(playerId, msgName, data)
		pass
	
	def SendMsgToAllClient(self, msgName, args):
		"""发送消息到所有客户端，仅能在服务端执行"""
		# 封装参数
		data = self.__system__.CreateEventData()
		for k, v in args.items():
			data[k] = v
		# 发消息
		self.__system__.BroadcastToAllClient(msgName, data)
		pass
	
	def SendMsgToMultiClient(self, players, msgName, args):
		"""发送消息到指定的一批客户端，仅能在服务端执行"""
		# 封装参数
		data = self.__system__.CreateEventData()
		for k, v in args.items():
			data[k] = v
		# 发消息
		self.__system__.NotifyToMultiClients(players, msgName, data)
		pass

	def BroadcastEvent(self, msgName, args):
		"""同端广播事件"""
		# 封装参数
		data = self.__system__.CreateEventData()
		for k, v in args.items():
			data[k] = v
		# 发消息
		self.__system__.BroadcastEvent(msgName, data)
		pass
	