# -*- coding: utf-8 -*-
import math

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils, Vector3
from ScukeSurviveScript.modClient.display.gunAnimator import GunAnimatorController
from ScukeSurviveScript.modClient.display.weaponParticle import WeaponParticleController
from ScukeSurviveScript.modClient.display.weaponSound import WeaponSoundController
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig, eventConfig
from ScukeSurviveScript.modCommon.cfg import gunConfig as GunConfig
from ScukeSurviveScript.modCommon.cfg import weaponCommonCfg as WeaponConfig
from ScukeSurviveScript.modCommon.handler.gunHandler import GunHandler

CompFactory = clientApi.GetEngineCompFactory()

OneSecondUpdate = 30.0
UpdateTimeMs = 1000.0 / OneSecondUpdate
OverheadViewAnchor = (-0.8, 0, 0)
OverheadViewAnchorDis = MathUtils.TupleLength(OverheadViewAnchor)
OverheadViewOffset = (0, 0.3, -2)
OverheadViewResetDelay = 0.1
OverheadViewCheckPoint = [
	(1, 0.2, 0),
	(-1, 0.2, 0),
	(0, 0.2, 1),
	(0, 0.2, -1),
	(1, 0.2, 1),
	(-1, 0.2, -1),
	(-1, 0.2, 1),
	(1, 0.2, -1),
]
AssistedAimSensitive = 1.0
AssistedAimSensitiveRange = (0.3, 1.0)
AssistedAimDetectRadius = 64  # 辅助瞄准目标范围
AssistedAimVelocity = 40/1000.0  # 辅助瞄准转向速度
AssistedAimRadiusK = 1.5  # 辅助瞄准目标半径系数
AssistedAimRadiusYK = 1.2  # 辅助瞄准目标半径Y系数
AssistedAimRadiusAddonBeginDis = 5  # 辅助瞄准目标半径放大开始距离
AssistedAimRadiusAddonByDis = 0.1  # 辅助瞄准目标半径随距离放大系数
AssistedAimRadiusAddonMax = 3  # 辅助瞄准目标半径放大最大值
AssistedAimPassBlock = [
	'minecraft:glass'
]
IgnoreTargets = [
	'minecraft:item'
]


class GunClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(GunClientSystem, self).__init__(namespace, systemName)
		self._isReady = False
		self._time = 0
		self._tickFrame = 0
		# TODO make it be a manager
		self._weaponDisplayMap = {}
		self._weaponHandler = None
		self._crossHairControl = None

		self._needKeyDown = False
		self._needKeyUp = False
		self._needZoomIn = False
		self._needZoomOut = False

		self._walking = False
		self._sprinting = False

		self._playerCamComp = None
		self._playerViewComp = None
		self._viewResetTimer = None
		self._viewPersp = 0
		self._cameraRot = (0, 0, 0)
		self._curAnchor = (0, 0, 0)

		self._blockComp = CompFactory.CreateBlockInfo(self.mLevelId)
		self._gameComp = CompFactory.CreateGame(self.mLevelId)
		self._queryVariableComp = CompFactory.CreateQueryVariable(self.mPlayerId)

		Instance.mEventMgr.RegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameTick)

		self._S_infiniteClip = False

		self._aimRoundEntities = []

		self._keyState = {
			'shoot': False,
			'zoom': False,
			'reload': False,
		}
		self._initBtn = False
		self._defaultBtnData = {}

		self._loadedEntity = {}
		self._waitingOp = []

	def Add(self, eid, identifier, config):
		displayConfig = config['display']
		self._weaponDisplayMap[eid] = {
			'eid': eid,
			'identifier': identifier,
			'config': displayConfig,
			'weaponConfig': config,
		}

	def Get(self, eid):
		if eid in self._weaponDisplayMap:
			return self._weaponDisplayMap[eid]
		return None

	def Remove(self, eid):
		ret = None
		if eid in self._weaponDisplayMap:
			ret = self._weaponDisplayMap[eid]
			del self._weaponDisplayMap[eid]
		return ret

	@EngineEvent()
	def UiInitFinished(self, args):
		self._isReady = True
		eid = clientApi.GetLocalPlayerId()
		self._loadedEntity[eid] = True
		if self.Get(eid):
			self.SetGunDisplay(eid)
		gunHud = Instance.mUIManager.GetUI(UIDef.UI_SurviveHud)
		gunHud._hasSet = False
		settingClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
		posData = settingClient._settingDict['gunBtnData']
		def _wait():
			Instance.mEventMgr.NotifyEvent(eventConfig.SettingDataSubscribtEvent, {"stage": "gun", "posData": posData})
		engineApiGac.AddTimer(0.3, _wait)

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		eid = args['id']
		self._loadedEntity[eid] = True

	@EngineEvent()
	def RemoveEntityClientEvent(self, args):
		eid = args['id']
		if eid in self._loadedEntity:
			self._loadedEntity.pop(eid)

	@EngineEvent()
	def AddPlayerCreatedClientEvent(self, args):
		eid = args['playerId']
		self._loadedEntity[eid] = True

	@EngineEvent()
	def RemovePlayerAOIClientEvent(self, args):
		eid = args['playerId']
		if eid in self._loadedEntity:
			self._loadedEntity.pop(eid)

	@EngineEvent()
	def LeftClickBeforeClientEvent(self, args):
		eid = clientApi.GetLocalPlayerId()
		display = self.Get(eid)
		if not display:
			return
		args['cancel'] = True

		self.KeyDown()

	@EngineEvent()
	def LeftClickReleaseClientEvent(self, args):
		eid = clientApi.GetLocalPlayerId()
		display = self.Get(eid)
		if not display:
			return
		args['cancel'] = True

		self.KeyUp()

	@EngineEvent()
	def RightClickBeforeClientEvent(self, args):
		eid = clientApi.GetLocalPlayerId()
		display = self.Get(eid)
		if not display:
			return
		if self.HandleBlockUse(True):
			return
		args['cancel'] = True

		self.ZoomIn()

	@EngineEvent()
	def RightClickReleaseClientEvent(self, args):
		eid = clientApi.GetLocalPlayerId()
		display = self.Get(eid)
		if not display:
			return
		if self.HandleBlockUse(True):
			return
		args['cancel'] = True

		self.ZoomOut()

	@EngineEvent()
	def TapBeforeClientEvent(self, args):
		if self._weaponHandler:
			if self._weaponHandler.IsUsing():
				args['cancel'] = True
				return
			if self.HandleBlockUse(False):
				return
			args['cancel'] = True
			#self.Kick()

	@EngineEvent()
	def HoldBeforeClientEvent(self, args):
		if self._weaponHandler:
			if self._weaponHandler.IsUsing():
				args['cancel'] = True
				return
			if self.HandleBlockUse(False):
				return
			args['cancel'] = True
			# self.Kick()

	def HandleBlockUse(self, isClick):
		if not self._playerCamComp:
			return True
		pickDict = None
		if not isClick:
			pickDict = self._playerCamComp.GetChosen()
		else:
			pickDict = self._playerCamComp.PickFacing()
		if not pickDict or pickDict['type'] != 'Block':
			return False
		pos = (pickDict['x'], pickDict['y'], pickDict['z'])
		blockInfo = self._blockComp.GetBlock(pos)
		if not blockInfo:
			return False
		if not blockInfo[0].startswith('minecraft:') or blockInfo[0] in WeaponConfig.OperatingBlock:
			return True
		return False

	def KeyDown(self):
		self._keyState['shoot'] = True
		self._needKeyUp = False
		if not self.CheckCanUse():
			return
		if not self._weaponHandler.KeyDown(self._time):
			if not self._needKeyDown:
				self.ShowKeyDownNotValid()
			self._needKeyDown = True
			return
		self.SetKeyInputTaskWithout('shoot')
		self._needKeyDown = False
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.GunShootBegin(display)
		# To server
		self.NotifyToServer("OnGunShootBegin", {
			'playerId': eid
		})

	def ShowKeyDownNotValid(self):
		gun = self._weaponHandler
		if not gun:
			return
		if gun.Clip == 0:
			clipItem = gun.Config['clipIdentifier']
			itemCount = self.GetClipItemCount(gun.Eid, clipItem)
			if itemCount == 0:
				clipItemName = engineApiGac.GetChinese('item.%s.name' % clipItem)
				text = engineApiGac.GetChinese('scuke_survive.clip_item_not_enough.tips')
				Instance.mUIManager.ShowTips({'text': text % clipItemName, 'duration': 1.0})

	def ShowReloadNotValid(self):
		gun = self._weaponHandler
		if not gun:
			return
		clipItem = gun.Config['clipIdentifier']
		itemCount = self.GetClipItemCount(gun.Eid, clipItem)
		if itemCount == 0:
			clipItemName = engineApiGac.GetChinese('item.%s.name' % clipItem)
			text = engineApiGac.GetChinese('scuke_survive.clip_item_not_enough.tips')
			Instance.mUIManager.ShowTips({'text': text % clipItemName, 'duration': 1.0})

	def DoShootBullet(self, bullet):
		gun = self._weaponHandler
		eid = clientApi.GetLocalPlayerId()
		persp = self._viewPersp
		camera = self._playerCamComp
		dir = camera.GetForward()
		if persp == 0 or persp == 1:
			pos = MathUtils.TupleAdd(camera.GetPosition(), camera.GetCameraAnchor())
		else:
			pos = CompFactory.CreatePos(eid).GetPos()
			dir = MathUtils.TupleMul(dir, -1)
		dir = gun.DoScatter(dir)
		pos = MathUtils.TupleAddMul(pos, dir, 0.1)
		config = bullet['config']
		if config['type'] == 'projectile':
			pos = MathUtils.TupleAddMul(pos, dir, 2)
		# Display
		display = self.Get(gun.Eid)
		self.GunShootBullet(display, bullet)
		# To server
		shootInfo = {
			'playerId': gun.Eid,
			'identifier': gun.Config['identifier'],
			'position': pos,
			'direction': dir,
			'clip': gun.Clip,
			'charge': gun.ChargeInfo,
		}
		self.NotifyToServer("OnGunShootBullet", shootInfo)

	def KeyUp(self):
		self._keyState['shoot'] = False
		self._needKeyDown = False
		if not self._weaponHandler.KeyUp(self._time):
			self._needKeyUp = self._weaponHandler.IsShooting()
			return
		self.SetKeyInputTaskWithout('shoot')
		self._needKeyUp = False
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.GunShootEnd(display)
		# To server
		self.NotifyToServer("OnGunShootEnd", {
			'playerId': eid
		})

	def SwitchZoomState(self):
		if self._keyState['zoom'] is True:
			self.ZoomOut()
		else:
			self.ZoomIn()

	def ZoomIn(self):
		self._keyState['zoom'] = True
		if self._weaponHandler.IsZooming():
			return
		self._needZoomOut = False
		if not self._weaponHandler.SetZoomActive(self._time, True):
			self._needZoomIn = True
			return
		self.SetKeyInputTaskWithout('zoom')
		self._needZoomIn = False
		eid = clientApi.GetLocalPlayerId()
		# Display
		self.UpdateCrossHair(self._weaponHandler)
		display = self.Get(eid)
		self.GunZoomIn(display)
		# To server
		self.NotifyToServer("OnGunZoomIn", {
			'playerId': eid
		})

	def ZoomOut(self):
		self._keyState['zoom'] = False
		if not self._weaponHandler.IsZooming():
			return
		self._needZoomIn = False
		if not self._weaponHandler.SetZoomActive(self._time, False):
			self._needZoomOut = True
			return
		self.SetKeyInputTaskWithout('zoom')
		self._needZoomOut = False
		eid = clientApi.GetLocalPlayerId()
		# Display
		self.UpdateCrossHair(self._weaponHandler)
		display = self.Get(eid)
		self.GunZoomOut(display)
		# To server
		self.NotifyToServer("OnGunZoomOut", {
			'playerId': eid
		})

	def Reload(self, auto=False):
		if self._weaponHandler.IsShooting and auto:
			self.KeyUp()
		self.ClearKeyInputTask()
		if not self._weaponHandler.Reload(self._time):
			if not auto:
				self.ShowReloadNotValid()
			return
		self.SetKeyInputTaskWithout('reload')
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.GunReload(display)
		# To server
		self.NotifyToServer("OnGunReloadBegin", {
			'playerId': eid,
			'clip': self._weaponHandler.Clip,
		})

	def ReloadEnd(self):
		eid = clientApi.GetLocalPlayerId()
		self.NotifyToServer("OnGunReloadEnd", {
			'playerId': eid,
			'clip': self._weaponHandler.Clip,
		})

	def DoKickAttack(self):
		eid = clientApi.GetLocalPlayerId()
		pos = CompFactory.CreatePos(eid).GetPos()
		dir = self._playerCamComp.GetForward()
		if self._viewPersp == 2:
			dir = MathUtils.TupleMul(dir, -1)
		elif self._viewPersp == 1:
			comp = CompFactory.CreateRot(eid)
			camRot = self._playerCamComp.GetCameraRotation()
			rot = comp.GetRot()
			dir = clientApi.GetDirFromRot((camRot[0], rot[1]))
		self.NotifyToServer("OnGunKickAttack", {
			'playerId': eid,
			'position': pos,
			'direction': dir,
		})

	def Kick(self):
		if not self.CheckCanUse():
			return
		if not self._weaponHandler.Kick(self._time):
			return
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.GunKick(display)
		# To server
		self.NotifyToServer("OnGunKick", {
			'playerId': eid,
		})

	def DoWalking(self, state):
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.GunWalking(display, state)
		# To server
		self.NotifyToServer("OnGunWalking", {
			'playerId': eid,
			'state': state,
		})

	def DoSprinting(self, state):
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.GunSprinting(display, state)
		# To server
		self.NotifyToServer("OnGunSprinting", {
			'playerId': eid,
			'state': state,
		})

	def DoKeyInputTask(self):
		if self._needZoomIn:
			self.ZoomIn()
		if self._needZoomOut:
			self.ZoomOut()
		if self._needKeyDown:
			self.KeyDown()
		if self._needKeyUp:
			self.KeyUp()

	def ClearKeyInputTask(self):
		self._needKeyDown = False
		self._needKeyUp = False
		self._needZoomIn = False
		self._needZoomOut = False

	def SetKeyInputTaskWithout(self, keyState):
		if keyState != 'shoot':
			self._needKeyDown = self._keyState['shoot']
		if keyState != 'zoom':
			self._needZoomIn = self._keyState['zoom']

	def ClearKeyState(self):
		for k in self._keyState.keys():
			self._keyState[k] = False

	def GetKeyState(self, key):
		return self._keyState[key]

	def GetZoomState(self):
		if self._weaponHandler:
			return self._weaponHandler.IsZooming()
		return False

	def CheckValidOp(self, eid):
		if eid not in self._loadedEntity:
			return False
		return self._isReady

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnTakeGun(self, data):
		playerId = data['playerId']
		if not self.CheckValidOp(playerId):
			data['__op__'] = 'take'
			self._waitingOp.append(data)
			return
		self.OnTakeGunInner(data)

	def OnTakeGunInner(self, data):
		identifier = data['identifier']
		playerId = data['playerId']
		gunClip = 0
		if 'clip' in data:
			gunClip = data['clip']
		config = GunConfig.GetConfig(identifier)
		if not config:
			return
		self.Add(playerId, identifier, config)
		if playerId == clientApi.GetLocalPlayerId():
			self._weaponHandler = GunHandler(playerId, config, self.__GetClipItemCount(playerId, config))
			self._weaponHandler.SetClip(gunClip)
			self._walking = False
			self._sprinting = False
		if self._isReady:
			self.SetGunDisplay(playerId)

	def GetClipItemCount(self, eid, clipIdentifier):
		itemComp = CompFactory.CreateItem(eid)
		allItems = itemComp.GetPlayerAllItems(clientApi.GetMinecraftEnum().ItemPosType.INVENTORY)
		totalCount = 0
		for slotPos, itemDict in enumerate(allItems):
			if itemDict and itemDict['itemName'] == clipIdentifier:
				item_count = itemDict['count']
				totalCount += item_count
		if self._S_infiniteClip and totalCount <= 0:
			totalCount = 1
		return totalCount

	def SetGunDisplay(self, playerId):
		display = self.Get(playerId)
		if not display:
			return
		id = display['identifier']
		config = display['config']
		display['playerId'] = playerId
		display['particle'] = WeaponParticleController(playerId, config['particle'])
		display['sound'] = WeaponSoundController(playerId, config['sound'])
		animator = GunAnimatorController(playerId, id, config['animator'])
		animator.SetZoomTime(config['zoomTime'])
		display['animator'] = animator
		if playerId == clientApi.GetLocalPlayerId():
			self._playerViewComp = CompFactory.CreatePlayerView(playerId)
			self._playerCamComp = CompFactory.CreateCamera(playerId)
			self.SetUIActive(True, display)
			comp = CompFactory.CreatePlayerView(clientApi.GetLevelId())
			self._crossHairControl = comp.GetToggleOption(clientApi.GetMinecraftEnum().OptionId.SPLIT_CONTROLS)
			#clientApi.SetCrossHair(not self._setting['showCrossHair']['value'])

	def RemoveGunDisplay(self, playerId, force=False):
		display = self.Get(playerId)
		if display:
			if 'animator' in display:
				display['animator'].Reset()
		if playerId == clientApi.GetLocalPlayerId():
			if self._weaponHandler:
				recoil = self._weaponHandler.GetRestoreRecoil()
				zoom = self._weaponHandler.GetRestoreZoom()
				self.UpdateCamera(recoil, zoom, True, force)
				self._curAnchor = (0, 0, 0)
				self._lastPos = None
			self.SetUIActive(False, display)
			clientApi.SetCrossHair(self._crossHairControl == 1)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnRemoveGun(self, data):
		playerId = data['playerId']
		if not self.CheckValidOp(playerId):
			data['__op__'] = 'remove'
			self._waitingOp.append(data)
			i = 0
			ignoreOp = -1
			while i < len(self._waitingOp):
				d = self._waitingOp[i]
				if d['playerId'] == playerId:
					if d['__op__'] == 'take':
						if ignoreOp >= 0:
							self._waitingOp.pop(ignoreOp)
							i -= 1
						ignoreOp = i
					elif d['__op__'] == 'remove':
						if ignoreOp >= 0:
							self._waitingOp.pop(ignoreOp)
							i -= 1
						self._waitingOp.pop(i)
						ignoreOp = -1
				i += 1
			return
		self.OnRemoveGunInner(data)

	def OnRemoveGunInner(self, data):
		identifier = data['identifier']
		playerId = data['playerId']
		self.RemoveGunDisplay(playerId, data.get('force', False))
		self.Remove(playerId)
		if playerId == clientApi.GetLocalPlayerId():
			self._weaponHandler = None
			self.ClearKeyInputTask()
			self.ClearKeyState()

	def _NeedDoDisplay(self, data):
		pid = data['playerId']
		if pid == clientApi.GetLocalPlayerId():
			return None
		return self.Get(pid)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunShootBegin(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunShootBegin(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunShootBullet(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunShootBullet(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunShootEnd(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunShootEnd(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunReloadBegin(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunReload(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunKick(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunKick(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunZoomIn(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunZoomIn(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunZoomOut(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunZoomOut(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunWalking(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunWalking(display, data['state'])

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunSprinting(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.GunSprinting(display, data['state'])

	def GunShootBegin(self, display):
		display['animator'].BeginShoot()

	def CheckRotAndSetRot(self, display, localForce=False):
		eid = display['playerId']
		comp = CompFactory.CreateRot(eid)
		lookRot = comp.GetRot()
		bodyRot = comp.GetBodyRot()
		needForceRotate = False
		if eid == clientApi.GetLocalPlayerId():
			needForceRotate = self._viewPersp == 2 or localForce
		else:
			needForceRotate = True
		if needForceRotate and abs(lookRot[1] - bodyRot) > 0.01:
			comp.SetRot(lookRot)

	def GunShootBullet(self, display, bullet=None):
		display['animator'].ShootBullet()

	def GunShootEnd(self, display):
		display['animator'].EndShoot()

	def GunZoomIn(self, display):
		display['animator'].ZoomIn()

	def GunZoomOut(self, display):
		display['animator'].ZoomOut()

	def GunReload(self, display):
		display['animator'].Reload()

	def GunKick(self, display):
		self.CheckRotAndSetRot(display, self._viewPersp == 1)
		display['animator'].Kick()

	def GunWalking(self, display, state):
		if 'animator' not in display:
			return
		display['animator'].SetWalking(state)

	def GunSprinting(self, display, state):
		if 'animator' not in display:
			return
		display['animator'].SetSprinting(state)

	def Update(self):
		dTime = UpdateTimeMs
		time = self._time + dTime
		if self._weaponHandler:
			if self._playerCamComp:
				rot = self._playerCamComp.GetCameraRotation()
				delta = MathUtils.TupleSub(rot, self._cameraRot)
				if (-delta[1]) > 0.1:
					self._weaponHandler.ResetRecoil()
			self.DoKeyInputTask()
			self.UpdateGun(self._weaponHandler, time, dTime)
			if self._tickFrame == 0:
				self.UpdateAimEntities()
			self.UpdateAssistedAim(UpdateTimeMs)
			if self._playerCamComp:
				self._cameraRot = self._playerCamComp.GetCameraRotation()
		self._tickFrame = (self._tickFrame + 1) % 10
		self._time = time

		i = 0
		while i < len(self._waitingOp):
			data = self._waitingOp[i]
			playerId = data['playerId']
			if self.CheckValidOp(playerId):
				op = data['__op__']
				if op == 'take':
					self.OnTakeGunInner(data)
				elif op == 'remove':
					self.OnRemoveGunInner(data)
				self._waitingOp.pop(i)
				continue
			i += 1

	def OnGameTick(self, tick):
		for eid in self._weaponDisplayMap:
			display = self._weaponDisplayMap[eid]
			animator = display.get('animator', None)
			if not animator:
				continue
			if eid == self.mPlayerId:
				if self._playerViewComp is None:
					continue
				persp = self._playerViewComp.GetPerspective()
				# 第三人称视角
				overheadView = persp != 0
				if overheadView:
					animator.UpdateTpFixedRot((1, 1), (-10, 15))
			else:
				animator.UpdateTpFixedRot((1, 1), (-10, 15))

	def _GetClipItemCount(self, gun):
		return self.__GetClipItemCount(gun.Eid, gun.Config)

	def __GetClipItemCount(self, eid, config):
		clipItem = config['clipIdentifier']
		return self.GetClipItemCount(eid, clipItem)

	def CheckCanUse(self):
		itemComp = CompFactory.CreateItem(self.mPlayerId)
		carried = itemComp.GetCarriedItem()
		if carried:
			if carried['durability'] <= 1:
				CompFactory.CreateCustomAudio(self.mLevelId).PlayCustomMusic('scuke_survive.gun.jammed', entityId=self.mPlayerId)
				return False
		return True

	def UpdateGun(self, gun, time, dTime):
		if gun.IsUsing() and not self.CheckCanUse():
			self.KeyUp()
		movingNotValid = gun.IsReloading() or gun.IsUsing() or gun.IsKicking() or gun.IsZoomMoving()
		sprinting = self._queryVariableComp.GetMolangValue('query.is_sprinting') > 0
		walking = self._queryVariableComp.GetMolangValue('query.ground_speed') > 1
		if sprinting:
			walking = False
		if movingNotValid:
			sprinting = False
			walking = False
		if self._walking != walking:
			self.DoWalking(walking)
		if self._sprinting != sprinting:
			self.DoSprinting(sprinting)
		self._walking = walking
		self._sprinting = sprinting

		clipItemCount = self._GetClipItemCount(gun)
		clipCountChanged = gun.SetValidClipCount(clipItemCount)
		needReload, reloadCompleted = gun.UpdateGunReload(time, dTime)
		kickAttack, kickCompleted = gun.UpdateGunKick(time, dTime)
		if kickAttack:
			self.DoKickAttack()
		gun.UpdateGunShoot(time)
		bullet = gun.UpdateGunShootBullet(time)
		shootBullet = bullet is not None
		if shootBullet:
			self.DoShootBullet(bullet)
		recoil = gun.UpdateGunRecoil(time, dTime, shootBullet)
		scatter = gun.UpdateGunScatter(time, dTime, shootBullet)
		zoom = gun.UpdateGunZoom(time, dTime)
		if needReload:
			self.Reload(True)
		if reloadCompleted:
			self.ReloadEnd()
		# Display
		self.UpdateCamera(recoil, zoom)
		if scatter != 0 or gun.IsUsing():
			self.UpdateCrossHair(gun)
		if shootBullet or reloadCompleted or clipCountChanged:
			self.UpdateClip(gun.Clip, gun.MaxClip, clipItemCount)
		if gun.IsReloading() or reloadCompleted:
			start, duration = gun.ReloadingTime
			total = duration * 1000.0 if not reloadCompleted and start > 0 else 0
			percent = 0 if total == 0 else max(0, min((time - start) / total, 1.0))
			self.UpdateReloadProgress(percent, total)


	def SetUIActive(self, active, display):
		gun = self._weaponHandler
		gunUI = Instance.mUIManager.GetUI(UIDef.UI_GunHud)
		if active:
			if gunUI:
				gunUI.OnCarryGun(display['config'])
			clipItemCount = self._GetClipItemCount(gun)
			self.UpdateReloadProgress(0, 0)
			self.UpdateClip(gun.Clip, gun.MaxClip, clipItemCount)
			self.UpdateCrossHair(gun)
			if not self._initBtn:
				self._initBtn = True
				settingClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
				posData = settingClient._settingDict['gunBtnData']
				Instance.mEventMgr.NotifyEvent(eventConfig.SettingDataSubscribtEvent, {"stage": "gun", "posData": posData})
		else:
			if gunUI:
				gunUI.OnDropGun()

	def TestCameraBlock(self, pos, camRot, anchor):
		testOffset = Vector3(anchor)
		dis = testOffset.Length()
		if dis > 0:
			testOffset = testOffset * (1 + 0.5 / dis)

		camOffset = camRot * testOffset
		camPos = MathUtils.TupleAdd(pos, camOffset.ToTuple())
		for offset in OverheadViewCheckPoint:
			camBlockCollision = self._blockComp.GetBlockCollision(
				MathUtils.TupleFloor2Int(MathUtils.TupleAdd(camPos, offset)))
			# TODO 可以直接判断名字加速
			size = MathUtils.TupleSub(camBlockCollision['max'], camBlockCollision['min'])
			sizeMax = max(size)
			if sizeMax > 0:
				return True

		return False

	# 相机表现
	def UpdateCamera(self, recoil, zoom, reset=False, rightNow=False):
		if not self._playerCamComp:
			return
		camera = self._playerCamComp
		rot = camera.GetCameraRotation()
		curRot = (rot[0] - recoil[0], rot[1] + recoil[1], 0)
		camera.SetCameraRotation(curRot)
		fov = camera.GetFov()
		deltaFov = recoil[2] - zoom
		if deltaFov != 0:
			camera.SetFov(fov + deltaFov)

		# camera and animator
		eid = clientApi.GetLocalPlayerId()
		display = self.Get(eid)
		if not display or 'animator' not in display or self._playerViewComp is None:
			return
		persp = self._playerViewComp.GetPerspective()
		animator = display['animator']
		# 第三人称越肩视角
		overheadView = persp == 1
		if reset:
			overheadView = False
		if self._viewResetTimer:
			engineApiGac.CancelTimer(self._viewResetTimer)
			self._viewResetTimer = None
		if overheadView:
			curPos = engineApiGac.GetEntityPos(eid)  # 头部坐标
			camDir = camera.GetForward()
			rot = MathUtils.LookDirection(Vector3(camDir))
			curAnchor = self._curAnchor
			camBlocked = self.TestCameraBlock(curPos, rot, curAnchor)
			if camBlocked:
				curAnchor = MathUtils.TupleMul(curAnchor, 0.5)
			else:
				extendAnchor = MathUtils.TupleMul(curAnchor, 1.1)
				anchorDis = MathUtils.TupleLength(extendAnchor)
				if anchorDis < 0.5:
					extendAnchor = MathUtils.TupleMul(OverheadViewAnchor, 0.5 / OverheadViewAnchorDis)
				if anchorDis > OverheadViewAnchorDis:
					extendAnchor = OverheadViewAnchor
				if not self.TestCameraBlock(curPos, rot, extendAnchor):
					curAnchor = extendAnchor
			#animator.SetView(1)
			camera.SetCameraOffset(OverheadViewOffset)
			offset = Vector3(curAnchor)
			anchor = (rot * offset).ToTuple()
			#camera.SetCameraAnchor(anchor)
			self.BroadcastEvent('ChangeCameraAnchor', {
				'anchor': anchor
			})
			self._curAnchor = curAnchor
			# 检测是否太近
			camPos = MathUtils.TupleAdd(camera.GetPosition(), camera.GetCameraAnchor())
			camPosDelta = MathUtils.TupleSub(camPos, curPos)
			camClose = MathUtils.TupleLength(camPosDelta) < 0.6
			#animator.SetParam('gun_view_close', 1 if camClose else 0)

		if persp != self._viewPersp or reset:
			#animator.SetView(0)
			if reset and not rightNow:
				self._viewResetTimer = engineApiGac.AddTimer(OverheadViewResetDelay, self._ResetCameraView)
			else:
				self._ResetCameraView()
			#animator.SetParam('gun_view_close', 0)
		if persp != self._viewPersp:
			Instance.mUIManager.GetUI(UIDef.UI_GunHud).SetCrossHairVisible(persp != 2)
		self._viewPersp = persp

	def UpdateAimEntities(self):
		if not self.AssistedAimEnabled():
			return
		eid = clientApi.GetLocalPlayerId()
		entities = self._gameComp.GetEntitiesAround(eid, AssistedAimDetectRadius, {})
		healthEnum = clientApi.GetMinecraftEnum().AttrType.HEALTH
		self._aimRoundEntities = []
		for entityId in entities:
			if entityId == eid:
				continue
			comp = CompFactory.CreateEngineType(entityId)
			identifier = comp.GetEngineTypeStr()
			if identifier in IgnoreTargets:
				continue
			attrComp = CompFactory.CreateAttr(entityId)
			maxHealth = attrComp.GetAttrMaxValue(healthEnum)
			if maxHealth is None or maxHealth <= 0:
				continue
			size = CompFactory.CreateCollisionBox(entityId).GetSize()
			if size is None or max(size) <= 0:
				continue
			self._aimRoundEntities.append({
				'eid': entityId,
				'size': size,
				'identifier': identifier,
			})

	def AssistedAimEnabled(self):
		return self._weaponHandler and self._weaponHandler.IsZooming() and self._viewPersp != 2

	def UpdateAssistedAim(self, deltaTime):
		if not self.AssistedAimEnabled():
			return
		if not self._playerCamComp:
			return
		camera = self._playerCamComp
		eid = clientApi.GetLocalPlayerId()
		entities = self._aimRoundEntities
		validEntities = []
		for aimEntity in entities:
			pos = engineApiGac.GetEntityFootPos(aimEntity['eid'])
			if not pos:
				continue
			aimEntity['pos'] = pos
			validEntities.append(aimEntity)

		forward = Vector3(camera.GetForward())
		right = Vector3.Cross(Vector3.Up(), forward)
		up = Vector3.Cross(forward, right)
		xzForward = Vector3(forward.x, 0, forward.z)
		xzForward.Normalize()
		camPos = Vector3(camera.GetPosition())+Vector3(camera.GetCameraAnchor())
		camRot = camera.GetCameraRotation()
		aimTarget = None
		closest = -1

		xzRotateAngle = 0
		xzDeltaAngle = 0
		for target in validEntities:
			size = target['size']
			sizeHalfDis = MathUtils.TupleLength(size)/2.0
			vPos = Vector3(target['pos'])+Vector3(0,size[1]/2.0,0)
			dPos = vPos - camPos
			axisDis = Vector3.Dot(dPos, forward)
			if axisDis <= 0:
				continue
			dis = dPos.Length()
			axisHPos = dPos - axisDis*forward
			axisHPosYDis = abs(Vector3.Dot(axisHPos, up))
			axisHDis = axisHPos.Length()
			if axisHPosYDis > size[1]/2 * AssistedAimRadiusYK:
				continue
			addonRadius = 0
			if dis >= AssistedAimRadiusAddonBeginDis:
				addonRadius += min(AssistedAimRadiusAddonMax, (dis-AssistedAimRadiusAddonBeginDis) * AssistedAimRadiusAddonByDis)
			enableRadius = sizeHalfDis * AssistedAimRadiusK + addonRadius
			if axisHDis > enableRadius:
				continue
			if self.DetectTargetBlocked(camPos, dPos.Normalized(), dis):
				continue

			target['axisHPos'] = axisHPos
			target['axisHDis'] = axisHDis
			target['enableRadius'] = enableRadius
			target['dPos'] = dPos
			target['dis'] = dis
			score = axisHDis*dis
			if closest < 0 or closest > score:
				closest = score
				aimTarget = target

		sensitive = AssistedAimSensitive
		if aimTarget:
			axisHPos = aimTarget['axisHPos']
			dis = aimTarget['dis']
			dPos = aimTarget['dPos']
			enableRadius = aimTarget['enableRadius']
			xzDir = Vector3(dPos.x / dis, 0, dPos.z / dis)
			xzDir.Normalize()
			xzAngle = math.degrees(math.acos(Vector3.Dot(xzDir, xzForward)))
			side = Vector3.Dot(right, axisHPos)
			rotateDir = 1 if side < 0 else -1
			xzRotateAngle = rotateDir * AssistedAimVelocity * deltaTime * MathUtils.Clamp(axisHPos.Length() / enableRadius, 0, 1)
			xzDeltaAngle = rotateDir * xzAngle
			sensitive = MathUtils.Clamp(sensitive*(1.0-dis/AssistedAimDetectRadius), AssistedAimSensitiveRange[0], AssistedAimSensitiveRange[1])

		if abs(xzDeltaAngle) > sensitive:
			camera.SetCameraRotation((camRot[0], camRot[1]+xzRotateAngle))

	def DetectTargetBlocked(self, fromPos, dir, dis):
		checkDis = 0.5
		step = 1.0
		while checkDis < dis:
			pos = MathUtils.TupleFloor2Int((fromPos + checkDis*dir).ToTuple())
			collision = self._blockComp.GetBlockCollision(pos)
			size = MathUtils.TupleSub(collision['max'], collision['min'])
			if max(size) > 0:
				info = self._blockComp.GetBlock(pos)
				if not info[0] or info[0] not in AssistedAimPassBlock:
					return True
			checkDis += step
		return False

	def _ResetCameraView(self):
		if not self._playerCamComp:
			return
		camera = self._playerCamComp
		camera.SetCameraOffset((0, 0, 0))
		#camera.SetCameraAnchor((0, 0, 0))
		self.BroadcastEvent('ChangeCameraAnchor', {
			'anchor': (0, 0, 0)
		})
		self._viewResetTimer = None


	# 弹夹数表现
	def UpdateClip(self, cur, max, clipItemCount):
		self.BroadcastEvent("UIUpdateClip", {'clip': cur, 'maxClip': max, 'clipItem': clipItemCount})

	# 换弹进度表现
	def UpdateReloadProgress(self, percent, duration):
		self.BroadcastEvent('UIUpdateReloadProgress', {
			'percent': percent,
			'duration': duration,
		})

	# 准星表现
	def UpdateCrossHair(self, gun):
		display = self.Get(gun.Eid)
		if not display:
			return
		crossHairConfig = display['config']['crossHair']
		angle = gun.ScatterAngle
		chargeInfo = None
		if gun.IsUsing():
			chargeInfo = gun.ChargeInfo
		self.BroadcastEvent('UIUpdateCrossHair', {
			'angle': angle,
			'zoom': gun.IsZooming(),
			'charge': chargeInfo,
			'config': crossHairConfig
		})

	def _GetTrailCamType(self, eid):
		trailCamType = 'third'
		if eid == clientApi.GetLocalPlayerId():
			if self._playerViewComp.GetPerspective() == 0:
				trailCamType = 'first'
				if self._weaponHandler and self._weaponHandler.IsZooming():
					trailCamType = 'first_zoom'
		return trailCamType

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnHitTargets(self, data):
		eid = data['fromId']
		display = self.Get(eid)
		if not display:
			return
		trailCamType = self._GetTrailCamType(eid)
		trailType = display['config']['trailType']
		particle = display['particle']
		sound = display['sound']
		levelIndex = data['level']-1
		for (targetId, hit) in zip(data['targets'], data['hits']):
			hitPos = (hit['x'], hit['y'], hit['z'])
			if trailType == 'hitscan':
				particle.EmitTrail('trail', trailCamType, hitPos, index=levelIndex)
			if targetId != '-1':
				particle.Emit(targetId, 'hit_target', hitPos, index=levelIndex)
				sound.Play(targetId, 'hit_target', hitPos, index=levelIndex)
			else:
				particle.Emit(targetId, 'hit_static', hitPos, index=levelIndex)
				particle.Emit(targetId, 'hit_drop', hitPos, index=levelIndex)
				sound.Play(targetId, 'hit', hitPos, index=levelIndex)


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnHitEnd(self, data):
		eid = data['fromId']
		display = self.Get(eid)
		if not display:
			return
		trailCamType = self._GetTrailCamType(eid)
		trailType = display['config']['trailType']
		particle = display['particle']
		hitPos = data['endPosition']
		levelIndex = data['level'] - 1
		if trailType == 'hitscan':
			particle.EmitTrail('trail', trailCamType, hitPos, index=levelIndex)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnBulletEntityCreated(self, data):
		fromId = data['fromId']
		eid = data['eid']
		display = self.Get(fromId)
		if not display:
			return

		self.BroadcastEvent('OnClientBulletEntityCreated', {
			'fromId': fromId,
			'eid': eid,
			'config': display['weaponConfig']['shootEffect']
		})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BulletServerSystem)
	def OnBulletEntityDestroy(self, data):
		fromId = data['fromId']
		eid = data['eid']
		display = self.Get(fromId)
		if not display:
			return

		self.BroadcastEvent('OnClientBulletEntityDestroy', {
			'fromId': fromId,
			'eid': eid,
		})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DamageServerSystem)
	def OnHealthDamage(self, data):
		if data['source'] != 'gun':
			return
		if clientApi.GetLocalPlayerId() != data['fromId']:
			return
		damages = data['damages']
		killed = []
		targets = []
		for item in damages:
			targetEntityId = item['eid']
			if item['dead']:
				killed.append(targetEntityId)
			else:
				targets.append(targetEntityId)
		if len(targets) > 0:
			self.BroadcastEvent('UIUpdateCrossHairHit', {
				'eids': targets,
			})
		if len(killed) > 0:
			self.BroadcastEvent('UIUpdateCrossHairKill', {
				'eids': killed,
			})

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnForceDropOffhand(self, args):
		text = engineApiGac.GetChinese('scuke_survive.offhand_not_valid.tips')
		Instance.mUIManager.ShowTips({'text': text, 'duration': 3.0})

	def Destroy(self):
		super(GunClientSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.GameTickSubscribeEvent, self.OnGameTick)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem)
	def OnGunBreak(self, data):
		playerId = data['playerId']
		if playerId == self.mPlayerId:
			CompFactory.CreateCustomAudio(self.mLevelId).PlayCustomMusic('random.break', entityId=playerId)
