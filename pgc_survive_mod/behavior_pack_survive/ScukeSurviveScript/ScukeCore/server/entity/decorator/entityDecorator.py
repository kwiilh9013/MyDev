# -*- encoding: utf-8 -*-
import functools
# from ScukeSurviveScript.ScukeCore.server.entity.enum.componentMapping import ComponentClassMapping


"""
装饰器执行的时机是在对应代码被加载时执行, 比如import
"""


# def AddCompClsMapping(compType):
# 	"""添加组件类的映射 废弃"""
# 	# 使用装饰器的话，就不需要导入组件类，但不导入组件类，就无法加载py文件，从而不触发装饰器逻辑，形成死循环
# 	def decorator(cls):
# 		ComponentClassMapping.AddMapping(compType, cls)
# 		return cls
# 	return decorator


# 在这里无法传入self参数，只能给方法写入新属性，然后在对象初始化时，根据方法的属性来执行逻辑
def AddActionMapping(actionType):
	"""添加行为方法 装饰器"""
	def decorator(func):
		@functools.wraps(func)
		def wrapper(self, *args, **kwargs):
			return func(self, *args, **kwargs)
		# 向方法写入数据，以便在类初始化时获取到数据
		wrapper._actionType = actionType
		return wrapper
	return decorator

