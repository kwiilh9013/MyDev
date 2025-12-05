# -*- encoding: utf-8 -*-

Config = {
	'200001': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/ui/scuke_survive/task/200001',
		'desc': '初步考验',
		'info': '连续生存3天',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Record': {
					'livingDays': 3
				}
			}
		},
		'rewards': {
			'scuke_survive:melee_axe_red': 1,
		}
	},
	'200002': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/ui/scuke_survive/task/200002',
		'desc': '长久坚守',
		'info': '连续生存8天',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Record': {
					'livingDays': 8
				}
			}
		},
		'rewards': {
			'scuke_survive:melee_axe': 1,
		}
	},
	'200003': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/ui/scuke_survive/task/200003',
		'desc': '生存先锋',
		'info': '连续生存15天',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Record': {
					'livingDays': 15
				}
			}
		},
		'rewards': {
			'scuke_survive:melee_chainsaw_old': 1,
		}
	},
	'200004': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/ui/scuke_survive/task/200004',
		'desc': '月度生还者',
		'info': '连续生存30天',
		'level': 1,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Record': {
					'livingDays': 30
				}
			}
		},
		'rewards': {
			'scuke_survive:melee_chainsaw_golden': 1,
		}
	},
	'200005': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/ui/scuke_survive/task/200005',
		'desc': '坚韧不拔',
		'info': '连续生存45天',
		'level': 2,
		'type': 'numeric',
		'auto': True,
		'time': -1,
		'data': {
			'accumulations': {
				'Record': {
					'livingDays': 45
				}
			}
		},
		'rewards': {
			'scuke_survive:melee_pigsaw_golden': 1,
		}
	},
	'200006': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lead',
		'desc': '铅矿入门',
		'info': '挖掘5个铅矿',
		'level': 1,
		'type': 'a',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lead': 5,
				}
		},
		'rewards': {
			'scuke_survive:ingot_lead': 1,
		}
	},
    '200007': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lead',
		'desc': '铅矿老手',
		'info': '挖掘15个铅矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lead': 15
				}
		},
		'rewards': {
			'scuke_survive:ingot_lead': 7,
		}
	},
    '200008': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lead',
		'desc': '铅矿专家',
		'info': '挖掘30个铅矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lead': 30
				}
		},
		'rewards': {
			'scuke_survive:ingot_lead': 15,
		}
	},
    '200009': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lead',
		'desc': '铅矿暴发户',
		'info': '挖掘50个铅矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lead': 50
				}
		},
		'rewards': {
			'scuke_survive:ingot_lead': 20,
		}
	},
    '2000010': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lead_deepslate',
		'desc': '铅矿帝国',
		'info': '挖掘100个铅矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lead': 100
				}
		},
		'rewards': {
			'scuke_survive:ingot_lead': 30,
		}
	},
    '200011': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lithium',
		'desc': '锂矿入门',
		'info': '挖掘5个锂矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lithium': 5
				}
		},
		'rewards': {
			'scuke_survive:ingot_lithium': 1,
		}
	},
    '200012': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lithium',
		'desc': '锂矿老手',
		'info': '挖掘15个锂矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lithium': 15
				}
		},
		'rewards': {
			'scuke_survive:ingot_lithium': 7,
		}
	},
    '200013': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lithium',
		'desc': '锂矿专家',
		'info': '挖掘30个锂矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lithium': 30
				}
		},
		'rewards': {
			'scuke_survive:ingot_lithium': 15,
		}
	},
    '200014': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lithium',
		'desc': '锂矿暴发户',
		'info': '挖掘50个锂矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lithium': 50
				}
		},
		'rewards': {
			'scuke_survive:ingot_lithium': 20,
		}
	},
    '2000015': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_lithium_deepslate',
		'desc': '锂矿帝国',
		'info': '挖掘100个锂矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_lithium': 100
				}
		},
		'rewards': {
			'scuke_survive:ingot_lithium': 30,
		}
	},
    '200016': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_rare_earth',
		'desc': '稀土入门',
		'info': '挖掘5个稀土矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_rare_earth': 5
				}
		},
		'rewards': {
			'scuke_survive:ingot_rare_earth': 1,
		}
	},
    '200017': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_rare_earth',
		'desc': '稀土老手',
		'info': '挖掘15个稀土矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_rare_earth': 15
				}
		},
		'rewards': {
			'scuke_survive:ingot_rare_earth': 7,
		}
	},
    '200018': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_rare_earth',
		'desc': '稀土专家',
		'info': '挖掘30个稀土矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_rare_earth': 30
				}
		},
		'rewards': {
			'scuke_survive:ingot_rare_earth': 15,
		}
	},
    '200019': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_rare_earth',
		'desc': '稀土暴发户',
		'info': '挖掘50个稀土矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_rare_earth': 50
				}
		},
		'rewards': {
			'scuke_survive:ingot_rare_earth': 20,
		}
	},
    '2000020': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_rare_earth_deepslate',
		'desc': '稀土帝国',
		'info': '挖掘100个稀土矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_rare_earth': 100,
				}
		},
		'rewards': {
			'scuke_survive:ingot_rare_earth': 30,
		}
	},
    '200021': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_yttrium',
		'desc': '钇金陨石矿入门',
		'info': '挖掘5个钇金陨石矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_yttrium': 1
				}
		},
		'rewards': {
			'scuke_survive:ingot_yttrium': 1,
		}
	},
    '200022': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_yttrium',
		'desc': '钇金陨石矿老手',
		'info': '挖掘15个钇金陨石矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_yttrium': 10
				}
		},
		'rewards': {
			'scuke_survive:ingot_yttrium': 3,
		}
	},
    '200023': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_yttrium',
		'desc': '钇金陨石矿专家',
		'info': '挖掘30个钇金陨石矿',
		'level': 1,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_yttrium': 20
				}
		},
		'rewards': {
			'scuke_survive:ingot_yttrium': 5,
		}
	},
    '200024': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_yttrium',
		'desc': '钇金陨石矿暴发户',
		'info': '挖掘30个钇金陨石矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_yttrium': 30
				}
		},
		'rewards': {
			'scuke_survive:ingot_yttrium': 7,
		}
	},
    '2000025': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/blocks/scuke_survive/ore_yttrium',
		'desc': '钇金陨石矿帝国',
		'info': '挖掘30个钇金陨石矿',
		'level': 2,
		'type': 'consume',
		'auto': True,
		'time': -1,
		'data': {
			'blocks': {
					'scuke_survive:ore_yttrium': 30
				}
		},
		'rewards': {
			'scuke_survive:ingot_yttrium': 10,
		}
	},
    '2000026': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/drink_speed1',
		'desc': '冰爽一刻',
		'info': '食用5次康帅傅小瓶冰红茶',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_drink_speed1': 5
				}
		},
		'rewards': {
			'scuke_survive:food_drink_speed1': 1,
		}
	},
    '2000027': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/drink_speed2',
		'desc': '饮爽无限',
		'info': '食用5次康帅傅大瓶冰红茶',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_drink_speed2': 5
				}
		},
		'rewards': {
			'scuke_survive:food_drink_speed2': 1,
		}
	},
    '2000028': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/hotwater_small',
		'desc': '热心呵护',
		'info': '食用5次小瓶热开水',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_hotwater_small': 5
				}
		},
		'rewards': {
			'scuke_survive:food_hotwater_small': 1,
		}
	},
    '2000029': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/hotwater_large',
		'desc': '温暖相伴',
		'info': '食用5次大瓶热开水',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_hotwater_large': 5
				}
		},
		'rewards': {
			'scuke_survive:food_hotwater_large': 1,
		}
	},
    '2000030': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/coldwater_small',
		'desc': '清凉一刻',
		'info': '食用5次小瓶凉开水',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_coldwater_small': 5
				}
		},
		'rewards': {
			'scuke_survive:food_coldwater_small': 1,
		}
	},
    '2000031': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/coldwater_large',
		'desc': '清凉一夏',
		'info': '食用5次大瓶凉开水',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_coldwater_large': 5
				}
		},
		'rewards': {
			'scuke_survive:food_coldwater_large': 1,
		}
	},
    '2000032': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/drink_aim',
		'desc': '大汽水喝大窑',
		'info': '食用5次大窑汽水',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_drink_aim': 5
				}
		},
		'rewards': {
			'scuke_survive:food_drink_aim': 1,
		}
	},
    '2000033': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/drink_power',
		'desc': '能量满满',
		'info': '食用5次红牛',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_drink_power': 5
				}
		},
		'rewards': {
			'scuke_survive:food_drink_power': 1,
		}
	},
    '2000034': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/spicy_strip',
		'desc': '辣条狂欢',
		'info': '食用5次辣条',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_spicy_strip': 5
				}
		},
		'rewards': {
			'scuke_survive:food_spicy_strip': 1,
		}
	},
    '2000035': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/beef',
		'desc': '肥牛盛宴',
		'info': '食用5次真香肥牛',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_beef': 5
				}
		},
		'rewards': {
			'scuke_survive:food_beef': 1,
		}
	},
    '2000036': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/senbei',
		'desc': '好运旺旺',
		'info': '食用5次旺旺仙贝',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_senbei': 5
				}
		},
		'rewards': {
			'scuke_survive:food_senbei': 1,
		}
	},
    '2000037': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/nougat',
		'desc': '甜蜜回忆',
		'info': '食用5次牛轧糖',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_nougat': 5
				}
		},
		'rewards': {
			'scuke_survive:food_nougat': 1,
		}
	},
    '2000038': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/bubble_gum_red',
		'desc': '糖果传奇',
		'info': '食用5次泡泡糖',
		'level': 2,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_bubble_gum_red': 5
				}
		},
		'rewards': {
			'scuke_survive:food_bubble_gum_red': 1,
		}
	},
    '2000039': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/hawthorn',
		'desc': '益胃消食',
		'info': '食用5次山楂条',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_hawthorn': 5
				}
		},
		'rewards': {
			'scuke_survive:food_hawthorn': 1,
		}
	},
    '2000040': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/mylikes',
		'desc': '童年味道',
		'info': '食用5次麦丽素',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_mylikes': 5
				}
		},
		'rewards': {
			'scuke_survive:food_mylikes': 1,
		}
	},
    '2000041': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/rice_crust',
		'desc': '米香四溢',
		'info': '食用5次小米锅巴',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_rice_crust': 5
				}
		},
		'rewards': {
			'scuke_survive:food_rice_crust': 1,
		}
	},
    '2000042': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/chocolate',
		'desc': '心醉一口',
		'info': '食用5次酒心巧克力',
		'level': 2,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_chocolate': 5
				}
		},
		'rewards': {
			'scuke_survive:food_chocolate': 1,
		}
	},
    '2000043': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/cold_paste',
		'desc': '贴心降温',
		'info': '使用5次冰宝贴',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_cold_paste': 5
				}
		},
		'rewards': {
			'scuke_survive:food_cold_paste': 1,
		}
	},
    '2000044': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/warm_paste',
		'desc': '温暖随行',
		'info': '使用5次暖宝宝',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_warm_paste': 5
				}
		},
		'rewards': {
			'scuke_survive:food_warm_paste': 1,
		}
	},
    '2000045': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/hp_painkiller',
		'desc': '疼痛克星',
		'info': '使用5次止痛药',
		'level': 2,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_hp_painkiller': 5
				}
		},
		'rewards': {
			'scuke_survive:food_hp_painkiller': 1,
		}
	},
    '2000046': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/hp_firstaid_pack',
		'desc': '安全随行',
		'info': '使用5次急救包',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_hp_firstaid_pack': 5
				}
		},
		'rewards': {
			'scuke_survive:food_hp_firstaid_pack': 1,
		}
	},
    '2000047': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/hp_bandage',
		'desc': '迅速包扎',
		'info': '使用5次绷带',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_hp_bandage': 5
				}
		},
		'rewards': {
			'scuke_survive:food_hp_bandage': 1,
		}
	},
    '2000048': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/epinephrine',
		'desc': '活力反应',
		'info': '使用5次肾上腺素',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_epinephrine': 5
				}
		},
		'rewards': {
			'scuke_survive:food_epinephrine': 1,
		}
	},
    '2000049': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/antibiotic',
		'desc': '免疫支持',
		'info': '使用5次抗生素',
		'level': 1,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_antibiotic': 5
				}
		},
		'rewards': {
			'scuke_survive:food_antibiotic': 1,
		}
	},
    '2000050': {
		'branch': 'sub',
		'group': 'living',
		'icon': 'textures/items/scuke_survive/food/eye_drops',
		'desc': '火力全开',
		'info': '使用5次珍视明',
		'level': 2,
		'type': 'operate',
		'auto': True,
		'time': -1,
		'data': {
			'items': {
					'scuke_survive:food_eye_drops': 5
				}
		},
		'rewards': {
			'scuke_survive:food_eye_drops': 1,
		}
	},
}