# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.tasks.main import Config as MainTaskConfig
from ScukeSurviveScript.modCommon.cfg.tasks.against import Config as AgainstTaskConfig
from ScukeSurviveScript.modCommon.cfg.tasks.living import Config as LivingTaskConfig
from ScukeSurviveScript.modCommon.cfg.tasks.weapon import Config as WeaponTaskConfig
from ScukeSurviveScript.modCommon.cfg.tasks.building import Config as BuildingTaskConfig
from ScukeSurviveScript.modCommon.cfg.tasks.vehicle import Config as VehicleTaskConfig

__allGroupConfig__ = [
	MainTaskConfig,
	AgainstTaskConfig,
	LivingTaskConfig,
	WeaponTaskConfig,
	BuildingTaskConfig,
	VehicleTaskConfig,
]

__dict__ = {}

for config in __allGroupConfig__:
	for k, v in config.iteritems():
		if k in __dict__:
			print 'Waring! %s already exist!' % k
		__dict__[k] = v

Config = __dict__

def GetTaskConfig(uid):
	return __dict__.get(uid, None)
