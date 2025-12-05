# -*- coding: utf-8 -*-
import math
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg.struct import buildStructConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
compFactory = clientApi.GetEngineCompFactory()


class BuildStructClientSystem(BaseClientSystem):
	"""一键建造 客户端"""
	def __init__(self, namespace, systemName):
		super(BuildStructClientSystem, self).__init__(namespace, systemName)
		
		# 记录已经生成的几何体模型: {name: size, }
		self._blockGeometryDict = {}
		# 绑定模型的实体id，用于等待客户端创建实体后绑定
		self._bindBlockGeoEntityDict = {}

		# 建筑选址数据: {structId/建筑id, geoEntityId/建筑模型实体id, crossTimer/准星选点timer, 
		# lockGeoState/锁定模型位置状态, lastGeoPos/上次模型位置}
		self._buildStructDict = {}

		# 事件方法调用
		self._eventFunctions = {
			# 显示建造模型
			"build_range": self.SetBuildRange,
			# 建造特效
			"build_effects": self.SetBuildEffects,
			# 创建模型
			"create_geo": self.CreateBlockGeo,

			# 尝试建造
			"try_build": self.SetTryBuild,
			# 旋转
			"rotate": self.SetRotateBuild,
			# 偏移
			"move": self.SetMoveBuild,
			# 取消建造
			"cancel_build": self.CancelBuild,
			# 锁定模型位置
			"lock_geo": self.SetLockGeoState,
			# 打开选择界面
			"open_select_ui": self.SetOpenSelectUI,
			# 开始建造
			"start_build": self.SetStartBuild,
			# 撤销
			"revoke": self.SetRevokeBuild,
		}

		# 手持物品id
		self._carriedItemName = None

		pass

	def Destroy(self):
		super(BuildStructClientSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.BuildStructUIEvent, self.BuildStructUISubscribeEvent)
		self._eventFunctions.clear()
		self.ResetBuildData()
		pass
	
	# region 事件
	@EngineEvent()
	def UiInitFinished(self, args=None):
		# 延迟执行，此时可能还在初始化UI中
		def initUI():
			# 获取手持的物品
			self._carriedItemName = None
			item = clientApiMgr.GetPlayerCarriedItem(self.mPlayerId)
			self.OnCarriedNewItemChangedClientEvent({"itemDict": item})
		engineApiGac.AddTimer(0.1, initUI)

		# 监听事件
		Instance.mEventMgr.RegisterEvent(eventConfig.BuildStructUIEvent, self.BuildStructUISubscribeEvent)

		# 手持动画
		self.SetBuildInHandAnim(self.mPlayerId)
		pass
	
	@EngineEvent()
	def OnCarriedNewItemChangedClientEvent(self, args):
		"""主手持物品改变事件"""
		itemDict = args.get("itemDict")
		itemName = None
		if itemDict:
			itemName = itemDict.get("newItemName")
		# 如果手持的是建造道具，且之前不是手持，才显示UI
		if itemName != self._carriedItemName:
			if itemName == buildStructConfig.BuildItemName:
				# 显示UI
				Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "open_btn", "state": True})
			elif self._carriedItemName == buildStructConfig.BuildItemName:
				# 当前手持不是建造道具、且之前是，才隐藏UI
				Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "open_btn", "state": False})

			# 说明书物品UI
			if "ScukeSurviveGameIntroUI" in Instance.mUIManager.mUIDict:
				if itemName == "scuke_survive:game_introduce_book":
					Instance.mUIManager.mUIDict["ScukeSurviveGameIntroUI"].SetScreenVisible(True)
				elif self._carriedItemName == "scuke_survive:game_introduce_book":
					Instance.mUIManager.mUIDict["ScukeSurviveGameIntroUI"].SetScreenVisible(False)

		self._carriedItemName = itemName
		pass

	@EngineEvent()
	def AddEntityClientEvent(self, args):
		"""实体添加事件"""
		entityId = args.get("id")
		# 绑定方块几何体模型
		structId = self._bindBlockGeoEntityDict.get(entityId)
		if structId:
			self.BindBlockGeoToEntity(entityId, structId)
		pass

	@EngineEvent()
	def AddPlayerCreatedClientEvent(self, args):
		"""玩家进入视野范围后事件"""
		playerId = args.get("playerId")
		self.SetBuildInHandAnim(playerId)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BuildStructServerSystem)
	def BuildStructEvent(self, args):
		"""一键建造事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass

	def BuildStructUISubscribeEvent(self, args):
		"""订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region 建造选址
	def SetTryBuild(self, args):
		"""尝试建造"""
		# 获取建筑id
		structId = args.get("structId")
		self.ResetBuildData()
		# 发消息到服务端，生成显示模型的实体
		info = {
			"stage": "build_range",
			"structId": structId,
		}
		self.SendMsgToServer(eventConfig.BuildStructEvent, info)
		# 显示操作UI
		Instance.mEventMgr.NotifyEvent(eventConfig.BuildStructUIEvent, {"stage": "open_ctrl_ui", "structId": structId})
		# 启动timer
		if not self._buildStructDict.get("crossTimer"):
			timer = engineApiGac.AddRepeatedTimer(buildStructConfig.GetCrossPosTime, self.GetCrossTimer)
			self._buildStructDict["crossTimer"] = timer
		# 记录数据
		self._buildStructDict["structId"] = structId
		pass

	def GetCrossTimer(self):
		"""获取准星位置的timer"""
		entityId = self._buildStructDict.get("geoEntityId")
		if entityId and self._buildStructDict.get("lockGeoState") is not True:
			if clientApiMgr.IsScreenUI():
				pos = self.GetCrossPos(ignoreEntityList=[entityId])
				# 如果获取不到位置，则不进行更改
				if pos and pos != self._buildStructDict.get("lastGeoPos"):
					self._buildStructDict["lastGeoPos"] = pos
					# 判断距离，超过距离就不再设置过去
					if commonApiMgr.GetManhattanDistanceXZ(pos, self._buildStructDict.get("lastGeoPos")) <= buildStructConfig.GetCrossMaxDistanceManhattan:
						self.UpdateBuidPos(entityId, pos)
		pass

	def SetMoveBuild(self, args):
		"""设置模型偏移"""
		offsetRot = args.get("offsetRot")
		offsetY = args.get("offsetY")
		entityId = self._buildStructDict.get("geoEntityId")
		if entityId:
			offset = [0, 0, 0]
			# 前后左右，将以建筑为方位进行计算
			if offsetY is not None:
				# 上下
				offset[1] += offsetY
			elif offsetRot is not None:
				# 移动
				rot = engineApiGac.GetRot(entityId)
				offset = commonApiMgr.GetOffsetByRot((0, rot[1] + offsetRot), 1)
			# 手动设置一次位置
			pos = engineApiGac.GetEntityFootPos(entityId)
			# pos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
			# 对坐标偏移到方块中间（如果是方块坐标，需要传递往上偏移后的坐标）
			# 高度需四舍五入，不然会因为浮点数精度问题，导致偏移不了
			pos = (math.floor(pos[0] + offset[0]) + 0.5, round(pos[1] + offset[1]), math.floor(pos[2] + offset[2]) + 0.5)
			self.UpdateBuidPos(entityId, pos)
		pass

	def UpdateBuidPos(self, entityId, pos):
		"""更新建筑模型位置"""
		info = {
			"stage": "build_pos",
			"pos": pos,
			"entityId": entityId,
		}
		self.SendMsgToServer(eventConfig.BuildStructEvent, info)
		pass

	def SetLockGeoState(self, args):
		"""设置锁定模型状态"""
		state = args.get("state")
		self._buildStructDict["lockGeoState"] = state
		pass
	
	def SetRotateBuild(self, args=None):
		"""旋转建造模型"""
		info = {
			"stage": "rotate",
			"entityId": self._buildStructDict.get("geoEntityId"),
		}
		self.SendMsgToServer(eventConfig.BuildStructEvent, info)
		pass

	def CancelBuild(self, args=None):
		"""取消建造"""
		# 清除实体
		entityId = self._buildStructDict.get("geoEntityId")
		if entityId:
			info = {
				"stage": "cancel_build",
				"entityId": entityId,
			}
			self.SendMsgToServer(eventConfig.BuildStructEvent, info)
		self.ResetBuildData()
		pass

	def SetStartBuild(self, args):
		"""开始建造"""
		structId = args.get("structId")
		info = {
			"stage": "start_build",
			"structId": structId,
			"entityId": self._buildStructDict.get("geoEntityId"),
		}
		self.SendMsgToServer(eventConfig.BuildStructEvent, info)
		pass
	
	def SetRevokeBuild(self, args):
		"""撤销建造"""
		info = {
			"stage": "revoke",
		}
		self.SendMsgToServer(eventConfig.BuildStructEvent, info)
		pass


	def ResetBuildData(self):
		"""重置建造数据"""
		if self._buildStructDict.get("crossTimer"):
			engineApiGac.CancelTimer(self._buildStructDict.get("crossTimer"))
		self._buildStructDict.clear()
		pass

	def GetCrossPos(self, ignoreEntityList=[]):
		"""获取准星位置。如果是实体，则获取实体脚底位置；如果是方块，则获取上表面位置"""
		pos = None
		cameraComp = compFactory.CreateCamera(self.mLevelId)
		pickDict = cameraComp.PickFacing()
		if pickDict:
			if pickDict.get("type") == "Block":
				# 方块
				pos = (pickDict.get("x", 0), pickDict.get("y", 0) + 1, pickDict.get("z", 0))
			elif pickDict.get("type") == "Entity" and pickDict.get("entityId") not in ignoreEntityList:
				posComp = compFactory.CreatePos(pickDict.get("entityId"))
				pos = posComp.GetFootPos()
		return pos
	
	# endregion

	# region 建造表现
	def SetBuildRange(self, args):
		"""设置建造范围"""
		entityId = args.get("entityId")
		structId = args.get("structId")
		# 判断实体是否存在
		if engineApiGac.HasEntity(entityId):
			# 直接绑定模型
			self.BindBlockGeoToEntity(entityId, structId)
		else:
			# 客户端侧实体未加载，需延迟绑定
			self._bindBlockGeoEntityDict[entityId] = structId

		# 记录实体id
		playerId = args.get("playerId")
		if playerId == self.mPlayerId:
			self._buildStructDict["geoEntityId"] = entityId
		pass

	def BindBlockGeoToEntity(self, entityId, structId):
		"""绑定方块几何体模型"""
		# 几何体模型key
		geoKey = self.CreateBlockGeo({"structId": structId})
		# 模型绑定实体，需根据建筑长宽，将实体偏移到模型中间
		# 模型方向和实体方向相反，需转180度
		actorComp = compFactory.CreateActorRender(entityId)
		size = self._blockGeometryDict.get(geoKey, (1, 1, 1))
		offset = (size[1] // 2, 0, size[0] // 2)
		actorComp.AddActorBlockGeometry(geoKey, offset=offset, rotation=(0, 180, 0))
		actorComp.EnableActorBlockGeometryTransparent(geoKey, True)
		actorComp.SetActorBlockGeometryTransparency(geoKey, 0.5)
		pass

	def SetBuildEffects(self, args):
		"""设置建造特效"""
		buildPos = args.get("build_pos")
		# 播放一次动画，延迟销毁（微软粒子定点播放的话，粒子会是相对坐标；当绑定实体后，才能调整为世界坐标）
		for effectName, val in buildStructConfig.BuildEffects.iteritems():
			effectId = clientApiMgr.CreateMicroParticle(effectName, buildPos)
			# 延迟销毁
			engineApiGac.AddTimer(val.get("delay_time", 3), clientApiMgr.RemoveMicroParticle, effectId)
		# 播放音效
		clientApiMgr.PlayCustomMusic(buildStructConfig.BuildSound, buildPos)
		pass

	def CreateBlockGeo(self, args):
		"""创建方块几何体模型，同key会进行复用，而非重新创建"""
		structId = args.get("structId")
		# 几何体模型key
		geoKey = buildStructConfig.GetBlockGeoKey(structId)
		if not self._blockGeometryDict.get(geoKey):
			# 创建模型
			blockDict = buildStructConfig.GetStructPaletteDict(structId)
			if not blockDict:
				# 没有建造数据，结束逻辑
				return False
			# 获取方块调色板
			blockComp = compFactory.CreateBlock(self.mLevelId)
			palette = blockComp.GetBlankBlockPalette()
			palette.DeserializeBlockPalette(blockDict)
			# 生成模型
			geoComp = compFactory.CreateBlockGeometry(self.mLevelId)
			geoComp.CombineBlockPaletteToGeometry(palette, geoKey)
			self._blockGeometryDict[geoKey] = blockDict.get("volume", (1, 1, 1))
		return geoKey
	# endregion


	# region 选择建筑UI
	def SetOpenSelectUI(self, args):
		"""打开选择建筑UI"""
		# 取消建造
		self.CancelBuild()
		# 如果当前是在主界面
		if clientApiMgr.IsScreenUI():
			# 显示UI
			createParams = {
				# 方块几何体模型的列表
				"block_geo_list": self._blockGeometryDict.keys(),
			}
			Instance.mUIManager.PushUI(UIDef.UI_BuildStructSelect, createParams)
		pass
	# endregion

	# region 动画
	def SetBuildInHandAnim(self, playerId):
		"""设置建造手持动画"""
		cfg = buildStructConfig.AddAnimations
		# 添加动画
		renderComp = compFactory.CreateActorRender(playerId)
		renderComp.AddPlayerAnimation(cfg["animKey"], cfg["animName"])
		renderComp.AddPlayerScriptAnimate(cfg["animKey"], cfg["condition"])
		renderComp.RebuildPlayerRender()
		pass
	# endregion
