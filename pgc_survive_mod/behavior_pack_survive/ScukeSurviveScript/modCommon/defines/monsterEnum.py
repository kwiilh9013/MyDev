# -*- encoding: utf-8 -*-
class MonsterEnum:
	"""怪物id 枚举值"""

	ZombieBaby = "scuke_survive:zombie_baby"
	"""幼年僵尸"""
	ZombieNormal = "scuke_survive:zombie_normal"
	"""普通僵尸"""
	ZombieDog = "scuke_survive:zombie_dog"
	"""僵尸犬"""
	ZombieGuard = "scuke_survive:zombie_guard"
	"""保安僵尸"""
	ZombieChick = "scuke_survive:zombie_chick"
	"""辣妹僵尸"""
	ZombieGangs = "scuke_survive:zombie_gangs"
	"""帮派僵尸"""
	ZombieExplosive = "scuke_survive:zombie_explosive"
	"""自爆僵尸"""
	ZombieVenom = "scuke_survive:zombie_venom"
	"""毒液僵尸"""
	ZombieFat = "scuke_survive:zombie_fat"
	"""胖子僵尸"""
	ZombieOtaku = "scuke_survive:zombie_otaku"
	"""肥宅僵尸"""
	ZombieGrandpa = "scuke_survive:zombie_grandpa"
	"""老大爷僵尸"""
	ZombieJocker = "scuke_survive:zombie_jocker"
	"""小丑僵尸"""

	#变种僵尸
	ZombieCaptain = "scuke_survive:zombie_captain"
	"""僵尸队长"""
	ZombieGangsCaptain = "scuke_survive:zombie_gangs_captain"
	"""帮派头目僵尸"""
	ZombieSpicyChick = "scuke_survive:zombie_spicy_chick"
	"""麻辣辣妹僵尸"""
	ZombieHypertensionGrandpa = "scuke_survive:zombie_hypertension_grandpa"
	"""高血压老大爷僵尸"""
	ZombieFlameVenom= "scuke_survive:zombie_flame_venom"
	'''火焰毒液僵尸'''
	ZombieBabyExplose = "scuke_survive:zombie_baby_explose"
	'''巨型巨人僵尸所扔出的炸弹婴儿僵尸'''
	ZombieSuperTNT = "scuke_survive:zombie_supertnt"
	"""超级TNT僵尸"""
	ZombieTonsKing = "scuke_survive:zombie_tons_king"
	"""百吨王僵尸"""
	ZombieSpecialGuard = "scuke_survive:zombie_special_guard"
	"""特种保安僵尸"""
	ZombieBig = "scuke_survive:zombie_big"
	"""大型僵尸"""
	ZombieBigDog = "scuke_survive:zombie_big_dog"
	"""大型僵尸犬"""
	ZombieGoldenChick = "scuke_survive:zombie_golden_chick"
	"""黄金辣妹僵尸"""
	ZombieBlackVenom = "scuke_survive:zombie_black_venom"
	"""黑色毒液僵尸"""
	ZombieGiantKing = "scuke_survive:zombie_giant_king"
	"""雪崩巨人"""
	ZombieGiantSarcoma = "scuke_survive:zombie_giant_sarcoma"
	"""巨型肉瘤僵尸"""
	ZombieOtakuBlack = "scuke_survive:zombie_otaku_black"
	"""暗黑肥宅僵尸"""
	ZombieJockerKing = "scuke_survive:zombie_jocker_king"
	"""joker小丑僵尸"""
	# Boss
	ZombieGiant = "scuke_survive:zombie_giant"
	"""独眼巨人僵尸"""
	ZombieSarcoma = "scuke_survive:zombie_sarcoma"
	"""僵尸肉团"""
	ZombieFlyingLava = "scuke_survive:zombie_flyinglava"
	"""飞天熔岩僵尸"""
	ZombieBigGiant = "scuke_survive:zombie_big_giant"
	'''超大巨人僵尸'''

	# 第二批
	ZombieSnapKiller = "scuke_survive:zombie_snap_killer"
	"""瞬杀者"""
	ZombieWitch = "scuke_survive:zombie_witch"
	"""尖叫者"""
	ZombieWitchNormal = "scuke_survive:zombie_witch_normal"
	"""失落女孩"""

	# 反叛军
	RebelRagman = "scuke_survive:rebel_ragman"
	"""反叛军-破烂佬"""
	RebelVagrant = "scuke_survive:rebel_vagrant"
	"""反叛军-流浪者"""
	RebelSoilder = "scuke_survive:rebel_soldier"
	"""反叛军士兵"""
	RebelLeader = "scuke_survive:rebel_leader"
	"""反叛军队长"""
	RebelFlyingdrone = "scuke_survive:flyingdrone_boom"
	"""自爆无人机"""

	# 难民
	RefugeeBandit = "scuke_survive:refugee_bandit"
	"""强盗"""



_BossList = [
	MonsterEnum.ZombieGiant,
	MonsterEnum.ZombieBigGiant,
	MonsterEnum.ZombieSarcoma,
	MonsterEnum.ZombieFlyingLava,
	MonsterEnum.ZombieGiantKing,
	MonsterEnum.ZombieGiantSarcoma,
]
def GetBossList():
	return _BossList


class MosterAbilityEventEnum:
	"""怪物能力 枚举值"""
	Swimming = "scuke_survive:can_swimming_event"
	"""游泳"""
	PutBlock = "scuke_survive:can_put_block_event"
	"""放置方块"""
	BreakBlock = "scuke_survive:can_break_block_event"
	"""破坏方块"""
	FireResistance = "fire_resistance"
	"""抗火"""