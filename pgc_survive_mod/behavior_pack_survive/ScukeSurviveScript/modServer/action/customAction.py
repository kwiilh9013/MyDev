# -*- coding: utf-8 -*-


import mod.server.extraServerApi as serverApi

CustomGoalCls = serverApi.GetCustomGoalCls()
compFactory = serverApi.GetEngineCompFactory()


class CustomAction(CustomGoalCls):

	def __init__(self, entityID, argsJson):
		super(CustomAction, self).__init__(entityID, argsJson)

		self.entityId = entityID
		self.actionComp = compFactory.CreateAction(entityID)

