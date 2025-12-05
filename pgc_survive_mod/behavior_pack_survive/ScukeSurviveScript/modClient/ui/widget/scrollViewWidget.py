# -*- coding: utf-8 -*-
import time
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.ui.baseWidget import BaseWidget
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon.handler.tweenHandler import TweenHandler
from ScukeSurviveScript.modCommon import modConfig


class ScrollViewWidget(BaseWidget):

	def __init__(self, baseUI, path, contentPath, direct=1):
		super(ScrollViewWidget, self).__init__(baseUI, path)
		self._direct = direct
		self._container = self.GetBaseUIControl('')
		self._contentCtrl = self.GetBaseUIControl(contentPath).asButton()
		self._contentCtrl.AddTouchEventParams({"isSwallow": True})
		self._contentCtrl.SetButtonTouchUpCallback(self.OnContentUp)
		self._contentCtrl.SetButtonTouchCancelCallback(self.OnContentUp)
		self._contentCtrl.SetButtonTouchMoveCallback(self.OnContentMove)
		self._contentCtrl.SetButtonTouchDownCallback(self.OnContentDown)
		self._contentMovePos = None
		self._tweenHandler = None
		self._clickDownInfo = None
		self._clickInfo = None
		self._moveAcc = (0, 0)
		# 如果是电脑端，则适配滚轮
		self._isWin = clientApiMgr.IsWinPlatform()
		self._hoverInPos = None
		if self._isWin:
			self._contentCtrl.AddHoverEventParams()
			self._contentCtrl.SetButtonHoverInCallback(self.OnContentHoverIn)
			self._contentCtrl.SetButtonHoverOutCallback(self.OnContentHoverOut)
			self._clientSystem = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
			self._clientSystem.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "MouseWheelClientEvent", self, self.OnMouseWheelClientEvent)
		pass

	def Destroy(self):
		if self._isWin:
			if self._clientSystem:
				self._clientSystem.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "MouseWheelClientEvent", self, self.OnMouseWheelClientEvent)
			self._clientSystem = None
		return super(ScrollViewWidget, self).Destroy()

	@property
	def Direct(self):
		return self._direct

	@property
	def Position(self):
		return self._contentCtrl.GetPosition()

	def Update(self):
		if self._tweenHandler:
			self._tweenHandler.Update()

	def GetPivotPos(self, size, contentSize):
		pivot = (0.0, 0.0)
		pivotFrom = str(self._contentCtrl.GetAnchorFrom())
		reverse = False
		if pivotFrom.find('right') > -1:
			pivot = (size[0] - contentSize[0], pivot[1])
			reverse = True
		if pivotFrom.find('bottom') > -1:
			pivot = (pivot[0], size[1] - contentSize[1])
			reverse = True
		return pivot, reverse

	def GetMinMaxPos(self, size, contentSize):
		pivot, reverse = self.GetPivotPos(size, contentSize)
		if reverse:
			minPos = pivot
			maxPos = MathUtils.TupleAdd(MathUtils.TupleSub(pivot, size), contentSize)
		else:
			maxPos = pivot
			minPos = MathUtils.TupleSub(MathUtils.TupleAdd(pivot, size), contentSize)
		return minPos, maxPos

	def OnContentUp(self, args):
		btn = self._contentCtrl
		size = self._container.GetSize()
		contentSize = btn.GetSize()
		minPos, maxPos = self.GetMinMaxPos(size, contentSize)
		curPos = btn.GetPosition()
		targetX = curPos[0]
		targetY = curPos[1]
		tweenScroll = False
		if targetX < minPos[0] or targetX > maxPos[0]:
			targetX = MathUtils.Clamp(targetX, minPos[0], maxPos[0])
			tweenScroll = True
		if targetY < minPos[1] or targetY > maxPos[1]:
			targetY = MathUtils.Clamp(targetY, minPos[1], maxPos[1])
			tweenScroll = True
		mouseWheel = args.get('OnMouseWheel', False)
		isClick = False
		if self._clickDownInfo and not mouseWheel:
			deltaTime = time.time()-self._clickDownInfo['time']
			posX = args['TouchPosX']
			posY = args['TouchPosY']
			touchPos = (posX, posY)
			deltaPos = MathUtils.TupleSub(touchPos, self._clickDownInfo['pos'])
			if deltaTime < 0.3 and MathUtils.TupleLength(deltaPos) < 3:
				offset = self._container.GetGlobalPosition()
				contentOffset = self._contentCtrl.GetGlobalPosition()
				deltaOffset = MathUtils.TupleSub(touchPos, offset)
				contentPos = MathUtils.TupleSub(deltaOffset, MathUtils.TupleSub(contentOffset, offset))
				self._clickInfo = {
					'pos': contentPos,
					'touchPos': touchPos,
				}
				isClick = True
		if tweenScroll:
			self.DoTweenScroll(curPos, (targetX, targetY))
		elif not isClick and not mouseWheel:
			if self._direct == 1:
				accY = MathUtils.Clamp(targetY+MathUtils.Clamp(self._moveAcc[1]/10.0, -1.0, 1.0) * 50, minPos[1], maxPos[1])
				self.DoTweenScroll(curPos, (targetX, accY), 0.5)
			elif self._direct == 2:
				accX = MathUtils.Clamp(targetX+MathUtils.Clamp(self._moveAcc[0]/10.0, -1.0, 1.0) * 50, minPos[0], maxPos[0])
				self.DoTweenScroll(curPos, (accX, targetY), 0.5)
		self._contentMovePos = None

	def FlushClickInfo(self):
		ret = self._clickInfo
		self._clickInfo = None
		return ret

	def OnContentDown(self, args):
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		self._clickDownInfo = {
			'time': time.time(),
			'pos': (posX, posY)
		}

	def OnContentMove(self, args):
		btn = self._contentCtrl
		posX = args['TouchPosX']
		posY = args['TouchPosY']
		size = self._container.GetSize()
		contentSize = btn.GetSize()
		overSize = (min(size[0], contentSize[0]), min(size[1], contentSize[1]))
		if args.get('OnMouseWheel', False):
			overSize = (0, 0)
		overScroll = MathUtils.TupleMul(overSize, 0.5)
		minPos, maxPos = self.GetMinMaxPos(size, contentSize)
		if minPos[0] > maxPos[0]:
			minPos = (0, minPos[1])
			maxPos = (0, maxPos[1])
		if minPos[1] > maxPos[1]:
			minPos = (minPos[0], 0)
			maxPos = (maxPos[0], 0)
		maxPosWithOver = MathUtils.TupleAdd(maxPos, overScroll)
		minPosWithOver = MathUtils.TupleSub(minPos, overScroll)
		if self._contentMovePos:
			deltaX = posX - self._contentMovePos[0]
			deltaY = posY - self._contentMovePos[1]
			self._moveAcc = (deltaX, deltaY)
			curPos = btn.GetPosition()
			if self._direct != 1:  # 垂直
				deltaY = 0
			if self._direct != 2:  # 水平
				deltaX = 0
			curPosX = curPos[0] + deltaX
			curPosY = curPos[1] + deltaY
			if self._direct == 1:
				curPosY = MathUtils.Clamp(curPosY, minPosWithOver[1], maxPosWithOver[1])
			if self._direct == 2:
				curPosX = MathUtils.Clamp(curPosX, minPosWithOver[0], maxPosWithOver[0])
			btn.SetPosition((curPosX, curPosY))
			self._tweenHandler = None
		self._contentMovePos = (posX, posY)
		pass

	def DoTweenScroll(self, fromPos, toPos, duration=0.1):
		self._tweenHandler = TweenHandler('easeOutQuad', duration, fromPos, toPos, self.TweenScrollUpdate, self.TweenScrollEnd)

	def TweenScrollUpdate(self, value):
		self._contentCtrl.SetPosition(value)

	def TweenScrollEnd(self):
		self._tweenHandler = None

	def ScrollTo(self, pos, duration):
		btn = self._contentCtrl
		curPos = btn.GetPosition()
		targetX = pos[0]
		targetY = pos[1]
		size = self._container.GetSize()
		contentSize = btn.GetSize()
		minPos, maxPos = self.GetMinMaxPos(size, contentSize)
		if targetX < minPos[0] or targetX > maxPos[0]:
			targetX = MathUtils.Clamp(targetX, minPos[0], maxPos[0])
		if targetY < minPos[1] or targetY > maxPos[1]:
			targetY = MathUtils.Clamp(targetY, minPos[1], maxPos[1])
		self.DoTweenScroll(curPos, (targetX, targetY), duration)
	
	# region PC操作，滚轮
	def OnMouseWheelClientEvent(self, args):
		"""滚轮滚动事件"""
		if self._hoverInPos:
			delta = 10
			direction = args.get("direction")
			if direction == 0:
				delta = -delta
			self._hoverInPos[0] += delta
			self._hoverInPos[1] += delta
			self.OnContentMove({"TouchPosX": self._hoverInPos[0], "TouchPosY": self._hoverInPos[0], "OnMouseWheel": True})
		pass

	def OnContentHoverIn(self, args):
		self._hoverInPos = [args["TouchPosX"], args["TouchPosY"]]
		pass

	def OnContentHoverOut(self, args):
		if self._hoverInPos:
			args["TouchPosX"] = self._hoverInPos[0]
			args["TouchPosY"] = self._hoverInPos[1]
			args["OnMouseWheel"] = True
			self.OnContentUp(args)
		self._hoverInPos = None
		pass
	# endregion
