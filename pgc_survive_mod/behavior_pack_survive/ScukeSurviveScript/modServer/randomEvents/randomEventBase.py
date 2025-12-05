# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.server import engineApiGas
compFactory = serverApi.GetEngineCompFactory()


class RandomEventBase(CommonEventRegister):
	"""随机事件基类"""

	_mutexEvents = None
	"""互斥事件列表"""

	def __init__(self, system, eventType, targetId):
		CommonEventRegister.__init__(self, system)
		self.mSystem = system
		"""随机事件系统"""
		self.mEventType = eventType
		"""事件类型"""
		self.mTargetId = targetId
		"""事件目标id"""
		self.mDimension = engineApiGas.GetEntityDimensionId(targetId)
		"""所在维度"""
		self.mRunning = False
		"""是否正在运行"""

		# 组件
		self._posComp = None
		self._rotComp = None
		
		# 启动update
		self.mTick = 0
		self._updateTimer = None
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		if self._updateTimer:
			engineApiGas.CancelTimer(self._updateTimer)
			self._updateTimer = None
		if self.mRunning:
			self.End()
		self.mSystem = None
		del self
		pass

	@classmethod
	def GetMutexEvents(cls):
		"""获取互斥事件列表, 返回值为事件type"""
		if cls._mutexEvents is None:
			cls._mutexEvents = []
		# 子类重写：读取config，获取cfg的数据，并缓存下来
		return cls._mutexEvents

	def Start(self):
		"""开始事件"""
		self.mRunning = True
		# 启动update
		self._updateTimer = engineApiGas.AddRepeatTimer(0.1, self.Update)
		# 由子类重写
		pass

	def Update(self):
		"""更新事件, 1秒10帧"""
		self.mTick += 1
		# 由子类重写，并实现调用End逻辑
		pass

	def End(self):
		"""事件结束"""
		if self.mRunning:
			self.mRunning = False
			self.mSystem.CancelEvent(self.mTargetId)
		pass

	def IsRunning(self):
		"""是否正在运行"""
		return self.mRunning
	
	def IsUniqueness(self):
		""""是否是唯一事件(其他玩家不会重复创建)"""
		return False
	
	def GetUpdateTime(self, tick=None):
		"""获取update更新的时间, 单位秒"""
		if tick is None:
			tick = self.mTick
		return tick * 0.1
	
	def GetTickTime(self, t):
		"""将秒转换为tick, 1秒=10tick"""
		return t * 10

	def GetTargetPos(self):
		if self._posComp is None:
			self._posComp = compFactory.CreatePos(self.mTargetId)
		return self._posComp.GetPos()

	def GetTargetRot(self):
		if self._rotComp is None:
			self._rotComp = compFactory.CreateRot(self.mTargetId)
		return self._rotComp.GetRot()