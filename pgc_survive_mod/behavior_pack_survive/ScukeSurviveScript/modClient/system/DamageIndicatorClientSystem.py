# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import random

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.display.mobAnimator import MobAnimatorController
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, MathUtils



class DamageIndicatorTextBoard(object):
	def __init__(self, attachedEntityId, changeValue, context):
		self.attachedEntityId = attachedEntityId
		self.changeValue = changeValue
		self.context = context
		self.tickTime = 0
		self.textBoardComp = clientApi.GetEngineCompFactory().CreateTextBoard(clientApi.GetLevelId())
		m = int(changeValue)
		text = str.format('%d' % changeValue) if changeValue - m == 0 else str.format('%.1f' % changeValue)
		self.textBoardId = self.textBoardComp.CreateTextBoardInWorld(
			text, (1, 1, 1, 1), (0, 0, 0, 0), True)
		if not self.textBoardId:
			return

		self.color = (1, 1, 1, 1)
		self.InitDisplay(context['pos'])

	def __del__(self):
		if self.textBoardId:
			self.textBoardComp.RemoveTextBoard(self.textBoardId)
		self.textBoardComp = None

	def InitDisplay(self, pos=None):
		self.color = (1, 1, 1, 1)
		self.scale = 1.5
		if self.context['isHighDamage']:
			self.color = (1, 0, 0, 1)
			self.scale = 2
		self.deltaScale = self.scale * 1.0 / 30

		if not pos:
			pos = engineApiGac.GetEntityPos(self.attachedEntityId)

		fromPos = engineApiGac.GetEntityPos(self.context['fromId'])
		if fromPos:
			v0 = Vector3(fromPos)
			v1 = Vector3(pos)
			d = (v0 - v1).Normalized()
			pos = (v1 + d).ToTuple()
			pos = tuple(a + (random.random() - 0.5) for a in pos)
		self.textBoardPos = pos
		self.textBoardComp.SetBoardPos(self.textBoardId, self.textBoardPos)
		self.textBoardComp.SetBoardScale(self.textBoardId, (self.scale, self.scale))
		self.textBoardComp.SetBoardTextColor(self.textBoardId, self.color)

	def Update(self):
		self.tickTime = self.tickTime + 1
		tempPos = self.textBoardPos
		self.textBoardPos = (tempPos[0], tempPos[1] + 0.05, tempPos[2])
		self.textBoardComp.SetBoardPos(self.textBoardId, self.textBoardPos)
		self.color = (self.color[0], self.color[1], self.color[2], 1 - self.tickTime * 0.5 / 30)
		self.textBoardComp.SetBoardTextColor(self.textBoardId, self.color)
		self.scale = self.scale + self.deltaScale
		self.textBoardComp.SetBoardScale(self.textBoardId, (self.scale, self.scale))


class DamageIndicatorClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(DamageIndicatorClientSystem, self).__init__(namespace, systemName)
		self._boardDurationMap = {}
		self._mobAnimMap = {}
		self._S_showDamage = True

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DamageServerSystem)
	def OnHealthDamage(self, data):
		if not self._S_showDamage:
			return
		fromId = data['fromId']
		fromPos = engineApiGac.GetEntityPos(fromId)
		damages = data['damages']
		for item in damages:
			targetEntityId = item['eid']
			if targetEntityId == clientApi.GetLocalPlayerId():
				continue
			damage = item['damage']
			changeValue = -damage
			if changeValue < 0:
				critical = 'critical' in item and item['critical']
				pos = None if 'pos' not in item else item['pos']
				context = {'isHighDamage': critical, 'pos': pos, 'fromId': fromId}
				textBoard = DamageIndicatorTextBoard(targetEntityId, changeValue, context)
				self._boardDurationMap[textBoard] = {'object': textBoard, 'duration': 30}
				# 自定义命中表现
				identifier = clientApi.GetEngineCompFactory().CreateEngineType(targetEntityId).GetEngineTypeStr()
				if targetEntityId in self._mobAnimMap and identifier.startswith(modConfig.ModNameSpace):
					mobAnim = self._mobAnimMap[targetEntityId]
					mobAnim.SetHurt(fromPos, MathUtils.Clamp(damage/5, 0.2, 1.2))

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DamageServerSystem)
	def OnDamageKnock(self, data):
		toEid = data['toId']
		if toEid == clientApi.GetLocalPlayerId():
			motionComp = clientApi.GetEngineCompFactory().CreateActorMotion(toEid)
			motionComp.SetMotion(data['motion'])

	# 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
	def Update(self):
		for textBoardId, textBoardInfo in self._boardDurationMap.items():
			textBoardInfo['object'].Update()
			duration = textBoardInfo['duration'] - 1
			textBoardInfo['duration'] = duration
			if duration <= 0:
				del self._boardDurationMap[textBoardId]

	def Destroy(self):
		super(DamageIndicatorClientSystem, self).Destroy()
		if len(self._boardDurationMap) > 0:
			for entityId, textBoardInfo in self._boardDurationMap.items():
				if textBoardInfo['object']:
					del textBoardInfo['object']
		self._boardDurationMap.clear()

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		identifier = args['engineTypeStr']
		id = args['id']
		comp = clientApi.GetEngineCompFactory().CreateEngineType(id)
		entityType = comp.GetEngineType()
		EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType
		if entityType & EntityTypeEnum.Mob == EntityTypeEnum.Mob:
			self._mobAnimMap[id] = MobAnimatorController(id, identifier)

	@EngineEvent()
	def RemoveEntityClientEvent(self, args):
		id = args['id']
		if id in self._mobAnimMap:
			del self._mobAnimMap[id]