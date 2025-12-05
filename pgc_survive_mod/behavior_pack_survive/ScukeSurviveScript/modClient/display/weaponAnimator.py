# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.entityWeaponConfig import EntityPreloadWeapons

CompFactory = clientApi.GetEngineCompFactory()


def RegisterParam(name, defaultValue=0):
	key = 'query.mod.' + name
	comp = CompFactory.CreateQueryVariable(clientApi.GetLevelId())
	comp.Register(key, defaultValue)

RegisterParam('scuke_survive_weapon_carried', 0)
RegisterParam('scuke_survive_weapon_carried_t', 0)
RegisterParam('scuke_survive_tp_rot_y', 0)
RegisterParam('scuke_survive_tp_rot_x', 0)

ReverseAnimation = {
	'first_person': {
		'scuke_survive_empty_hand': 'animation.scuke_survive_weapon.cancel_empty_hand',
		'scuke_survive_swap_item': 'animation.scuke_survive_weapon.cancel_swap_item',
		'scuke_survive_attack_rotation': 'animation.scuke_survive_weapon.cancel_attack',
	},
	'third_person': {
		'scuke_survive_walk_hand': 'animation.scuke_survive_weapon.cancel_walk_hand',
	}
}

class ModelCacheManager(object):
	_GeometryCache = {}
	_CacheIndex = 0
	_CacheSize = 5

	@staticmethod
	def GetCache(eid):
		cache = ModelCacheManager._GeometryCache
		if eid not in cache:
			cache[eid] = {}
		return cache[eid]

	@staticmethod
	def AddModel(eid, resKey, resPath):
		comp = CompFactory.CreateActorRender(eid)
		typeComp = CompFactory.CreateEngineType(eid)
		identifier = typeComp.GetEngineTypeStr()
		player = identifier == 'minecraft:player'
		if not player:
			eid = identifier  # 不是玩家，直接用identifier来唯一标记
		cache = ModelCacheManager.GetCache(eid)
		ModelCacheManager._CacheIndex += 1
		index = ModelCacheManager._CacheIndex
		if resKey in cache:
			record = cache[resKey]
			if record['path'] != resPath:
				print 'ModelCache Failed %s %s' % (resKey, resPath)
				del cache[resKey]
				if player:
					comp.RemovePlayerGeometry(resKey)
				else:
					comp.RemoveActorGeometry(identifier, resKey)
		if resKey not in cache:
			if len(cache) >= ModelCacheManager._CacheSize and player:  # 玩家才使用缓存
				expireKey = None
				oldest = -1
				for key, item in cache.iteritems():
					if oldest < 0 or item['index'] < oldest:
						oldest = item['index']
						expireKey = key
				if expireKey is not None:
					del cache[expireKey]
					if player:
						comp.RemovePlayerGeometry(expireKey)
					else:
						comp.RemoveActorGeometry(identifier, expireKey)
			cache[resKey] = {
				'index':  index,
				'path': resPath,
			}
			if player:
				comp.AddPlayerGeometry(resKey, resPath)
			else:
				comp.AddActorGeometry(identifier, resKey, resPath)
		else:
			cache[resKey]['index'] = index

	@staticmethod
	def HasModel(eid, resKey, resPath=None):
		typeComp = CompFactory.CreateEngineType(eid)
		identifier = typeComp.GetEngineTypeStr()
		player = identifier == 'minecraft:player'
		if not player:
			eid = identifier
		cache = ModelCacheManager.GetCache(eid)
		if resKey not in cache:
			return False
		record = cache[resKey]
		return resPath is None or record['path'] == resPath

	@staticmethod
	def RemoveModel(eid, resKey, resPath=None):
		comp = CompFactory.CreateActorRender(eid)
		typeComp = CompFactory.CreateEngineType(eid)
		identifier = typeComp.GetEngineTypeStr()
		player = identifier == 'minecraft:player'
		if not player:
			eid = identifier
		cache = ModelCacheManager.GetCache(eid)
		if resKey not in cache:
			return None
		record = cache[resKey]
		if resPath is not None:
			if resPath != record['path']:
				return None
		if player:
			comp.RemovePlayerGeometry(resKey)
		else:
			comp.RemoveActorGeometry(identifier, resKey)
		del cache[resKey]
		return record['path']

	@staticmethod
	def RemoveAllModel(eid):
		comp = CompFactory.CreateActorRender(eid)
		typeComp = CompFactory.CreateEngineType(eid)
		identifier = typeComp.GetEngineTypeStr()
		player = identifier == 'minecraft:player'
		if not player:
			eid = identifier
		cache = ModelCacheManager.GetCache(eid)
		for resKey in cache:
			if player:
				comp.RemovePlayerGeometry(resKey)
			else:
				comp.RemoveActorGeometry(identifier, resKey)
		del ModelCacheManager._GeometryCache[eid]

class WeaponAnimatorController(object):
	def __init__(self, eid, identifier, animatorConfig, params, conflictParams):
		self._eid = eid
		self._config = animatorConfig
		self._identifier = identifier
		self._queryVariableComp = None
		self._rotComp = CompFactory.CreateRot(eid)
		self._params = params
		self._conflictParams = conflictParams

		self._addonGeometry = []
		self._addonRenderController = []
		self._addonAnimationController = []

		self._actorComp = CompFactory.CreateActorRender(self._eid)
		typeComp = CompFactory.CreateEngineType(self._eid)
		self._typeIdentifier = typeComp.GetEngineTypeStr()
		self._player = self._typeIdentifier == 'minecraft:player'
		self._preloadMode = not self._player and self._typeIdentifier in EntityPreloadWeapons
		self._preloaded = False
		if self._preloadMode:
			preloadConfig = EntityPreloadWeapons[self._typeIdentifier]
			self._preloaded = preloadConfig.get('animatorLoaded', False)


		# 初始化状态参数
		self.InitAnimatorStateParams(eid)

		if self._player:
			resKey = animatorConfig['resKey']
			condition = 'query.mod.scuke_survive_weapon_carried'
			handsCondition = 'variable.is_first_person && query.mod.scuke_survive_weapon_carried'
			handsConfig = animatorConfig['hands']
			handsResKey = handsConfig['resKey']
			self.AddModel(handsResKey, handsConfig, handsCondition)
			self.AddModel(resKey, animatorConfig, condition)
			# 添加手部抵消动画
			self.AddReverseAnimation()
			# 添加第一人称动画
			self.AddAnimationController('first_person', 'first', resKey, animatorConfig['first'], condition)
			# 添加第三人称动画
			self.AddAnimationController('third_person', 'third', resKey, animatorConfig['third'], condition)
			self.SetParam('scuke_survive_weapon_carried', 1)
			self.RebuildPlayerRender()
		else:
			needRebuild = not self._preloadMode
			if self._preloadMode and not self._preloaded:
				preloadConfig = EntityPreloadWeapons[self._typeIdentifier]
				displays = preloadConfig.get('display', None)
				if displays:
					for displayConfig in displays:
						pAnimatorConfig = displayConfig.get('animator', None)
						if pAnimatorConfig and pAnimatorConfig != animatorConfig:
							self.AddEntityAnimator(pAnimatorConfig)
					preloadConfig['animatorLoaded'] = True
					self._preloaded = True
					needRebuild = True

			carried_t, carried = self.AddEntityAnimator(animatorConfig)
			if needRebuild:
				self.RebuildPlayerRender()
			self.SetParam('scuke_survive_weapon_carried_t', carried_t)
			self.SetParam('scuke_survive_weapon_carried', carried)

	def AddEntityAnimator(self, animatorConfig):
		resKey = animatorConfig['resKey']
		carried_t = hash(animatorConfig.get('textureKey', animatorConfig['model'])) % 100000  # 非玩家实体只能全部按类型挂载（挂载影响同类实体
		condition = 'query.mod.scuke_survive_weapon_carried_t == %d' % carried_t
		self.AddModel(resKey, animatorConfig, condition)
		# 添加第三人称动画
		carried = hash(animatorConfig['model']) % 100000  # 非玩家实体只能全部按类型挂载（挂载影响同类实体
		condition = 'query.mod.scuke_survive_weapon_carried == %d' % carried
		self.AddAnimationController('third_person', 'third', resKey, animatorConfig['third'], condition, str(carried))
		return carried_t, carried


	def AddModel(self, resKey, config, condition):
		actorComp = self._actorComp
		identifier = self._typeIdentifier
		player = self._player
		if 'model' in config:
			mKey = config.get('modelKey', resKey)
			ModelCacheManager.AddModel(self._eid, mKey, config['model'])

		if 'texture' in config:
			tKey = config.get('textureKey', resKey)
			if isinstance(config['texture'], list):
				for i in range(0, len(config['texture'])):
					if player:
						actorComp.AddPlayerTexture(tKey + str(i), config['texture'][i])
					else:
						actorComp.AddActorTexture(identifier, tKey + str(i), config['texture'][i])
			else:
				if player:
					actorComp.AddPlayerTexture(tKey, config['texture'])
				else:
					actorComp.AddActorTexture(identifier, tKey, config['texture'])
		if 'renderController' in config:
			if player:
				actorComp.AddPlayerRenderController(config['renderController'], condition)
			else:
				actorComp.AddActorRenderController(identifier, config['renderController'], condition)
			self._addonRenderController.append(config['renderController'])

	def AddAnimationController(self, stateName, flag, resKey, config, condition, ctrlFlag=''):
		if 'resKey' in config:
			resKey = config['resKey']
		actorComp = self._actorComp
		identifier = self._typeIdentifier
		player = self._player
		animations = config['animations']
		controller = config['controller']
		controllerKey = '%s_%s_%s' % (modConfig.ModNameSpace, flag, 'weapon_ctl')
		if player:
			for k, v in animations.iteritems():
				key = '%s_%s_%s' % (resKey, flag, k)
				actorComp.AddPlayerAnimation(key, v)
			actorComp.AddPlayerAnimationController(controllerKey, controller)
			actorComp.AddPlayerAnimationIntoState('root', stateName, controllerKey, condition)
			self._addonAnimationController.append(controllerKey)
		else:
			controllerKey = '%s_%s' % (controllerKey, ctrlFlag)
			for k, v in animations.iteritems():
				key = '%s_%s_%s' % (resKey, flag, k)
				actorComp.AddActorAnimation(identifier, key, v)
			actorComp.AddActorAnimationController(identifier, controllerKey, controller)
			actorComp.AddActorScriptAnimate(identifier, controllerKey, condition)
			self._addonAnimationController.append(controllerKey)

	def AddReverseAnimation(self):
		actorComp = self._actorComp
		player = self._player
		identifier = self._typeIdentifier
		condition = 'query.mod.scuke_survive_weapon_carried'
		if player:
			for state in ReverseAnimation:
				animations = ReverseAnimation[state]
				for k in animations:
					anim = animations[k]
					actorComp.AddPlayerAnimation(k, anim)
					actorComp.AddPlayerAnimationIntoState('root', state, k, condition)
		else:
			for state in ReverseAnimation:
				animations = ReverseAnimation[state]
				for k in animations:
					anim = animations[k]
					actorComp.AddActorAnimation(identifier, k, anim)
					actorComp.AddActorScriptAnimate(identifier, k, condition)

	def RebuildPlayerRender(self):
		actorComp = self._actorComp
		identifier = self._typeIdentifier
		player = self._player
		if player:
			actorComp.RebuildPlayerRender()
		else:
			actorComp.RebuildActorRender(identifier)

	def InitAnimatorStateParams(self, eid):
		self._queryVariableComp = CompFactory.CreateQueryVariable(eid)
		for k, v in self._params.iteritems():
			self.SetParam(k, v)

	def SetParam(self, name, value):
		if not self._queryVariableComp:
			return
		self._params[name] = value
		key = 'query.mod.' + name
		self._queryVariableComp.Set(key, value)


	def SetParamOnlyOne(self, name, value):
		for k in self._conflictParams:
			if k == name:
				self.SetParam(name, value)
			else:
				self.SetParam(k, 0)


	def Reset(self):
		self._queryVariableComp = CompFactory.CreateQueryVariable(self._eid)
		for k, v in self._params.iteritems():
			self.SetParam(k, 0)
		self.RemoveAddon()


	def RemoveAddon(self):
		actorComp = self._actorComp
		identifier = self._typeIdentifier
		player = self._player
		if not self._preloaded:
			# for k in self._addonAnimationController:
			#	actorComp.RemovePlayerAnimationController(k)
			self._addonAnimationController = None
			for k in self._addonGeometry:
				if player:
					actorComp.RemovePlayerGeometry(k)
				else:
					actorComp.RemoveActorGeometry(identifier, k)
			self._addonGeometry = None
			for k in self._addonRenderController:
				if player:
					actorComp.RemovePlayerRenderController(k)
				else:
					actorComp.RemoveActorRenderController(identifier, k)
			self._addonRenderController = None
			self.RebuildPlayerRender()
		self.SetParam('scuke_survive_weapon_carried', 0)
		self.SetParam('scuke_survive_weapon_carried_t', 0)


	def UpdateTpFixedRot(self, weight=(1,1), offset=(0,0)):
		compRot = self._rotComp
		rot = compRot.GetRot()
		if rot is None:
			return
		deltaY = rot[1] - self._queryVariableComp.GetMolangValue('query.body_y_rotation')
		if deltaY > 180:
			deltaY = deltaY - 360
		elif deltaY < -180:
			deltaY = deltaY + 360
		deltaX = rot[0]
		self.SetParam('scuke_survive_tp_rot_x', (deltaX + offset[0]) * weight[0])
		self.SetParam('scuke_survive_tp_rot_y', (deltaY + offset[1]) * weight[1])

