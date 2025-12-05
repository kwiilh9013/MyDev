# -*- encoding: utf-8 -*-

from ScukeSurviveScript.modCommon.cfg.gun.gun_bazooka1_s1 import Config as GunBazooka1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_bazooka1_s2 import Config as GunBazooka1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_bazooka1_s3 import Config as GunBazooka1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_hmg1_s1 import Config as GunHmg1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_hmg1_s2 import Config as GunHmg1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_hmg1_s3 import Config as GunHmg1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_lmg1_s1 import Config as GunLmg1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_lmg1_s2 import Config as GunLmg1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_lmg1_s3 import Config as GunLmg1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_pistol1_s1 import Config as GunPistol1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_pistol1_s2 import Config as GunPistol1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_pistol1_s3 import Config as GunPistol1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_rifle1_s1 import Config as GunRifle1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_rifle1_s2 import Config as GunRifle1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_rifle1_s3 import Config as GunRifle1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_shotgun1_s1 import Config as GunShotgun1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_shotgun1_s2 import Config as GunShotgun1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_shotgun1_s3 import Config as GunShotgun1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_smg1_s1 import Config as GunSmg1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_smg1_s2 import Config as GunSmg1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_smg1_s3 import Config as GunSmg1_S3
from ScukeSurviveScript.modCommon.cfg.gun.gun_sniper1_s1 import Config as GunSniper1_S1
from ScukeSurviveScript.modCommon.cfg.gun.gun_sniper1_s2 import Config as GunSniper1_S2
from ScukeSurviveScript.modCommon.cfg.gun.gun_sniper1_s3 import Config as GunSniper1_S3
from ScukeSurviveScript.modCommon import modConfig

__gunList__ = [
	GunBazooka1_S1,
	GunBazooka1_S2,
	GunBazooka1_S3,
	GunHmg1_S1,
	GunHmg1_S2,
	GunHmg1_S3,
	GunLmg1_S1,
	GunLmg1_S2,
	GunLmg1_S3,
	GunPistol1_S1,
	GunPistol1_S2,
	GunPistol1_S3,
	GunRifle1_S1,
	GunRifle1_S2,
	GunRifle1_S3,
	GunShotgun1_S1,
	GunShotgun1_S2,
	GunShotgun1_S3,
	GunSmg1_S1,
	GunSmg1_S2,
	GunSmg1_S3,
	GunSniper1_S1,
	GunSniper1_S2,
	GunSniper1_S3,
]

__gunDic__ = {}
for config in __gunList__:
	__gunDic__[config['identifier']] = config


def GetConfig(identifier):
	if identifier in __gunDic__:
		return __gunDic__[identifier]
	return None


GunIdentifierPrefix = modConfig.ModNameSpace + ':gun_'

ForbidTakeGunRides = [
	'scuke_survive:base_car'
]
