# -*- encoding: utf-8 -*-


Config = {
	'@NpcConsumeTaskTemplate': {
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000110': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_golden_creeper',
		'name': '黄金苦力怕',
		'text': '',
		'phases': [
			{
				'type': 'random',
				'phases': [
					{
						'type': 'text',
						'text': '…………能给我吃好吃的炸药吗…',
						'weight': 80,
					},
					{
						'type': 'text',
						'text': '…………谁给我吃炸药，我就跟谁',
						'weight': 20,
					}
				],
			}
		],
		'next': ['1000111', '1000112'],
		'startActionData': None,
		'endActionData': None
	},
	'1000111': {
		'text': '给你炸药',
		'phases': [
			{
				'type': 'text',
				'text': '滋滋滋…',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': {
			'UseItemToNpc': {
				'value': 1,
				'item': 'minecraft:tnt',
				'name': '炸药'
			}
		}
	},
	'1000112': {
		'text': '算了，没有',
		'phases': [
			{
				'type': 'text',
				'text': '…要爆炸要爆炸…',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000120': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_golden_creeper',
		'name': '黄金苦力怕',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '…………能给我吃好吃的炸药吗…',
				'weight': 80,
			},
		],
		'next': ['1000111', '1000121', '1000122', '1000112'],
		'startActionData': None,
		'endActionData': None
	},
	'1000121': {
		'text': '我去去就来',
		'phases': [
			{
				'type': 'text',
				'text': '…滋…等…滋…你…',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': {
			'SetSitting': {'value': True}
		}
	},
	'1000122': {
		'text': '跟我走吧',
		'phases': [
			{
				'type': 'text',
				'text': '…滋…走…滋…',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': {
			'SetSitting': {'value': False}
		}
	},
	'1000210': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '你好，幸存者。我知道你迫切的想让发动机工作。但目前发动机遇到了些问题，无法运作。需要这些材料才能有效运作',
			}
		],
		'next': ['1000211', '1000212'],
		'startActionData': None,
		'endActionData': None
	},
	'1000211': {
		'text': '交付物品',
		'phases': [
			{
				'type': 'text',
				'text': '这些是必需品！',
			}
		],
		'next': '@GetNpcConsumeTasks',
		'startActionData': None,
		'endActionData': None,
	},
	'1000212': {
		'text': '再等等',
		'phases': [
			{
				'type': 'text',
				'text': '尽快！时间差不多咯',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000213': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '目标带来了吗？',
			}
		],
		'next': ['1000214', '1000212'],
		'startActionData': None,
		'endActionData': None
	},
	'1000214': {
		'text': '交付黄金苦力怕',
		'phases': [
			{
				'type': 'text',
				'text': '就差这个了！',
			}
		],
		'next': '@GetNpcConsumeCreeperTasks',
		'startActionData': None,
		'endActionData': None,
	},
	'1000215': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '现在就可以操作发动机！准备好了吗？！',
			}
		],
		'next': ['1000216', '1000212'],
		'startActionData': None,
		'endActionData': None,
	},
	'1000216': {
		'text': '操作发动机！',
		'phases': [
			{
				'type': 'text',
				'text': '启动发动机会惊扰怪物！我需要你争取一点时间！',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': {
			'StartGuardPlanetBooster': {
				'value': 0
			}
		},
	},
	'1000220': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '已经点火成功，快去寻找下一个吧！',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000230': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '这里似乎没有可以点火的装置...',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000240': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '当前轨道已点火，暂时无需操作',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000250': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '...你的身份没有权限执行此任务...',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000260': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_scientist',
		'name': '发动机工程师',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '...此处发动机未交付黄金苦力怕...',
			}
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000310': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_keke',
		'name': '韩可可',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '你醒了？太好了！我们得赶快行动，这里已经很危险了！赶紧拿好这些补给品，迅速行动！',
			},
			{
				'type': 'text',
				'text': '我们没有多少时间了，必须尽快修复发动机，逃离这个轨道！我相信我们一定能做到的，一起加油，别放弃！',
			},
		],
		'next': ['1000311', '1000312'],
		'startActionData': None,
		'endActionData': None
	},
	'1000311': {
		'text': '这里有资源补给？',
		'phases': [
			{
				'type': 'text',
				'text': '在我身边和卧室的箱子里，有一些重要的补给品，里面都是生存必需品。',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000312': {
		'text': '这里是什么情况？',
		'phases': [
			{
				'type': 'text',
				'text': '我们被拖入了火星轨道，不少星球发动机也损坏了。情况非常不妙！我们必须保持冷静，但也要迅速行动！',
			},
			{
				'type': 'text',
				'text': '我们没有多少时间了，必须尽快修复发动机，逃离这个轨道！我相信我们一定能做到的，一起加油，别放弃！',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000410': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_zhanjing',
		'name': '战京',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '你好，幸存者！欢迎来到车辆改造站。这里有一辆曾经的科技奇迹。它曾是我们的骄傲，但不幸的是，它被陨石砸坏了。现在看起来有些破败，但它依然有巨大的潜力。',
			},
		],
		'next': ['1000411', '1000413', '1000412'],
		'startActionData': None,
		'endActionData': None
	},
	'1000411': {
		'text': '如何修复它？',
		'phases': [
			{
				'type': 'text',
				'text': '你需要准备一些材料。',
			},
			{
				'type': 'text',
				'text': '虽然现在它看起来需要不少修理，但我相信，只要我们不放弃，它一定能重现辉煌！让我们一起努力，让它重新燃起希望的火焰吧！',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000412': {
		'text': '这车有什么用？',
		'phases': [
			{
				'type': 'text',
				'text': '如果你能修复它，这辆车可以再次乘风破浪，带你和你的伙伴们安全抵达目的地。此外，通过一些改造，它甚至可以进化为一台强大的战争机器，帮助你们在这个危险的世界中生存下去。',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000413': {
		'text': '我的车没了！',
		'phases': [
			{
				'type': 'text',
				'text': '幸存者，我这边还有一辆备用车。不过，燃料和资源都有限，你必须小心使用。',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': {
			'SpawnCar': {'value': 1}
		}
	},
	'1000510': {
		'avatar': 'textures/ui/scuke_survive/avatar/npc_wheelchair_man',
		'name': '陶吉吉',
		'text': '',
		'phases': [
			{
				'type': 'text',
				'text': '嘚~嘚~嘚~嘚……幸存者，你好。虽然这次轨道的脱离让我们损失惨重，多个星球发动机被摧毁。',
			},
			{
				'type': 'text',
				'text': '但别灰心，我们还有不少发动机可以拯救。只要咱们不放弃，就还有希望。来，咱们一起加油，把这些希望之火重新点燃！',
			},
		],
		'next': ['1000511', '1000512', '1000514', '1000513'],
		'startActionData': None,
		'endActionData': None
	},
	'1000511': {
		'text': '如何拯救这一切？',
		'phases': [
			{
				'type': 'text',
				'text': '哦~哦~额~唉~L……我们需要启动更多的星球发动机，只有这样才能让地球回到正轨。如果我们不能启动足够多的发动机，灾难就会再次降临。所以，加把劲儿，我们可是地球最后的希望！',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000512': {
		'text': '如何恢复发动机？',
		'phases': [
			{
				'type': 'text',
				'text': '噢~噢~耶呀~摇摇……不同发动机的损坏状态都不一样，但有一点相同——它们都缺少了核心的点燃材料——黄金苦力怕。黄金苦力怕可是我们研发出的最好的打火石。',
			},
			{
				'type': 'text',
				'text': '原本都好好地存放在地下实验室里，可这次灾难毁了那地方，黄金苦力只有在我身边这些，你可以带走它们，只有这样，我们才能重新启动这些发动机。',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000513': {
		'text': '怎么带走黄金苦力怕？',
		'phases': [
			{
				'type': 'text',
				'text': '啊~啊~啊~黄金苦力怕从小是吃TNT长大的，如果你手上拿着TNT。它就会和你成为好朋友！',
			},
			{
				'type': 'text',
				'text': '黄金苦力怕很聪明，它们甚至会坐车。',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': None
	},
	'1000514': {
		'text': '能给我黄金苦力怕吗？',
		'phases': [
			{
				'type': 'text',
				'text': '偶~偶~耶~我这里还有一些储备的黄金苦力怕，但是已经越来越少了，你必须好好珍惜它！',
			},
		],
		'next': None,
		'startActionData': None,
		'endActionData': {
			'SpawnGoldenCreeper': {'value': 1}
		}
	},
}