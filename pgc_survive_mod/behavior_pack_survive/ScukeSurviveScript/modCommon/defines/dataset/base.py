# -*- encoding: utf-8 -*-
import types

class DatasetObj(object):
	__type__ = dict
	_version_ = 1

	@staticmethod
	def Build(cls):
		all_attributes = dir(cls)
		class_variables = [attr for attr in all_attributes if not attr.startswith('__')]
		if cls.__type__ == dict:
			ret = {}
			for var in class_variables:
				vt = getattr(cls, var)
				if type(vt) == types.FunctionType:
					continue
				ret[var] = DatasetObj._GetValue(vt)
			return ret
		elif isinstance(cls.__type__, tuple):
			vt = cls.__type__
			len_v = len(vt)
			if len_v > 0:
				if vt[0] == list:
					return []
		return None

	@staticmethod
	def _GetValue(vt):
		if isinstance(vt, type) and issubclass(vt, DatasetObj):
			return DatasetObj.Build(vt)
		elif type(vt) == type or isinstance(vt, type):
			if vt is int:
				vt = 0
			elif vt is float:
				vt = 0.0
			elif vt is str:
				vt = ""
			elif vt is list:
				vt = []
			elif vt is dict:
				vt = {}
			elif vt is tuple:
				vt = ()
			elif vt is bool:
				vt = False
			else:
				vt = None
		elif isinstance(vt, tuple):
			len_v = len(vt)
			if len_v > 0:
				if isinstance(vt[0], type):
					vt = DatasetObj._GetValue(vt[0])
		return vt

	@staticmethod
	def Format(cls, data):
		if not (isinstance(cls, type) and issubclass(cls, DatasetObj)):
			return data
		built = DatasetObj.Build(cls)
		builtType = type(built)
		if builtType != type(data):
			return built
		if builtType == dict:
			keys = built.keys()
			old_version = data.get('_version_', 0)
			# For version update
			if old_version != cls._version_ and getattr(cls, 'Update', None) is not None:
				update = getattr(cls, 'Update', None)
				if update is not None:
					data = update(data, old_version)
			ret = {}
			for key in keys:
				value = built[key]
				if key not in data:
					ret[key] = value
				else:
					ret[key] = data[key]
					vt = getattr(cls, key)
					if isinstance(vt, type) and issubclass(vt, DatasetObj):
						ret[key] = DatasetObj.Format(vt, ret[key])
					elif isinstance(vt, tuple):
						len_v = len(vt)
						if len_v > 0:
							if vt[0] is list:
								dataValue = data[key]
								retValue = []
								i = 0
								while i < len(dataValue):
									retValue.append(DatasetObj.Format(vt[1], dataValue[i]))
									i += 1
								ret[key] = retValue
					# TODO tuple
			return ret
		elif builtType == list:
			vt = cls.__type__
			ret = []
			if isinstance(vt, tuple):
				i = 0
				while i < len(data):
					ret.append(DatasetObj.Format(vt[1], data[i]))
					i += 1
			return ret