# -*- encoding: utf-8 -*-

class ProjectileEnum:
	"""抛射物id 枚举值"""

	GrenadeSmall = "scuke_survive:items_grenade_small_entity"
	"""小手雷"""
	GrenadeMiddle = "scuke_survive:items_grenade_middle_entity"
	"""中手雷"""
	GrenadeLarge = "scuke_survive:items_grenade_large_entity"
	"""大手雷"""

	# 怪物抛射物
	Venom = "scuke_survive:projectile_venom"
	"""毒液"""

	Missile = "scuke_survive:projectile_missile"
	"""导弹"""

	EMMissile = "scuke_survive:projectile_em_missile"
	"""电磁弹"""

	# __EnumList__ = []
	# @staticmethod
	# def EnumList():
	# 	"""获取枚举列表"""
	# 	if not ProjectileEnum.__EnumList__:
	# 		EnumList = [value for name, value in ProjectileEnum.__dict__.items() if not name.startswith('__') and not callable(value)]
	# 		ProjectileEnum.__EnumList__ = EnumList
	# 	return ProjectileEnum.__EnumList__
