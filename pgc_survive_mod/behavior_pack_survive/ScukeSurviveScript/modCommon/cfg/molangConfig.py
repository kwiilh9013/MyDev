# -*- encoding: utf-8 -*-


"""
molang表达式的配置
"""


class QueryEnum:
	# region 载具
	"""query表达式枚举"""
	CarMoveUp = "query.mod.scuke_servive_car_up"
	"""载具移动方向（前进、倒退）"""
	CarPitchRot = "query.mod.scuke_servive_car_pitch"
	"""载具俯仰角度(绕z轴)"""
	CarRollRot = "query.mod.scuke_servive_car_roll"
	"""载具翻滚角度(绕x轴)"""
	CarCutState = "query.mod.scuke_servive_car_cut_state"
	"""载具刹车状态，不包含倒退"""

	RiderPosX = "query.mod.scuke_servive_rider_x_pos"
	"""乘客偏移x"""
	RiderPosY = "query.mod.scuke_servive_rider_y_pos"
	"""乘客偏移y"""
	RiderPosZ = "query.mod.scuke_servive_rider_z_pos"
	"""乘客偏移z"""

	InWater = "query.mod.scuke_servive_in_water"
	"""是否在水中"""
	InLava = "query.mod.scuke_servive_in_lava"
	"""是否在岩浆中"""
	
	Module1 = "query.mod.scuke_servive_module_1"
	"""变形模块1"""
	Module2 = "query.mod.scuke_servive_module_2"
	"""变形模块2"""

	FrontBumper = "query.mod.scuke_servive_front_bumper"
	"""前杠"""
	CarBody = "query.mod.scuke_servive_carbody"
	"""车身"""
	CarBothSides = "query.mod.scuke_servive_car_both_sides"
	"""车体两侧"""
	CarWheel = "query.mod.scuke_servive_car_wheel"
	"""车轮"""

	MissileShootNum = "query.mod.scuke_servive_car_missile_shoot_num"
	"""导弹发射动画"""

	CarFly = "query.mod.scuke_servive_car_fly"
	"""飞行动画"""
	# endregion

	# region 雷达
	PlayerRotYaw = "query.mod.scuke_servive_player_rot_yaw"
	"""玩家朝向的yaw角度"""
	LadarOutOfOrder = "query.mod.scuke_servive_ladar_out_of_order"
	"""雷达是否损坏"""
	LadarTarget1DistX = "query.mod.scuke_servive_ladar_target1_dist_x"
	"""目标1的距离x"""
	LadarTarget1DistZ = "query.mod.scuke_servive_ladar_target1_dist_z"
	"""目标1的距离z"""
	LadarTarget2DistX = "query.mod.scuke_servive_ladar_target2_dist_x"
	"""目标2的距离x"""
	LadarTarget2DistZ = "query.mod.scuke_servive_ladar_target2_dist_z"
	"""目标2的距离z"""
	LadarTarget3DistX = "query.mod.scuke_servive_ladar_target3_dist_x"
	"""目标3的距离x"""
	LadarTarget3DistZ = "query.mod.scuke_servive_ladar_target3_dist_z"
	"""目标3的距离z"""

	LadarEngine1DistX = "query.mod.scuke_servive_ladar_engine1_dist_x"
	"""发动机1的距离x"""
	LadarEngine1DistZ = "query.mod.scuke_servive_ladar_engine1_dist_z"
	"""发动机1的距离z"""
	LadarEngine1State = "query.mod.scuke_servive_ladar_engine1_state"
	"""发动机1的状态: 0=未发现, 1=未点燃, 2=点燃"""
	LadarEngine1Scale = "query.mod.scuke_servive_ladar_engine1_scale"
	"""发动机1的大小缩放 0.5-1"""
	LadarEngine2DistX = "query.mod.scuke_servive_ladar_engine2_dist_x"
	"""发动机2的距离x"""
	LadarEngine2DistZ = "query.mod.scuke_servive_ladar_engine2_dist_z"
	"""发动机2的距离z"""
	LadarEngine2State = "query.mod.scuke_servive_ladar_engine2_state"
	"""发动机2的状态: 0=未发现, 1=未点燃, 2=点燃"""
	LadarEngine2Scale = "query.mod.scuke_servive_ladar_engine2_scale"
	"""发动机2的大小缩放 0.5-1"""
	LadarEngine3DistX = "query.mod.scuke_servive_ladar_engine3_dist_x"
	"""发动机3的距离x"""
	LadarEngine3DistZ = "query.mod.scuke_servive_ladar_engine3_dist_z"
	"""发动机3的距离z"""
	LadarEngine3State = "query.mod.scuke_servive_ladar_engine3_state"
	"""发动机3的状态: 0=未发现, 1=未点燃, 2=点燃"""
	LadarEngine3Scale = "query.mod.scuke_servive_ladar_engine3_scale"
	"""发动机3的大小缩放 0.5-1"""

	LadarTargetDistList = [
		(LadarTarget1DistX, LadarTarget1DistZ),
		(LadarTarget2DistX, LadarTarget2DistZ),
		(LadarTarget3DistX, LadarTarget3DistZ),
	]
	LadarEngineDistList = [
		(LadarEngine1DistX, LadarEngine1DistZ, LadarEngine1Scale, LadarEngine1State,),
		(LadarEngine2DistX, LadarEngine2DistZ, LadarEngine2Scale, LadarEngine2State,),
		(LadarEngine3DistX, LadarEngine3DistZ, LadarEngine3Scale, LadarEngine3State,),
	]
	"""雷达目标距离molang列表"""
	# endregion

	# region 物品
	UseItem = "query.mod.scuke_servive_use_item"
	# endregion
	# region 生物
	# Witch
	Action = "query.mod.action"
	Attack1 = "query.mod.attack1"
	Attack2 = "query.mod.attack2"
	# endregion
	# 以上定义的molang，全部都需要添加到该列表中，用于初始化时注册molang
	MolangList = [
		CarMoveUp, CarPitchRot, CarRollRot, CarCutState, RiderPosX, RiderPosY, RiderPosZ, 
		InWater, InLava, 
		Module1, Module2, FrontBumper, CarBody, CarBothSides, CarWheel, MissileShootNum, CarFly,
		PlayerRotYaw, LadarOutOfOrder, 
		LadarTarget1DistX, LadarTarget1DistZ, LadarTarget2DistX, LadarTarget2DistZ, LadarTarget3DistX, LadarTarget3DistZ, 
		LadarEngine1DistX, LadarEngine1DistZ, LadarEngine1State, LadarEngine1Scale, 
			LadarEngine2DistX, LadarEngine2DistZ, LadarEngine2State, LadarEngine2Scale, 
			LadarEngine3DistX, LadarEngine3DistZ, LadarEngine3State, LadarEngine3Scale, 
		UseItem, 
		Action,Attack1,Attack2
	]
	"""所有molang列表"""

class VariableEnum:
	"""方块所用的molang枚举，需在方块模型的entity.json中注册"""
	WorkingState = "variable.working_state"
	"""方块工作状态"""



# 需要设置molang的实体config
_MolangConfig = {
	# 载具
	"scuke_survive:base_car": {
		"move_up": True,	# 移动方向
		"pitch_roll": {	# 俯仰、翻滚功能相关的参数
			"tick": 0.1,	# tick频率
			"rays": [	# 4个角的射线检测，位置偏移，需根据实体相对坐标系做偏移，比如实体左侧
				# 按对角顺序排列
				{"rot_vector": (0, -1, 0), "offset_rot": (0, -30), "offset_length": 5, "offset_height": 5, "distance": 10},
				{"rot_vector": (0, -1, 0), "offset_rot": (0, 150), "offset_length": 5, "offset_height": 5, "distance": 10},
				{"rot_vector": (0, -1, 0), "offset_rot": (0, 30), "offset_length": 5, "offset_height": 5, "distance": 10},
				{"rot_vector": (0, -1, 0), "offset_rot": (0, -150), "offset_length": 5, "offset_height": 5, "distance": 10},
			],
			"ignore_blocks": (
				"minecraft:water",
				"minecraft:flowing_water",
				"minecraft:lava",
				"minecraft:flowing_lava",
			),
			"all_riders": True,
		},
		"in_water": True,	# 是否在水中
		"in_lava": True,	# 是否在岩浆中
	},
}
def GetMolangCfg(engineTypeStr):
	"""获取实体的molang设置config"""
	return _MolangConfig.get(engineTypeStr, {})

