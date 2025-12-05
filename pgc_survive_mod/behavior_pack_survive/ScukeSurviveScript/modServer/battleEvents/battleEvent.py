# -*- coding: utf-8 -*-
import time

from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modCommon.storyline.posTransformer import PosTransformer
from ScukeSurviveScript.modServer.battleEvents.battlePhase import BattlePhaseBuilder


class BattleEvent(object):
	def __init__(self, eventHandler, playerId, config, data):
		self._eventHandler = eventHandler
		self._index = -1
		self._battlePhases = []
		self._data = data
		self._players = [playerId]
		self._outRangeTime = 0
		self._name = config.get('name', '')
		self._display = config.get('display', '')
		self._startTime = 0
		self._duration = config.get('duration', -1)
		self._timeSeconds = -1
		posTransConfig = config.get('posTransformer', None)
		posTransformer = None
		if posTransConfig:
			posTransformer = PosTransformer(eventHandler, playerId, posTransConfig)
		self._posTransformer = posTransformer
		# 有位置配置则使用配置进行变换，否则默认使用玩家位置
		if 'pos' in config:
			self._center = config['pos']
			if posTransformer:
				self._center = posTransformer.GetPos(self._center)
		else:
			self._center = engineApiGas.GetEntityFootPos(playerId)
		self._range = config.get('range', (32, 128, 32))
		self._outRangeDuration = config.get('outRangeDuration', 5.0)
		phasesConfig = config.get('phases', None)
		if phasesConfig:
			for phase in phasesConfig:
				battlePhase = BattlePhaseBuilder.GetBattlePhase(self, phase, data)
				if battlePhase is not None:
					self._battlePhases.append(battlePhase)
		for battlePhase in self._battlePhases:
			battlePhase.SetPosTransformer(posTransformer)


	@property
	def EventHandler(self):
		return self._eventHandler

	@property
	def Center(self):
		return self._center

	def Start(self):
		self._index = 0

		self.OnStart()

	def End(self):
		self.OnEnd()

	# def Join(self, pid):
	# 	if pid not in self._players:
	# 		self._players.append(pid)
	#
	# def Leave(self, pid):
	# 	pass

	def Update(self):
		ret = self.Check()
		if ret:
			ret = self.OnUpdate()
		seconds = int(time.time() - self._startTime)
		if seconds != self._timeSeconds:
			self.NotifyBattleEventInfo()
			self._timeSeconds = seconds
		if not ret:
			self.OnEnd()

	def Check(self):
		inRangePlayer = 0
		bCenter = self._center
		bRange = self._range
		for pid in self._players:
			pos = engineApiGas.GetEntityFootPos(pid)
			if pos is not None:
				delta = MathUtils.TupleSub(pos, bCenter)
				if abs(delta[0]) >= bRange[0] or abs(delta[1]) >= bRange[1] or abs(delta[2]) >= bRange[2]:
					continue
				inRangePlayer += 1
		if inRangePlayer <= 0:
			if self._outRangeTime <= 0:
				self._outRangeTime = time.time()
		else:
			self._outRangeTime = 0
		if self._outRangeTime > 0 and time.time() - self._outRangeTime >= self._outRangeDuration:
			if 0 <= self._index < len(self._battlePhases):
				phase = self._battlePhases[self._index]
				phase.OnOutRange()
		return True


	@property
	def State(self):
		pass

	def SetState(self, states):
		pass

	def OnStart(self):
		self._eventHandler.BroadcastToAllClient('OnAddBattleAreaDisplay', {
			'display': self._display,
			'pos': self._center
		})
		self._startTime = time.time()
		self.Update()  # 立刻update一次

	# def OnJoin(self, pid):
	# 	pass

	def OnUpdate(self):
		ret = True
		curIndex = self._index
		while 0 <= curIndex < len(self._battlePhases):
			phase = self._battlePhases[curIndex]
			phase.OnUpdate()
			if phase.Completed():
				phase.OnEnd()
				self.Next()
			if curIndex == self._index:
				break
			curIndex = self._index
		return ret

	def OnEnd(self):
		self._index = -2
		self._eventHandler.BroadcastToAllClient('OnRemoveBattleAreaDisplay', {
			'display': self._display
		})
		self.NotifyBattleEventInfo()


	def Next(self):
		self._index += 1
		if self._index >= len(self._battlePhases):
			self.OnEnd()

	@property
	def Ended(self):
		return self._index == -2

	@property
	def Players(self):
		return self._players

	@property
	def Name(self):
		return self._name

	def NotifyBattleEventInfo(self):
		data = {
			'name': self._name,
			'duration': self._duration,
			'passedTime': time.time() - self._startTime,
			'phaseIndex': self._index,
			'players': self._players,
			'data': self._data,
		}
		if 0 <= self._index < len(self._battlePhases):
			phase = self._battlePhases[self._index]
			data['phaseInfo'] = phase.State
		if self._outRangeTime > 0:
			data['outRange'] = time.time()-self._outRangeTime
			data['outRangeDuration'] = self._outRangeDuration
		self._eventHandler.BroadcastToAllClient('OnBattleEventInfo', data)
