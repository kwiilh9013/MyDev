# -*- encoding: utf-8 -*-

def GetOwner(self):
	return self._owner

def SetOwner(self, actor):
	self._owner = actor

def GetParent(self):
	return self._parent

class PropertyMeta(type):
	def __new__(cls, name, bases, dct):  # noqa
		# data member
		dct['_prop_id'] = 0 # int
		dct['_prop_type'] = 1 # PropertyValueType
		dct['_owner'] = None # property owner: type(Entity), readonly
		dct['_parent'] = None # parent property: type(PropertyBase), readonly
		dct['_state'] = -1 # number
		dct['property_key'] = None # string | number
		# method member
		dct["GetOwner"] = GetOwner
		dct["GetParent"] = GetParent
		dct["SetOwner"] = SetOwner
		newcls = super(PropertyMeta, cls).__new__(cls, name, bases, dct)
		return newcls

class MInt(object):
	def __init__(self, val):
		self.value = val

	def __index__(self):
		return self.value
	
	def set(self, val):
		self.value = val
	
	def get(self):
		return self.value

class AoiProperty(object):
	__metaclass__ = PropertyMeta

	def __init__(self, propId, obj):
		self.py_obj = obj
		self.prop_id = propId
		
	def GetPyObject(self):
		return self.py_obj

	def Set(self, val):
		self.py_obj and self.py_obj.Set(val)

class Actor(object):
	def __init__(self, entityId, identifier):
		self.mEntityId = entityId
		self.mIdentifier = identifier
		self.mPropDict = {}
	
	def __getattr__(self, name):
		val = self.mPropDict.get(name, None)
		if val is not None:
			return val.get()
		return super(Actor, self).__getattr__(name)
	
	def __setattr__(self, name, value):
		val = self.mPropDict.get(name, None)
		if val is not None:
			val.set(value)
		else:
			super(Actor, self).__setattr__(name, value)
