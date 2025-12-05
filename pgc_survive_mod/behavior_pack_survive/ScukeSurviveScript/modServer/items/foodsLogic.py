# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.modCommon.cfg.debuffConfig import debuffs
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class FoodsLogic(CommonEventRegister):
	"""食物类物品 逻辑对象，每个玩家一个对象"""
	def __init__(self, severHandler, playerId):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		self._playerId = playerId
		
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self._server = None
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
	def PlayerEatFoodServerEvent(self, args):
		#吃下抗生素后清除现在已经存在的原版debuff
		"""吃下食物事件"""
		playerId = args.get("playerId")
		if playerId == self._playerId:
			itemDict = args.get("itemDict")
			if itemDict['newItemName'] == 'scuke_survive:food_antibiotic':
				effectList = compFactory.CreateEffect(playerId).GetAllEffects()
				if effectList:
					for effect in effectList:
						effectName = effect['effectName']
						if effectName in debuffs:
							compFactory.CreateEffect(playerId).RemoveEffectFromEntity(effectName)

			# 如果是指定的食物，则触发相关的逻辑
			# 读取config，根据config调用方法，执行逻辑
		pass
	# endregion

	# region 逻辑入口
	'''抗生素免疫原版debuff逻辑'''
	@EngineEvent()
	def WillAddEffectServerEvent(self,args):
		entityId,effectName = args.get("entityId"),args.get("effectName")
		if entityId == self._playerId:
			playerEffectName = "scuke_survive:effect_debuff_immunity"
			if compFactory.CreateEffect(entityId).HasEffect(playerEffectName) and effectName in debuffs:
				args['cancel']=True

	# endregion
