# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.action.customAction import CustomAction


class MobAction(CustomAction):

	def __init__(self, entityID, argsJson):
		super(MobAction, self).__init__(entityID, argsJson)

		self.mFrame = 0

	def CanUse(self):
		self.mFrame += 1
		if self.mFrame % 1000 == 0:
			return True
		return False

	def Start(self):
		print "mobAction: %s start action" % self.entityId

	def Stop(self):
		print "mobAction: %s stop action" % self.entityId
