# -*- encoding: utf-8 -*-


class EntityTagEnum:
	"""实体tag 枚举, 用于AddEntityTag接口"""

	TaskEntity = "task_entity"
	"""任务实体, 影响怪物仇恨范围"""


class EntityFamilyEnum:
	"""实体family标签 枚举"""

	Player = "player"
	"""玩家"""
	Mercenary = "mercenary"
	"""雇佣兵, 驯服的黄金苦力怕"""

	Monster = "monster"
	"""怪物"""
	Zombie = "zombie"
	"""僵尸"""

	Rebel = "rebel"
	"""反叛军"""
	Refugee = "refugee"
	"""难民、强盗"""

