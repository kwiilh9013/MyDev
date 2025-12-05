# -*- encoding: utf-8 -*-

Config = {
	'600001': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600001',
		'desc': '科目3起步',
		'info': '行驶2000格',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'moved': 2000}
			}
		},
		'rewards': {
			'scuke_survive:car_repair': 3,
		}
	},
	'600002': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600002',
		'desc': '科目3通过',
		'info': '行驶5000格',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'moved': 5000}
			}
		},
		'rewards': {
			'scuke_survive:car_rescue': 2,
		}
	},
	'600003': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600003',
		'desc': '里程先锋 ',
		'info': '行驶8000格',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'moved': 8000}
			}
		},
		'rewards': {
			'scuke_survive:items_grenade_small': 3,
		}
	},
	'600004': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600004',
		'desc': '道路征服者 ',
		'info': '行驶12000格',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'moved': 12000}
			}
		},
		'rewards': {
			'scuke_survive:food_epinephrine': 3,
		}
	},
	'600005': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600005',
		'desc': '终极远征者 ',
		'info': '行驶20000格',
		'level': 2,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'moved': 20000}
			}
		},
		'rewards': {
			'scuke_survive:food_antibiotic': 5,
		}
	},
	'600006': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/items/scuke_survive/car_repair',
		'desc': '初级维修师 ',
		'info': '修复2次载具',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'repaired': 2}
			}
		},
		'rewards': {
			'scuke_survive:items_barricade_iron': 5,
		}
	},
	'600007': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/items/scuke_survive/car_repair',
		'desc': '中级保养 ',
		'info': '修复10次载具',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'repaired': 10}
			}
		},
		'rewards': {
			'scuke_survive:items_grenade_large': 2,
		}
	},
	'600008': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/items/scuke_survive/car_rescue',
		'desc': '新手救援 ',
		'info': '使用救援信号发射器2次',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'rescued': 2}
			}
		},
		'rewards': {
			'scuke_survive:items_trap': 2,
		}
	},
	'600009': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/items/scuke_survive/car_rescue',
		'desc': '快速响应 ',
		'info': '使用救援信号发射器10次',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'rescued': 10}
			}
		},
		'rewards': {
			'scuke_survive:items_grenade_large': 2,
		}
	},
	'600010': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/items/scuke_survive/car_repair',
		'desc': '高级调试 ',
		'info': '修复20次载具',
		'level': 2,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'repaired': 20}
			}
		},
		'rewards': {
			'scuke_survive:items_landmine': 5,
		}
	},
	'600011': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600011',
		'desc': '初级清道夫 ',
		'info': '通过撞击击杀5名任意怪物',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'killed': 5}
			}
		},
		'rewards': {
			'scuke_survive:food_hp_bandage': 2,
		}
	},
	'600012': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600012',
		'desc': '僵尸粉碎者 ',
		'info': '通过撞击击杀15名任意怪物',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'killed': 15}
			}
		},
		'rewards': {
			'scuke_survive:food_hp_painkiller': 2,
		}
	},
	'600013': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600013',
		'desc': '僵尸噩梦 ',
		'info': '通过撞击击杀30名任意怪物',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'killed': 30}
			}
		},
		'rewards': {
			'scuke_survive:food_drink_power': 3,
		}
	},
	'600014': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600014',
		'desc': '末日清扫者 ',
		'info': '通过撞击击杀50名任意怪物',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'killed': 50}
			}
		},
		'rewards': {
			'scuke_survive:food_hp_firstaid_pack': 5,
		}
	},
	'600015': {
		'branch': 'sub',
		'group': 'vehicle',
		'icon': 'textures/ui/scuke_survive/task/600015',
		'desc': '僵尸灭绝者 ',
		'info': '通过撞击击杀100名任意怪物',
		'level': 2,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Car': {'killed': 50}
			}
		},
		'rewards': {
			'scuke_survive:gun_bazooka1_s2': 1,
		}
	},
}