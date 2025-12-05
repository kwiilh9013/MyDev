# -*- coding: utf-8 -*-
from ScukeSurviveScript.modCommon.manager import singleton


class SingletonGas(object):
	__metaclass__ = singleton.Singleton

Instance = SingletonGas()