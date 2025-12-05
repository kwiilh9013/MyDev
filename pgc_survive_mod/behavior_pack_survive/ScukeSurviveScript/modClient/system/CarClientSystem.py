# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.modClient.car.baseCar import BaseCar
from ScukeSurviveScript.modCommon import modConfig
compFactory = clientApi.GetEngineCompFactory()


class CarClientSystem(BaseClientSystem):
	"""载具 客户端"""
	def __init__(self, namespace, systemName):
		super(CarClientSystem, self).__init__(namespace, systemName)
		
		# 载具对象
		self._baseCar = BaseCar(self)

		# engineType缓存（如果频繁获取会卡）
		self._engineTypeStrCache = {}
		
		pass

	def Destroy(self):
		super(CarClientSystem, self).Destroy()
		if self._baseCar:
			self._baseCar.Destroy()
		self._baseCar = None
		self._engineTypeStrCache.clear()
		pass
	
	# region 事件
	@EngineEvent()
	def EntityStopRidingEvent(self, args):
		"""停止骑乘事件"""
		playerId = args.get("id")
		# 本地玩家
		if playerId == self.mPlayerId:
			# 下骑
			if self._baseCar:
				self._baseCar.StopRiding()
		pass

	@EngineEvent()
	def RemoveEntityClientEvent(self, args):
		"""实体被移除事件"""
		entityId = args.get("id")
		if self._baseCar and entityId == self._baseCar.GetRideId():
			# 下骑
			self._baseCar.StopRiding()
		# 清除缓存
		self.ClearEngineTypeStrCache(entityId)
		pass
	
	@EngineEvent()
	def UiInitFinished(self, args):
		# 给玩家自己添加动画
		self.SetPlayerRideAnim(self.mPlayerId)
		pass

	@EngineEvent()
	def AddPlayerCreatedClientEvent(self, args):
		"""添加玩家事件"""
		playerId = args.get("playerId")
		# 给玩家添加动画
		self.SetPlayerRideAnim(playerId)
		pass

	# @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.CarServerSystem)
	# def CarCtrlEvent(self, args):
	# 	"""载具控制事件"""
	# 	stage = args.get("stage")
	# 	if stage == "rider_anim":
	# 		# 乘客动画逻辑
	# 	pass
	# endregion

	# region 功能
	def GetEngineTypeStr(self, entityId):
		"""获取实体engineTypeStr，缓存"""
		engineTypeStr = self._engineTypeStrCache.get(entityId)
		if engineTypeStr is None:
			engineComp = compFactory.CreateEngineType(entityId)
			engineTypeStr = engineComp.GetEngineTypeStr()
			self._engineTypeStrCache[entityId] = engineTypeStr
		return engineTypeStr

	def ClearEngineTypeStrCache(self, entityId):
		"""清除engineTypeStr缓存"""
		self._engineTypeStrCache.pop(entityId, None)

	def SetPlayerRideAnim(self, playerId):
		"""设置玩家骑乘动画"""
		renderComp = compFactory.CreateActorRender(playerId)
		renderComp.AddPlayerAnimation("scuke_car_ride_anim", "animation.scuke_survive_car_actor.ride")
		renderComp.AddPlayerAnimationIntoState("root", "third_person", "scuke_car_ride_anim", "query.is_riding")
		renderComp.RebuildPlayerRender()
		pass
	# endregion

	# region 属性
	# endregion
