# -*- encoding: utf-8 -*-
import math
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import molangConfig
from ScukeSurviveScript.modCommon import eventConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class MolangServerSystem(BaseServerSystem):
	"""molang 服务端"""
	def __init__(self, namespace, systemName):
		super(MolangServerSystem, self).__init__(namespace, systemName)

		# 实体对象
		self._entityDict = {}

		
		Instance.mEventMgr.RegisterEvent(eventConfig.MolangUpdateEvent, self.SubscriptMolangUpdateEvent)
		pass

	def Destroy(self):
		super(MolangServerSystem, self).Destroy()
		Instance.mEventMgr.UnRegisterEvent(eventConfig.MolangUpdateEvent, self.SubscriptMolangUpdateEvent)
		for obj in self._entityDict.values():
			obj.Destroy()
		self._entityDict.clear()
		pass

	# region 事件
	@EngineEvent()
	def AddEntityServerEvent(self, args):
		"""实体添加事件"""
		engineTypeStr = args.get("engineTypeStr")
		# 创建实体对象
		entityId = args.get("id")
		self.CreateLogicObj(entityId, engineTypeStr)
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		"""实体被移除事件"""
		entityId = args.get("id")
		# 清除实体对象
		self.PopLogicObj(entityId)
		pass
	
	def SubscriptMolangUpdateEvent(self, args):
		"""订阅molang更新事件"""
		stage = args.get("stage")
		if stage == "set_entity":
			# 更新某个实体的molang到所有客户端
			entityId = args.get("entityId")
			molangValue = args.get("molangValue")
			self.SetEntityMultiMolangs(entityId, molangValue)
		elif stage == "set_block":
			# 更新某个方块的molang到同维度的客户端
			pos = args.get("pos")
			dimension = args.get("dimension")
			molangValue = args.get("molangValue")
			# 更新某个molang到所有客户端
			self.SetBlockMultiMolangs(pos, dimension, molangValue)
		pass
	# endregion

	# region 创建对象
	def CreateLogicObj(self, entityId, engineTypeStr):
		"""创建载具对象"""
		obj = self._entityDict.get(entityId)
		if obj is None:
			cfg = molangConfig.GetMolangCfg(engineTypeStr)
			if cfg:
				obj = MolangEntityCar(self, entityId, engineTypeStr)
				self._entityDict[entityId] = obj
		return obj
	
	def GetCarLogicObj(self, entityId):
		"""获取载具对象"""
		return self._entityDict.get(entityId)
	
	def PopLogicObj(self, entityId):
		"""删除载具对象"""
		obj = self._entityDict.pop(entityId, None)
		if obj:
			obj.Destroy()
		pass
	# endregion

	# region 设置molang
	def SetEntityMolang(self, entityId, molang, value):
		"""设置实体molang值"""
		info = {
			"entityId": entityId,
			"stage": "set_molang",
			"molang": molang,
			"value": value,
		}
		self.SendMsgToAllClient(eventConfig.MolangUpdateEvent, info)
		pass

	def SetEntityMultiMolangs(self, entityId, molangValues):
		"""
		设置实体多个molang值
		:param molangValues: {molang: value}
		"""
		info = {
			"entityId": entityId,
			"stage": "set_molangs",
			"molangValue": molangValues,
		}
		self.SendMsgToAllClient(eventConfig.MolangUpdateEvent, info)
		pass
	
	def SetMultiEntitysMolangs(self, entityList, molangValues):
		"""设置多个实体的多个molang值"""
		info = {
			"entities": entityList,
			"stage": "set_entitys_molang",
			"molangValue": molangValues,
		}
		self.SendMsgToAllClient(eventConfig.MolangUpdateEvent, info)
		pass


	def SetBlockMultiMolangs(self, pos, dimension, molangValues):
		"""
		设置方块多个molang值，且仅更新同维度的客户端
		:param molangValues: {molang: value}
		"""
		playerList = serverApiMgr.GetPlayerListByDimension(dimension)
		info = {
			"pos": pos,
			"stage": "set_block_molangs",
			"molangValue": molangValues,
		}
		self.SendMsgToMultiClient(playerList, eventConfig.MolangUpdateEvent, info)
		pass
	# endregion


class MolangEntityCar(CommonEventRegister):
	"""用于设置molang的实体对象"""
	def __init__(self, serverHandler, entityId, engineTypeStr):
		CommonEventRegister.__init__(self, serverHandler)
		self._serverHandler = serverHandler
		self._entityId = entityId
		self._engineTypeStr = engineTypeStr
		self._cfg = molangConfig.GetMolangCfg(engineTypeStr)

		# molang缓存
		self._molangValueCache = {}
		# 乘骑实体列表
		self._riderList = []

		# 飞行状态
		self._flyState = False

		self._posComp = compFactory.CreatePos(self._entityId)
		self._rotComp = compFactory.CreateRot(self._entityId)
		self._dimensionComp = compFactory.CreateDimension(self._entityId)

		self._pitchRollTimer = None
		self._lastPos = None
		# 根据config，启动对应的timer
		if self._cfg.get("pitch_roll"):
			param = self._cfg.get("pitch_roll")
			self._pitchRollTimer = engineApiGas.AddRepeatTimer(param.get("tick", 0.2), self.UpdatePitchRollTimer)

		if self._cfg.get("move_up"):
			Instance.mEventMgr.RegisterEvent(eventConfig.MolangUpdateEvent, self.SubscriptMolangUpdateEvent)
		pass

	def Destroy(self):
		"""销毁实体对象"""
		CommonEventRegister.OnDestroy(self)
		if self._cfg.get("move_up"):
			Instance.mEventMgr.UnRegisterEvent(eventConfig.MolangUpdateEvent, self.SubscriptMolangUpdateEvent)
		if self._pitchRollTimer:
			engineApiGas.CancelTimer(self._pitchRollTimer)
			self._pitchRollTimer = None
		self._molangValueCache.clear()
		self._cfg = None
		del self
		pass

	# region 事件
	@EngineEvent()
	def EntityStartRidingEvent(self, args):
		"""开始骑乘事件"""
		rideId = args.get("rideId")
		if rideId == self._entityId:
			self.UpdateRiderList()
		pass

	@EngineEvent()
	def EntityStopRidingEvent(self, args):
		"""停止骑乘事件"""
		riderId = args.get("id")
		rideId = args.get("rideId")
		cancel = args.get("cancel")
		if cancel is False and rideId == self._entityId:
			# 下骑
			self.UpdateRiderList()
			# 重置该实体的molang
			info = {
				"entityId": riderId, 
				"molangValue": {
					molangConfig.QueryEnum.CarPitchRot: 0.0,
					molangConfig.QueryEnum.CarRollRot: 0.0,
					molangConfig.QueryEnum.RiderPosX: 0.0,
					molangConfig.QueryEnum.RiderPosY: 0.0,
					molangConfig.QueryEnum.RiderPosZ: 0.0,
				},
				"stage": "set_entity",
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass

	def UpdateRiderList(self):
		"""更新骑乘列表"""
		self._riderList = serverApiMgr.GetAllRiders(self._entityId)
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.MolangClientSystem)
	def MolangUpdateEvent(self, args):
		"""更新molang事件"""
		entityId = args.get("entityId")
		if entityId == self._entityId:
			stage = args.get("stage")
			if stage == "get_molang":
				self.SyncAllMolangToClient(args)
		pass

	def SubscriptMolangUpdateEvent(self, args):
		"""订阅molang更新事件"""
		entityId = args.get("entityId")
		if entityId == self._entityId:
			# 更新飞行状态，影响倾斜逻辑的启用
			flyState = args.get("flyState")
			if flyState is not None:
				self._flyState = flyState
				if self._flyState:
					molangValue = {
						molangConfig.QueryEnum.CarRollRot: 0,
						molangConfig.QueryEnum.CarPitchRot: 0,
					}
					self.SetEntityMultiMolangs(molangValue, self._riderList)
				return
			
			# 更新多个molang到所有客户端
			molangValues = args.get("molangValues")
			if molangValues:
				if molangValues.get(molangConfig.QueryEnum.CarPitchRot) is not None:
					self.SetEntityMultiMolangs(molangValues, self._riderList)
				else:
					self.SetEntityMultiMolangs(molangValues)
				return
			
			# 更新某个molang到所有客户端
			molang = args.get("molang")
			value = args.get("value")
			self.SetEntityMolang(molang, value)
		pass
	# endregion


	# region 功能
	def UpdatePitchRollTimer(self):
		"""更新pitch、roll的timer，常用于载具"""
		# 如果是飞行状态，则不更新
		if self._flyState:
			return

		# 位置
		pos = self._posComp.GetPos()
		if pos and pos != self._lastPos:
		# if True:
			pitchRollCfg = self._cfg.get("pitch_roll", {})
			dimension = self._dimensionComp.GetEntityDimensionId()
			rot = self._rotComp.GetRot()
			# 射线检测
			pitchRot, rollRot = self.GetTiltingPitchRollRotByRay(pos, rot, dimension, pitchRollCfg)
			# 修改molang
			molangVals = {
				molangConfig.QueryEnum.CarRollRot: rollRot * 0.5,
				molangConfig.QueryEnum.CarPitchRot: pitchRot * 0.5,
			}
			if pitchRollCfg.get("all_riders"):
				# TODO 同时设定乘客的molang（在客户端进行计算）
				riderList = self._riderList
				self.SetEntityMultiMolangs(molangVals, riders=riderList)
				# riderList.append(self._entityId)
				# self.SetMultiEntitysMolangs(riderList, molangVals)
			else:
				self.SetEntityMultiMolangs(molangVals)
			
			# 方案二：按角度发射射线，比如0度时，有命中方块，则偏10度，如果没命中，则表示载具要倾斜这个角度
			# pass，无法实现，因为有倾斜度后，射线过长，就总是会命中方块；如果射线过短，则达不到检测的目的

		self._lastPos = pos
		pass

	def CalcRotByRay(self, pos, rot, rayList, dimension):
		"""计算实体的倾斜角度、翻滚【废弃】"""
		crot = 0
		i = 0
		for ray in rayList:
			if ray.get("offset_rot"):
				length = ray.get("offset_length", 1)
				rayPos = commonApiMgr.GetNextPosByRot(pos, (rot[0] + ray["offset_rot"][0], rot[1] + ray["offset_rot"][1]), length)
				rayPos = (rayPos[0], rayPos[1] + ray.get("offset_height", 0), rayPos[2])
			else:
				offset = ray.get("offset", (0, 0, 0))
				length = commonApiMgr.GetDistanceXZ((0, 0, 0), offset)
				rayPos = (pos[0] + offset[0], pos[1] + offset[1] + ray.get("offset_height", 0), pos[2] + offset[2])
			# 射线
			blockList = serverApi.getEntitiesOrBlockFromRay(dimension, rayPos, ray.get("rot_vector", (0, 0, 0)), ray.get("distance", 3), False, minecraftEnum.RayFilterType.OnlyBlocks)
			if blockList:
				for block in blockList:
					if block.get("type") == "Block" and block.get("hitPos") and "water" not in block.get("identifier", ""):
						blockPos = block["hitPos"]
						# 计算角度
						height = blockPos[1] - pos[1] if i != 0 else pos[1] - blockPos[1]
						if abs(height) > 0.1:
							newRot = math.degrees(math.atan2(height, length))
							if abs(newRot) > abs(crot):
								crot = newRot
						break
			i += 1
		# 限制范围
		return max(min(crot, 30), -30)
	
	def GetTiltingPitchRollRotByRay(self, pos, rot, dimension, pitchRollCfg):
		"""计算载具的倾斜角度，通过平面来计算"""
		# 获取4个车轮方位的地面位置，再结合载具位置，找出2个车轮最低的位置，从而得到3个坐标，从而确定一个平面
		# 求出平面法向量，根据法向量去计算该平面和x轴、z轴的夹角（使用载具的坐标系）
		rayList = pitchRollCfg.get("rays", [])
		ignoreBlocks = pitchRollCfg.get("ignore_blocks", [])

		# TODO 如果posList初始为None列表，则后台代码检测会提示后面的curPos、lastPos is unsubscriptable，故初始值改为具体的值
		posList = [(0, -1000, 0), (0, -1000, 0), (0, -1000, 0), (0, -1000, 0)]
		lowPosList = []
		# 射线检测，同时在对角的两个点中，挑选最低/最高的点
		# 不能获取后进行排序选择，会有可能选到对角的两个点，就导致算出的平面不对
		i = 0
		for ray in rayList:
			length = ray.get("offset_length", 1)
			rayPos = commonApiMgr.GetNextPosByRot(pos, (rot[0] + ray["offset_rot"][0], rot[1] + ray["offset_rot"][1]), length)
			rayPos = (rayPos[0], rayPos[1] + ray.get("offset_height", 0), rayPos[2])
			# 射线
			blockList = serverApi.getEntitiesOrBlockFromRay(dimension, rayPos, ray.get("rot_vector", (0, 0, 0)), ray.get("distance", 3), False, minecraftEnum.RayFilterType.OnlyBlocks)
			inWater = False
			if blockList:
				for block in blockList:
					if block.get("type") == "Block" and block.get("hitPos"):
						if block.get("identifier", "") not in ignoreBlocks:
							blockPos = block["hitPos"]
							posList[i] = blockPos
							break
						else:
							inWater = True
			elif inWater is False:
				posList[i] = (rayPos[0], rayPos[1] - ray.get("distance", 3), rayPos[2])
			# 判断对角线的最低点/最高点
			curPos = posList[i]
			if curPos[1] != -1000 and i % 2 == 1:
				lastPos = posList[i - 1]
				if lastPos != -1000 and abs(lastPos[1] - pos[1]) > abs(curPos[1] - pos[1]):
					lowPosList.append(lastPos)
				else:
					lowPosList.append(curPos)
			i += 1
		pitchRot = 0
		rollRot = 0
		if len(lowPosList) >= 2:
			pos1 = lowPosList[0]
			pos2 = lowPosList[1]
			# 计算平面法向量
			normalV = commonApiMgr.PlaneNormalVector3(pos, pos1, pos2)
			# 如果坐标在载具后方，则计算出的法向量会是朝下的，所以需要取反
			if normalV[1] < 0:
				normalV = (-normalV[0], -normalV[1], -normalV[2])
			# 计算平面法向量与x轴、z轴的夹角
			# 实体正向为x轴
			xVector = serverApi.GetDirFromRot((0, rot[1]))
			# 实体右侧为z轴
			zVector = serverApi.GetDirFromRot((0, rot[1] + 90))
			# 法向量和轴的夹角，并不是平面和轴的夹角，需-90进行转换
			pitchRot = commonApiMgr.VectorAngle(normalV, xVector) - 90
			rollRot = commonApiMgr.VectorAngle(normalV, zVector) - 90
			# print("__________ GetTiltingRotByRay", pitchRot, rollRot, pos, pos1, pos2)
			# print("__________ GetTiltingRotByRay", normalV, xVector)
		# 在动画中，pitch往上是负，所以需要取反
		return -pitchRot, rollRot
	
	def SyncAllMolangToClient(self, args):
		"""同步实体molang到客户端"""
		playerId = args.get("__id__")
		# 设置载具自己、乘客的molang
		riderList = [self._entityId]
		riderList.extend(self._riderList)
		info = {
			"entities": riderList,
			"stage": "set_entitys_molang",
			"molangValue": self._molangValueCache,
		}
		self.SendMsgToClient(playerId, eventConfig.MolangUpdateEvent, info)
		pass

	def SetEntityMolang(self, molang, value):
		"""设置实体molang值"""
		oldVal = self._molangValueCache.get(molang)
		if oldVal != value:
			info = {
				"entityId": self._entityId,
				"stage": "set_molang",
				"molang": molang,
				"value": value,
			}
			self.SendMsgToAllClient(eventConfig.MolangUpdateEvent, info)
			# 更新缓存
			self._molangValueCache[molang] = value
		pass

	def SetEntityMultiMolangs(self, molangValues, riders=None):
		"""
		设置实体多个molang值
		:param molangValues: {molang: value}
		"""
		info = {
			"entityId": self._entityId,
			"riders": riders,
			"stage": "set_molangs",
			"molangValue": {},
		}
		isSet = False
		for molang, value in molangValues.iteritems():
			oldVal = self._molangValueCache.get(molang)
			if oldVal != value:
				isSet = True
				info["molangValue"][molang] = value
				# 更新缓存
				self._molangValueCache[molang] = value
		if isSet:
			self.SendMsgToAllClient(eventConfig.MolangUpdateEvent, info)
		pass
	
	def SetMultiEntitysMolangs(self, entityList, molangValues):
		"""设置多个实体的多个molang值"""
		info = {
			"entities": entityList,
			"stage": "set_entitys_molang",
			"molangValue": molangValues,
		}
		self.SendMsgToAllClient(eventConfig.MolangUpdateEvent, info)
		pass

	# endregion
