# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.blocks.blockBase import BlockBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg import molangConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BlockTrap(BlockBase):
	"""捕兽夹逻辑类"""
	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		super(BlockTrap, self).__init__(severHandler, playerId, blockName, pos, dimension, param)

		# 咬住的实体id
		self._biteEntityId = None
		# 禁锢的坐标（方块中间稍微高一点）
		self._bitePos = (
			self.mPos[0] + (0.5 if self.mPos[0] > 0 else -0.5), 
			self.mPos[1] + 0.15, 
			self.mPos[2] + (0.5 if self.mPos[0] > 0 else -0.5)
		)
		self._biteTimer = None
		self._biteTotalTime = 0

		self._biteTickCD = self.mCfg.get("tick_cd", 0.2)
		pass

	def Destroy(self, remove=False):
		if self._biteTimer:
			engineApiGas.CancelTimer(self._biteTimer)
		super(BlockTrap, self).Destroy(remove)
		pass
	
	# region 事件
	@EngineEvent()
	def StepOnBlockServerEvent(self, args):
		"""实体移动到实心方块事件"""
		entityId = args.get("entityId")
		# 对摆放的玩家不造成伤害
		if entityId != self.mPlayerId and self._biteEntityId is None:
		# if self._biteEntityId is None:
			blockName = args.get("blockName")
			if blockName == self.mBlockName:
				dimension = args.get("dimensionId")
				pos = (args.get("blockX"), args.get("blockY"), args.get("blockZ"))
				if dimension == self.mDimension and pos == self.mPos:
					# 有实体踩到方块
					self.SetBiteEntity(entityId)
		pass
	# endregion

	def SetBiteEntity(self, entityId):
		"""设置咬住实体"""
		# 判断实体是否有血量
		attrComp = compFactory.CreateAttr(entityId)
		health = attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
		if health > 0:
			if not self.IsCheck(entityId):
				return
			self._biteEntityId = entityId
			# 造成一次伤害
			hurtComp = compFactory.CreateHurt(entityId)
			hurtComp.Hurt(self.mCfg.get("damage", 1), minecraftEnum.ActorDamageCause.EntityAttack, self.mPlayerId)
			# 开启禁锢tick
			self._biteTimer = engineApiGas.AddRepeatTimer(self._biteTickCD, self.BiteTimer)
			# 播放动画
			info = {
				"stage": "set_block",
				"pos": self.mPos,
				"dimension": self.mDimension,
				"molangValue": {molangConfig.VariableEnum.WorkingState: 1.0},
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass

	def BiteTimer(self):
		"""咬住实体的tick"""
		if self._biteEntityId:
			# tp坐标为方块坐标
			posComp = compFactory.CreatePos(self._biteEntityId)
			posComp.SetFootPos(self._bitePos)
			# 累计时长
			self._biteTotalTime += self._biteTickCD
			if self._biteTotalTime >= self.mCfg.get("bite_time", 3):
				# 禁锢结束
				self._biteEntityId = None
				engineApiGas.CancelTimer(self._biteTimer)
				self._biteTimer = None
				# 破坏方块
				engineApiGas.SetBlockNew(self.mPos, itemsConfig.AirBlockDict, dimensionId=self.mDimension)
		pass
