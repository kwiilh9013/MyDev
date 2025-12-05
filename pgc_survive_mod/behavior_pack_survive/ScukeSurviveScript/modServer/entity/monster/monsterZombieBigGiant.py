# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.modServer.entity.entityBase import EntityBase
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()
EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType


class MonsterZombieBigGiant(EntityBase):
	"""巨型僵尸"""
	
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		super(MonsterZombieBigGiant, self).__init__(severHandler, entityId, engineTypeStr, param)

		self._attrComp = compFactory.CreateAttr(self.mEntityId)
		# 爆炸威力
		self._lightningRadius = 0
		self._lightningNum = 0
		self._onfireRadius = 0
		self._onfireTime = 0
		self._onfireTimer = None
		if self.mCfg:
			self._lightningNum,self._lightningRadius,self._onfireRadius,self._onfireTime = self.mCfg.get("lightning_num",1),self.mCfg.get("lightning_radius",1),self.mCfg.get("onfire_radius",17),self.mCfg.get("onfire_time",5)
		pos = engineApiGas.GetEntityPos(self.mEntityId)
		if self._lightningRadius and self._lightningRadius > 0:
			self._lightningRadius = int(self._lightningRadius)
			cmdStr = "/summon minecraft:lightning_bolt {} {} {}"
			offsetList = [
				(-3, 3), (-3, -3), (3, 3), (3, -3), 
			]
			for offset in offsetList:
				engineApiGas.SetCommand(cmdStr.format(pos[0] + offset[0], pos[1], pos[2] + offset[1]))
		dimension = serverApiMgr.GetEntityDimension(self.mEntityId)
		self._onfireTimer = engineApiGas.AddRepeatTimer(3,self.SetPlayerOnFireTimer,dimension, self.mEntityId, self._onfireRadius)
		pass

	def Destroy(self):
		self._lightningRadius = None
		self._lightningNum = None
		self._onfireRadius = None
		self._onfireTime = None
		if self._onfireTimer:
			engineApiGas.CancelTimer(self._onfireTimer)
		super(MonsterZombieBigGiant, self).Destroy()

	# region 功能
	def SetPlayerOnFireTimer(self,dimension, entityId, radius):
		entityPos = engineApiGas.GetEntityPos(entityId)
		if entityPos:
			startX = entityPos[0]-radius
			startY = entityPos[1]
			startZ = entityPos[2]-radius
			endX = entityPos[0]+radius
			endY = entityPos[1]+18+radius
			endZ = entityPos[2]+radius
			allPlayerList = serverApi.GetPlayerList()
			for playerId in allPlayerList:
				if serverApiMgr.GetEntityDimension(playerId) == dimension:
					playerPos = engineApiGas.GetEntityPos(playerId)
					if startX<=playerPos[0]<=endX and startY<=playerPos[1]<=endY and startZ<= playerPos[2]<=endZ:
						compFactory.CreateAttr(playerId).SetEntityOnFire(self._onfireTime, 1)
						engineApiGas.AddEffectToEntity(playerId,'scuke_survive:effect_player_burn',self._onfireTime,0,True)
						engineApiGas.SetCommand("/particle scuke_survive:zombie_big_giant_water_vapor_onfire "+str(playerPos[0])+' ~ '+str(playerPos[2]))
	# endregion