# -*- encoding: utf-8 -*-
Config = {
	'100010': {
		'branch': 'main',
		'group': 'mars',
		'icon': 'textures/ui/scuke_survive/task/img_p_mars',
		'desc': '火星',
		'info': '在 §l火星 §r撞击阶段，找到完整的星球发动机，向工程师交付\n§b辣条x10 铅锭x10\n§e黄金苦力怕x1\n§r点燃星球发动机！',
		'level': 2,
		'type': 'numeric',
		'depends': ['100011', '100012', '100013', '100014'],
		'auto': False,
		'time': -1,
		'data': {
			'global_accumulations': {
				'PlanetBooster': {'activated': 1}
			}
		},
		'rewards': {
			'scuke_survive:gun_rifle1_s1': 1,
			'scuke_survive:clip_advanced': 6,
			'scuke_survive:items_grenade_small': 6,
			'scuke_survive:armor_snow01_helmet': 1,
			'scuke_survive:key_mars': 1,
		},
		'completed': {
			'op': 'ActivatePlanetBooster',
			'value': 1,
		},
		'failed': {
			'op': 'EscapeFailed',
			'value': 1,
		}
	},
	'100011': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '辣条x10',
		'info': '吃点辣条，我才能有精神干活',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:food_spicy_strip': 10
			},
		},
		'rewards': {},
	},
	'100012': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '铅锭x10',
		'info': '发动机需要更多铅锭，来修复',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:ingot_lead': 10
			},
		},
		'rewards': {},
	},
	'100013': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '黄金苦力怕x1',
		'info': '黄金苦力怕，是世上最好的爆燃物',
		'level': 0,
		'type': 'npcConsumeCreeper',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'entities': {
				'scuke_survive:npc_golden_creeper': 1
			},
		},
		'rewards': {},
	},
	'100014': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '操作发动机！',
		'info': '启动发动机会惊扰怪物！我需要你争取一点时间！',
		'level': 0,
		'type': 'guardPlanetBooster',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'global_accumulations': {
				'PlanetBooster': {'guard': 1}
			}
		},
		'rewards': {},
	},
	'100020': {
		'branch': 'main',
		'group': 'asteroid_belt',
		'icon': 'textures/ui/scuke_survive/task/img_p_asteroid_belt2',
		'desc': '小行星带',
		'info': '在 §l小行星带 §r撞击阶段，找到完整的星球发动机，向工程师交付\n§b金锭x20 稀土锭x20 小型电子芯片x2\n§e黄金苦力怕x2\n§r点燃星球发动机！',
		'level': 2,
		'type': 'numeric',
		'depends': ['100021', '100022', '100023', '100024', '100025'],
		'auto': False,
		'time': -1,
		'data': {
			'global_accumulations': {
				'PlanetBooster': {'activated': 1}
			}
		},
		'rewards': {
			'scuke_survive:gun_hmg1_s1': 1,
			'scuke_survive:clip_energy': 6,
			'scuke_survive:items_grenade_middle': 6,
			'scuke_survive:armor_safety_helmet': 1,
			'scuke_survive:key_asteroid': 1,
		},
		'completed': {
			'op': 'ActivatePlanetBooster',
			'value': 1,
		},
		'failed': {
			'op': 'EscapeFailed',
			'value': 1,
		}
	},
	'100021': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '金锭x20',
		'info': '没有黄金，怎么干活？',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'minecraft:gold_ingot': 10
			},
		},
		'rewards': {},
	},
	'100022': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '稀土锭x20',
		'info': '稀土是点燃发动机的重要材料',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:ingot_rare_earth': 10
			},
		},
		'rewards': {},
	},
	'100023': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '小型电子芯片x2',
		'info': '操作的机器，芯片坏了',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:mat_chip_small': 2
			},
		},
		'rewards': {},
	},
	'100024': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '黄金苦力怕x2',
		'info': '黄金苦力怕，是世上最好的爆燃物',
		'level': 0,
		'type': 'npcConsumeCreeper',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'entities': {
				'scuke_survive:npc_golden_creeper': 2
			},
		},
		'rewards': {},
	},
	'100025': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '操作发动机！',
		'info': '启动发动机会惊扰怪物！我需要你争取一点时间！',
		'level': 0,
		'type': 'guardPlanetBooster',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'global_accumulations': {
				'PlanetBooster': {'guard': 1}
			}
		},
		'rewards': {},
	},
	'100030': {
		'branch': 'main',
		'group': 'jupiter',
		'icon': 'textures/ui/scuke_survive/task/img_p_jupiter',
		'desc': '木星',
		'info': '在 §l木星 §r撞击阶段，找到完整的星球发动机，向工程师交付\n§b大窖汽水x5 大型电子芯片x2\n钇金陨石锭x30 抗生素x2\n§e黄金苦力怕x3\n§r点燃星球发动机！',
		'level': 2,
		'type': 'numeric',
		'depends': ['100031', '100032', '100033', '100036', '100035', '100037'],
		'auto': False,
		'time': -1,
		'data': {
			'global_accumulations': {
				'PlanetBooster': {'activated': 1}
			}
		},
		'rewards': {
			'scuke_survive:gun_lmg1': 1,
			'scuke_survive:clip_energy': 6,
			'scuke_survive:items_grenade_large': 6,
			'scuke_survive:armor_armor01_helmet': 1,
			'scuke_survive:key_jupiter': 1,
		},
		'completed': {
			'op': 'ActivatePlanetBooster',
			'value': 1,
		},
		'failed': {
			'op': 'EscapeFailed',
			'value': 1,
		}
	},
	'100031': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '大窖汽水x5',
		'info': '我需要更多气泡，来思考问题',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:food_drink_aim': 5
			},
		},
		'rewards': {},
	},
	'100032': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '大型电子芯片x2',
		'info': '操作的机器，芯片坏了',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:mat_chip_middle': 2
			},
		},
		'rewards': {},
	},
	'100033': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '钇金陨石锭x20',
		'info': '钇金是修复发动机的重要材料',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:ingot_yttrium': 20
			},
		},
		'rewards': {},
	},
	'100035': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '黄金苦力怕x3',
		'info': '黄金苦力怕，是世上最好的爆燃物',
		'level': 0,
		'type': 'npcConsumeCreeper',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'entities': {
				'scuke_survive:npc_golden_creeper': 3
			},
		},
		'rewards': {},
	},
	'100036': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '抗生素x2',
		'info': '我身体状况不好，需要点抗生素，来治疗！',
		'level': 0,
		'type': 'npcConsume',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'items': {
				'scuke_survive:food_antibiotic': 2
			},
		},
		'rewards': {},
	},
	'100037': {
		'branch': 'main_depends',
		'group': 'scuke_survive:npc_igniter',
		'icon': '',
		'desc': '操作发动机！',
		'info': '启动发动机会惊扰怪物！我需要你争取一点时间！',
		'level': 0,
		'type': 'guardPlanetBooster',
		'auto': False,
		'time': -1,
		'hide': True,
		'data': {
			'global_accumulations': {
				'PlanetBooster': {'guard': 1}
			}
		},
		'rewards': {},
	},
	'100040': {
		'branch': 'main',
		'group': 'saturn',
		'icon': '',
		'desc': '土星',
		'info': '未解锁，敬请期待',
		'level': 2,
		'type': 'default',
		'auto': False,
		'time': -1,
		'data': {},
		'rewards': {},
	},
	'100050': {
		'branch': 'main',
		'group': 'uranus',
		'icon': ' ',
		'desc': '天王星',
		'info': '未解锁，敬请期待',
		'level': 2,
		'type': 'default',
		'auto': False,
		'time': -1,
		'data': {},
		'rewards': {},
	},
	'100060': {
		'branch': 'main',
		'group': 'neptune',
		'icon': '',
		'desc': '海王星',
		'info': '未解锁，敬请期待',
		'level': 2,
		'type': 'default',
		'auto': False,
		'time': -1,
		'data': {},
		'rewards': {},
	},
}
