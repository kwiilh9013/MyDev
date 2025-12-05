# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.defines.dataset.base import DatasetObj
from ScukeSurviveScript.modCommon.defines.attributeEnum import AttributeEnum
from ScukeSurviveScript.modCommon.cfg.livingConfig import Config as LivingConfig

class BuffState(DatasetObj):
	eid = str
	type = str
	interval = float
	duration = float
	amplifier = int
	attr = str
	value = float
	undo = bool
	immediate = bool
	_modified = float
	_passedTime = float

class BuffServerData(DatasetObj):
	__type__ = (list, BuffState)
