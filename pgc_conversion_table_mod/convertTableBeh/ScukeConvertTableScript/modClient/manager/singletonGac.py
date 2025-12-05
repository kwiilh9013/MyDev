# -*- coding: utf-8 -*-
from ScukeConvertTableScript.modCommon.manager import singleton


class SingletonGac(object):
	__metaclass__ = singleton.Singleton


Instance = SingletonGac()
