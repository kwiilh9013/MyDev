# -*- coding: utf-8 -*-
from ScukeConvertTableScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeConvertTableScript.modCommon import modConfig
import mod.server.extraServerApi as serverApi
from ScukeConvertTableScript.modCommon.cfg import ItemEMCConfig
from ScukeConvertTableScript.ScukeCore.server import engineApiGas


"""
# 需要在服务端脚本加载完毕后3秒后才能使用（建议）
def LoadServerAddonScriptsAfter(self, args=None):
	def _timerLink():
		linkSys = serverApi.GetSystem("scuke", "LinkServer")
		days100Cfg = {
			('scuke_survive:food_beef', 0): ['真相牛肉', 2333],
			('scuke_survive:melee_chainsaw', 0): ['电锯人', 8848],
		}
		if linkSys:
			linkSys.LinkEmcData("【惊变·星球生存】", days100Cfg)
			print "联动链接================="
	engineApiGas.AddTimer(3.0, _timerLink)
"""


class LinkServer(BaseServerSystem):
	"""
	其他模组联动方案
	其他模组需要设置emc值，通过此系统进行链接，这个系统的作用是避开直接对核心系统的设置干扰，防止其他开发者直接反注册核心系统
	"""
	def __init__(self, namespace, systemName):
		super(LinkServer, self).__init__(namespace, systemName)
		self.__mainServer__ = None
		self.baseCfg = ItemEMCConfig._AllItemEmc
		self.notice = serverApi.GetEngineCompFactory().CreateGame(engineApiGas.levelId).SetNotifyMsg

	def LinkEmcData(self, sysCnName="未知", linkEmcCfg=None):
		"""
		检验联动数据是否符合要求
		1.联动数据不能包含原版物品数据，如果带有任何一个原版物品数据，则直接联动失败；
		2.联动数据的数据格式校验，如果数据格式有误，则联动失败；
		"""
		# 模组名称格式检验
		if type(sysCnName) != str:
			self.notice("§cEMC联动失败！某模组传递了错误的信息，无法正常联动...")
			return
		# 模组EMC配置格式检验
		if type(linkEmcCfg) != dict:
			self.notice("§cEMC联动失败！%s传递了错误的EMC配置，无法正常联动..." % sysCnName)
			return
		if type(linkEmcCfg) == dict and not linkEmcCfg:
			self.notice("§cEMC联动失败！%s传递了空的EMC配置，无法正常联动..." % sysCnName)
			return
		for key, value in linkEmcCfg.items():
			if type(key) != tuple:
				self.notice("§cEMC联动失败！%s传递了错误的EMC键，无法正常联动..." % sysCnName)
				return
			if len(key) != 2:
				self.notice("§cEMC联动失败！%s传递的键有问题，无法正常联动..." % sysCnName)
				return
			k1, k2 = key
			if type(k1) != str or type(k2) != int:
				self.notice("§cEMC联动失败！%s传递的键的数据类型有问题，无法正常联动..." % sysCnName)
				return
			if type(value) != list:
				self.notice("§cEMC联动失败！%s传递了错误的EMC值，无法正常联动..." % sysCnName)
				return
			if len(value) != 2:
				self.notice("§cEMC联动失败！%s传递的值有问题，无法正常联动..." % sysCnName)
				return
			v1, v2 = value
			if type(v1) != str or type(v2) != int:
				self.notice("§cEMC联动失败！%s传递的值的数据类型有问题，无法正常联动..." % sysCnName)
				return
			# 模组EMC配置和原版物品冲突检验
			if key in self.baseCfg:
				self.notice("§cEMC联动失败！%s的配置和原版物品有冲突，无法正常联动..." % sysCnName)
				return
		mainServer = serverApi.GetSystem(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableMainServer)
		if not mainServer:
			self.notice("§cEMC联动失败！获取核心系统失败（可能是获取的时机不对）...请联系酸黄瓜" % sysCnName)
			return
		self.BroadcastEvent("OnLinkEmcDataSend", {"data": linkEmcCfg, "sysName": sysCnName})
