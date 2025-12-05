# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum
from ScukeSurviveScript.modCommon.cfg.livingConfig import Config as LivingConfig

class AttrServerData(DatasetObj):
	@staticmethod
	def Update(data, version):
		return data

setattr(AttrServerData, AttributeEnum.BodyTemp, LivingConfig['bodyTemp'])
setattr(AttrServerData, AttributeEnum.BodyColdResistance, LivingConfig['bodyColdResistance'])
setattr(AttrServerData, AttributeEnum.BodyHeatResistance, LivingConfig['bodyHeatResistance'])
setattr(AttrServerData, AttributeEnum.BodyRadiationResistance, LivingConfig['bodyRadiationResistance'])
setattr(AttrServerData, AttributeEnum.RadiationAbsorption, LivingConfig['radiationAbsorption'])

setattr(AttrServerData, AttributeEnum.Temperature, 0)
setattr(AttrServerData, AttributeEnum.Radiation, 0)
setattr(AttrServerData, AttributeEnum.HeatResistance, 0)
setattr(AttrServerData, AttributeEnum.ColdResistance, 0)
setattr(AttrServerData, AttributeEnum.RadiationResistance, 0)
setattr(AttrServerData, AttributeEnum.GunDamage, 0)
setattr(AttrServerData, AttributeEnum.MeleeDamage, 0)
