# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
import ScukeSurviveScript.modCommon.cfg.phaseConfig as PhaseConfig

ComFactory = clientApi.GetEngineCompFactory()

class PhaseClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(PhaseClientSystem, self).__init__(namespace, systemName)
		self._phaseInfo = None
		self._bloodMoon = False
		self._mobNightList = []
		self._night = False
		self._nightMatUniform1 = (0.0, 0.0, 0.0, 0.0)
		self._meteorites = []
		self._meteoritesShake = 0.0
		self._posComp = ComFactory.CreatePos(self.mPlayerId)
		self.__cameraSystem__ = None

	@property
	def _cameraSystem(self):
		if not self.__cameraSystem__:
			self.__cameraSystem__ = clientApi.GetSystem(modConfig.ModNameSpace,
														 modConfig.ClientSystemEnum.CameraClientSystem)
		return self.__cameraSystem__

	@property
	def PhaseInfo(self):
		return self._phaseInfo

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnBloodMoonUpdate(self, data):
		self._bloodMoon = data['state']
		self.SetBloodMoon(self._bloodMoon)

	@EngineEvent()
	def AppResumeFromBackgroundClientEvent(self, args):
		self.SetBloodMoon(self._bloodMoon)

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		if args['engineTypeStr'].startswith(modConfig.ModNameSpace):
			self.AddNightVisualMob(args['id'])

	@EngineEvent()
	def RemoveEntityClientEvent(self, args):
		self.RemoveNightVisualMob(args['id'])

	def Update(self):
		night = engineApiGac.GetTime() % 24000 > 13000
		if night != self._night:
			self._night = night
			self.SetNightVisual(night)
			self.ApplyNightMobVisual()

		if len(self._meteorites) > 0:
			self._meteoritesShake = 0.0
			curPos = self._posComp.GetFootPos()
			n = 0
			for eid in self._meteorites:
				pos = engineApiGac.GetEntityFootPos(eid)
				if pos:
					dis = MathUtils.TupleLength(MathUtils.TupleSub(pos, curPos))
					shaking = min(16.0 / max(1.0, dis), 1.0) * 0.5
					self._meteoritesShake += shaking
					n += 1
			if n > 0:
				self._meteoritesShake = min(self._meteoritesShake/n, 0.5)
				self._cameraSystem.SetCameraShaking(self._meteoritesShake)

	def AddNightVisualMob(self, eid):
		if eid not in self._mobNightList:
			self._mobNightList.append(eid)
			self.ApplyNightMobVisual(eid)

	def RemoveNightVisualMob(self, eid):
		if eid in self._mobNightList:
			self._mobNightList.remove(eid)

	def ApplyNightMobVisual(self, eid=None):
		if eid == None:
			for _eid in self._mobNightList:
				self.ApplyNightMobVisual(_eid)
			return
		actorRenderComp = clientApi.GetEngineCompFactory().CreateActorRender(eid)
		actorRenderComp.SetEntityExtraUniforms(1, self._nightMatUniform1)

	def SetNightVisual(self, active, emissionColor=(1.0, 1.0, 1.0), force=False):
		flag = 0.0
		if active:
			flag = 0.5
		if force:
			flag = 1.0
		self._nightMatUniform1 = (emissionColor[0], emissionColor[1], emissionColor[2], flag)

	def SetBloodMoon(self, active):
		# 设置血月视觉效果
		levelId = clientApi.GetLevelId()
		skyComp = clientApi.GetEngineCompFactory().CreateSkyRender(levelId)
		ppComp = clientApi.GetEngineCompFactory().CreatePostProcess(levelId)
		ppComp.SetEnableColorAdjustment(active)
		if active:
			skyComp.SetSkyColor((0.1, 0, 0, 1))
			ppComp.SetColorAdjustmentTint(0.4, (255, 0, 0))
			ppComp.SetColorAdjustmentBrightness(1.8)
			self.SetNightVisual(self._night, (1.0, 0.0, 0.0), True)
		else:
			skyComp.ResetSkyColor()
			self.SetNightVisual(self._night)

		self.ApplyNightMobVisual()

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnMeteoriteSapwn(self, data):
		self._meteorites.append(data['eid'])

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnMeteoriteHit(self, data):
		curPos = self._posComp.GetFootPos()
		eid = data['eid']
		pos = data['pos']
		dis = MathUtils.TupleLength(MathUtils.TupleSub(pos, curPos))
		shaking = min(32.0 / max(1.0, dis), 1.0) * 1.0
		self._cameraSystem.EmitCameraShaking(shaking, 3.0)

		if eid in self._meteorites:
			self._meteorites.remove(eid)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.PhaseServerSystem)
	def OnUpdatePhaseInfo(self, data):
		self._phaseInfo = data
		if data['days'] == PhaseConfig.EndDays:
			ui = Instance.mUIManager.GetUI(UIDef.UI_SurviveTips)
			if ui:
				ui.ShowAnnounce([
					None,
					None,
					None,
					{'offset': 0.5, 'fadein': 2, 'keep': 4, 'fadeout': 1},
				])
