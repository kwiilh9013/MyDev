# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.modClient.display.meleeAnimator import MeleeAnimatorController
from ScukeSurviveScript.modClient.display.weaponParticle import WeaponParticleController
from ScukeSurviveScript.modClient.display.weaponSound import WeaponSoundController
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon.cfg import meleeConfig as MeleeConfig
from ScukeSurviveScript.modCommon.cfg import weaponCommonCfg as WeaponConfig
from ScukeSurviveScript.modCommon import modConfig, eventConfig
from ScukeSurviveScript.modCommon.handler.meleeHandler import MeleeHandler

CompFactory = clientApi.GetEngineCompFactory()

OneSecondUpdate = 30.0
UpdateTimeMs = 1000.0 / OneSecondUpdate


class MeleeClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(MeleeClientSystem, self).__init__(namespace, systemName)
		self._isReady = False
		self._time = 0
		# TODO make it be a manager
		self._weaponDisplayMap = {}
		self._weaponHandler = None

		self._needKeyDown = False
		self._needKeyUp = False

		self._meleeLevel = -1

		self._keyState = {
			'melee': False,
		}

		self._playerCamComp = CompFactory.CreateCamera(self.mPlayerId)
		self._blockComp = CompFactory.CreateBlockInfo(self.mLevelId)
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

	def CheckValidOp(self, eid):
		if eid not in self._loadedEntity:
			return False
		return self._isReady

	@EngineEvent()
	def UiInitFinished(self, args):
		self._isReady = True
		eid = clientApi.GetLocalPlayerId()
		self._loadedEntity[eid] = True
		if self.Get(eid):
			self.SetMeleeDisplay(eid)
		meleeHud = Instance.mUIManager.GetUI(UIDef.UI_MeleeHud)
		meleeHud._hasSet = False
		settingClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
		posData = settingClient._settingDict['meleeBtnData']
		def _wait():
			Instance.mEventMgr.NotifyEvent(eventConfig.SettingDataSubscribtEvent, {"stage": "melee", "posData": posData})
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

	@EngineEvent()
	def RightClickReleaseClientEvent(self, args):
		eid = clientApi.GetLocalPlayerId()
		display = self.Get(eid)
		if not display:
			return
		if self.HandleBlockUse(True):
			return
		args['cancel'] = True

	@EngineEvent()
	def TapBeforeClientEvent(self, args):
		if self._weaponHandler:
			if self._weaponHandler.IsUsing():
				args['cancel'] = True
				return
			if self.HandleBlockUse(False):
				return
			args['cancel'] = True
			self.KeyDown()
			engineApiGac.AddTimer(0.2, self.KeyUp)

	@EngineEvent()
	def HoldBeforeClientEvent(self, args):
		if self._weaponHandler:
			if self._weaponHandler.IsUsing():
				args['cancel'] = True
				return
			if self.HandleBlockUse(False):
				return
			args['cancel'] = True
			self.KeyDown()
			engineApiGac.AddTimer(0.2, self.KeyUp)

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
		self._keyState['melee'] = True
		self._needKeyUp = False
		if not self.CheckCanUse():
			return
		if not self._weaponHandler.KeyDown(self._time):
			self._needKeyDown = True
			return
		self.SetKeyInputTaskWithout('melee')
		self._needKeyDown = False
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.MeleeBegin(display)
		# To server
		self.NotifyToServer("OnMeleeBegin", {
			'playerId': eid
		})

	def DoMeleeCast(self, castMelee):
		melee = self._weaponHandler
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.MeleeCast(display, melee.Combo, melee.Level)
		# To server
		castInfo = {
			'playerId': melee.Eid,
			'identifier': melee.Config['identifier'],
			'combo': melee.Combo,
			'level': melee.Level,
		}
		self.NotifyToServer("OnMeleeCast", castInfo)

	def DoMeleeAttack(self, meleeAttack):
		melee = self._weaponHandler
		eid = clientApi.GetLocalPlayerId()
		playerViewComp = CompFactory.CreatePlayerView(eid)
		persp = playerViewComp.GetPerspective()
		camera = CompFactory.CreateCamera(clientApi.GetLevelId())
		if persp == 0:
			pos = camera.GetPosition()
		else:
			pos = CompFactory.CreatePos(eid).GetPos()
		dir = camera.GetForward()
		pos = tuple((a + b * 0.1) for a, b in zip(pos, dir))
		config = meleeAttack['config']
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.MeleeAttack(display, config, meleeAttack['combo'])
		# To server
		attackInfo = {
			'playerId': melee.Eid,
			'identifier': melee.Config['identifier'],
			'position': pos,
			'direction': dir,
			'combo': meleeAttack['combo'],
			'castTime': meleeAttack['castTime'],
			'meleeTime': meleeAttack['meleeTime'],
		}
		self.NotifyToServer("OnMeleeAttack", attackInfo)


	def KeyUp(self):
		self._keyState['melee'] = False
		self._needKeyDown = False
		if not self._weaponHandler.KeyUp(self._time):
			self._needKeyUp = True
			return
		self.SetKeyInputTaskWithout('melee')
		self._needKeyUp = False
		eid = clientApi.GetLocalPlayerId()
		# Display
		display = self.Get(eid)
		self.MeleeEnd(display)
		# To server
		self.NotifyToServer("OnMeleeEnd", {
			'playerId': eid
		})

	def DoKeyInputTask(self):
		if self._needKeyDown:
			self.KeyDown()
		if self._needKeyUp:
			self.KeyUp()

	def ClearKeyInputTask(self):
		self._needKeyDown = False
		self._needKeyUp = False

	def SetKeyInputTaskWithout(self, keyState):
		if keyState != 'melee':
			self._needKeyDown = self._keyState['melee']

	def ClearKeyState(self):
		for k in self._keyState.keys():
			self._keyState[k] = False

	def GetKeyState(self, key):
		return self._keyState[key]

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnTakeMelee(self, data):
		playerId = data['playerId']
		if not self.CheckValidOp(playerId):
			data['__op__'] = 'take'
			self._waitingOp.append(data)
			return
		self.OnTakeMeleeInner(data)

	def OnTakeMeleeInner(self, data):
		identifier = data['identifier']
		playerId = data['playerId']
		config = MeleeConfig.GetConfig(identifier)
		if not config:
			return
		self.Add(playerId, identifier, config)
		if playerId == clientApi.GetLocalPlayerId():
			self._weaponHandler = MeleeHandler(playerId, config, self.__GetClipItemCount(playerId, config))
		if self._isReady:
			self.SetMeleeDisplay(playerId)

	def _NeedDoDisplay(self, data):
		pid = data['playerId']
		if pid == clientApi.GetLocalPlayerId():
			return None
		return self.Get(pid)

	def GetClipItemCount(self, eid, clipIdentifier):
		itemComp = CompFactory.CreateItem(eid)
		allItems = itemComp.GetPlayerAllItems(clientApi.GetMinecraftEnum().ItemPosType.INVENTORY)
		totalCount = 0
		for slotPos, itemDict in enumerate(allItems):
			if itemDict and itemDict['itemName'] == clipIdentifier:
				item_count = itemDict['count']
				totalCount += item_count

		return totalCount

	def CheckCanUse(self):
		itemComp = CompFactory.CreateItem(self.mPlayerId)
		carried = itemComp.GetCarriedItem()
		if carried:
			if carried['durability'] <= 1:
				CompFactory.CreateCustomAudio(self.mLevelId).PlayCustomMusic('scuke_survive.gun.jammed', entityId=self.mPlayerId)
				return False
		return True

	def SetMeleeDisplay(self, playerId):
		display = self.Get(playerId)
		if not display:
			return
		id = display['identifier']
		config = display['config']
		display['particle'] = WeaponParticleController(playerId, config['particle'])
		display['sound'] = WeaponSoundController(playerId, config['sound'])
		animator = MeleeAnimatorController(playerId, id, config['animator'])
		animator.MeleeTaking(config['takingTime'])
		display['animator'] = animator
		if playerId == clientApi.GetLocalPlayerId():
			self.SetUIActive(True, display)

	def RemoveMeleeDisplay(self, playerId):
		display = self.Get(playerId)
		if display:
			if 'animator' in display:
				display['animator'].Reset()
		if playerId == clientApi.GetLocalPlayerId():
			if self._weaponHandler:
				recoilFov = self._weaponHandler.GetRestoreRecoilFov()
				self.UpdateCamera(recoilFov)
			self.SetUIActive(False, display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnRemoveMelee(self, data):
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
		self.OnRemoveMeleeInner(data)

	def OnRemoveMeleeInner(self, data):
		identifier = data['identifier']
		playerId = data['playerId']
		self.RemoveMeleeDisplay(playerId)
		self.Remove(playerId)
		if playerId == clientApi.GetLocalPlayerId():
			self._weaponHandler = None
			self.ClearKeyInputTask()
			self.ClearKeyState()

	def MeleeBegin(self, display):
		display['animator'].MeleeBegin()

	def MeleeCast(self, display, combo, level):
		display['animator'].MeleeCast(combo, level)

	def MeleeAttack(self, display, attack, combo):
		pass

	def MeleeEnd(self, display):
		display['animator'].MeleeEnd()

	def Update(self):
		dTime = UpdateTimeMs
		time = self._time + dTime
		if self._weaponHandler:
			self.DoKeyInputTask()
			self.UpdateMelee(self._weaponHandler, time, dTime)
		self._time = time

		i = 0
		while i < len(self._waitingOp):
			data = self._waitingOp[i]
			playerId = data['playerId']
			if self.CheckValidOp(playerId):
				op = data['__op__']
				if op == 'take':
					self.OnTakeMeleeInner(data)
				elif op == 'remove':
					self.OnRemoveMeleeInner(data)
				self._waitingOp.pop(i)
				continue
			i += 1

	def _GetClipItemCount(self, gun):
		return self.__GetClipItemCount(gun.Eid, gun.Config)

	def __GetClipItemCount(self, eid, config):
		if 'clipIdentifier' not in config:
			return 0
		clipItem = config['clipIdentifier']
		return self.GetClipItemCount(eid, clipItem)

	def UpdateMelee(self, melee, time, dTime):
		if melee.IsUsing() and not self.CheckCanUse():
			self.KeyUp()
		castMelee = melee.UpdateMelee(time, dTime)
		if castMelee:
			self.DoMeleeCast(castMelee)
		attack = melee.UpdateMeleeAttack(time)
		if attack:
			self.DoMeleeAttack(attack)
		curLevel = melee.Level
		if curLevel != self._meleeLevel:
			self.UpdateMeleeLevel(curLevel)
		recoilFov = melee.UpdateMeleeRecoilFov(time, dTime, castMelee is not None)
		self.UpdateCamera(recoilFov)

	def UpdateMeleeLevel(self, level):
		self._meleeLevel = level
		self.BroadcastEvent('UIUpdateMeleeLevel', {
			'level': level,
		})

	def SetUIActive(self, active, display):
		melee = self._weaponHandler
		if active:
			Instance.mUIManager.GetUI(UIDef.UI_MeleeHud).OnCarryMelee(melee.Config['identifier'])
			if not self._initBtn:
				self._initBtn = True
				settingClient = clientApi.GetSystem(modConfig.ModName, modConfig.ClientSystemEnum.SettingClientSystem)
				posData = settingClient._settingDict['meleeBtnData']
				Instance.mEventMgr.NotifyEvent(eventConfig.SettingDataSubscribtEvent, {"stage": "melee", "posData": posData})
		else:
			Instance.mUIManager.GetUI(UIDef.UI_MeleeHud).OnDropMelee()


	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeAttackServerSystem)
	def OnHitTargets(self, data):
		display = self.Get(data['fromId'])
		if not display:
			return
		particle = display['particle']
		sound = display['sound']
		for target in data['targets']:
			hitPos = (target['x'], target['y'], target['z'])
			targetId = target['entityId']
			if targetId != '-1':
				particle.Emit(targetId, 'hit_target', hitPos)
				sound.Play(targetId, 'hit_target', hitPos)

	def UpdateCamera(self, recoilFov):
		camera = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId())
		fov = camera.GetFov()
		camera.SetFov(fov + recoilFov)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnMeleeBegin(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.MeleeBegin(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnMeleeCast(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.MeleeCast(display, data['combo'], data['level'])

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnMeleeAttack(self, data):
		pass

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnMeleeEnd(self, data):
		display = self._NeedDoDisplay(data)
		if not display:
			return
		self.MeleeEnd(display)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.MeleeServerSystem)
	def OnMeleeBreak(self, data):
		playerId = data['playerId']
		if playerId == self.mPlayerId:
			CompFactory.CreateCustomAudio(self.mLevelId).PlayCustomMusic('random.break', entityId=playerId)