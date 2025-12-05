# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.modServer.blocks.blockBase import BlockBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.cfg.items import itemsConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BlockBarricade(BlockBase):
	"""阻拦伤害方块逻辑类：拒马、铁丝网等"""
	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		super(BlockBarricade, self).__init__(severHandler, playerId, blockName, pos, dimension, param)

		self._damage = self.mCfg.get("damage")
		if self._damage:
			self._damage = int(self._damage)

		# 伤害CD
		self._damageCD = self.mCfg.get("damage_cd", 0.5)
		# 伤害cd数据: {entityId: time}
		self._hurtCDDict = {}
		
		self._blockEntityComp = compFactory.CreateBlockEntityData(self.mLevelId)
		pass

	def Destroy(self, remove=False):
		self._hurtCDDict.clear()
		super(BlockBarricade, self).Destroy(remove)
		pass
	
	# region 事件
	@EngineEvent()
	def OnEntityInsideBlockServerEvent(self, args):
		"""实体在方块内事件"""
		if self._damage:
			entityId = args.get("entityId")
			# 对摆放的玩家不造成伤害
			if entityId != self.mPlayerId:
				blockName = args.get("blockName")
				if blockName == self.mBlockName:
					pos = (args.get("blockX"), args.get("blockY"), args.get("blockZ"))
					if pos == self.mPos:
						dimension = engineApiGas.GetEntityDimensionId(entityId)
						if dimension == self.mDimension:
							# 有实体触碰到方块
							self.SetHurtToEntity(entityId)
		pass

	def SetHurtToEntity(self, entityId):
		"""设置对实体造成伤害"""
		if not self.IsCheck(entityId):
			return
		# 判断CD
		t = time.time()
		if t - self._hurtCDDict.get(entityId, 0) >= self._damageCD:
			attrComp = compFactory.CreateAttr(entityId)
			health = attrComp.GetAttrValue(minecraftEnum.AttrType.HEALTH)
			if health > 0:
				hurtComp = compFactory.CreateHurt(entityId)
				hurtComp.Hurt(self._damage, minecraftEnum.ActorDamageCause.EntityAttack, self.mPlayerId)
				# 扣除耐久
				self.DeductDurability(1)
				# 记录cd
				self._hurtCDDict[entityId] = t
		pass

	def DeductDurability(self, durability):
		"""扣除耐久"""
		blockData = self._blockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
		if blockData:
			data = blockData[itemsConfig.BlockEntityDataKey]
			if data is None:
				data = {}
			curDurability = data.get("durability")
			if not curDurability:
				curDurability = self.mCfg.get("durability", 100)
			data["durability"] = curDurability - durability
			if data["durability"] <= 0:
				# 破坏方块
				engineApiGas.SetBlockNew(self.mPos, itemsConfig.AirBlockDict, dimensionId=self.mDimension)
			else:
				blockData[itemsConfig.BlockEntityDataKey] = data
		pass

