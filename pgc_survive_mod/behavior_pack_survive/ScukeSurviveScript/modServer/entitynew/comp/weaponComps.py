# -*- encoding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeSurviveScript.ScukeCore.server.entity.component.activeComponentBase import ActiveComponentBase
from ScukeSurviveScript.ScukeCore.server.entity.decorator.entityDecorator import AddActionMapping
from ScukeSurviveScript.modCommon.defines.entityAIEnum import GameActionEnum
minecraftEnum = serverApi.GetMinecraftEnum()


"""
枪械、近战武器 相关的组件
非通用组件，需行为包、实体类有相关内容的支持
"""

class WeaponComp(ActiveComponentBase):
	"""枪械、近战武器 组件"""
	def __init__(self, entityObj, config):
		super(WeaponComp, self).__init__(entityObj, config)

		self._gunSystem = entityObj.mGunSystem
		self._meleeSystem = entityObj.mMeleeSystem
		pass

	@AddActionMapping(GameActionEnum.GunShoot)
	def GunShoot(self, cfg):
		"""射击"""
		if cfg.get("state"):
			# 开始射击
			args = {
				"id": self.mEntityId,
				"identifier": self.mEntityObj.mCurItem,
				"taragetId": self.mEntityObj.GetAttackTargetId(),
			}
			self._gunSystem.OnShootKeyDownByAI(args)
		else:
			# 停止射击
			args = {
				"id": self.mEntityId,
				"identifier": self.mEntityObj.mCurItem,
			}
			self._gunSystem.OnShootKeyUpByAI(args)
		pass

	@AddActionMapping(GameActionEnum.GunReload)
	def GunReload(self, cfg):
		"""装弹"""
		args = {
			"id": self.mEntityId,
			"identifier": self.mEntityObj.mCurItem,
		}
		self._gunSystem.OnReloadKeyDonwByAI(args)
		pass
	
	@AddActionMapping(GameActionEnum.WeaponMelee)
	def WeaponMelee(self, cfg):
		"""枪械、武器 近战攻击"""
		# 枪械只有在True时执行一次
		# 近战武器则是按下、松开分别执行
		if cfg.get("state"):
			args = {
				"id": self.mEntityId,
				"identifier": self.mEntityObj.mCurItem,
				"taragetId": self.mEntityObj.GetAttackTargetId(),
			}
			if self.mEntityObj.mIsRangedAttack:
				self._gunSystem.OnMeleeKeyDownByAI(args)
			else:
				self._meleeSystem.OnAttackKeyDownByAI(args)
		else:
			args = {
				"id": self.mEntityId,
				"identifier": self.mEntityObj.mCurItem,
			}
			self._meleeSystem.OnAttackKeyUpByAI(args)
		pass
