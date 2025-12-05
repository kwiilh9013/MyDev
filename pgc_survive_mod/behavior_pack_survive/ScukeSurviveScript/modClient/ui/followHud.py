# -*- coding: utf-8 -*-
import random
from operator import attrgetter

from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.poolableWidget import PoolableWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()

CompFactory = clientApi.GetEngineCompFactory()

def _npcTalkSorter(followItem):
	return followItem['_order']

class FollowHud(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(FollowHud, self).__init__(namespace, name, param)
		self._npcTalkUpdateTimer = engineApiGac.AddRepeatedTimer(0.5, self.OnNpcTalkUpdate)
		self._posTalkUpdateTimer = engineApiGac.AddRepeatedTimer(0.5, self.OnPosTalkUpdate)
		self._npcTalkMap = {}
		self._posTalkMap = {}

	def Create(self):
		super(FollowHud, self).Create()
		self._followAnchor = self.GetBaseUIControl('/anchor/npc/talk01')
		self._npcTalkPool = PoolableWidget(self, '/anchor/npc', '', '/talk01')
		self._posTalkPool = PoolableWidget(self, '/anchor/pos', '', '/talk01')


	def ShowNpcTalk(self, eid, data, offset=None):
		followItem = self._npcTalkMap.get(eid, None)
		if offset is None:
			entitySize = CompFactory.CreateCollisionBox(eid).GetSize()
			offset = (0, entitySize[1]+0.2, 0)
		if followItem is not None:
			if followItem.get('offset', None) == offset:
				followItem['data'] = data
				followItem['_alpha'] = -1
				followItem['_scale'] = -1
				followItem['_order'] = 0
				return
			else:
				self.HideNpcTalk(eid)
		def _updateFunc(_followItem):
			return lambda bindPos, bindSize: self.OnTalkUpdate(_followItem, bindPos, bindSize)
		ctrlItem = self._npcTalkPool.AddItemCtrl()

		ctrl = ctrlItem['ctrl']
		followItem = {
			'eid': eid,
			'ctrlItem': ctrlItem,
			'data': data,
			'offset': offset,
			'_bg': ctrl.GetChildByPath('/bg').asImage(),
			'_text': ctrl.GetChildByPath('/bg/label').asLabel(),
			'_alpha': -1,
			'_scale': -1,
			'_order': 0,
		}
		bindNode = Instance.mUIManager.CreateBindAnchorByEid(eid, offset, _updateFunc(followItem))
		followItem['bindNode'] = bindNode
		self._npcTalkMap[eid] = followItem

	def HideNpcTalk(self, eid):
		followItem = self._npcTalkMap.get(eid, None)
		if followItem:
			bindNode = followItem['bindNode']
			bindNode.SetRemove()
			ctrlItem = followItem['ctrlItem']
			self._npcTalkPool.RemoveItemCtrl(ctrlItem)
			del self._npcTalkMap[eid]

	def ShowPosTalk(self, pos, dim, data, offset=None):
		key = (pos, dim)
		followItem = self._posTalkMap.get(key, None)
		if offset is None:
			offset = (0, 0.5, 0)
		if followItem is not None:
			if followItem.get('offset', None) == offset:
				followItem['data'] = data
				followItem['_alpha'] = -1
				followItem['_scale'] = -1
				followItem['_order'] = 0
				return
			else:
				self.HidePosTalk(pos, dim)

		def _updateFunc(_followItem):
			return lambda bindPos, bindSize: self.OnTalkUpdate(_followItem, bindPos, bindSize)

		ctrlItem = self._posTalkPool.AddItemCtrl()

		ctrl = ctrlItem['ctrl']
		followItem = {
			'key': key,
			'ctrlItem': ctrlItem,
			'data': data,
			'offset': offset,
			'_bg': ctrl.GetChildByPath('/bg').asImage(),
			'_text': ctrl.GetChildByPath('/bg/label').asLabel(),
			'_alpha': -1,
			'_scale': -1,
			'_order': 0,
		}
		bindNode = Instance.mUIManager.CreateBindAnchorByPos(dim, pos, offset, _updateFunc(followItem))
		followItem['bindNode'] = bindNode
		self._posTalkMap[key] = followItem

	def HidePosTalk(self, pos, dim):
		key = (pos, dim)
		followItem = self._posTalkMap.get(key, None)
		if followItem:
			bindNode = followItem['bindNode']
			bindNode.SetRemove()
			ctrlItem = followItem['ctrlItem']
			self._posTalkPool.RemoveItemCtrl(ctrlItem)
			del self._posTalkMap[key]


	def OnTalkUpdate(self, followItem, bindPos, bindSize):
		scale = MathUtils.Clamp(bindSize[0] / 100.0, 0.5, 2.0)
		alpha = MathUtils.Clamp((bindSize[0] - 20.0) / 50.0, 0.0, 1.0)
		_alpha = followItem['_alpha']
		_scale = followItem['_scale']
		data = followItem['data']
		if data.get('alwaysShow', False):
			alpha = 1.0
		ctrl = followItem['ctrlItem']['ctrl']
		if alpha != _alpha or scale != _scale:
			_bg = followItem['_bg']
			_text = followItem['_text']
			_text.SetText(data['text'])
			_text.SetTextFontSize(scale)
			_text.SetMinSize((1, 1 + random.random()))
			_text.SetAlpha(alpha)
			_bg.SetAlpha(alpha)
		if _alpha > 0.0:
			ctrl.SetPosition(bindPos)
		if _alpha < 0:
			ctrl.SetVisible(True)
		followItem['_alpha'] = alpha
		followItem['_scale'] = scale
		followItem['_order'] = bindSize[1]

	def OnNpcTalkUpdate(self):
		removed = []
		for followItem in self._npcTalkMap.itervalues():
			eid = followItem['eid']
			if engineApiGac.GetEntityFootPos(eid) is None:
				removed.append(eid)
		for eid in removed:
			self.HideNpcTalk(eid)
		# orderList = sorted(self._npcTalkMap.itervalues(), key=_npcTalkSorter)
		# for i in xrange(len(orderList)):
		# 	followItem = orderList[i]
		# 	eid = followItem['eid']
		# 	if engineApiGac.GetEntityFootPos(eid) is not None:
		# 		ctrl = followItem['ctrlItem']['ctrl']
		# 		ctrl.SetLayer((i+1)*3, False, False)
		# 	else:
		# 		self.HideNpcTalk(eid)

	def OnPosTalkUpdate(self):
		pass

	def Destroy(self):
		super(FollowHud, self).Destroy()
		if self._npcTalkUpdateTimer:
			engineApiGac.CancelTimer(self._npcTalkUpdateTimer)
			self._npcTalkUpdateTimer = None
