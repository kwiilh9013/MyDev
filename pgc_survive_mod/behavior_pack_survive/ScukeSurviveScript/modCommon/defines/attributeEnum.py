# -*- encoding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.utils.mathUtils import MathUtils


class AttributeEnum(object):
	# Enum
	Health = 'Health'
	Speed = 'Speed'
	Damage = 'Damage'
	UnderwaterSpeed = 'UnderwaterSpeed'  # 水下移动速度
	Hunger = 'Hunger'  # 饥饿值
	Saturation = 'Saturation'  # 饱和值
	Absorption = 'Absorption'  # 伤害吸收生命值
	LavaSpeed = 'LavaSpeed'  # 岩浆移动速度
	Luck = 'Luck'  # 幸运值
	FollowRange = 'FollowRange'  # 跟随方块数(一般指怪的仇恨范围)
	KnockbackResistance = 'KnockbackResistance'  # 击退抵抗
	JumpStrength = 'JumpStrength'  # 跳跃力(指骑乘后跳跃可跳跃的高度)
	Armor = 'Armor'  # 护甲值，取决于身上穿戴的护甲总防御量
	# MaxAttr
	MaxHealth = 'MaxHealth'

	# Addon for Mod
	BodyTemp = 'BodyTemp'  # 体温
	Temperature = 'Temperature'  # 温度
	Radiation = 'Radiation'  # 辐射值
	RadiationAbsorption = 'RadiationAbsorption'  # 最大辐射吸收
	BodyHeatResistance = 'BodyHeatResistance'  # 自身耐热值
	BodyColdResistance = 'BodyColdResistance'  # 自身抗寒值
	HeatResistance = 'HeatResistance'  # 耐热值
	ColdResistance = 'ColdResistance'  # 抗寒值
	BodyRadiationResistance = 'BodyRadiationResistance'  # 自身抗辐射值
	RadiationResistance = 'RadiationResistance'  # 抗辐射值
	GunDamage = 'GunDamage'  # 枪械增伤
	MeleeDamage = 'MeleeDamage'  # 近战增伤

	# //////////////////////////////////////////////
	__RegisterAttrMCDic__ = {}
	__RegisterAttrRange__ = {}
	@staticmethod
	def Binding(attrType, mcAttrType, isMax=False, range=None):
		AttributeEnum.__RegisterAttrMCDic__[attrType] = {
			'type': mcAttrType,
			'isMax': isMax,
		}
		AttributeEnum.SetRange(attrType, range)

	@staticmethod
	def SetRange(attrType, range):
		AttributeEnum.__RegisterAttrRange__[attrType] = range

	@staticmethod
	def Clamp(attrType, value):
		range = AttributeEnum.__RegisterAttrRange__.get(attrType, None)
		if not range:
			return value
		return MathUtils.Clamp(value, range[0], range[1])

	@staticmethod
	def GetMCAttrType(attrType):
		if attrType in AttributeEnum.__RegisterAttrMCDic__:
			return AttributeEnum.__RegisterAttrMCDic__[attrType]
		return None