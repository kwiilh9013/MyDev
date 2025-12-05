# -*- coding: utf-8 -*-

from ScukeSurviveScript.ScukeCore.common.log.logManager import LogManager
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.dialogueConfig import Config as DialogueConfig
from ScukeSurviveScript.modCommon.handler.dialogueHandler import DialogueHandler


class DialogueClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(DialogueClientSystem, self).__init__(namespace, systemName)
		self._curDialogue = None
		self._curDialogueNodeConfig = None
		self._dialogueContext = {}
		self._dialogueUI = None

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def OnDialogueData(self, data):
		self._dialogueContext = data

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def OpenDialogue(self, data):
		self.SetDialogueDisplay(False)  # 关闭确保当前无进行对话
		config = DialogueConfig.get(data['identifier'], None)
		if not config:
			return
		self._curDialogue = DialogueHandler(self._dialogueContext, data['entityId'], data['entryId'])
		self.DialogueNextPhase()

	@AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.DialogueServerSystem)
	def NextDialogue(self, data):
		if not self._curDialogue:
			return
		self._curDialogue.ChangeNode(data['entryId'], data.get('override', None))
		self.DialogueNextPhase()

	def SetDialogueDisplay(self, active, phaseData=None, nextNodeData=None, curNodeData=None):
		if active:
			if self._dialogueUI is None:
				self._dialogueUI = Instance.mUIManager.PushUI(UIDef.UI_DialogueUI)
			if curNodeData:
				self._dialogueUI.SetDialogueNodeData(curNodeData)
			self._dialogueUI.SetDialogueData(phaseData, nextNodeData, self.DialogueNextPhase)
		else:
			if self._dialogueUI:
				Instance.mUIManager.PopUI()
			self._dialogueUI = None

	def DialogueNextPhase(self, selectNode='-1'):
		if self._curDialogue is None:
			return
		phase = self._curDialogue.Update()
		if phase is None and self._curDialogue.Ended():
			index = -1
			if type(selectNode) is dict:
				index = selectNode['_index']
				selectNode = selectNode['_template']
			info = {
				'playerId': self.mPlayerId,
				'nodeId': selectNode,
				'index': index,
			}
			self.NotifyToServer('OnDialogueNodeNext', info)
			if selectNode == '-1':
				self.SetDialogueDisplay(False)
				self._curDialogueNodeConfig = None
			return
		isLast, next = self._curDialogue.IsLastPhase()
		curNodeConfig = self._curDialogue.NodeConfig
		nodeChanged = curNodeConfig != self._curDialogueNodeConfig
		self.SetDialogueDisplay(True, phase, next, curNodeConfig if nodeChanged else None)
		self._curDialogueNodeConfig = self._curDialogue.NodeConfig
