# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modClient.ui.baseUI import *
from ScukeConvertTableScript.modClient.ui.uiDef import UIDef
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance

compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
safePath0 = '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix'
safePath = safePath0+'/safezone_screen_panel/root_screen_panel'
levelId = clientApi.GetLevelId()
getConfigData = compFactory.CreateConfigClient(levelId).GetConfigData
setConfigData = compFactory.CreateConfigClient(levelId).SetConfigData
getScreenSize = compFactory.CreateGame(levelId).GetScreenSize


class TableHud(ModBaseUI):
	"""转化桌可拖动UI"""
	def __init__(self, namespace, name, param):
		super(TableHud, self).__init__(namespace, name, param)
		self._screenSize = getScreenSize()
		self._BtnMovePos = None
		self._uiKey = UIDef.UI_TableHud['ui_key']
		self._btnName = "hud_button"
		self._time = 0
		self._markPos = (0, 0)
		self.paramCache = {}
		self.isPushing = False
		self.isInMainScreen = False

	def Create(self):
		super(TableHud, self).Create()
		self._TableBtn =self.GetBaseUIControl(safePath+'/'+self._btnName).asButton()
		self._TableBtn.AddTouchEventParams({"isSwallow": True})
		self._TableBtn.SetButtonTouchMoveCallback(self.OnTableBtnMove)
		self._TableBtn.SetButtonTouchDownCallback(self.OnTableBtnTouchDown)
		self._TableBtn.SetButtonTouchUpCallback(self.OnTableBtnTouchUp)
		self.UIInit()

	def UIInit(self):
		pos = getConfigData(self._uiKey)
		if pos:
			pos = tuple(pos[self._btnName])
			self._TableBtn.SetPosition(pos)
			print '=======Has Set ConfigDataPos %s Successs======= '%self._btnName
		else:
			self.SetPosInSafetyZone(self._TableBtn)
			print '=======Has Set ConfigDataPos %s Fail======= '%self._btnName

	def SetPosInSafetyZone(self,btnCtl):
		size = btnCtl.GetSize()
		safeSize = self.GetSize(safePath)
		safeSize = (safeSize[0]-size[0],safeSize[1]-size[1])
		pos = btnCtl.GetPosition()
		pos = tuple(max(min(safeSize[n], pos[n]), 0)for n in(0, 1))
		btnCtl.SetPosition(pos)
		setConfigData(self._uiKey,{self._btnName:pos})
		return pos

	def OnTableBtnMove(self, args):
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		btn = self._TableBtn
		curPos = btn.GetPosition()
		if self._BtnMovePos:
			RelativeX = posX - self._BtnMovePos[0]
			RelativeY = posY - self._BtnMovePos[1]
			btn.SetPosition((curPos[0] + RelativeX, curPos[1] + RelativeY))
		self._BtnMovePos = (posX,posY)

	def OnTableBtnTouchDown(self, args):
		self._BtnMovePos = None
		self._markPos = (args['TouchPosX'], args['TouchPosY'])

	def OnTableBtnTouchUp(self,args):
		self.SetPosInSafetyZone(self._TableBtn)
		posX,posY = args['TouchPosX'],args['TouchPosY']
		if self.isPushing: return
		if self._markPos and abs(posX - self._markPos[0]) < 3 and abs(posY - self._markPos[1]) < 3:
			self.isPushing = True
			self.SendMsgToServer("TryPushTableMainUI", {"pid": self.mPlayerId})

	def Update(self):
		# 检测分辨率是否变化
		screenSize = getScreenSize()
		if screenSize != self._screenSize:
			if self._TableBtn:
				self.SetPosInSafetyZone(self._TableBtn)
				self._screenSize = screenSize

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def PushTableMainUI(self, args):
		self.paramCache = args
		self.isPushing = False
		self.isInMainScreen = True
		Instance.mUIManager.PushUI(UIDef.UI_TableMain, self.paramCache)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def ResetHudUI(self, args):
		"""重置玩家HudUI位置"""
		safeSize = self.GetSize(safePath)
		safeSize = (safeSize[0]/2,safeSize[1]/2)
		self._TableBtn.SetPosition(safeSize)


	@EngineEvent()
	def OnKeyPressInGame(self, args):
		isDown, key = args["isDown"] is "1", args["key"]
		if key == "86" and not isDown:
			# "V"
			if not self.isInMainScreen:
				engineApiGac.compFactory.CreateGame(self.mPlayerId).SimulateTouchWithMouse(False)
				self.isPushing = True
				self.SendMsgToServer("TryPushTableMainUI", {"pid": self.mPlayerId})
			else:
				clientApi.PopScreen()
