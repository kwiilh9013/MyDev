# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import Vector3, Quaternion, MathUtils
from ScukeSurviveScript.modClient.display.fbx.fbxModel import FbxModel
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modCommon import eventConfig, modConfig
import mod.client.extraClientApi as clientApi

class FbxBattleAreaModel(FbxModel):
	def __init__(self, eventHandler, eid, config):
		super(FbxBattleAreaModel, self).__init__(eventHandler, eid, config)
		self._data = config.get('data', None)
		self._pos = None
		self._rot = None
		if self._data:
			self._pos = self._data.get('pos', None)
			self._rot = self._data.get('rot', None)
		self.CreateModel()

	def CreateModel(self):
		modelComp = self._modelComp
		modelId = modelComp.CreateFreeModel(self._modelName)
		modelComp.SetModelMaterial(modelId, self._matName)
		pos = self._pos
		if pos:
			modelComp.SetFreeModelPos(modelId, pos[0], pos[1], pos[2])
		rot = self._rot
		if rot:
			modelComp.SetFreeModelRot(modelId, rot[0], rot[1], rot[2])
		modelComp.SetFreeModelBoundingBox(modelId, (-self._scale[0], -self._scale[1], -self._scale[2]), (self._scale[0], self._scale[1], self._scale[2]))
		modelComp.SetExtraUniformValue(modelId, 1, self._color)
		modelComp.SetExtraUniformValue(modelId, 2, (self._scale[0], self._scale[1], self._scale[2], 0.0))
		self._modelId = modelId
		return modelId


	def OnDestroy(self):
		super(FbxBattleAreaModel, self).OnDestroy()
		self.RemoveModel()