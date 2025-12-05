# -*- coding: utf-8 -*-

# region 枚举
class NodeEnum(object):
	"""行为树 节点名字枚举"""
	Decorator = "Decorator"
	"""装饰节点：只有一个子节点，用于修饰或改变子节点的行为"""
	Action = "Action"
	"""动作节点"""
	Condition = "Condition"
	"""条件节点：检查条件是否满足"""
	Sequence = "Sequence"
	"""顺序节点：按顺序执行所有子节点，直到一个失败或全部成功"""
	Selector = "Selector"
	"""选择节点：按顺序执行子节点，直到一个成功或全部失败"""
	WeightedAction = "WeightedAction"
	"""加权动作节点"""
	WeightedSelector = "WeightedSelector"
	"""加权选择节点：根据子节点的权重随机选择一个子节点执行"""
	Repeater = "Repeater"
	"""重复节点：重复执行子节点指定次数"""
	Inverter = "Inverter"
	"""反转节点：反转子节点的执行结果"""

class KeyEnum(object):
	"""行为树 json的key枚举"""
	Type = "type"
	"""节点类型"""
	Action = "action"
	"""动作"""
	Condition = "condition"
	"""条件"""
	Weight = "weight"
	"""权重"""
	Children = "children"
	"""子节点列表"""
	Child = "child"
	"""子节点"""
	Repeats = "repeats"
	"""重复次数"""

class NodeStatus(object):
	"""
	定义节点可能的状态
	"""
	SUCCESS = 1  # 节点执行成功
	FAILURE = 2  # 节点执行失败
	RUNNING = 3  # 节点正在执行
# endregion

# region 节点类
class Node(object):
	"""
	所有节点的基类
	"""
	def __init__(self):
		self._parent = None  # 父节点引用

	def Run(self, context=None):
		"""
		抽象方法，子类必须实现
		"""
		raise NotImplementedError("子类必须实现Run方法")

class Composite(Node):
	"""
	复合节点：可以包含多个子节点的节点
	"""
	def __init__(self, children):
		super(Composite, self).__init__()
		self.mChildren = children  # 子节点列表
		for child in self.mChildren:
			child._parent = self  # 设置每个子节点的父节点

class Decorator(Node):
	"""
	装饰节点：只有一个子节点，用于修饰或改变子节点的行为
	"""
	def __init__(self, child):
		super(Decorator, self).__init__()
		self.mChild = child  # 单个子节点
		self.mChild._parent = self  # 设置子节点的父节点

class Action(Node):
	"""
	动作节点：执行具体动作的叶节点
	"""
	def __init__(self, actionFunc):
		super(Action, self).__init__()
		self._actionFunc = actionFunc  # 存储动作函数

	def Run(self, context=None):
		"""
		执行动作函数并返回结果
		"""
		return self._actionFunc(context)

class Condition(Node):
	"""
	条件节点：检查条件是否满足的叶节点
	"""
	def __init__(self, conditionFunc):
		super(Condition, self).__init__()
		self._conditionFunc = conditionFunc  # 存储条件函数

	def Run(self, context=None):
		"""
		执行条件函数，根据结果返回成功或失败
		"""
		return NodeStatus.SUCCESS if self._conditionFunc(context) else NodeStatus.FAILURE

class Sequence(Composite):
	"""
	顺序节点：按顺序执行所有子节点，直到一个失败或全部成功
	"""
	def Run(self, context=None):
		for child in self.mChildren:
			status = child.Run(context)
			if status != NodeStatus.SUCCESS:
				# 如果有一个子节点失败，立即返回失败状态
				return status
		# 所有子节点都成功，返回成功状态
		return NodeStatus.SUCCESS

class Selector(Composite):
	"""
	选择节点：按顺序执行子节点，直到一个成功或全部失败
	"""
	def Run(self, context=None):
		for child in self.mChildren:
			status = child.Run(context)
			if status == NodeStatus.SUCCESS:
				# 如果有一个子节点成功，立即返回成功状态
				return NodeStatus.SUCCESS
			elif status == NodeStatus.RUNNING:
				# 如果子节点正在运行，返回运行状态
				return NodeStatus.RUNNING
		# 所有子节点都失败，返回失败状态
		return NodeStatus.FAILURE
	
class WeightedNode(Node):
	"""
	加权节点：多了权重的参数
	"""
	def __init__(self, weight=0):
		super(WeightedNode, self).__init__()
		self.weight = weight

class WeightedAction(WeightedNode, Action):
	"""
	加权动作节点：执行动作逻辑，多了权重的参数
	"""
	def __init__(self, actionFunc, weight=0):
		WeightedNode.__init__(self, weight)
		Action.__init__(self, actionFunc)

class WeightedSelector(Composite):
	"""
	加权选择节点：根据子节点的权重随机选择一个子节点执行
	只能出现Action节点
	"""
	def __init__(self, children):
		super(WeightedSelector, self).__init__(children)
		self._totalWeight = sum(child.mWeight for child in self.mChildren)

	def Run(self, context=None):
		import random
		choice = random.uniform(0, self._totalWeight)
		cumulativeWeight = 0
		for child in self.mChildren:
			cumulativeWeight += child.mWeight
			if choice <= cumulativeWeight:
				return child.Run(context)
		return NodeStatus.FAILURE  # 理论上不应该到达这里
	
class Repeater(Decorator):
	"""
	重复节点：重复执行子节点指定次数
	"""
	def __init__(self, child, numRepeats):
		super(Repeater, self).__init__(child)
		self._numRepeats = numRepeats  # 重复次数

	def Run(self, context=None):
		for _ in xrange(self._numRepeats):
			status = self.mChild.Run(context)
			if status != NodeStatus.SUCCESS:
				# 如果子节点失败或正在运行，立即返回该状态
				return status
		# 所有重复都成功完成，返回成功状态
		return NodeStatus.SUCCESS

class Inverter(Decorator):
	"""
	反转节点：反转子节点的执行结果
	"""
	def Run(self, context=None):
		status = self.mChild.Run(context)
		if status == NodeStatus.SUCCESS:
			return NodeStatus.FAILURE
		elif status == NodeStatus.FAILURE:
			return NodeStatus.SUCCESS
		# 如果子节点正在运行，保持运行状态
		return NodeStatus.RUNNING
# endregion

# region 行为树类
class BehaviorTree(object):
	"""
	行为树类：封装整个行为树
	"""
	def __init__(self, root):
		self.mRoot = root  # 行为树的根节点

	def Run(self, context=None):
		"""
		从根节点开始执行行为树
		"""
		return self.mRoot.Run(context)
	
	@classmethod
	def FromJsonOrDict(cls, jsonConfig, actionDict, conditionDict):
		"""
		从JSON配置/字典创建行为树
		:param jsonConfig: JSON格式的行为树配置
		:param actionDict: 动作函数字典
		:param conditionDict: 条件函数字典
		:return: BehaviorTree实例
		"""
		def CreateWeightedNode(config):
			nodeType = config[KeyEnum.Type]
			weight = config.get(KeyEnum.Weight, 0)  # 如果没有配置权重，默认为0

			if nodeType == NodeEnum.Action:
				return WeightedAction(actionDict[config[KeyEnum.Action]], weight)
			else:
				raise ValueError("Invalid node type for WeightedSelector child: " + nodeType)

		def CreateNode(config):
			nodeType = config[KeyEnum.Type]

			if nodeType == NodeEnum.WeightedSelector:
				children = [CreateWeightedNode(c) for c in config[KeyEnum.Children]]
				return WeightedSelector(children)
			
			nodeCreators = {
				NodeEnum.Sequence: lambda: Sequence([CreateNode(c) for c in config[KeyEnum.Children]]),
				NodeEnum.Selector: lambda: Selector([CreateNode(c) for c in config[KeyEnum.Children]]),
				NodeEnum.WeightedSelector: lambda: WeightedSelector([CreateNode(c) for c in config[KeyEnum.Children]]),
				NodeEnum.Repeater: lambda: Repeater(CreateNode(config[KeyEnum.Child]), config[KeyEnum.Repeats]),
				NodeEnum.Inverter: lambda: Inverter(CreateNode(config[KeyEnum.Child])),
				NodeEnum.Action: lambda: Action(actionDict[config[KeyEnum.Action]]),
				NodeEnum.Condition: lambda: Condition(conditionDict[config[KeyEnum.Condition]])
			}
			nodeCeatorFunc = nodeCreators.get(nodeType)
			if nodeCeatorFunc:
				return nodeCeatorFunc()  # 调用 lambda 函数创建节点
			else:
				raise ValueError("Unknown node type: " + nodeType)

		if isinstance(jsonConfig, str):
			# 是字符串，转换为字典
			import json
			configDict = json.loads(jsonConfig)
		else:
			configDict = jsonConfig
		root = CreateNode(configDict)
		return cls(root)

"""
行为树 格式：
{
	"type": "Selector",
	"children": [
		{
			"type": "Sequence",
			"children": [
				{
					"type": "Condition",
					"condition": "IsEnemyVisible"
				},
				{
					"type": "Action",
					"action": "MoveToEnemy"
				},
				{
					"type": "Action",
					"action": "AttackEnemy"
				}
			]
		},
		{
			"type": "WeightedSelector",
			"children": [
				{
					"type": "Action",
					"weight": 0.7,
					"action": "Patrol"
				},
				{
					"type": "Action",
					"weight": 0.7,
					"action": "Hide"
				}
			]
		},
		{
			"type": "Repeater",
			"child": {
				"type": "Action",
				"action": "Patrol"
			},
			"repeats": 2
		},
		{
			"type": "Inverter",
			"child": {
				"type": "Action",
				"action": "Patrol"
			}
		},
	]
}
"""
# endregion