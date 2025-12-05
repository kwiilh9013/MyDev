# -*- coding: UTF-8 -*-
import time
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon.cfg.car import carConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetPartSkillConfig
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import PartEnum
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon.cfg import molangConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
from ScukeSurviveScript.modCommon.cfg.car import carTestConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BaseCarDrive(CommonEventRegister):
	"""基地车 驾驶逻辑 服务端"""
	def __init__(self, severHandler, entityId, carLogicObj):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		# 载具逻辑对象
		self._carLogicObj = carLogicObj
		
		# 载具config数据
		self._carConfig = carConfig.BaseCarConfig
		# 更新tick频率
		self._tickCD = self._carConfig.get("tickCD", 0.03)

		# 坐骑id
		self._entityId = entityId
		# 玩家id列表，第一个是驾驶员
		self._playerList = []

		# 当前速度
		self._currentSpeed = 0.0
		# 当前加速状态: 加速、刹车等
		self._speedState = None
		# 转向状态：左右转
		self._turnState = None

		# 实际移速，用于判断是否撞墙/卡住
		self._realSpeed = 0.0
		self._realSpeedCount = 0
		# 上移高度，用于速度衰减（爬坡速度变慢）、计算实际移速
		self._stepPos = None
		# 行为包event
		self._currentEvent = None

		# 破坏方块的cd数据
		self._breakBlocksCD = 0.0

		# 修改速度timer
		self._updateSpeedTimer = None

		self._attrComp = compFactory.CreateAttr(self._entityId)
		self._posComp = compFactory.CreatePos(self._entityId)
		self._rotComp = compFactory.CreateRot(self._entityId)
		self._eventComp = compFactory.CreateEntityEvent(self._entityId)
		self._plyRotComp = None
		self._motionComp = compFactory.CreateActorMotion(self._entityId)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self._server = None
		if self._updateSpeedTimer:
			engineApiGas.CancelTimer(self._updateSpeedTimer)
			self._updateSpeedTimer = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def MobGriefingBlockServerEvent(self, args):
		"""生物破坏方块事件"""
		entityId = args.get("entityId")
		if entityId == self._entityId:
			# 破坏方块减速
			curT = time.time()
			if curT - self._breakBlocksCD > 1:
				# 减速
				self.SetCutSpeedByBreakBlock()
				# 记录cd（不然会触发多次）
				self._breakBlocksCD = curT
		pass
	
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.CarClientSystem)
	def CarCtrlEvent(self, args):
		"""载具控制事件"""
		playerId = args.get("__id__")
		stage = args.get("stage")
		# 驾驶员操作
		if playerId in self._playerList:
			if stage in ("up", "cut", ):
				# 加速, 刹车/倒退
				self._speedState = stage
			elif stage == "cancel":
				# 松手
				self._speedState = None
			elif stage in ("left", "right", "tCancel",):
				# 左转、右转、松手
				self._turnState = stage if stage != "tCancel" else None
				pass
			elif stage == "getoff":
				# 下骑
				rideComp = serverApi.GetEngineCompFactory().CreateRide(playerId)
				rideComp.StopEntityRiding()
		pass
	# endregion

	# region 乘骑
	def StartRiding(self, playerId):
		"""设置乘骑"""
		if len(self._playerList) <= 0:
			# 驾驶员
			self._plyRotComp = compFactory.CreateRot(playerId)
			# 重置角度为载具角度（需延迟重置）
			rot = self._rotComp.GetRot()
			rot = (0, rot[1])
			engineApiGas.AddTimer(0.01, self._plyRotComp.SetRot, rot)
			engineApiGas.AddTimer(self._tickCD, self._rotComp.SetRot, rot)
			# 重置速度
			self._currentSpeed = 0.0
			self._attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, self._currentSpeed)
			# 启动timer
			if self._updateSpeedTimer is None:
				self._updateSpeedTimer = engineApiGas.AddRepeatTimer(self._tickCD, self.UpdateSpeedTurnTimer)
		else:
			# 乘客
			# 仅改玩家自己的角度
			rot = self._rotComp.GetRot()
			plyRotComp = compFactory.CreateRot(playerId)
			engineApiGas.AddTimer(0.01, plyRotComp.SetRot, (0, rot[1]))
		
		# 记录玩家数据
		self._playerList.append(playerId)
		pass

	def StopRiding(self, playerId):
		"""停止乘骑/下骑"""
		if playerId in self._playerList:
			self._playerList.remove(playerId)
			# 如果是没有乘客了，则重置数据
			if len(self._playerList) <= 0:
				self._plyRotComp = None
				if self._updateSpeedTimer:
					engineApiGas.CancelTimer(self._updateSpeedTimer)
					self._updateSpeedTimer = None
				# 重置速度
				self._currentSpeed = 0.0
				self._attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, self._currentSpeed)
			else:
				# 下一位乘客改为驾驶员
				nextPlayer = self.GetRider()
				# 同步乘骑数据到客户端
				info = {
					"stage": "startRiding",
					"rideId": self._entityId,
					"isRider": True,
				}
				self.SendMsgToClient(nextPlayer, eventConfig.CarCtrlEvent, info)
			# 重置移动状态
			self._turnState = None
			self._speedState = None
		pass
	# endregion

	# region 移速
	def UpdateSpeedTurnTimer(self):
		"""更新速度、转向，每秒20帧"""
		# # TODO: TEST
		# carTestConfig.GetTestConfig(self)
		pos = self._posComp.GetPos()
		if not pos:
			return
		
		# 计算当前的行为包移速
		speed = self.GetCurrentAddonSpeed()

		# 爬坡衰减 & 实际速度计算
		lastRealSpeed = self._realSpeed
		if self._stepPos and self._stepPos != pos:
			# 计算实际移速
			# 如果是飞行模式，则再计算y轴
			if self._carLogicObj.GetFlyState():
				self._realSpeed = commonApiMgr.GetDistance(self._stepPos, pos)
			else:
				self._realSpeed = commonApiMgr.GetDistanceXZ(self._stepPos, pos)
			height = pos[1] - self._stepPos[1]
			if height >= 0.99:	# 在水里时会上下浮动
				speed = speed * self._carConfig.get("mountainSpeed", 0.5)
			self._realSpeedCount = 0
		elif self._realSpeed != 0:
			# 有时会正在跑，但获取到的坐标一致，需增加容错率（可能是检测频率过高）
			self._realSpeedCount += 1
			if self._realSpeedCount >= 3:
				self._realSpeedCount = 0
				self._realSpeed = 0.0
				# 当前速度非0，才会重置为0；启动阶段会是坐标不变
				if self._currentSpeed != 0:
					speed = 0.0
		self._stepPos = pos
			
		# 根据速度差值，计算撞方块的伤害
		if lastRealSpeed > self._realSpeed and self._currentSpeed > 0:
			damage = carConfig.GetCrashDamage(lastRealSpeed - self._realSpeed)
			if damage > 0:
				# 检测是否撞到方块，进行二次校验
				if self.IsForwordHasBlock():
					self._carLogicObj.SetUpdateDurability(-damage)
					# print("_______ UpdateSpeedTurnTimer speed", damage, lastRealSpeed, self._realSpeed)
				# 降低速度
				self.SetCutSpeedByCrash()
			pass

		# # 根据速度，修改event，从而破坏不同硬度的方块
		# event = carConfig.GetBreakBlockEvent(self._realSpeed)
		# if event and self._currentEvent != event:
		# 	# self._eventComp.TriggerCustomEvent(self._entityId, event)
		# 	self._currentEvent = event
		# 	print("___________ event", event)
		
		# 更新速度
		if self._currentSpeed != speed:
			lastSpeed = self._currentSpeed
			self._currentSpeed = speed

			# 更新速度（需根据是否是倒车，修改数值）
			backSpeedRatio = self._carConfig.get("backSpeed", 1.5)
			groundSpeed = abs(self._currentSpeed)
			waterSpeed = abs(self._currentSpeed * self._carConfig.get("waterSpeed", 0.25))
			lavaSpeed = abs(self._currentSpeed * self._carConfig.get("lavaSpeed", 0.5))
			if self._speedState == "cut":
				groundSpeed *= backSpeedRatio
				waterSpeed *= backSpeedRatio
				lavaSpeed *= backSpeedRatio

			# 如果是飞行状态、且是加速、刹车等状态，则修改速度
			if self._carLogicObj.GetFlyState():
				skillCfg = GetPartSkillConfig(PartEnum.Fly)
				flySpeedRatio = skillCfg.get("flySpeedRatio", 20)
				groundSpeed *= flySpeedRatio
				waterSpeed *= flySpeedRatio
				lavaSpeed *= flySpeedRatio
			
			self._attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, groundSpeed)
			# 同数值下水里移速比陆地高一倍（可能是摩擦力更小）
			if self._carLogicObj.IsCanRunInWater():
				self._attrComp.SetAttrValue(minecraftEnum.AttrType.UNDERWATER_SPEED, waterSpeed)
				# 岩浆移速（同数值下和陆地一样）
				self._attrComp.SetAttrValue(minecraftEnum.AttrType.LAVA_SPEED, lavaSpeed)
			else:
				# 不可在水上行驶，则移速非常低
				rate = 0.05
				self._attrComp.SetAttrValue(minecraftEnum.AttrType.UNDERWATER_SPEED, waterSpeed * rate)
				self._attrComp.SetAttrValue(minecraftEnum.AttrType.LAVA_SPEED, lavaSpeed * rate)
			# print("___________ speed", self._currentSpeed, "_____ real speed", self._realSpeed, "_________ aSpeed", aSpeed)
			# 更新客户端操作vector
			upStage = None
			hover = False
			if lastSpeed <= 0 and self._currentSpeed > 0:
				upStage = "up"
			elif lastSpeed >= 0 and self._currentSpeed < 0:
				upStage = "cut"
			if abs(lastSpeed) > 0.01 and abs(self._currentSpeed) <= 0.01:
				hover = True
			if upStage:
				rider = self.GetRider()
				if rider:
					self.SendMsgToClient(rider, eventConfig.CarCtrlEvent, {"stage": upStage})
				# 更新移动方向的molang
				info = {
					"entityId": self._entityId, 
					"molang": molangConfig.QueryEnum.CarMoveUp, 
					"value": 1.0 if upStage == "up" else -1.0
				}
				Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
				# 如果是飞行状态，则同时更新倾斜角度
				if self._carLogicObj.GetFlyState():
					info = {
						"entityId": self._entityId, 
						"molangValues": {molangConfig.QueryEnum.CarPitchRot: 20 if upStage == "up" else -20},
					}
					Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
					# 加速音效
					skillCfg = GetPartSkillConfig(PartEnum.Fly)
					if skillCfg.get("speedup_sound"):
						info = {
							"stage": "fly_sound",
							"path": skillCfg.get("speedup_sound"),
							"entityId": self._entityId,
							"loop": True,
						}
						self.SendMsgToAllClient(eventConfig.CarSkillsEvent, info)
			elif hover:
				# 停止状态，则倾斜角度归零（飞行悬停时，不要有倾斜效果）
				if self._carLogicObj.GetFlyState():
					info = {
						"entityId": self._entityId, 
						"molangValues": {molangConfig.QueryEnum.CarPitchRot: 0}, 
					}
					Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
					# 悬停音效
					skillCfg = GetPartSkillConfig(PartEnum.Fly)
					if skillCfg.get("hover_sound"):
						info = {
							"stage": "fly_sound",
							"path": skillCfg.get("hover_sound"),
							"entityId": self._entityId,
							"loop": True,
						}
						self.SendMsgToAllClient(eventConfig.CarSkillsEvent, info)
				
			# 修改刹车状态的molang，用于播放刹车音效
			info = {
				"entityId": self._entityId, 
				# 刹车状态：当前按下后退，且速度仍是向前
				"molang": molangConfig.QueryEnum.CarCutState,
				"value": 1 if (self._speedState == "cut" and self._currentSpeed > 0) else 0,
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)

		self.UpdateTurn()
		pass

	def GetCurrentAddonSpeed(self):
		"""获取当前的行为包速度，根据当前加速状态、滑行状态计算"""
		# 有耐久、能源、不瘫痪等，才能进行加速减速；没有后，仍会滑行，直到停止
		aSpeed = 0.0
		if self._carLogicObj.IsCanSteer() and not self._carLogicObj.IsInhibit():
			# 获取加速度
			if self._speedState == "up":
				aSpeed = carConfig.GetASpeed(self._currentSpeed)
			elif self._speedState == "cut":
				aSpeed = carConfig.GetCutASpeed(self._currentSpeed)
			
		# 计算速度
		speed = 0.0
		if aSpeed:
			# 加减速
			speed = self._currentSpeed + aSpeed * self._tickCD
		elif abs(self._currentSpeed) > 0.01:
			# 不能直接判断>0，浮点数可能并非为0，需有一定容错范围
			# 当前仍有速度，则计算摩擦力，缓慢停下；倒退会更快停下
			# 如果实际移速为0，则速度直接设置为0；否则当倒退时，需要从0.5渐变到-0.5
			if self._realSpeed < 0.03:
				# 撞到方块等，卡住
				speed = 0
			else:
				friction = self._carConfig.get("frictionSpeed") if self._currentSpeed > 0 else -self._carConfig.get("cutFrictionSpeed")
				speed = self._currentSpeed - friction * self._tickCD
		
		# 消耗能源: 只有加速、倒车阶段、飞行阶段 会消耗能源
		flyState = self._carLogicObj.GetFlyState()
		if flyState or (aSpeed and ((self._currentSpeed > 0 and speed >= self._currentSpeed) or (self._currentSpeed < 0 and speed <= self._currentSpeed))):
			self._carLogicObj.SetRunConsumeEnergy(self._realSpeed)
		return speed

	def UpdateTurn(self):
		"""更新转向"""
		# 更新转向（转向速度和移速成正比）
		if self._currentSpeed != 0:
			turnRot = 0
			if self._turnState == "left":
				turnRot = -self._carConfig.get("turnSpeed") * self._tickCD
			elif self._turnState == "right":
				turnRot = self._carConfig.get("turnSpeed") * self._tickCD
			if turnRot:
				# 旋转速度和移速成正比；如果是倒退，实际速度会比_currentSpeed要小，所以此时需减小_currentSpeed的值再使用
				turnRot *= (0.5 if self._currentSpeed < 0 else 1) * self._currentSpeed / self._carConfig.get("maxSpeed", 1.0)
				rot = self._plyRotComp.GetRot()
				# 修改所有驾驶员、乘客的角度
				setRot = (0, rot[1] + turnRot)
				for plyId in self._playerList:
					rotComp = compFactory.CreateRot(plyId)
					rotComp.SetRot(setRot)
				# 不设置载具角度，效果反而更好
				# self._rotComp.SetRot((0, rot[1] + turnRot))
				# print("___________ rot", turnRot, (rot[0], rot[1] + turnRot))
		pass

	def SetCutSpeedByKnock(self):
		"""撞击实体而降低速度"""
		self._currentSpeed *= self._carConfig.get("knockEntitySpeed", 0.95)
		pass

	def SetCutSpeedByBreakBlock(self):
		"""破坏方块而降低速度"""
		self._currentSpeed *= self._carConfig.get("breakBlockSpeed", 0.9)
		pass

	def SetCutSpeedByCrash(self):
		"""撞方块而降低速度"""
		self._currentSpeed *= self._carConfig.get("crashBlockSpeed", 0.5)
		pass

	def IsForwordHasBlock(self):
		"""前方是否有方块，即是否是撞到方块而停止"""
		isCrash = False
		pos = self._posComp.GetFootPos()
		rot = self._rotComp.GetRot()
		if pos and rot:
			pos = commonApiMgr.GetBlockPosByEntityPos(pos)
			# 计算偏移到载具前方各个方位的坐标，然后获取这些坐标的方块数据
			# 实际会阻挡前进的宽度 = 行为包中collision_box的宽度
			# 往前*格，再以该坐标为中心，往左、往右偏移
			width, height = self._carConfig.get("collision")
			radius = int(width * 0.5) + 1
			centerPos = commonApiMgr.GetNextPosByRot(pos, (0, rot[1]), radius)
			centerPos = (centerPos[0], centerPos[1] + 1.5, centerPos[2])	# 起始点往上移，一格高的地方不算碰撞
			# 从下往上，发射多根射线，如果有命中方块，则表示碰撞到方块
			rayRot = (0, 1, 0)
			rayDistance = int(height)
			rayXZPosList = []
			for i in xrange(-radius, radius + 1):
				rayPos = centerPos
				if i != 0:
					rotY = rot[1] + (90 if i > 0 else -90)
					rayPos = commonApiMgr.GetNextPosByRot(centerPos, (0, rotY), i)
					xzPos = (rayPos[0], rayPos[2])
					if xzPos in rayXZPosList:
						continue
					rayXZPosList.append(xzPos)
				# 射线
				blockList = serverApi.getEntitiesOrBlockFromRay(self._carLogicObj.GetDimension(), rayPos, rayRot, rayDistance, False, minecraftEnum.RayFilterType.OnlyBlocks)
				if blockList:
					for block in blockList:
						if block.get("type") == "Block" and carConfig.IsRayIngoreBlock(block.get("identifier")) is False:
							isCrash = True
							break
				if isCrash:
					break
		return isCrash
	# endregion

	# region 属性
	def GetPlayerList(self):
		"""获取乘客列表（仅玩家）"""
		return self._playerList
	
	def GetRider(self):
		"""获取驾驶员"""
		if len(self._playerList) > 0:
			return self._playerList[0]
		return None
	
	def GetCurrentRealSpeed(self):
		"""获取当前实际移速"""
		return self._realSpeed
	# endregion
