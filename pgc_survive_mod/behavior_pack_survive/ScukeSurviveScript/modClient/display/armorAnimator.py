# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.modCommon import modConfig

CompFactory = clientApi.GetEngineCompFactory()


def RegisterParam(name, defaultValue=0):
	key = 'query.mod.' + name
	comp = CompFactory.CreateQueryVariable(clientApi.GetLevelId())
	comp.Register(key, defaultValue)

TypeNames = [
	'helmet',
	'chest',
	'legs',
	'boots'
]

for _k in TypeNames:
	RegisterParam('scuke_survive_armor_'+_k, 0)

class ArmorAnimatorController(object):
	def __init__(self, eid, identifier, aid, animatorConfig, firstInit=False):
		self._eid = eid
		self._identifier = identifier
		self._queryVariableComp = None
		self._params = {}

		self._addonGeometry = []
		self._addonRenderController = []
		self._addonAnimationController = []

		self._armorId = aid
		self._actorComp = CompFactory.CreateActorRender(self._eid)

		resKey = animatorConfig['resKey']
		condition = animatorConfig.get('condition', '')
		# 模型
		self.AddModel(resKey, animatorConfig, condition)
		# 动画
		self.InitAnimationController(firstInit)
		# Apply
		self.RebuildPlayerRender()

	@property
	def ArmorId(self):
		return self._armorId

	def AddModel(self, resKey, config, condition=''):
		if 'model' not in config:
			return
		actorComp = CompFactory.CreateActorRender(self._eid)
		actorComp.AddPlayerGeometry(resKey, config['model'])
		if isinstance(config['texture'], list):
			for i in range(0, len(config['texture'])):
				actorComp.AddPlayerTexture(resKey+str(i), config['texture'][i])
		else:
			actorComp.AddPlayerTexture(resKey, config['texture'])
		actorComp.AddPlayerRenderController(config['renderController'], condition)
		self._addonGeometry.append(resKey)
		self._addonRenderController.append(config['renderController'])

	def InitAnimationController(self, addEmpty=False):
		actorComp = self._actorComp
		if addEmpty:
			animationKeyPrefix = '%s_%s' % (modConfig.ModNameSpace, 'armor_')
			for k in TypeNames:
				actorComp.AddPlayerAnimation(animationKeyPrefix+k, 'animation.scuke_survive_armor.empty')
		controllerKey = '%s_%s' % (modConfig.ModNameSpace, 'armor_ctl')
		actorComp.AddPlayerAnimationController(controllerKey, 'controller.animation.scuke_survive_armor')
		actorComp.AddPlayerAnimationIntoState('root', 'first_person', controllerKey)
		actorComp.AddPlayerAnimationIntoState('root', 'third_person', controllerKey)
		self._addonAnimationController.append(controllerKey)

	def RebuildPlayerRender(self):
		self._actorComp.RebuildPlayerRender()

	def SetPartActive(self, typeName, active, config=None):
		self.SetParam('armor_' + typeName, self._armorId if active else 0)
		if config and 'animations' in config:
			animations = config['animations']
			if typeName in animations:
				animationKeyPrefix = '%s_%s' % (modConfig.ModNameSpace, 'armor_')
				animation = 'animation.scuke_survive_armor.empty'
				if active:
					animation = animations[typeName]
				self._actorComp.AddPlayerAnimation(animationKeyPrefix+typeName, animation)

	def SetParam(self, name, value):
		if not self._queryVariableComp:
			return
		if value != 0:
			self._params[name] = value
		elif name in self._params:
			del self._params[name]
		key = 'query.mod.' + name
		self._queryVariableComp.Set(key, value)

	def Reset(self):
		self._queryVariableComp = CompFactory.CreateQueryVariable(self._eid)
		for k, v in self._params.iteritems():
			self.SetParam(k, 0)
		self.RemoveAddon()

	def RemoveAddon(self):
		actorComp = CompFactory.CreateActorRender(self._eid)
		#for k in self._addonAnimationController:
		#	actorComp.RemovePlayerAnimationController(k)
		self._addonAnimationController = None
		for k in self._addonGeometry:
			actorComp.RemovePlayerGeometry(k)
		self._addonGeometry = None
		for k in self._addonRenderController:
			actorComp.RemovePlayerRenderController(k)
		self._addonRenderController = None

		self.RebuildPlayerRender()
