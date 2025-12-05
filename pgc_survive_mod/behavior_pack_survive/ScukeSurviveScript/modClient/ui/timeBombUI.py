# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.widget.imageMultiNumberWidget import ImageMultiNumberWidget
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
ViewBinder = clientApi.GetViewBinderCls()


NumberTextures = [
	"textures/ui/scuke_survive/hud/hud_0",
	"textures/ui/scuke_survive/hud/hud_1",
	"textures/ui/scuke_survive/hud/hud_2",
	"textures/ui/scuke_survive/hud/hud_3",
	"textures/ui/scuke_survive/hud/hud_4",
	"textures/ui/scuke_survive/hud/hud_5",
	"textures/ui/scuke_survive/hud/hud_6",
	"textures/ui/scuke_survive/hud/hud_7",
	"textures/ui/scuke_survive/hud/hud_8",
	"textures/ui/scuke_survive/hud/hud_9",
]

TimeShowPath = "/mainPanel/timeShowPanel"
TimeShowChildPath = [
	"/minNum1/num",
	"/minNum2/num",
	"/secNum1/num",
	"/secNum2/num"
]
TimeShowChildPath.reverse()

NumPanel = "/mainPanel/numPanel"
NumBtnMap = {
	"num_1": NumPanel + "/panel1/btn3",
	"num_2": NumPanel + "/panel2/btn3",
	"num_3": NumPanel + "/panel3/btn3",
	"num_4": NumPanel + "/panel1/btn2",
	"num_5": NumPanel + "/panel2/btn2",
	"num_6": NumPanel + "/panel3/btn2",
	"num_7": NumPanel + "/panel1/btn1",
	"num_8": NumPanel + "/panel2/btn1",
	"num_9": NumPanel + "/panel3/btn1",
	"num_0": NumPanel + "/panel2/btn4",
	"delete": NumPanel + "/panel1/btn4",
	"confirm": NumPanel + "/panel3/btn4",
	"close": "/scrBtn"
}


class TimeBombUI(ModBaseUI):
	"""定时炸弹UI"""
	def __init__(self, namespace, name, param):
		super(TimeBombUI, self).__init__(namespace, name, param)
		self.showText = None
		self.btnDict = {}
		self.tempInputNum = ""
		# sec
		self.value = 0

	def Destroy(self):
		pass

	def Create(self):
		self.showText = ImageMultiNumberWidget(self, TimeShowPath, TimeShowChildPath, NumberTextures)
		for key, path in NumBtnMap.items():
			param = {"type": key, "isSwallow": True}
			clientApiMgr.UICreateBtn(self, self.btnDict, key, path, param, self.OnNumBtnPressUp)

	def OnNumBtnPressUp(self, args):
		Type = args['AddTouchEventParams']['type']
		if Type == "close":
			clientApi.PopScreen()
		elif Type == "delete":
			self.tempInputNum = self.tempInputNum[0:-1]
			self.UpdateShowNum(self.tempInputNum)
		elif Type == "confirm":
			clientApi.PopScreen()
			if self.value != 0:
				engineApiGac.SetTipMessage("设置定时时间为%s秒" % self.value)
				self.SetTimeValue()
			else:
				engineApiGac.SetTipMessage("无效的时间")
		elif Type.startswith("num_"):
			num = Type.split("_")[1]
			self.tempInputNum = self.tempInputNum + num
			if len(self.tempInputNum) > 5:
				self.tempInputNum = self.tempInputNum[1:]
			self.UpdateShowNum(self.tempInputNum)
			clientApiMgr.PlayCustomMusic("scuke_survive.block.time_bomb_btn_press", engineApiGac.GetEntityPos(self.mPlayerId), 0.2, 2.0)

	def UpdateShowNum(self, num):
		tLen = len(self.tempInputNum)
		if tLen >= 1:
			num = int(num)
			if num > 5999: num = 5999
			self.value = num
			val = self.InputValueToMinSec(num)
			self.showText.SetNumber(val)
		if tLen == 0:
			self.value = 0
			self.showText.SetNumber(0)

	def InputValueToMinSec(self, num):
		Mins = int(num // 60)
		Secs = int(num % 60)
		return Mins * 100 + Secs

	def SetTimeValue(self):
		"""将倒计时时间设置广播出去"""
		Instance.mEventMgr.NotifyEvent(eventConfig.TimeBombSetTimeEvent, {"value": self.value})
