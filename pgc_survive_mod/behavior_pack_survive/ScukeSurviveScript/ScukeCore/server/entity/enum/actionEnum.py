# -*- encoding: utf-8 -*-


class ActionEnum(object):
	"""动作方法 枚举"""

	SetMolang = "SetMolang"
	"""设置molang"""
	TriggerAddEvent = "TriggerAddEvent"
	"""触发行为包event"""
	ResetAttackTarget = "ResetAttackTarget"
	"""清除仇恨目标"""

	AreaAttack = "AreaAttack"
	"""范围攻击"""
	TeleportToTarget = "TeleportToTarget"
	"""瞬移到指定位置"""
	SummonEntity = "SummonEntity"
	"""生成实体"""

