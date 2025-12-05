# -*- coding: utf-8 -*-
import time
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modCommon import modConfig
import mod.client.extraClientApi as extraClientApi
import ScukeSurviveScript.ScukeCore.client.engineApiGac as engineApiGac
from ScukeSurviveScript.modCommon.cfg.dialogueNodesConfig import Config as DialogueNodesConfig

OptionBtnPath = [
	'/stack_panel/group0/panel1',
	'/stack_panel/group0/panel2',
	'/stack_panel/group1/panel1',
	'/stack_panel/group1/panel2',
]

class DialogueUI(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(DialogueUI, self).__init__(namespace, name, param)
		self._NextCallback = None
		self._NextOptionNode = None
		self._PhaseConfig = None
		self._NodeConfig = None
		self._UpdateTime = 0.0

	def Create(self):
		super(DialogueUI, self).Create()
		self._OptionPanel = self.GetBaseUIControl('/stack_panel')
		self._OptionBtns = []
		for i in range(0, len(OptionBtnPath)):
			def _selectOptionFunc(index):
				return lambda (args): self.SelectOption(index)
			panelCtrl = self.GetBaseUIControl(OptionBtnPath[i])
			btnCtrl = panelCtrl.GetChildByName('button').asButton()
			btnCtrl.AddTouchEventParams({"isSwallow": True})
			btnCtrl.SetButtonTouchUpCallback(_selectOptionFunc(i))
			self._OptionBtns.append({
				'panel': panelCtrl,
				'button': btnCtrl
			})
		self._OutterBtn = self.GetBaseUIControl('/outter').asButton()
		self._OutterBtn.AddTouchEventParams({"isSwallow": True})
		self._OutterBtn.SetButtonTouchUpCallback(self.GotoNextPhase)
		self._AvatarImg = self.GetBaseUIControl('/panel/avatar/image').asImage()
		self._AvatarName = self.GetBaseUIControl('/panel/avatar_bg/avatar_name').asLabel()
		self._DialogueContent = self.GetBaseUIControl('/panel/dialogue_content').asLabel()
		self._ContinueIcon = self.GetBaseUIControl('/panel/continue')

		self.UpdateDialogueNodeDisplay()
		self.UpdateDialoguePhaseDisplay()
		self.UpdateDialogueOptionDisplay()

	def SelectOption(self, index):
		if self._NextCallback:
			self._NextCallback(self._NextOptionNode[index])

	def GotoNextPhase(self, args):
		if time.time() - self._UpdateTime < 0.5:
			return
		hasOption = self._NextOptionNode and len(self._NextOptionNode) > 0
		if hasOption:
			return
		if self._NextCallback:
			self._NextCallback('-1')

	def SetDialogueNodeData(self, nodeConfig):
		self._NodeConfig = nodeConfig
		if self.Inited:
			self.UpdateDialogueNodeDisplay()

	def UpdateDialogueNodeDisplay(self):
		if self._NodeConfig is None:
			return
		avatar = self._NodeConfig.get('avatar', None)
		if avatar is not None:
			self._AvatarImg.SetSprite(avatar)
		name = self._NodeConfig.get('name', None)
		if name is not None:
			self._AvatarName.SetText(name)

	def SetDialogueData(self, phase, next, nextCallback):
		self._NextCallback = nextCallback
		self._NextOptionNode = next
		self._PhaseConfig = phase
		if self.Inited:
			self.UpdateDialoguePhaseDisplay()
			self.UpdateDialogueOptionDisplay()

	def UpdateDialoguePhaseDisplay(self):
		self._UpdateTime = time.time()
		self._UpdateDialoguePhaseDisplay(self._PhaseConfig)

	def _UpdateDialoguePhaseDisplay(self, config):
		import random
		if not config:
			return
		phaseType = config['type']
		if phaseType == 'text':
			self.UpdatePhaseTextDisplay(config)
		elif phaseType == 'random':
			phases = config['phases']
			r = random.random() * 100
			w = 0
			for _config in phases:
				w += _config['weight']
				if r <= w:
					self._UpdateDialoguePhaseDisplay(_config)
					return

	def UpdatePhaseTextDisplay(self, config):
		self._DialogueContent.SetText(config['text'])


	def UpdateDialogueOptionDisplay(self):
		active = self._NextOptionNode and len(self._NextOptionNode) > 0
		self._ContinueIcon.SetVisible(not active)
		if not active:
			self._OptionPanel.SetVisible(False)
			return
		for i in range(0, len(self._OptionBtns)):
			enabled = False
			if i < len(self._NextOptionNode):
				node = self._NextOptionNode[i]
				nodeConfig = node
				if type(node) is str:
					nodeConfig = DialogueNodesConfig.get(node, None)
				if nodeConfig:
					text = nodeConfig.get('text', 'None')
					button = self._OptionBtns[i]['button']
					button.GetChildByPath('/button_label').asLabel().SetText(text)
					enabled = True
			self._OptionBtns[i]['panel'].SetVisible(enabled)
		if active != self._OptionPanel.GetVisible():
			self._OptionPanel.SetVisible(active)
