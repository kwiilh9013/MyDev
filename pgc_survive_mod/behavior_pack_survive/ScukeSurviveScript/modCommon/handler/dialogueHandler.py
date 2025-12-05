# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.dialogueNodesConfig import Config as DialogueNodesConfig


class DialogueHandler(object):
	def __init__(self, context, entityId, nodeId):
		self._context = context
		self._entityId = entityId
		self._entryNodeId = nodeId
		self._startNodeId = nodeId
		self._nextNodeId = nodeId
		self._currentNodeId = '-1'
		self._currentNode = None
		self._currentNodeIndex = -1
		self._overrideConfig = None

	@property
	def NodeId(self):
		return self._currentNodeId

	@property
	def EntryNodeId(self):
		return self._entryNodeId

	@property
	def EntityId(self):
		return self._entityId

	@property
	def NodeConfig(self):
		return self._currentNode

	def Update(self, nextNodeId=None):
		if nextNodeId is None:
			nextNodeId = self._startNodeId
		if self._currentNodeId == nextNodeId:
			if self._currentNode and self._currentNodeIndex >= 0:
				phases = self._currentNode['phases']
				self._currentNodeIndex += 1
				if self._currentNodeIndex < len(phases):
					return phases[self._currentNodeIndex]
				else:
					self._currentNodeIndex = -1
			return None
		nodeConfig = DialogueNodesConfig.get(nextNodeId, None)
		if not nodeConfig:
			return None
		self._currentNodeId = nextNodeId
		self._currentNode = self._CombineOverride(nodeConfig)
		self._currentNodeIndex = 0
		return self._currentNode['phases'][self._currentNodeIndex]

	def _CombineOverride(self, config):
		if self._overrideConfig is None:
			return config
		for k in config:
			if k not in self._overrideConfig:
				self._overrideConfig[k] = config[k]
		return self._overrideConfig


	def ChangeNode(self, nodeId, overrideConfig=None):
		self._startNodeId = nodeId
		self._overrideConfig = overrideConfig

	def StartEventData(self):
		if self._currentNode is None:
			return None
		return self._currentNode['startEventData']

	def EndEventData(self):
		if self._currentNode is None:
			return None
		return self._currentNode['endEventData']

	def IsLastPhase(self):
		if self._currentNode is None:
			return False, None
		phases = self._currentNode['phases']
		if self._currentNodeIndex+1 >= len(phases):
			return True, self._currentNode.get('next', None)
		return False, None

	def Ended(self):
		return self._currentNodeIndex == -1