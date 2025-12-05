# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modCommon import eventConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class ProjectileLogic(CommonEventRegister):
	"""抛射物类物品 逻辑对象，每个玩家一个对象"""
	def __init__(self, severHandler, playerId):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		self._playerId = playerId

		# 当前手持物品
		self._currentItemName = None

		self._posComp = compFactory.CreatePos(self._playerId)
		self._rotComp = compFactory.CreateRot(self._playerId)
		
		self._createTimer = None
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self._server = None
		if self._createTimer:
			engineApiGas.CancelTimer(self._createTimer)
			self._createTimer = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def PlayerIntendLeaveServerEvent(self, args):
		"""玩家即将退出事件"""
		playerId = args.get("playerId")
		if playerId == self._playerId:
			# 销毁
			self.Destroy()
		pass

	@EngineEvent()
	def ItemReleaseUsingServerEvent(self, args):
		"""蓄力 释放正在使用物品事件"""
		#  如要修改物品数据，需延迟处理
		playerId = args.get("playerId")
		if playerId == self._playerId:
			itemDict = args.get("itemDict")
			if itemDict:
				self.CreateProjectile(itemDict)
		pass

	@EngineEvent()
	def ItemUseAfterServerEvent(self, args):
		"""右键/长按 使用物品事件"""
		# playerId = args.get("entityId")
		# if playerId == self._playerId:
		# 	itemDict = args.get("itemDict")
		# 	if itemDict:
		# 		self.CreateProjectile(itemDict)
		pass

	@EngineEvent()
	def OnCarriedNewItemChangedServerEvent(self, args):
		"""玩家主手物品改变事件"""
		playerId = args.get("playerId")
		if playerId == self._playerId:
			newItemDict = args.get("newItemDict")
			itemName = None
			if newItemDict:
				itemName = newItemDict.get("newItemName")

			# 如果切换到新的物品，则打断之前的逻辑
			if self._currentItemName != itemName:
				if self._createTimer:
					engineApiGas.CancelTimer(self._createTimer)
					self._createTimer = None

			self._currentItemName = itemName
		pass
	# endregion

	# region 逻辑入口
	def CreateProjectile(self, itemDict):
		"""创建抛射物实体"""
		# 如果当前有延迟timer，则不再执行新的
		if self._createTimer:
			return
		
		itemName = itemDict.get("newItemName")
		cfg = itemsConfig.GetProjectileConfig(itemName)
		if cfg and cfg.get("projectile_str"):
			# 创建抛射物
			if cfg.get("delay_create"):
				# 延迟创建
				self._createTimer = engineApiGas.AddTimer(cfg["delay_create"], self.DelayCreateProjectileTimer, itemName, cfg)
			else:
				self.DelayCreateProjectileTimer(itemName, cfg)
			# 客户端执行逻辑
			if cfg.get("use_anim_cfg"):
				info = {
					"playerId": self._playerId,
					"stage": "use_projectile",
					"itemName": itemName,
				}
				self.SendMsgToAllClient(eventConfig.ItemUsedEvent, info)
		pass

	def DelayCreateProjectileTimer(self, itemName, cfg):
		"""延迟创建抛射物"""
		self._createTimer = None
		# 如果当前物品不一样，则停止逻辑
		if self._currentItemName != itemName:
			return
		
		# 创建抛射物
		pos = self._posComp.GetPos()
		rot = self._rotComp.GetRot()
		# 为了生成时不会挡视野，生成位置需往下偏移一点
		if cfg.get("height_offset"):
			pos = (pos[0], pos[1] + cfg["height_offset"], pos[2])
		if cfg.get("rot_offset"):
			rot = (rot[0] + cfg["rot_offset"], rot[1])
		projectileId = serverApiMgr.SpawnProjectile(self._playerId, cfg["projectile_str"], pos, rot, power=cfg.get("power"), gravity=cfg.get("gravity"))
		if projectileId:
			# 扣除物品数量
			if cfg.get("deduct_item_count"):
				serverApiMgr.DeductItemCount(self._playerId, itemName, cfg["deduct_item_count"], minecraftEnum.ItemPosType.CARRIED)
		pass
	# endregion
