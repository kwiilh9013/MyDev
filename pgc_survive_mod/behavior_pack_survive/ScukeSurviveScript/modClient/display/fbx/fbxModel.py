# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi


class FbxModelBuilder(object):
	__bindingFbxModel__ = {}

	@staticmethod
	def BindingFbxModel(name, cls):
		FbxModelBuilder.__bindingFbxModel__[name] = cls

	@staticmethod
	def GetFbxModel(eventHandler, eid, config):
		tType = config['type']
		if tType not in FbxModelBuilder.__bindingFbxModel__:
			return FbxModel(eventHandler, eid, config)
		cls = FbxModelBuilder.__bindingFbxModel__[tType]
		return cls(eventHandler, eid, config)

class FbxModel(object):
	def __init__(self, eventHandler, eid, config):
		self._eid = eid
		self._eventHandler = eventHandler
		self._modelName = config['model']
		self._matName = config['mat']
		self._scale = config.get('scale', (1.0, 1.0, 1.0))
		self._color = config.get('color', (1.0, 1.0, 1.0, 1.0))
		self._modelComp = clientApi.GetEngineCompFactory().CreateModel(eid)
		self._posComp = clientApi.GetEngineCompFactory().CreatePos(eid)
		self._modelId = None


	def CreateModel(self):
		modelComp = self._modelComp
		modelId = modelComp.CreateFreeModel(self._modelName)
		modelComp.SetModelMaterial(modelId, self._matName)
		pos = self._posComp.GetFootPos()
		modelComp.SetFreeModelPos(modelId, pos[0], pos[1], pos[2])
		modelComp.SetExtraUniformValue(modelId, 1, self._color)
		modelComp.SetExtraUniformValue(modelId, 2, (self._scale[0], self._scale[1], self._scale[2], 0.0))
		self._modelId = modelId
		return modelId

	def RemoveModel(self):
		if self._modelId is not None:
			self._modelComp.RemoveFreeModel(self._modelId)
			self._modelId = None

	def OnUpdate(self):
		pass

	def OnDestroy(self):
		pass
