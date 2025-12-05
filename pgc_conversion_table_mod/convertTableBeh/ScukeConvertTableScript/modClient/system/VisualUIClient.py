# -*- coding: utf-8 -*-

from ScukeConvertTableScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi
from ScukeConvertTableScript.ScukeCore.client import engineApiGac
from ScukeConvertTableScript.ScukeCore.client.api import clientApiMgr
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.modClient.ui.uiDef import UIDef
from ScukeConvertTableScript.ScukeCore.client.localDataMgr import *
import random


class VisualUIClient(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(VisualUIClient, self).__init__(namespace, systemName)
		self._V_Count = 6
		
		self._S_metaVisualUI = False

		self._buyItemList = [] # 玩家最近购买6个物品名称
		self._sellItemList = [] # 玩家最近出售6个物品名称
		self._sortTypeList = [] # 玩家排序整理类型的列表
		self._sellAllItems = 0

		self._VisualList = [] # 储存需要显示的文字列表

		self._VisualText = ""
		self._time = 0

		self._funcTime = 0

	def Destroy(self):
		super(VisualUIClient, self).Destroy()

	def Update(self):
		if self._S_metaVisualUI:
			self._time += 1
			if self._time >= 30:
				self._time = 0
				
				if len(self._buyItemList) > 3:
					self._buyItemList = self._buyItemList[3:]
				if len(self._sellItemList) > 3:
					self._sellItemList = self._sellItemList[3:]
				if len(self._sellItemList) == 3 and len(self._buyItemList) == 3 and (self._sellItemList == self._buyItemList):
					print "买卖3次同样的东西：触发变红"
					self._sellItemList = []
					self._buyItemList = []

					text = "你……小子……是在嘲弄我吗？"
					color = []
					intervalTime = 0.2
					removeTime = 5
					YOffset = []
					funcDic = {
						0:[self.SetVisualUIText],
						5:[self.SetUIAnimaState],
					}
					paramDic = {
						0:[(text, color, intervalTime, removeTime, YOffset)],
						5:[["angry"]],
					}
					self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)
				

				if len(self._sortTypeList) > self._V_Count:
					self._sortTypeList = self._sortTypeList[6:]
					if self.IsAlternateSequence(self._sortTypeList):
						print "来回点击竖直和水平排序共计6次：触发变红"
						self._sortTypeList = []

						text = "你的身边：仿佛出现无尽黑暗的触手……毛骨悚然……"
						YOffset = []
						color = [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)]
						intervalTime = 0.2
						removeTime = 6
						funcDic = {
							0:[self.SetVisualUIText],
							5:[self.SetUIAnimaState],
						}
						paramDic = {
							0:[(text, color, intervalTime, removeTime, YOffset)],
							5:[["angry"]],
						}
						self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)
					
					
		if self._VisualList and self.IsInMainPanel():
			# VisualData = {"fun": funcDic, "param": paramDic, "UiTime": UiTime}
			nowUI = self._VisualList[0]
			funcDic = nowUI["func"]
			paramDic = nowUI["param"]
			if funcDic and self._funcTime in funcDic:
				funcList = funcDic[self._funcTime]
				paramList = paramDic[self._funcTime]
				i = 0
				for func in funcList:
					func(*paramList[i])
					i += 1
			self._funcTime += 1
			nowUI["UiTime"] -= 1
			if nowUI["UiTime"] <= 0:
				self._VisualList.pop(0)
				self._funcTime = 0
		
		# region 监听事件

	# endregion

	# region 同端事件
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TryLeaveTeam(self, args):
		"""离开团队时动效"""
		if self._S_metaVisualUI:
			text = "将一切都支离破碎吧……"
			YOffset = []
			color = [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)]
			intervalTime = 0.2
			removeTime = 4
			funcDic = {
				0:[self.SetVisualUIText],
				5:[self.SetUIAnimaState],
			}
			paramDic = {
				0:[(text, color, intervalTime, removeTime, YOffset)],
				5:[["angry"]],
			}
			self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def RefuseInvite(self, args):
		"""拒绝邀请时动效"""
		if self._S_metaVisualUI:
			text = "真……愚蠢"
			YOffset = []
			color = [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)]
			intervalTime = 0.2
			removeTime = 3
			funcDic = {
				0:[self.SetVisualUIText],
				5:[self.SetUIAnimaState],
			}
			paramDic = {
				0:[(text, color, intervalTime, removeTime, YOffset)],
				5:[["angry"]],
			}
			self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TryInviteTeam(self, args):
		"""发送邀请时……"""
		if self._S_metaVisualUI:
			text = "祭品多多益善……"
			YOffset = []
			color = [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)]
			intervalTime = 0.2
			removeTime = 3.5
			funcDic = {
				0:[self.SetVisualUIText],
				5:[self.SetUIAnimaState],
			}
			paramDic = {
				0:[(text, color, intervalTime, removeTime, YOffset)],
				5:[["angry"]],
			}
			self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def NoInvite(self, args):
		"""接受邀请时动效"""
		if self._S_metaVisualUI:
			text = "你好……新的祭品……"
			YOffset = []
			color = [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)]
			intervalTime = 0.2
			removeTime = 3
			funcDic = {
				0:[self.SetVisualUIText],
				5:[self.SetUIAnimaState],
			}
			paramDic = {
				0:[(text, color, intervalTime, removeTime, YOffset)],
				5:[["angry"]],
			}
			self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def TrySellInvAllItems(self, args):
		"""出售全部物品"""
		if self._S_metaVisualUI:
			if 0 < self._sellAllItems <= 10:
				if random.randint(0,2) == 0:
					text = "等价交换……宇宙的法则……"
					color = []
					intervalTime = 0.2
					removeTime = 5
					YOffset = []
					funcDic = {
						0:[self.SetVisualUIText],
						5:[self.SetUIAnimaState],
					}
					paramDic = {
						0:[(text, color, intervalTime, removeTime, YOffset)],
						5:[["angry"]],
					}
					self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)

			elif 10< self._sellAllItems <= 20:
				if random.randint(0,2) == 0:
					if random.randint(0, 1) == 0:
						text = "人性……是贪婪的……"
						removeTime = 3
					else:
						text = "知道……贤者之石……是怎么炼成的吗？"
						removeTime = 5
					color = []
					intervalTime = 0.2
					YOffset = []
					funcDic = {
						0:[self.SetVisualUIText],
						5:[self.SetUIAnimaState],
					}
					paramDic = {
						0:[(text, color, intervalTime, removeTime, YOffset)],
						5:[["angry"]],
					}
					self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)

			elif 20 <= self._sellAllItems:
				if random.randint(0,2) == 0:
					if random.randint(0, 1) == 0:
						text = "更多……更多……无尽的贪婪"
						removeTime = 4
					else:
						text = "你仿佛感受到了无数双手，向你推向了无尽的深渊……"
						removeTime = 6
					color = []
					intervalTime = 0.2
					YOffset = []
					funcDic = {
						0:[self.SetVisualUIText],
						5:[self.SetUIAnimaState],
					}
					paramDic = {
						0:[(text, color, intervalTime, removeTime, YOffset)],
						5:[["angry"]],
					}
					self.AddVisualUIText(text, color, intervalTime, removeTime, YOffset, funcDic, paramDic)
		self._sellAllItems += 1
	# endregion

	# region 服务端事件
	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def PushTableMainUI(self, args):
		"""只用于获取设置，Meta表现是否开启"""
		globalSetting = args['globalSetting']
		if globalSetting:
			self._S_metaVisualUI = globalSetting['metaVisualUI']

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def UpdateSettingData(self, args):
		"""更新设置"""
		globalSetting = args['data']
		if globalSetting:
			self._S_metaVisualUI = globalSetting['metaVisualUI']

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def HasBuyItem(self, args):
		itemName = args['itemName']
		if len(self._buyItemList) > self._V_Count:
			self._buyItemList = self._buyItemList[self._V_Count:]
		self._buyItemList.append(itemName)
	
	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
	def HasSellItem(self, args):
		itemName = args['itemName']
		if len(self._sellItemList) > self._V_Count:
			self._sellItemList = self._sellItemList[:-1]
		self._sellItemList.append(itemName)

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.PlayInventorySystem)
	def SortInventory(self, args):
		sortType = args['sortType']
		if len(self._sortTypeList) > self._V_Count:
			self._sortTypeList = self._sortTypeList[:-1]
		self._sortTypeList.append(sortType)
	# endregion

	# region 方法
	def AddVisualUIText(self, text, color = [], intervalTime = 0.2, removeTime = 0, YOffset = [], funcDic = {}, paramDic = {}):
		"""添加眼睛上互动文字到列表中,会计算文字消失时间在timeline中进行维护"""
		UiTime = ((len(list(text.decode('utf-8'))) - 1) * intervalTime + removeTime) * 30
		VisualData = {
			"func": funcDic,
			"param": paramDic,
			"UiTime": UiTime
		}
		self._VisualList.append(VisualData)
		

	def SetVisualUIText(self, text, color = [], intervalTime = 0.2, removeTime = 0, YOffset = []):
		"""
		设置眼睛上互动文字
		:param text = 文字 str
		:param color = 每个文字对应的颜色 list
		:param intervalTime 文字出现间隔时间 int
		:param removeTime 文字消失的时间
		"""
		textLen, colorLen = len(list(text.decode('utf-8'))), len(color)
		if textLen < colorLen:
			color = []
			for i in range(textLen):
				color.append((1, 1, 1))
		elif textLen > colorLen:
			for i in range(textLen - colorLen):
				color.append((1, 1, 1))
		lastLen = 0
		if self._VisualText:
			lastLen = len(self._VisualText)
		self._VisualText = text
		data = {
			"text": text,
			"color": color,
			"lastLen": lastLen,
			"intervalTime": intervalTime,
			"removeTime": removeTime,
			"YOffset": YOffset
		}
		self.BroadcastEvent("SetVisualText", data)

	def SetUIAnimaState(self, state):
		"""控制UI动效显示"""
		self.BroadcastEvent("SetVisualUI", {"state": state})

	def IsInMainPanel(self):
		"""是否处于主界面,也即是否可播放动效"""
		topScree = clientApi.GetTopScreen()
		UIDef.UI_TableMain['ui_namespace']
		if topScree and topScree.GetScreenName() == UIDef.UI_TableMain['ui_namespace']:
			return True
		return False
	
	def IsAlternateSequence(self, lst):
		"""
		判断列表是否以间隔排序。
		:param lst: 输入列表
		:return: 如果是间隔排序返回 True，否则返回 False
		"""
		if len(lst) < 2:
			return True  # 少于2个元素一定是间隔排序
		# 假设列表有偶数间隔
		for i in range(len(lst) - 2):
			if lst[i] != lst[i + 2]:
				return False
		return True
	# endregion