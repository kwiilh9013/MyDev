# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Inf
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.entity.component.componentBase import ComponentBase
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityBase(CommonEventRegister):
	"""实体基类"""
	def __init__(self, server, entityId, engineTyteStr, config=None):
		CommonEventRegister.__init__(self, server)
		self.mServer = server
		"""服务端sys"""
		self.mEntityId = entityId
		"""实体id"""
		self.mEngineTypeStr = engineTyteStr
		"""实体类型"""
		self.mTick = 0
		"""当前tick, 对象创建时tick=0"""

		self.mConfig = config
		"""实体配置"""""
		self.mCheckCompCD = 2 * 30
		"""轮询行为的间隔"""

		self.mRunComp = None
		"""当前正在执行的组件"""

		self.mEventName = ""
		"""客户端消息的事件名称"""

		# 生物攻击力
		self._attackDamage = None
		# 所在维度
		self._dimension = None

		# ai组件: {key: compObj}
		self._componentDict = {}

		# 根据config进行初始化
		self.Init()

		# sdk组件
		self.mActionComp = compFactory.CreateAction(self.mEntityId)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		# 销毁组件
		for compObj in self._componentDict.itervalues():
			compObj.Destroy()
		self._componentDict = None
		self.mServer = None
		self.mConfig = None
		self.mRunComp = None
		del self
	
	# region 事件
	@EngineEvent()
	def OnScriptTickServer(self):
		if not self.mConfig:
			return
		self.mTick += 1

		self.Update()
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体移除事件"""
		if args["id"] == self.mEntityId:
			# 销毁
			self.Destroy()
		pass
	# endregion

	def Init(self):
		"""根据config初始化实体逻辑"""
		if not self.mConfig:
			return
		if "components" not in self.mConfig:
			return
		
		# 初始化组件
		for compKey, compCfg in self.mConfig["components"].iteritems():
			# 根据枚举，获得组件对象
			clazz = compCfg.get("type", ComponentBase)
			if clazz:
				obj = clazz(self, compCfg)
				self._componentDict[compKey] = obj
		pass

	def Update(self):
		"""tick方法, 1秒30帧"""
		# 轮询行为逻辑
		if self.mTick % self.mCheckCompCD == 0:
			self.CheckNextCompTick()
		
		# 运行组件
		if self.mRunComp and self.mRunComp.GetRunState():
			self.mRunComp.Update()
		pass

	def CheckNextCompTick(self):
		"""决策下一个行为逻辑"""
		# 是否有正在执行comp
		if self.mRunComp and self.mRunComp.GetRunState():
			return
		# 获取下一个comp
		nextComp = self.GetNextComponent()
		if nextComp:
			# 运行comp
			nextComp.Start()
		self.mRunComp = nextComp
		pass

	# region 需子类重写
	def GetNextComponent(self):
		"""
		获取下一个组件, 根据实际情况使用行为树 or if..else
			return: Component | None
		"""
		raise NotImplementedError("{%s} GetNextComponent not implemented" % self.__class__.__name__)

	def IsCanHit(self, targetId):
		"""是否可以对目标造成伤害, 默认不对自己造成伤害"""
		if self.mEntityId == targetId:
			return False
		return True
	# endregion

	# region api
	def SetConfig(self, config):
		"""设置实体配置"""
		self.mConfig = config

	def GetConfig(self):
		"""获取实体配置"""
		return self.mConfig
	
	def GetDimension(self):
		"""获取实体所在维度"""
		if self._dimension is None:
			self._dimension = engineApiGas.GetEntityDimensionId(self.mEntityId)
		return self._dimension
	
	def GetAttackDamage(self):
		"""获取攻击力"""
		if self._attackDamage is None:
			self._attackDamage = int(engineApiGas.GetAttrValue(self.mEntityId, minecraftEnum.AttrType.DAMAGE))
		return self._attackDamage
	
	def GetComponent(self, compEnum):
		"""获取实体组件"""
		return self._componentDict.get(compEnum)
	
	def GetAttackTargetId(self):
		"""获取仇恨目标"""
		targetId = self.mActionComp.GetAttackTarget()
		if targetId == "-1":
			return None
		return targetId
	
	def GetTargetDistanceXZ(self, targetId):
		"""获取自己与目标的xz轴距离"""
		if not targetId:
			return Inf
		tpos = engineApiGas.GetEntityPos(targetId)
		pos = engineApiGas.GetEntityPos(self.mEntityId)
		dist = commonApiMgr.GetDistanceXZSqrt(pos, tpos)
		return dist

	def SendOneMsgToAllClient(self, args):
		"""发消息到所有客户端"""
		args["entityId"] = self.mEntityId
		self.SendMsgToAllClient(self.mEventName, args)

	def SendOneMsgToClient(self, playerId, args):
		"""发消息到某个客户端"""
		args["entityId"] = self.mEntityId
		self.SendMsgToClient(playerId, self.mEventName, args)
	# endregion
