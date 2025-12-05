# -*- encoding: utf-8 -*-
MeteoriteImpact = [
	{
		'days': 1,
		'name': '陨石冲击',
		'desc': '',
		'startTime': 0,
		'endTime': 22000,
		#持续时间
		'random': {
			'duration': (400, 400)
		},
		#陨石生成池
		'meteorites': {
			'scuke_survive:meteorite_normal': 100 #生成实体以及其权重
		},
		#生成半径
		'spawnArea': (30, 30),
		#生成高度
		'spawnHeight': (280, 300),
		#生成朝向
		'spawnDir': (-1, -0.8, -1),
		#生成间隔
		'spawnInterval': (90, 110),
		#实体是否禁止入睡
		'forbidSleep': True,
		# 陨石矿石配置
		'oreData': {
			# 方块生成的间隔
			'cd': 0.25,
			# 生成方块的位置随机范围
			'range': 3,
			'block': {"name": "scuke_survive:ore_yttrium", "aux": 0},
			# 范围随机: (min, max)/固定值
			'count': (2, 2),
		},
	},
	{
		'days': 19,
		'name': '陨石冲击',
		'desc': '',
		'startTime': 0,
		'endTime': 22000,
		#持续时间
		'random': {
			'duration': (600, 600)
		},
		#陨石生成池
		'meteorites': {
			'scuke_survive:meteorite_large': 100 #生成实体以及其权重
		},
		#生成半径
		'spawnArea': (50, 50),
		#生成高度
		'spawnHeight': (280, 300),
		#生成朝向
		'spawnDir': (-1, -0.8, -1),
		#生成间隔
		'spawnInterval': (90, 110),
		#实体是否禁止入睡
		'forbidSleep': True,
		# 陨石矿石配置
		'oreData': {
			# 方块生成的间隔
			'cd': 0.25,
			# 生成方块的位置随机范围
			'range': 3,
			'block': {"name": "scuke_survive:ore_yttrium", "aux": 0},
			# 范围随机: (min, max)/固定值
			'count': (3, 3),
		},
	},
]

MeteoriteRain = [
	{
		'days': 1,
		'name': '陨石冲击',
		'desc': '',
		'startTime': 0,
		'endTime': 22000,
		#持续时间
		'random': {
			'duration': (900, 900)
		},
		#陨石生成池
		'meteorites': {
			'scuke_survive:meteorite_rain': 100 #生成实体以及其权重
		},
		#生成半径
		'spawnArea': (80, 80),
		#生成高度
		'spawnHeight': (280, 300),
		#生成朝向
		'spawnDir': (-1, -0.8, -1),
		#生成间隔
		'spawnInterval': (50, 70),
		#实体是否禁止入睡
		'forbidSleep': True,
		# 陨石矿石配置
		'oreData': {
			# 方块生成的间隔
			'cd': 0.25,
			# 生成方块的位置随机范围
			'range': 3,
			'block': {"name": "scuke_survive:ore_yttrium", "aux": 0},
			# 范围随机: (min, max)/固定值
			'count': (4, 4),
		},
	}
]

# 陨石生成时可替换的方块id
MeteoriteReplaceBlocks = (
	"minecraft:stone",
	"minecraft:cobblestone",
	"minecraft:grass",
	"minecraft:dirt",
	"minecraft:podzol",
	"minecraft:sand",
	"minecraft:gravel",
	"minecraft:flowing_water",
	"minecraft:water",
	"minecraft:flowing_lava",
	"minecraft:lava",
)
