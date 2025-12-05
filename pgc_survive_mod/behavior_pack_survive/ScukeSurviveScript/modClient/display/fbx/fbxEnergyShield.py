# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, Quaternion, MathUtils
from ScukeSurviveScript.modClient.display.fbx.fbxModel import FbxModel
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import eventConfig, modConfig
import mod.client.extraClientApi as clientApi

class FbxEnergyShieldModel(FbxModel):
	def __init__(self, eventHandler, eid, config):
		super(FbxEnergyShieldModel, self).__init__(eventHandler, eid, config)
		self._fbxEntity = None
		self._eventHandler.ListenForEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuffServerSystem, 'OnEnergySheildInfo', self, self.OnEnergySheildInfo)
		self._eventHandler.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), 'AddEntityClientEvent', self, self.AddEntityClientEvent)
		self._fadeTimer = engineApiGac.AddRepeatedTimer(0.05, self.OnFadeUpdate)
		self._hited = 0.0

	def CreateModel(self):
		modelComp = self._modelComp
		modelId = modelComp.SetModel(self._modelName)
		modelComp.SetModelMaterial(modelId, self._matName)
		modelComp.SetExtraUniformValue(modelId, 1, self._color)
		modelComp.SetExtraUniformValue(modelId, 2, (self._scale[0], self._scale[1], self._scale[2], self._hited))
		self._modelId = modelId
		return modelId


	def OnUpdate(self):
		pass

	def OnFadeUpdate(self):
		if self._hited > 0:
			self._hited = max(0.0, self._hited - 0.05)
			if self._modelId is not None:
				modelComp = self._modelComp
				modelComp.SetExtraUniformValue(self._modelId, 2, (self._scale[0], self._scale[1], self._scale[2], self._hited))


	def OnDestroy(self):
		super(FbxEnergyShieldModel, self).OnDestroy()
		self._eventHandler.UnListenForEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuffServerSystem, 'OnEnergySheildInfo', self, self.OnEnergySheildInfo)
		self._eventHandler.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
										  'AddEntityClientEvent', self, self.AddEntityClientEvent)
		if self._fadeTimer:
			engineApiGac.CancelTimer(self._fadeTimer)
			self._fadeTimer = None

	def _ActiveFbxModel(self, fbxEntity):
		self.RemoveModel()
		self._modelComp = clientApi.GetEngineCompFactory().CreateModel(fbxEntity)
		self._fbxEntity = fbxEntity
		self.CreateModel()
		self._modelComp.SetEntityShadowShow(False)
		self._modelComp.BindEntityToEntity(self._eid)

	def OnEnergySheildInfo(self, data):
		self._hited = 0.3

	def AddEntityClientEvent(self, args):
		if args['engineTypeStr'] == 'scuke_survive:fbx_entity' and self._fbxEntity is None:
			fbxEntity = args['id']
			comp = clientApi.GetEngineCompFactory().CreateAction(fbxEntity)  # 靠AttackTarget绑定关系
			if comp.GetAttackTarget() == self._eid:
				self._ActiveFbxModel(fbxEntity)
