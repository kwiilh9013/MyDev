# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.server.entity.enum.actionEnum import ActionEnum


"""
实体AI相关的枚举
"""


class GameActionEnum(ActionEnum):
	"""本模组的动作方法 枚举"""

	GunShoot = "GunShoot"
	"""枪械发射子弹"""
	GunReload = "GunReload"
	"""枪械装弹"""
	WeaponMelee = "WeaponMelee"
	"""枪械、武器 近战"""
	WitchSummonEtity = "WitchSummonEtity"
	"""witch生成生物"""
	SnapKillerJumpAttack = "SnapKillerJumpAttack"
	"""瞬杀者跳跃攻击"""


class GameCompEnum():
	"""
	本模组的组件key 枚举
		用于config填写、行为逻辑判断使用, 同一个实体不同组件都需要单独的key(同一类组件、不同配置当作不同组件处理)。
		不同实体, 可复用同一个key。
	"""
	# Witch 组件
	WitchSummonEtity = "witch_summon_entity"
	"""witch生成生物"""
	WitchSitDownToCry = "witch_sit_down_to_cry"
	"""witch坐下"""
	WitchSitUp= "witch_sit_up"
	"""witch起立"""
	WitchMoveUp = "witch_move_up"
	"""witch移动起"""
	WitchMoveDownToCry = "witch_move_down_to_cry"
	"""witch移动下"""
	WitchMeleeAttack1 = "witch_melee_attack1"
	"""witch攻击方式1"""
	WitchMeleeAttack2 = "witch_melee_attack2"
	"""witch攻击方式2"""

	# 瞬杀者 组件
	SnapKillerMeleeAttack1 = "snap_killer_melee_attack1"
	"""瞬杀者攻击方式1"""
	SnapKillerMeleeAttack2 = "snap_killer_melee_attack2"
	"""瞬杀者攻击方式1"""
	SnapKillerJumpReady = "snap_Killer_jump_ready"
	"""瞬杀者跳跃准备"""
	SnapKillerJumpFly = "snap_Killer_jump_fly"
	"""瞬杀者跳跃"""
	SnapKillerCoerceAttack = "snap_killer_coerce_attack"
	"""瞬杀者抓挠攻击"""
	SnapKillerCancelJumpReady = "snap_killer_cancel_jump_ready"
	"""瞬杀者取消跳跃准备"""


	Shoot1 = "shoot_1"
	"""射击1"""
	Reload = "reload"
	"""装弹"""
	MeleeAttack1 = "melee_1"
	"""近战攻击1"""
	Teleport = "teleport"
	"""瞬移"""

	# 被动
	ImmuneProjectile = "immune_projectile"
	"""免疫远程伤害"""
	HealthRecover = "recover"
	"""低血量喝药回血"""
	AvoidMob = "avoid_mob"
	"""低血量躲避怪物"""
	SummonRebel = "summon_rebel"
	"""召唤反叛军"""
	SummonFlyingdrone = "summon_flyingdrone"
	"""召唤无人机"""
	ShowParachute = "show_parachute"
	"""显示降落伞"""
	HideParachute = "hide_parachute"
	"""隐藏降落伞"""

