# -*- coding: utf-8 -*-
from Preset.Model.PartBase import PartBase


class PlayerWrapper(PartBase):

	def SetPlayerPosSafe(self, playerId, pos):
		health = self.GetEntityAttrValue(playerId, self.GetMinecraftEnum().AttrType.HEALTH)
		if health == 0:
			return
		player = PartBase.GetPlayerObject(self, playerId)
		player and player.SetPos(pos)

	def SetPlayerRotSafe(self, playerId, rot):
		health = self.GetEntityAttrValue(playerId, self.GetMinecraftEnum().AttrType.HEALTH)
		if health == 0:
			return
		player = PartBase.GetPlayerObject(self, playerId)
		player and player.SetRot((0,rot))