# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.common.system.commonEventRegister import CommonEventRegister
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent
from ScukeSurviveScript.ScukeCore.server.api import serverApiMgr
from ScukeSurviveScript.ScukeCore.server import engineApiGas
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modCommon.cfg.car.carConfig import ExtraDataKeyEnum
from ScukeSurviveScript.modCommon.cfg.car.carRemoldConfig import GetRemoldTypeTabsList, GetRemoldParts, GetPartConfig, GetRemoldTypeMolangConfig, \
	RemoldTypeEnum, PartEnum
from ScukeSurviveScript.modServer.manager.singletonGas import Instance
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BaseCarRemold(CommonEventRegister):
	"""基地车 改造 服务端"""
	def __init__(self, severHandler, entityId, carObj):
		CommonEventRegister.__init__(self, severHandler)
		self._server = severHandler
		self._levelId = self._server.mLevelId
		# 载具主对象
		self._carObj = carObj
		# 坐骑id
		self._entityId = entityId

		# 解锁配件数据
		self._unlockPartList = []
		# 安装配件数据
		self._usePartData = {}
		
		self._globalExtraComp = compFactory.CreateExtraData(self._levelId)
		self._extraComp = compFactory.CreateExtraData(self._entityId)

		self._eventFunctions = {
			"install": self.SetInstallPart,
			"sync_part_molangs": self.SyncPartsMolangs,
		}

		# 延迟初始化，有可能此时是生成实体后再写入数据(延迟的时间，需慢于attr的初始化)
		engineApiGas.AddTimer(0.2, self.Init)
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self._server = None
		# 存储数据
		self.SaveRemoldData()
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.CarClientSystem)
	def CarCtrlEvent(self, args):
		"""载具控制事件"""
		entityId = args.get("entityId")
		if entityId == self._entityId:
			stage = args.get("stage")
			func = self._eventFunctions.get(stage)
			if func:
				func(args)
		pass

	def CarSubscribeEvent(self, args):
		"""载具订阅事件"""
		stage = args.get("stage")
		func = self._eventFunctions.get(stage)
		if func:
			func(args)
		pass
	# endregion

	# region 改造UI相关
	def OpenRemoldUI(self, playerId):
		"""打开改造UI请求"""
		info = {
			"stage": "open_remold",
			"entityId": self._entityId,
			"usePartData": self._usePartData,
			"unlockPartList": self._unlockPartList,
		}
		self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass

	def SetInstallPart(self, args):
		"""安装配件"""
		playerId = args.get("__id__")
		partId = args.get("partId")
		remoldType = args.get("remold")
		# 校验配件和类型是否匹配
		partList = GetRemoldParts(remoldType)
		if partId not in partList:
			return
		
		usePart = self._usePartData.get(remoldType)
		if usePart != partId:
			# 对变形模块特殊处理：如果安装的是已使用的配件，则交换type的配件
			if "module" in remoldType:
				# 获取使用了该配件的类型
				userPartType = None
				for key, value in self._usePartData.iteritems():
					if value == partId:
						userPartType = key
						break
				# 直接更换数据，不需要执行卸载
				if userPartType is not None:
					self._usePartData[remoldType] = partId
					self._usePartData[userPartType] = usePart
					# 更新UI
					info = {
						"stage": "update_remold",
						"type": remoldType,
						"partId": partId,
					}
					self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
					info = {
						"stage": "update_remold",
						"type": userPartType,
						"partId": usePart,
					}
					self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
					return
				# 没有在使用的，则执行通用逻辑
			# 判断是否解锁
			canInstall = False
			if partId in self._unlockPartList:
				canInstall = True
			else:
				# 扣除物品，进行解锁
				partCfg = GetPartConfig(partId)
				if partCfg and partCfg.get("itemName"):
					material = [{"newItemName": partCfg.get("itemName"), "newAuxValue": 0, "count": 1}]
					isDeduct = serverApiMgr.DeductMultiItemsCount(playerId, material)
					if isDeduct:
						canInstall = True
						# 记录解锁数据
						self._unlockPartList.append(partId)
			if canInstall:
				# 安装
				self.InstallPartAttr(remoldType, partId)
				# 更新客户端UI
				info = {
					"stage": "update_remold",
					"type": remoldType,
					"partId": partId,
				}
				self.SendMsgToClient(playerId, eventConfig.CarCtrlEvent, info)
		pass
	# endregion

	# region 改造功能
	def Init(self):
		"""初始化改造数据"""
		# 加载改造数据
		self.LoadRemoldData()

		# 默认解锁的配件
		for rtype in GetRemoldTypeTabsList():
			partList = GetRemoldParts(rtype)
			for partId in partList:
				cfg = GetPartConfig(partId)
				if cfg:
					if cfg.get("unlock") and partId not in self._unlockPartList:
						# 解锁配件
						self._unlockPartList.append(partId)
					if cfg.get("use") and self._usePartData.get(rtype) is None:
						# 安装配件
						if cfg.get("use_to_remold"):
							if cfg["use_to_remold"] == rtype:
								self.InstallPartAttr(rtype, partId)
						else:
							self.InstallPartAttr(rtype, partId)
			pass

		# 同步一次molang数据到客户端
		self.SyncPartsMolangs()
		pass

	def InstallPartAttr(self, remoldType, partId):
		"""安装配件的属性处理"""
		lastPart = self._usePartData.get(remoldType)
		self._usePartData[remoldType] = partId
		# 存储数据
		self.SaveRemoldData()

		# 如果之前的配件有属性加成，则需减少这些属性
		addDurabilityCache = 0
		addEnergyCache = 0
		lastCfg = GetPartConfig(lastPart)
		if lastCfg and lastCfg.get("attrs"):
			attrCfg = lastCfg.get("attrs")
			# 最大耐久
			durability = attrCfg.get("max_durability")
			if durability > 0:
				addDurabilityCache -= durability
			# 最大能源
			energy = attrCfg.get("max_energy")
			if energy > 0:
				addEnergyCache -= energy
		
		# 如果该配件有属性加成，则增加属性上去
		cfg = GetPartConfig(partId)
		if cfg and cfg.get("attrs"):
			attrCfg = cfg.get("attrs")
			# 最大耐久
			durability = attrCfg.get("max_durability")
			if durability > 0:
				addDurabilityCache += durability
			# 最大能源
			energy = attrCfg.get("max_energy")
			if energy > 0:
				addEnergyCache += energy
		if addDurabilityCache != 0:
			self._carObj.UpdateMaxDurability(addDurabilityCache)
		if addEnergyCache != 0:
			self._carObj.UpdateMaxEnergy(addEnergyCache)
		
		# 设置外观表现
		self.SetPartMolangs(remoldType)
		pass

	def UnInstallPartAttr(self, remoldType):
		"""卸载配件的属性处理"""
		lastPart = self._usePartData.get(remoldType)
		self._usePartData.pop(remoldType, None)
		# 存储数据
		self.SaveRemoldData()

		# 如果之前的配件有属性加成，则需减少这些属性
		addDurabilityCache = 0
		addEnergyCache = 0
		lastCfg = GetPartConfig(lastPart)
		if lastCfg and lastCfg.get("attrs"):
			attrCfg = lastCfg.get("attrs")
			# 最大耐久
			durability = attrCfg.get("max_durability")
			if durability > 0:
				addDurabilityCache -= durability
			# 最大能源
			energy = attrCfg.get("max_energy")
			if energy > 0:
				addEnergyCache -= energy
		
		if addDurabilityCache != 0:
			self._carObj.UpdateMaxDurability(addDurabilityCache)
		if addEnergyCache != 0:
			self._carObj.UpdateMaxEnergy(addEnergyCache)
		
		# 设置外观表现
		self.SetPartMolangs(remoldType)
		pass

	def SetPartMolangs(self, remoldType):
		"""设置配件的molangs, 根据当前装的配件"""
		partId = self._usePartData.get(remoldType)
		value = 0
		if partId:
			cfg = GetPartConfig(partId)
			if cfg and cfg.get("molangValue") is not None:
				value = cfg.get("molangValue")
		molang = GetRemoldTypeMolangConfig(remoldType)
		if molang:
			# 根据改造类型，设置molangs
			info = {
				"entityId": self._entityId, 
				"molangValue": {
					molang: value,
				},
				"stage": "set_entity",
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass

	def SyncPartsMolangs(self):
		"""同步所有使用中的改造配件的molangs"""
		molangValues = {}
		for remoldType, partId in self._usePartData.iteritems():
			molang = GetRemoldTypeMolangConfig(remoldType)
			if molang:
				cfg = GetPartConfig(partId)
				if cfg and cfg.get("molangValue"):
					molangValues[molang] = cfg.get("molangValue")
		if molangValues:
			info = {
				"entityId": self._entityId,
				"molangValue": molangValues,
				"stage": "set_entity",
			}
			Instance.mEventMgr.NotifyEvent(eventConfig.MolangUpdateEvent, info)
		pass
	# endregion

	# region 属性方法
	def IsCanRunInWater(self):
		"""是否装配了水上行驶的配件"""
		return self._usePartData.get(RemoldTypeEnum.Module1) == PartEnum.RunWater or self._usePartData.get(RemoldTypeEnum.Module2) == PartEnum.RunWater
	
	def GetUsePartData(self):
		"""获取使用中的改造配件数据"""
		return self._usePartData
	
	def GetFrontBumperPartAttrCfg(self):
		"""获取前杠的attr加成数据"""
		partId = self._usePartData.get(RemoldTypeEnum.FrontBumper)
		if partId:
			cfg = GetPartConfig(partId)
			if cfg:
				return cfg.get("attrs")
		return None
	# endregion

	# region 改造数据存取
	def ExportDataToEntity(self, entityId):
		"""导出改造数据到实体"""
		extraComp = compFactory.CreateExtraData(entityId)
		data = {
			"usePartData": self._usePartData,
			"unlockPartList": self._unlockPartList,
		}
		extraComp.SetExtraData(ExtraDataKeyEnum.RemoldData, data)
		extraComp.SaveExtraData()
		pass

	def LoadRemoldData(self):
		"""获取改造数据"""
		isInit = False
		data = self._extraComp.GetExtraData(ExtraDataKeyEnum.RemoldData)
		if data is None:
			# 如果没有数据，则初始化使用全局的解锁进度数据
			data = self.GetGlobalRemoldData()
			if data is None:
				isInit = True
				data = {"usePartData": {}, "unlockPartList": []}
			else:
				# 继承旧车辆的数据，需重新设置一次attr
				for rtype, partId in data.get("usePartData", {}).iteritems():
					self.InstallPartAttr(rtype, partId)
		self._usePartData = data.get("usePartData", {})
		self._unlockPartList = data.get("unlockPartList", [])
		# 保存一次
		if isInit:
			self.SaveRemoldData()
		return data
	
	def SaveRemoldData(self):
		"""保存改造数据"""
		data = {
			"usePartData": self._usePartData,
			"unlockPartList": self._unlockPartList,
		}
		self._extraComp.SetExtraData(ExtraDataKeyEnum.RemoldData, data)
		self._extraComp.SaveExtraData()
		self.SaveGlobalRemoldData(self._unlockPartList, self._usePartData)
		pass

	def GetGlobalRemoldData(self):
		"""获取全局改造数据"""
		return self._globalExtraComp.GetExtraData(ExtraDataKeyEnum.RemoldData)
	
	def SaveGlobalRemoldData(self, unlockPartList, usePartData):
		"""保存全局改造数据"""
		data = self.GetGlobalRemoldData()
		if data is None:
			data = {"usePartData": usePartData, "unlockPartList": unlockPartList}
		else:
			# 仅保存新增的部分
			for partId in unlockPartList:
				if partId not in data["unlockPartList"]:
					data["unlockPartList"].append(partId)
			for rtype, partId in usePartData.iteritems():
				data["usePartData"][rtype] = partId
		self._globalExtraComp.SetExtraData(ExtraDataKeyEnum.RemoldData, data)
		self._globalExtraComp.SaveExtraData()
		pass
	# endregion
