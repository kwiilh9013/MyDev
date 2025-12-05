# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.manager.commonMgr import CommonManager
from mod_log import logger


class LobbyManagerGas(CommonManager):
	# 大厅管理器
	def __init__(self, system):
		super(LobbyManagerGas, self).__init__(system)

		self.mPlayers = {} # {playerId: playerGas}
		self.mPlayer2Pos = {}
		self.mWaitingPlayers = []
		self.mCameraPresets = {}

		self.mRedundantPlayers = []

	def OnJoin(self, player):
		logger.info("player join lobby: %s", player.GetEntityId())

		if player.GetEntityId() in self.mPlayers:
			return

		self.mPlayers[player.GetEntityId()] = player

		self._onJoin(player.GetEntityId())

	def _onJoin(self, playerId):
		"""
		服务端玩家加入/游戏结束后处理：传送到大厅位置等
		这里只做从外部进入游戏内的操作 一轮游戏结束后回到大厅的操作放到阶段内处理
		"""
		pass

	def OnLeft(self, player):
		logger.info("player left lobby: %s", player.GetEntityId())
		if player.GetEntityId() in self.mPlayers:
			del self.mPlayers[player.GetEntityId()]

		if player.GetEntityId() in self.mWaitingPlayers:
			self.mWaitingPlayers.remove(player.GetEntityId())

	def GetAllPlayers(self):
		return self.mPlayers.values()

	def HasPlayer(self, entityId):
		return entityId in self.mPlayers

	def GetPlayer(self, entityId):
		return self.mPlayers[entityId]