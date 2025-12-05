# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modClient.display.fbx.fbxModel import FbxModelBuilder
from ScukeSurviveScript.modClient.display.fbx.fbxEnergyShield import FbxEnergyShieldModel
from ScukeSurviveScript.modClient.display.fbx.fbxBattleArea import FbxBattleAreaModel
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.displayConfig import Config as DisplayConfig
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modClient.display.ctrl.ctrl import CancelPlayerCtrl, CtrlBuilder
CompFactory = clientApi.GetEngineCompFactory()


# 注册display对应的逻辑类
FbxModelBuilder.BindingFbxModel('energy_shield', FbxEnergyShieldModel)
FbxModelBuilder.BindingFbxModel('battle_area', FbxBattleAreaModel)

CtrlBuilder.BindingClass('cancel_all_ctrl', CancelPlayerCtrl)


def _RemoveValueFromList(list, value):
	try:
		index = list.index(value)
		if index > -1:
			return list.pop(index)
		else:
			print 'ERROR _RemoveValueFromList Not Found', list, value
	except IndexError:
		print 'ERROR _RemoveValueFromList Failed', list, value
	return None


class DisplayClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(DisplayClientSystem, self).__init__(namespace, systemName)
		self._playerDisplay = {}
		self._inited = False

		self._postComp = CompFactory.CreatePostProcess(self.mLevelId)
		self._gameComp = CompFactory.CreateGame(self.mLevelId)
		self._fbxModelUpdateTimer = engineApiGac.AddRepeatedTimer(1.0, self.OnFbxModelUpdate)

		self.RegisterParam('scuke_survive_render_effect')
		self.RegisterParam('scuke_survive_low_temp_shaking')

	def RegisterParam(self, name, defaultValue=0):
		key = 'query.mod.' + name
		comp = CompFactory.CreateQueryVariable(clientApi.GetLevelId())
		comp.Register(key, defaultValue)

	def SetParam(self, eid, name, value):
		key = 'query.mod.' + name
		CompFactory.CreateQueryVariable(eid).Set(key, value)

	@EngineEvent()
	def UiInitFinished(self, args):
		if not self._inited:
			self.RegisterBloom()
		self.UpdateDisplay(self.mPlayerId)
		# 更新特效
		self.RefreshParticles()
		self._inited = True

	@EngineEvent()
	def AddPlayerCreatedClientEvent(self, args):
		playerId = args['playerId']
		renderComp = CompFactory.CreateActorRender(playerId)
		renderComp.AddPlayerAnimation('scuke_survive_fp_low_temp_shaking',
									  'animation.scuke_survive_player.shaking_first')
		renderComp.AddPlayerAnimation('scuke_survive_tp_low_temp_shaking',
									  'animation.scuke_survive_player.shaking_third')
		renderComp.AddPlayerAnimationIntoState('root', 'first_person',
											   'scuke_survive_fp_low_temp_shaking',
											   'query.mod.scuke_survive_low_temp_shaking')

		renderComp.AddPlayerAnimationIntoState('root', 'third_person',
											   'scuke_survive_tp_low_temp_shaking',
											   'query.mod.scuke_survive_low_temp_shaking')
		condition = '!variable.is_first_person && !variable.map_face_icon && query.mod.scuke_survive_render_effect == 0'
		renderComp.RemovePlayerRenderController('controller.render.player.third_person')
		renderComp.AddPlayerRenderController('controller.render.player.third_person', condition)
		condition = '!variable.is_first_person && !variable.map_face_icon && query.mod.scuke_survive_render_effect == 1'
		renderComp.AddPlayerRenderController('controller.render.scuke_survive_player.tp_low_temp', condition)
		condition = '!variable.is_first_person && !variable.map_face_icon && query.mod.scuke_survive_render_effect == 2'
		renderComp.AddPlayerRenderController('controller.render.scuke_survive_player.tp_high_temp', condition)
		renderComp.RebuildPlayerRender()

	@EngineEvent()
	def AppResumeFromBackgroundClientEvent(self, args):
		self.UpdateDisplay(self.mPlayerId)

	@EngineEvent()
	def ScreenSizeChangedClientEvent(self, args):
		engineApiGac.AddTimer(0, self.UpdateDisplay, self.mPlayerId)

	def AddDisplayByStr(self, eid, keyName, update=True):
		if keyName not in DisplayConfig:
			return
		self.AddDisplay(eid, DisplayConfig[keyName], update)

	def RemoveDisplayByStr(self, eid, keyName, update=True):
		if keyName not in DisplayConfig:
			return
		self.RemoveDisplay(eid, DisplayConfig[keyName], update)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BattleEventServerSystem)
	def OnAddBattleAreaDisplay(self, data):
		displayName = data['display']
		if displayName not in DisplayConfig:
			return
		config = DisplayConfig[displayName].copy()
		config['data'] = data
		self.AddDisplay('-1', config)

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.BattleEventServerSystem)
	def OnRemoveBattleAreaDisplay(self, data):
		displayName = data['display']
		if displayName not in DisplayConfig:
			return
		config = DisplayConfig[displayName]
		self.RemoveDisplay('-1', config)

	def AddDisplay(self, eid, config, update=True):
		self.SetDisplay(eid, config, True, update)

	def RemoveDisplay(self, eid, config, update=True):
		self.SetDisplay(eid, config, False, update)

	def SetDisplay(self, eid, config, active, update=True):
		if eid not in self._playerDisplay:
			self._playerDisplay[eid] = {
				'molang_query': {},
				'screen_vignette': [],
				'screen_texture': [],
				'fbx': {},
				'particle': {},
				'ctrls': {},
			}
		curDisplay = self._playerDisplay[eid]
		priority = 0 if 'priority' not in config else config['priority']
		curMolangs = curDisplay['molang_query']
		if 'molang' in config:
			molang = config['molang']
			for key, value in molang.iteritems():
				if key not in curMolangs:
					curMolangs[key] = []
				while (priority >= len(curMolangs[key])):
					curMolangs[key].append([])
				if active:
					curMolangs[key][priority].append(value)
				else:
					_RemoveValueFromList(curMolangs[key][priority], value)
		# 渐晕
		curScreenVignette = curDisplay['screen_vignette']
		while priority >= len(curScreenVignette):
			curScreenVignette.append([])
		if 'vignette' in config:
			if active:
				curScreenVignette[priority].append(config)
			else:
				_RemoveValueFromList(curScreenVignette[priority], config)
		# 屏幕贴图
		curScreenTexture = curDisplay['screen_texture']
		while priority >= len(curScreenTexture):
			curScreenTexture.append([])
		if 'texture' in config:
			if active:
				curScreenTexture[priority].append(config)
			else:
				_RemoveValueFromList(curScreenTexture[priority], config)

		# fbx表现
		curFbxs = curDisplay['fbx']
		if 'fbx' in config:
			uidKey = config['uid']
			if active:
				fbxDisplay = FbxModelBuilder.GetFbxModel(self, eid, config)
				if fbxDisplay:
					curFbxs[uidKey] = fbxDisplay
			else:
				fbxDisplay = curFbxs.get(uidKey, None)
				if fbxDisplay:
					fbxDisplay.OnDestroy()
					del curFbxs[uidKey]
		
		# 粒子特效
		curParticles = curDisplay['particle']
		if 'particles' in config:
			if 'type' in config:
				if active:
					# 如果有创建粒子，则不再创建
					if not curParticles.get(config['type']):
						# 记录这一类型的对应特效，用于销毁
						parList = self.CreateParticleByCfg(eid, config['particles'])
						curParticles[config['type']] = {
							'particleList': parList,
							'config': config,
						}
				else:
					# 销毁
					parVal = curParticles.pop(config['type'], None)
					if parVal:
						for parId in parVal.get('particleList', []):
							clientApiMgr.RemoveMicroParticle(parId)
			else:
				raise ValueError('DisplayClientSystem.SetDisplay: type must be in particle config!')
			pass

		# 针对玩家的控制类逻辑，仅本地玩家执行逻辑，同时只能存在一种控制（后的覆盖前的）
		curCtrls = curDisplay['ctrls']
		if eid == self.mPlayerId and 'ctrl' in config:
			obj = curCtrls.pop('obj', None)
			if obj:
				obj.OnDestroy()
			if active:
				obj = CtrlBuilder.CreateObj(self, eid, config)
				if obj:
					curCtrls['obj'] = obj
			pass

		if update:
			self.UpdateDisplay(eid)

	def _GetTopDisplayConfig(self, eid, typeName):
		if eid not in self._playerDisplay:
			return None
		curDisplay = self._playerDisplay[eid]
		curDisplayConfigs = curDisplay[typeName]
		return self.__GetTopDisplayConfig(curDisplayConfigs)

	def __GetTopDisplayConfig(self, curDisplayConfigs):
		i = len(curDisplayConfigs) - 1
		displayConfig = None
		while i >= 0:
			n = len(curDisplayConfigs[i])
			if n > 0:
				displayConfig = curDisplayConfigs[i][n - 1]
				break
			i -= 1
		return displayConfig

	def UpdateDisplay(self, eid):
		if eid not in self._playerDisplay:
			return
		levelId = clientApi.GetLevelId()
		curDisplay = self._playerDisplay[eid]
		curMolangs = curDisplay['molang_query']
		for key, values in curMolangs.iteritems():
			curMolangValue = self.__GetTopDisplayConfig(values)
			if curMolangValue is None:
				self.SetParam(eid, key, 0)
			else:
				self.SetParam(eid, key, curMolangValue)
		if eid != self.mPlayerId:
			return
		# 渐晕
		vignetteComp = clientApi.GetEngineCompFactory().CreatePostProcess(levelId)
		vignette = self._GetTopDisplayConfig(eid, 'screen_vignette')
		if vignette is None:
			vignetteComp.SetVignetteSmoothness(0)
			vignetteComp.SetVignetteRGB((0, 0, 0))
			vignetteComp.SetVignetteRadius(0)
			vignetteComp.SetEnableVignette(False)
		else:
			vignetteComp.SetEnableVignette(vignette['vignette'])
			vignetteComp.SetVignetteCenter(vignette['center'])
			vignetteComp.SetVignetteRGB(vignette['rgb'])
			vignetteComp.SetVignetteRadius(vignette['radius'])
			vignetteComp.SetVignetteSmoothness(vignette['smoothness'])
		# 屏幕贴图
		screenUI = Instance.mUIManager.GetUI(UIDef.UI_SurviveScreen)
		if screenUI:
			screenTexture = self._GetTopDisplayConfig(eid, 'screen_texture')
			if screenTexture is None:
				screenUI.SetTexture('', 0, 0.1)
			else:
				screenUI.SetTexture(screenTexture['path'], screenTexture['alpha'], screenTexture['blend'])
		
		# 当前没有tick逻辑，所以先关闭
		# # 针对玩家的控制类逻辑
		# curCtrls = curDisplay['ctrls']
		# if 'obj' in curCtrls:
		# 	obj = curCtrls['obj']
		# 	obj.OnUpdate()
		pass

	def OnFbxModelUpdate(self):
		for eid, displayItem in self._playerDisplay.iteritems():
			fbxModels = displayItem['fbx']
			for fbxModel in fbxModels.itervalues():
				fbxModel.OnUpdate()

	def SetBloomActive(self, active, radius):
		postComp = self._postComp
		width, height, offsetX, offsetY = self._gameComp.GetScreenViewInfo()
		postComp.SetEnableByName('scuke_survive_bloom', active)
		postComp.SetParameter('scuke_survive_bloom', 'uv_x', 1.0 / width)
		postComp.SetParameter('scuke_survive_bloom', 'uv_y', 1.0 / height)
		postComp.SetParameter('scuke_survive_bloom', 'radius', radius)

	def RegisterBloom(self):
		dic = {
			"name": "scuke_survive_bloom",
			"enable": False,
			"paras": [
				{"name": "uv_x", "value": 0.0, "range": [0.0, 1.0]},
				{"name": "uv_y", "value": 0.0, "range": [0.0, 1.0]},
				{"name": "radius", "value": 1.0, "range": [0.0, 10.0]}
			],
			"pass_array": [
				{
					"render_target": {
						"width": 1.0,
						"height": 1.0
					},
					"material": "scuke_survive_bloom_start",
					"depth_enable": True
				},
				{
					"render_target": {
						"width": 0.5,
						"height": 0.5
					},
					"material": "scuke_survive_bloom"
				},
				{
					"render_target": {
						"width": 0.25,
						"height": 0.25
					},
					"material": "scuke_survive_bloom"
				},
				{
					"render_target": {
						"width": 0.125,
						"height": 0.125
					},
					"material": "scuke_survive_bloom"
				},
				{
					"render_target": {
						"width": 0.25,
						"height": 0.25
					},
					"material": "scuke_survive_bloom"
				},
				{
					"render_target": {
						"width": 0.50,
						"height": 0.50
					},
					"material": "scuke_survive_bloom"
				},
				{
					"render_target": {
						"width": 1.0,
						"height": 1.0
					},
					"material": "scuke_survive_bloom_end"
				}
			]
		}
		self._postComp.AddPostProcess(dic, 0)

	def RefreshParticles(self):
		"""传送维度后，刷新特效"""
		eid = self.mPlayerId
		curDisplay = self._playerDisplay.get(eid)
		if curDisplay:
			curParticles = curDisplay['particle']
			# 如果有创建粒子，则不再创建
			for ctype, partVal in curParticles.iteritems():
				# 根据config，重新生成特效
				config = partVal.get("config")
				if config:
					# 记录这一类型的对应特效，用于销毁
					partList = self.CreateParticleByCfg(eid, config['particles'])
					partVal['particleList'] = partList
		pass

	def CreateParticleByCfg(self, eid, particleList):
		"""根据config生成粒子"""
		partList = []
		for particle in particleList:
			path = particle['path']
			if particle.get("bind_entity"):
				parId = clientApiMgr.CreateMicroParticleBindEntity(path, eid)
				partList.append(parId)
		return partList

	def OnDestroy(self):
		super(DisplayClientSystem, self).OnDestroy()
		if self._fbxModelUpdateTimer:
			engineApiGac.CancelTimer(self._fbxModelUpdateTimer)
			self._fbxModelUpdateTimer = None