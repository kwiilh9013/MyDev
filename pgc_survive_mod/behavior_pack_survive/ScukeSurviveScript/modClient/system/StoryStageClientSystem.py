# -*- coding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon.cfg.storyStageConfig import Config as StoryStageConfig
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3, Quaternion
from ScukeSurviveScript.modCommon.cfg.buildingPlaceConfig import GetMarkerConfig

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.defines.storyLineEnum import StoryLineEnvEnum
from ScukeSurviveScript.modCommon.storyline.storyStage import StoryStage
from ScukeSurviveScript.modCommon.storyline.storyLine import StoryLineBuilder
from ScukeSurviveScript.modClient.storyline.cameraMoving import CameraMovingLine

from ScukeSurviveScript.modCommon.cfg.cutscenesConfig import Config as CutScenesConfig

StoryLineBuilder.BindingStoryLine('cameraMoving', CameraMovingLine)

UpdateDeltaTime = 1000.0/30.0

class StoryStageClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(StoryStageClientSystem, self).__init__(namespace, systemName)
		self._buildingsInfo = []
		self._playersStoryStage = {}

		self._debugRecords = []
		self._debugBuilding = None

		self._storyPlaying = False
		self._cutsceneRequest = []
		self._pendingMissionCutscene = False

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.StoryStageServerSystem)
	def OnStartStoryStage(self, data):
		if data['playerId'] != self.mPlayerId:
			return
		self.StartStoryStage(data['playerId'], data['name'], data['data'])

	def StartStoryStage(self, playerId, name, data):
		config = StoryStageConfig.get(name, None)
		if not config:
			return
		stage = StoryStage(self, playerId, name, config, data, StoryLineEnvEnum.Client)
		self._playersStoryStage[playerId] = stage
		self._storyPlaying = True

	def Update(self):
		players = self._playersStoryStage.keys()
		total = 0
		for playerId in players:
			stage = self._playersStoryStage[playerId]
			stage.UpdateStage(UpdateDeltaTime)
			if stage.Completed:
				del self._playersStoryStage[playerId]
			else:
				total += 1
		self._storyPlaying = total > 0
		if not self._storyPlaying:
			openCutscene = False
			while len(self._cutsceneRequest) > 0:
				Instance.mUIManager.PushCutscene(self._cutsceneRequest.pop(0))
				openCutscene = True
			if openCutscene:
				Instance.mUIManager.SetCutsceneCompletedCallback(self.OnCutsceneEnd)

	def GetBuildingInfo(self, playerId, identifier, filter):
		buildings = []
		for building in self._buildingsInfo:
			if building['identifier'] == identifier:
				buildings.append(building)
		ret = None
		if len(buildings) > 0:
			ret = buildings[0]
		if filter == 'closest':
			pos = engineApiGac.GetEntityPos(playerId)
			if pos:
				minDis = -1
				for building in buildings:
					dis = MathUtils.TupleLength(MathUtils.TupleSub(building['pos'], pos))
					if minDis < 0 or dis < minDis:
						minDis = dis
						ret = building
		return ret

	def _GetClosestBuilding(self):
		buildings = self._buildingsInfo
		ret = None
		if len(buildings) > 0:
			ret = buildings[0]
		pos = engineApiGac.GetEntityPos(self.mPlayerId)
		if pos:
			minDis = -1
			for building in buildings:
				config = GetMarkerConfig(building['identifier'])
				if config is None:
					continue
				dis = MathUtils.TupleLength(MathUtils.TupleSub(building['pos'], pos))
				if minDis < 0 or dis < minDis:
					minDis = dis
					ret = building
		return ret

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnUpdateBuildingsInfo(self, data):
		#print 'OnUpdateBuildingsInfo', data
		buildings = data['buildings']
		for building in buildings:
			self._buildingsInfo.append(building)

	@EngineEvent()
	def OnKeyPressInGame(self, args):
		if not engineApiGac.IsDevMode():
			return
		KeyBoardType = clientApi.GetMinecraftEnum().KeyBoardType
		key = int(args['key'])
		isDown = int(args['isDown']) == 1
		screenName = args['screenName']
		if screenName == "hud_screen" and isDown:
			if key == KeyBoardType.KEY_P:
				recordsPos = []
				recordsRot = []
				for record in self._debugRecords:
					recordsPos.append(record['pos'])
					recordsRot.append(record['rot'])
				print ('上一个记录的点位：\npos: %r\nrot:%r' % (recordsPos, recordsRot))
				self._debugRecords = []
				building = self._GetClosestBuilding()
				buildingName = 'None'
				buildingPos = None
				buildingRot = None
				if building:
					buildingName = building['identifier']
					buildingPos = building['pos']
					buildingRot = building['rot']
				self._debugBuilding = building
				print  '开始记录当前建筑(%s) %r %r，L键记录' % (buildingName, buildingPos, buildingRot)
			elif key == KeyBoardType.KEY_L:
				curPos = engineApiGac.GetEntityPos(self.mPlayerId)
				curRot = engineApiGac.GetRot(self.mPlayerId)
				curRot = (curRot[0], curRot[1], 0)
				markerConfig = None
				center = (0, 0, 0)
				buildingPos = (0, 0, 0)
				buildingRot = 0
				if self._debugBuilding:
					buildingPos = self._debugBuilding['pos']
					buildingRot = self._debugBuilding['rot']
					markerConfig = GetMarkerConfig(self._debugBuilding['identifier'])
				if markerConfig:
					center = markerConfig['center']
				offsetPos = MathUtils.TupleSub(curPos, buildingPos)
				offsetPos = MathUtils.RotByFace(offsetPos, -buildingRot)
				offsetPos = MathUtils.TupleAdd(offsetPos, center)
				curRotQ = Quaternion.Euler(curRot[0], curRot[1], curRot[2])
				offsetRotQ = Quaternion.AngleAxis(-buildingRot, Vector3.Up()) * curRotQ
				offsetRot = offsetRotQ.EulerAngles().ToTuple()
				record = {
					'pos': MathUtils.TupleRound(offsetPos, 1),
					'rot': MathUtils.TupleRound(offsetRot, 1)
				}
				self._debugRecords.append(record)
				print ('新增点位：pos:%r, rot:%r' % (record['pos'], record['rot']))

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BuildingServerSystem)
	def OnShelterBorn(self, data):
		print 'OnShelterBorn', data
		self._InShelterHideUI()
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene00'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene01'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene02'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene03'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene04'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene05'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene06'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene07'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene08'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene09'])
		Instance.mUIManager.PushCutscene(CutScenesConfig['Cutscene10'])
		Instance.mUIManager.SetCutsceneCompletedCallback(self.ShowAnnounce)

	def _InShelterHideUI(self):
		hudUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
		if hudUI:
			hudUI.CloseNotifyPanel()  # 关闭倒计时
			hudUI.FlashMenu()

	def ShowAnnounce(self):
		ui = Instance.mUIManager.GetUI(UIDef.UI_SurviveTips)
		if ui:
			ui.ShowAnnounce([
				{'offset': 1.0, 'fadein': 2, 'keep': 2, 'fadeout': 1},
				{'offset': 7.0, 'fadein': 2, 'keep': 2, 'fadeout': 1},
				{'offset': 13.0, 'fadein': 2, 'keep': 2, 'fadeout': 1},
			])

	def _SetHudActive(self, active):
		hudUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
		if hudUI:
			hudUI.SetHudActive(active)


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnJumpToNextPhase(self, data):
		missionId = data['taskId']
		self._pendingMissionCutscene = True
		self._SetHudActive(False)
		self._cutsceneRequest.append(CutScenesConfig['MissionSuccess%s' % missionId])

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.TaskServerSystem)
	def OnEscapeFailed(self, data):
		missionId = data['taskId']
		self._pendingMissionCutscene = True
		self._SetHudActive(False)
		self._cutsceneRequest.append(CutScenesConfig['MissionFailed%s' % missionId])

	def OnCutsceneEnd(self):
		if self._pendingMissionCutscene:
			self._SetHudActive(False)
			self._SetHudActive(True)
			phaseClientSystem = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.PhaseClientSystem)
			if phaseClientSystem:
				phaseInfo = phaseClientSystem.PhaseInfo
				engineApiGac.AddTimer(0.2, self._DelayPhaseInfoUpdate, phaseInfo)
			self._pendingMissionCutscene = False

	def _DelayPhaseInfoUpdate(self, phaseInfo):
		hudUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
		if hudUI:
			hudUI.OnUpdatePhaseInfo(phaseInfo)
