# -*- coding: utf-8 -*-
import time

from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.baseUI import ModBaseUI
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
from ScukeSurviveScript.modClient.ui.widget.bannerViewWidget import BannerViewWidget
from ScukeSurviveScript.modClient.ui.widget.gridTaskGroupWidget import GridTaskGroupWidget
from ScukeSurviveScript.modClient.ui.widget.listViewWidget import ListViewWidget
from ScukeSurviveScript.modClient.ui.widget.safeAreaWidget import SafeAreaWidget
from ScukeSurviveScript.modClient.ui.widget.scrollViewWidget import ScrollViewWidget
from ScukeSurviveScript.modClient.ui.widget.tabViewWidget import TabViewWidget
from ScukeSurviveScript.modCommon import modConfig
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.modCommon.cfg.taskConfig import GetTaskConfig
from ScukeSurviveScript.modCommon.defines.phaseTagEnum import PhaseTagEnum

ViewBinder = clientApi.GetViewBinderCls()

SubTaskGroupData = [
	{'name': '生存', 'group': 'living'},
	{'name': '装备', 'group': 'weapon'},
	{'name': '讨伐', 'group': 'against'},
	{'name': '制造', 'group': 'building'},
	{'name': '载具', 'group': 'vehicle'},
]
mainTaskContentPath = '/panel/content/pages/main_task/scroll_content/main_planet_task'
MainTaskInfo = [
	{'path': mainTaskContentPath + '/phase1', 'name': PhaseTagEnum.Mars, 'size': (150, 150), 'rail': True},
	{'path': mainTaskContentPath + '/phase2', 'name': PhaseTagEnum.AsteroidBelt, 'size': (150, 1200), 'rail': False},
	{'path': mainTaskContentPath + '/phase3', 'name': PhaseTagEnum.Jupiter, 'size': (150, 150), 'rail': True},
	{'path': mainTaskContentPath + '/phase4', 'name': PhaseTagEnum.Saturn, 'size': (300, 150), 'rail': True},
	{'path': mainTaskContentPath + '/phase5', 'name': PhaseTagEnum.Uranus, 'size': (150, 150), 'rail': True},
	{'path': mainTaskContentPath + '/phase6', 'name': PhaseTagEnum.Neptune, 'size': (150, 150), 'rail': True},
]
RailPoints = [
	{'path': mainTaskContentPath + '/phase0', 'name': '_earth_'},
	{'path': mainTaskContentPath + '/phase1', 'name': PhaseTagEnum.Mars},
	{'path': mainTaskContentPath + '/phase2', 'name': PhaseTagEnum.AsteroidBelt},
	{'path': mainTaskContentPath + '/phase3', 'name': PhaseTagEnum.Jupiter},
]


class TasksUI(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(TasksUI, self).__init__(namespace, name, param)

	def Create(self):
		super(TasksUI, self).Create()
		self._CloseBtn = self.GetBaseUIControl('/panel/head/close_btn').asButton()
		self._CloseBtn.AddTouchEventParams({"isSwallow": True})
		self._CloseBtn.SetButtonTouchUpCallback(self.Close)
		self._phaseClientSystem = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.PhaseClientSystem)
		self._taskClientSystem = clientApi.GetSystem(modConfig.ModNameSpace, modConfig.ClientSystemEnum.TaskClientSystem)
		# 漂流地球
		self._earthRailPoints = []
		self._earthPoint = self.GetBaseUIControl(mainTaskContentPath + '/phase0/earthPoint').asImage()
		# Tab
		self._taskBranchIndex = -1
		self._mainTaskData = []
		self._mainTaskInfoIndex = -1
		self._tabView = TabViewWidget(self, '/panel', [
			'/head/tabs/main_task',
			'/head/tabs/sub_task',
		], [
			'/content/pages/main_task',
			'/content/pages/sub_task',
		], self.OnTabChange)

		self._mainTaskPanel = self.GetBaseUIControl('/panel/content/pages/main_task/scroll_content')
		self._mainTaskScrollView = ScrollViewWidget(self, '/panel/content/pages/main_task', '/scroll_content', 2)
		# 主线任务详情
		self._mainTaskInfoPanel = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info')
		self._mainTaskInfoPanelBannerView = BannerViewWidget(self, '/panel/content/pages/main_task/main_task_info', '/banner', self.OnBannerItemActive, self.OnBannerItemChange, 2)
		self._mainTaskInfoPanelName = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info/content/detail/name').asLabel()
		self._mainTaskInfoPanelInfo = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info/content/detail/info').asLabel()
		self._mainTaskInfoPanelDetail = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info/content/detail')
		mainTaskDetailRewardsPath = '/panel/content/pages/main_task/main_task_info/content/detail/stack_panel/rewards'
		self._mainTaskInfoPanelRewardScrollView = ScrollViewWidget(self, mainTaskDetailRewardsPath, '/scroll_content', 2)
		self._mainTaskInfoPanelRewardListView = ListViewWidget(self, mainTaskDetailRewardsPath, '/scroll_content/rewards', '/scroll_content/rewards/item', self.OnTaskInfoRewardsItemActive, self.OnRewardItemClick, self._mainTaskInfoPanelRewardScrollView, 0)
		self._mainTaskInfoCloseBtn = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info/button').asButton()
		self._mainTaskInfoCloseBtn.AddTouchEventParams({"isSwallow": True})
		self._mainTaskInfoCloseBtn.SetButtonTouchUpCallback(lambda args: self.SetMainTaskInfoActive(False))
		self._mainTaskInfoPanelBannerPrev = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info/prev').asButton()
		self._mainTaskInfoPanelBannerPrev.AddTouchEventParams({"isSwallow": True})
		self._mainTaskInfoPanelBannerPrev.SetButtonTouchUpCallback(lambda args: self.OnBannerMove(-1))
		self._mainTaskInfoPanelBannerNext = self.GetBaseUIControl('/panel/content/pages/main_task/main_task_info/next').asButton()
		self._mainTaskInfoPanelBannerNext.AddTouchEventParams({"isSwallow": True})
		self._mainTaskInfoPanelBannerNext.SetButtonTouchUpCallback(lambda args: self.OnBannerMove(1))

		# 支线任务
		self._subTaskPageData = []
		self._taskDisplayType = None
		self._taskGroupIndex = -1
		# 支线任务TabPage页面Top
		self._subTaskPageName = self.GetBaseUIControl('/panel/content/pages/sub_task/sub_task_pages/panel_top/group_name').asLabel()
		self._subTaskPageProgress = self.GetBaseUIControl('/panel/content/pages/sub_task/sub_task_pages/panel_top/progress').asLabel()

		# 任务宫格
		self._gridItemSelected = None
		self._subTaskGridData = []
		self._subTaskGridWidgetMap = {}
		gridTaskPath = '/panel/content/pages/sub_task/sub_task_pages/panel/grid_task'
		self._subTaskGridScrollView = ScrollViewWidget(self, gridTaskPath, '/scroll_content', 2)
		self._subTaskGridListView = ListViewWidget(self, gridTaskPath, '/scroll_content/tasks', '/scroll_content/tasks/group', self.OnTaskGridGroupActive, self.OnTaskGridGroupClick, self._subTaskGridScrollView, 20)

		# 任务列表
		self._listItemSelected = -1
		listTaskPath = '/panel/content/pages/sub_task/sub_task_pages/panel/list_task'
		self._subTaskListScrollView = ScrollViewWidget(self, listTaskPath, '/scroll_content', 1)
		self._subTaskListView = ListViewWidget(self, listTaskPath,'/scroll_content/tasks', '/scroll_content/tasks/item', self.OnTaskListItemActive, self.OnTaskListItemClick, self._subTaskListScrollView, 5)

		# 支线任务TabPage页面Bottom
		self._subTaskDisplayTabView = TabViewWidget(self, '/panel/content/pages/sub_task/sub_task_pages', [
			'/panel_bottom/tabsbg/tabs/grid',
			'/panel_bottom/tabsbg/tabs/list'
		], [
			'/panel/grid_task',
			'/panel/list_task',
		], self.OnSubTaskDisplayTabChange)
		self._subTaskTakeAll = self.GetBaseUIControl(
			'/panel/content/pages/sub_task/sub_task_pages/panel_bottom/button').asButton()
		self._subTaskTakeAll.AddTouchEventParams({"isSwallow": True})
		self._subTaskTakeAll.SetButtonTouchUpCallback(self.OnTakeAllTaskRewards)
		# 支线任务Tab
		self._subTaskTabView = TabViewWidget(self, '/panel/content/pages/sub_task', [
			'/sub_task_tabs/stack_panel/living',
			'/sub_task_tabs/stack_panel/weapon',
			'/sub_task_tabs/stack_panel/against',
			'/sub_task_tabs/stack_panel/building',
			'/sub_task_tabs/stack_panel/vehicle',
		], None, self.OnSubTaskTabChange)

		# 任务领取事件
		self.ListenForEvent(modConfig.ServerSystemEnum.TaskServerSystem, 'OnTakeTaskRewards', self, self.OnTakeTaskRewards)
		self.ListenForEvent(modConfig.ServerSystemEnum.TaskServerSystem, 'OnTakeAllTaskRewards', self, self.OnTakeTaskRewards)
		# 任务 列表item 点击详情
		self._listItemInfoPanel = self.GetBaseUIControl('/list_task_info_panel').asButton()
		self._listItemInfoPanel.AddTouchEventParams({"isSwallow": True})
		self._listItemInfoPanel.SetButtonTouchUpCallback(lambda args: self.SetListItemTaskInfoActive(False))
		self._listItemInfoPanelName = self.GetBaseUIControl('/list_task_info_panel/detail/name').asLabel()
		self._listItemInfoPanelInfo = self.GetBaseUIControl('/list_task_info_panel/detail/info').asLabel()
		listDetailRewardsPath = '/list_task_info_panel/detail/rewards'
		self._listItemInfoPanelRewardScrollView = ScrollViewWidget(self, listDetailRewardsPath, '/scroll_content', 2)
		self._listItemInfoPanelRewardListView = ListViewWidget(self, listDetailRewardsPath, '/scroll_content/rewards', '/scroll_content/rewards/item', self.OnTaskInfoRewardsItemActive, self.OnRewardItemClick, self._listItemInfoPanelRewardScrollView, 1)
		# 任务 grid item 点击详情
		self._gridItemInfoSafeAreaWidget = SafeAreaWidget(self, '/grid_task_info_panel', '/detail')
		self._gridItemInfoPanel = self.GetBaseUIControl('/grid_task_info_panel').asButton()
		self._gridItemInfoPanel.AddTouchEventParams({"isSwallow": True})
		self._gridItemInfoPanel.SetButtonTouchUpCallback(lambda args: self.SetGridItemTaskInfoActive(False))
		self._gridItemInfoPanelDetail = self.GetBaseUIControl('/grid_task_info_panel/detail')
		self._gridItemInfoPanelName = self.GetBaseUIControl('/grid_task_info_panel/detail/name').asLabel()
		self._gridItemInfoPanelInfo = self.GetBaseUIControl('/grid_task_info_panel/detail/info').asLabel()
		gridDetailRewardsPath = '/grid_task_info_panel/detail/stack_panel/rewards'
		self._gridItemInfoPanelRewardScrollView = ScrollViewWidget(self, gridDetailRewardsPath, '/scroll_content', 2)
		self._gridItemInfoPanelRewardListView = ListViewWidget(self, gridDetailRewardsPath, '/scroll_content/rewards', '/scroll_content/rewards/item', self.OnTaskInfoRewardsItemActive, self.OnRewardItemClick, self._gridItemInfoPanelRewardScrollView, 1)

	def UpdateMainTaskDisplay(self):
		i = 0
		pahseInfo = self._phaseClientSystem.PhaseInfo
		phaseTag = pahseInfo['phase']['tag']
		while i < len(MainTaskInfo):
			taskItem = MainTaskInfo[i]
			taskData = self._mainTaskData[i]

			ctrl = self.GetBaseUIControl(taskItem['path'])
			btn = ctrl.GetChildByPath('/' + taskItem['name']).asButton()
			btn.AddTouchEventParams({"isSwallow": True})

			stateDefault = btn.GetChildByPath('/desc/default')
			statePending = btn.GetChildByPath('/desc/pending')

			pending = taskItem['name'] == phaseTag
			stateDefault.SetVisible(not pending)
			statePending.SetVisible(pending)

			def _mainTaskInfoFunc(item, index, data):
				return lambda (args): self.OnMainTaskInfoClick(item, index, data)

			btn.SetButtonTouchUpCallback(_mainTaskInfoFunc(taskItem, i, taskData))
			if self._mainTaskInfoIndex == i:
				self.SetMainTaskInfoActive(True, taskItem, i, taskData)
			i += 1
		i = 1
		p = -1
		while i < len(RailPoints):
			item = RailPoints[i]
			if item['name'] == phaseTag:
				p = i-1
				break
			i += 1
		if p >= 0:
			nextPhaseDays = pahseInfo['nextPhaseDays']
			phaseDays = pahseInfo['phaseDays']
			t = float(phaseDays)/(phaseDays+nextPhaseDays)
			pos = MathUtils._CubicSplineLerp(self._earthRailPoints, p, t)
			self._earthPoint.SetPosition((pos[0]-10, pos[1]-30))
		self._earthPoint.SetVisible(p >= 0)


	def BuildMainTaskData(self):
		mainTaskData, pendingCount, completedCount, receivedCount, totalCount = self._taskClientSystem.FilterTaskDataByGroup(
			'main', None)
		ret = []
		for taskItem in MainTaskInfo:
			taskData = None
			for task in mainTaskData:
				config = GetTaskConfig(task['uid'])
				if config['group'] == taskItem['name']:
					taskData = task
					break
			ret.append(taskData)
		self._earthRailPoints = []
		for pointItem in RailPoints:
			point = self.GetBaseUIControl(pointItem['path']+'/point')
			pos = point.GetGlobalPosition()
			self._earthRailPoints.append((pos[0], pos[1], 0))
		self._mainTaskData = ret

	def OnTabChange(self, prev, current):
		if current == 0:
			self.BuildMainTaskData()
			self.UpdateMainTaskDisplay()
		elif current == 1:
			self.OnSubTaskTabChange(-1, self._taskGroupIndex)
		self._taskBranchIndex = current

	def OnSubTaskTabChange(self, prev, current):
		curGroup = SubTaskGroupData[current]
		self._subTaskPageData, pendingCount, completedCount, receivedCount, totalCount = self._taskClientSystem.FilterTaskDataByGroup('sub', curGroup['group'])
		'''
		ret = []
		for i in range(0,2):
			for item in self._subTaskPageData:
				ret.append(item)
		self._subTaskPageData = ret
		'''

		if self._taskDisplayType == 'grid':
			self.BuildSubTaskGridDisplay()
		elif self._taskDisplayType == 'list':
			self.BuildSubTaskListDisplay()

		self._subTaskPageName.SetText(curGroup['name'])
		self._subTaskPageProgress.SetText('%d/%d' % (completedCount+receivedCount, totalCount))
		self._subTaskTakeAll.SetVisible(completedCount > 0)
		self._taskGroupIndex = current

	def OnSubTaskDisplayTabChange(self, prev, current):
		if current == 0:
			self._taskDisplayType = 'grid'
			self.BuildSubTaskGridDisplay()
		elif current == 1:
			self._taskDisplayType = 'list'
			self.BuildSubTaskListDisplay()

	def OnTaskItemTakeRewards(self, uid):
		self._taskClientSystem.TakeTaskRewards(uid)

	def OnTakeAllTaskRewards(self, args):
		ret = []
		for item in self._subTaskPageData:
			tType = item['type']
			if tType == 'completed':
				ret.append(item['uid'])
		self._taskClientSystem.TakeAllTaskRewards(ret)


	def GridBoxFilter(self, item):
		config = GetTaskConfig(item['uid'])
		return config['level'] > 1, config.get('levelGroup', 1000)

	def BuildSubTaskGridDisplay(self):
		self._subTaskGridData = GridTaskGroupWidget.SplitGridMapData(self._subTaskPageData, self.GridBoxFilter)
		self._subTaskGridListView.UpdateData(self._subTaskGridData)

	def BuildSubTaskListDisplay(self):
		self._subTaskListView.UpdateData(self._subTaskPageData)

	def SetListItemTaskInfoActive(self, active, data=None):
		if data:
			config = GetTaskConfig(data['uid'])
			name = config['desc']
			info = config['info']
			rewards = config['rewards']
			rewardsData = []
			for k in rewards:
				rewardsData.append({
					'identifier': k,
					'count': rewards[k]
				})
			self._listItemInfoPanelName.SetText(name)
			self._listItemInfoPanelInfo.SetText(info)
			self._listItemInfoPanelRewardListView.UpdateData(rewardsData)
		self._listItemInfoPanel.SetVisible(active)
		if not active:
			self._listItemSelected = -1
		self._subTaskListView.UpdateView()

	def SetGridItemTaskInfoActive(self, active, args=None, data=None):
		if data:
			uid = data['uid']
			tType = data['type']
			config = GetTaskConfig(uid)
			name = config['desc']
			info = config['info']
			rewards = config['rewards']
			rewardsData = []
			for k in rewards:
				rewardsData.append({
					'identifier': k,
					'count': rewards[k]
				})
			self._gridItemInfoPanelName.SetText(name)
			self._gridItemInfoPanelInfo.SetText(info)
			self._gridItemInfoPanelRewardListView.UpdateData(rewardsData)

			btn = self._gridItemInfoPanelDetail.GetChildByPath('/stack_panel/panel/button').asButton()
			btn.AddTouchEventParams({"isSwallow": True})

			def _takeRewardsFunc(uid):
				return lambda (args): self.OnTaskItemTakeRewards(uid)

			btn.SetButtonTouchUpCallback(_takeRewardsFunc(uid))

			taked = self._gridItemInfoPanelDetail.GetChildByPath('/stack_panel/panel/taked')
			progress = self._gridItemInfoPanelDetail.GetChildByPath('/stack_panel/panel/progress')
			sleep = self._gridItemInfoPanelDetail.GetChildByPath('/stack_panel/panel/sleep')

			btn.SetVisible(tType == 'completed')
			taked.SetVisible(tType == 'received')
			progress.SetVisible(tType == 'pending')
			sleep.SetVisible(tType == 'sleep')

		self._gridItemInfoPanel.SetVisible(active)
		if active:
			pos = args['touchPos']
			self._gridItemInfoSafeAreaWidget.UpdatePos(pos)
		else:
			self._gridItemSelected = None
		self._subTaskGridListView.UpdateView()

	def Close(self, args):
		Instance.mUIManager.PopUI()

	@ViewBinder.binding(ViewBinder.BF_BindString, "#main.gametick")
	def OnGameTick(self):
		if self.Inited:
			self._mainTaskScrollView.Update()
			if self._taskDisplayType == 'grid':
				self._subTaskGridListView.Update()
			elif self._taskDisplayType == 'list':
				self._subTaskListView.Update()
			if self._mainTaskInfoPanelInfo.GetVisible():
				self._mainTaskInfoPanelRewardListView.Update()
			if self._listItemInfoPanel.GetVisible():
				self._listItemInfoPanelRewardListView.Update()
			if self._gridItemInfoPanel.GetVisible():
				self._gridItemInfoPanelRewardListView.Update()
			self._mainTaskInfoPanelBannerView.Update()

	def OnMainTaskInfoClick(self, item, index, data):
		self.SetMainTaskInfoActive(True, item, index, data)

	def OnTaskGridGroupActive(self, path, ctrl, index, data):
		if path not in self._subTaskGridWidgetMap:
			self._subTaskGridWidgetMap[path] = GridTaskGroupWidget(self, path, '/content', '/content/item', self.OnTaskGridGroupItemActive, self.OnTaskGridGroupItemClick)
		self._subTaskGridWidgetMap[path].UpdateData(data)

	def OnBannerItemActive(self, path, ctrl, index, data):
		name = data['name']
		img = 'textures/ui/scuke_survive/task/img_p_'+name
		imgBtn = ctrl.GetChildByPath('/content/image').asImage()
		ctrl.GetChildByPath('/content/rail').SetVisible(data['rail'])
		imgBtn.SetSprite(img)
		imgBtn.SetSize(data['size'], True)

	def OnBannerItemChange(self, path, ctrl, index, data):
		if self._mainTaskInfoIndex > -1:
			self.SetMainTaskInfoActive(True, MainTaskInfo[index], index, self._mainTaskData[index])

	def OnTaskGridGroupClick(self, path, ctrl, index, data, args):
		self._subTaskGridWidgetMap[path].OnClick(path, ctrl, index, data, args)

	def OnTaskGridGroupItemActive(self, path, ctrl, index, data):
		uid = data['uid']
		tType = data['type']
		configData = GetTaskConfig(uid)
		icon = configData['icon']

		img = ctrl.GetChildByPath('/icon/image').asImage()
		img.SetSprite(icon)
		active = tType == 'received' or tType == 'completed'
		img.SetAlpha(1.0)
		img.SetSpriteColor((1.0, 1.0, 1.0) if active else (0.3, 0.3, 0.3))
		ctrl.GetChildByPath('/icon/pending_bg').SetVisible(not active)
		ctrl.GetChildByPath('/icon/completed_bg').SetVisible(active)

		ctrl.GetChildByPath('/selected').SetVisible(self._gridItemSelected == path)


	def OnTaskGridGroupItemClick(self, path, ctrl, index, data, args):
		self._gridItemSelected = path
		self.SetGridItemTaskInfoActive(True, args, data)

	def OnTaskListItemActive(self, path, ctrl, index, data):
		uid = data['uid']
		tType = data['type']
		configData = GetTaskConfig(uid)
		desc = configData['desc']
		icon = configData['icon']

		ctrl.GetChildByPath('/content/label').asLabel().SetText(desc)
		img = ctrl.GetChildByPath('/content/icon/image').asImage()
		img.SetSprite(icon)

		btn = ctrl.GetChildByPath('/content/state/button').asButton()
		btn.AddTouchEventParams({"isSwallow": True})

		def _takeRewardsFunc(uid):
			return lambda (args): self.OnTaskItemTakeRewards(uid)

		btn.SetButtonTouchUpCallback(_takeRewardsFunc(uid))

		taked = ctrl.GetChildByPath('/content/state/taked')
		progress = ctrl.GetChildByPath('/content/state/progress')
		sleep = ctrl.GetChildByPath('/content/state/sleep')

		btn.SetVisible(tType == 'completed')
		taked.SetVisible(tType == 'received')
		progress.SetVisible(tType == 'pending')
		sleep.SetVisible(tType == 'sleep')

		active = tType == 'received' or tType == 'completed'
		img.SetAlpha(1.0)
		img.SetSpriteColor((1.0, 1.0, 1.0) if active else (0.3, 0.3, 0.3))
		ctrl.GetChildByPath('/content/icon/pending_bg').SetVisible(not active)
		ctrl.GetChildByPath('/content/icon/completed_bg').SetVisible(active)

		ctrl.GetChildByPath('/content/selected').SetVisible(self._listItemSelected == index)

	def OnTaskListItemClick(self, path, ctrl, index, data, args):
		self._listItemSelected = index
		self.SetListItemTaskInfoActive(True, data)

	def OnTaskInfoRewardsItemActive(self, path, ctrl, index, data):
		identifier = data['identifier']
		count = data['count']
		aux = 0
		ctrl.GetChildByPath('/count').asLabel().SetText('x%d' % count)
		ctrl.GetChildByPath('/icon').asItemRenderer().SetUiItem(identifier, aux)

	def SetMainTaskInfoActive(self, active, item=None, index=-1, data=None):
		if item and data:
			uid = data['uid']
			tType = data['type']
			config = GetTaskConfig(uid)
			name = config['desc']
			info = config['info']
			rewards = config['rewards']
			rewardsData = []
			for k in rewards:
				rewardsData.append({
					'identifier': k,
					'count': rewards[k]
				})
			self._mainTaskInfoPanelName.SetText(name)
			self._mainTaskInfoPanelInfo.SetText(info)
			self._mainTaskInfoPanelRewardListView.UpdateData(rewardsData)

			btn = self._mainTaskInfoPanelDetail.GetChildByPath('/stack_panel/panel/button').asButton()
			btn.AddTouchEventParams({"isSwallow": True})

			def _takeRewardsFunc(uid):
				return lambda (args): self.OnTaskItemTakeRewards(uid)

			btn.SetButtonTouchUpCallback(_takeRewardsFunc(uid))

			taked = self._mainTaskInfoPanelDetail.GetChildByPath('/stack_panel/panel/taked')
			progress = self._mainTaskInfoPanelDetail.GetChildByPath('/stack_panel/panel/progress')
			sleep = self._mainTaskInfoPanelDetail.GetChildByPath('/stack_panel/panel/sleep')
			notValid = self._mainTaskInfoPanelDetail.GetChildByPath('/stack_panel/panel/notValid')
			if tType == 'completed' and data.get('fromMainTask', False):
				tType = 'notValid'
			notValid.SetVisible(tType == 'notValid')
			btn.SetVisible(tType == 'completed')
			taked.SetVisible(tType == 'received')
			progress.SetVisible(tType == 'pending')
			sleep.SetVisible(tType == 'sleep')
			self._mainTaskInfoPanelBannerView.UpdateData(MainTaskInfo)
			self._mainTaskInfoPanelBannerView.SetCurrent(index)

		self._mainTaskInfoPanel.SetVisible(active)
		self._mainTaskPanel.SetVisible(not active)
		self._mainTaskInfoIndex = index

	def OnBannerMove(self, dir):
		self._mainTaskInfoPanelBannerView.Move(dir)

	def OnTakeTaskRewards(self, data):
		self.OnTabChange(-1, self._taskBranchIndex)
		self.SetGridItemTaskInfoActive(False)
		self.SetListItemTaskInfoActive(False)

	def OnRewardItemClick(self, path, ctrl, index, data, args):
		Instance.mUIManager.PushUI(UIDef.UI_ItemInfoUI, {
			'identifier': data['identifier'],
			'touchPos': args['touchPos']
		})
