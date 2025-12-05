# -*- coding: utf-8 -*-


ModName = "scuke_survive"
ModScriptName = "ScukeSurviveScript"
ModVersion = '0.0.1'
ModNameSpace = "scuke_survive"

DefaultGameType = 0
DefaultGameDifficulty = 2  # Normal

ServerSystemPath = "%s.modServer.system" % ModScriptName
ClientSystemPath = "%s.modClient.system" % ModScriptName


class ServerSystemEnum(object):
	ServerSystem = "ServerSystem"
	EditorServerSystem = "EditorServerSystem"
	AttrServerSystem = "AttrServerSystem"
	BuffServerSystem = "BuffServerSystem"
	TaskServerSystem = "TaskServerSystem"
	SettingServerSystem = "SettingServerSystem"
	IllustrateServerSystem = "IllustrateServerSystem"
	BuildingServerSystem = "BuildingServerSystem"
	AreaServerSystem = "AreaServerSystem"
	MobServerSystem = "MobServerSystem"
	PhaseServerSystem = "PhaseServerSystem"
	EnvServerSystem = "EnvServerSystem"
	LivingServerSystem = "LivingServerSystem"
	FeatureServerSystem = "FeatureServerSystem"
	CombatCoreServerSystem = "CombatCoreServerSystem"
	GunServerSystem = "GunServerSystem"
	BulletServerSystem = "BulletServerSystem"
	DamageServerSystem = "DamageServerSystem"
	MeleeServerSystem = "MeleeServerSystem"
	MeleeAttackServerSystem = "MeleeAttackServerSystem"
	ArmorServerSystem = "ArmorServerSystem"
	DialogueServerSystem = "DialogueServerSystem"
	StoryStageServerSystem = "StoryStageServerSystem"
	BattleEventServerSystem = "BattleEventServerSystem"
	CarServerSystem = "CarServerSystem"
	"""载具"""
	MolangServerSystem = "MolangServerSystem"
	"""Molang"""
	ItemsServerSystem = "ItemsServerSystem"
	"""item道具"""
	BlocksServerSystem = "BlocksServerSystem"
	"""方块"""
	BuildStructServerSystem = "BuildStructServerSystem"
	"""一键建造"""
	LadarServerSystem = "LadarServerSystem"
	"""雷达"""
	EntityServerSystem = "EntityServerSystem"
	"""实体"""
	ElectricServerSystem = "ElectricServerSystem"
	"""电力系统"""
	NPCServerSystem = "NPCServerSystem"
	"""NPC"""
	RandomEventServerSystem = "RandomEventServerSystem"
	"""随机事件"""



class ClientSystemEnum(object):
	ClientSystem = "ClientSystem"
	DisplayClientSystem = "DisplayClientSystem"
	CameraClientSystem = "CameraClientSystem"
	AttrClientSystem = "AttrClientSystem"
	BuffClientSystem = "BuffClientSystem"
	TaskClientSystem = "TaskClientSystem"
	SettingClientSystem = "SettingClientSystem"
	IllustrateClientSystem = "IllustrateClientSystem"
	PhaseClientSystem = "PhaseClientSystem"
	EnvClientSystem = "EnvClientSystem"
	DamageIndicatorClientSystem = "DamageIndicatorClientSystem"
	GunClientSystem = "GunClientSystem"
	BulletClientSystem = "BulletClientSystem"
	CombatCoreClientSystem = "CombatCoreClientSystem"
	MeleeClientSystem = "MeleeClientSystem"
	ArmorClientSystem = "ArmorClientSystem"
	DialogueClientSystem = "DialogueClientSystem"
	StoryStageClientSystem = "StoryStageClientSystem"
	CarClientSystem = "CarClientSystem"
	"""载具"""
	MolangClientSystem = "MolangClientSystem"
	"""Molang"""
	ItemsClientSystem = "ItemsClientSystem"
	"""item道具"""
	BlocksClientSystem = "BlocksClientSystem"
	"""方块"""
	BuildStructClientSystem = "BuildStructClientSystem"
	"""一键建造"""
	LadarClientSystem = "LadarClientSystem"
	"""雷达"""
	ElectricClientSystem = "ElectricClientSystem"
	"""电力系统"""
	EffectClientSystem = "EffectClientSystem"
	"""特效系统"""
	EntityClientSystem = "EntityClientSystem"
	"""实体系统"""


ServerSystemList = [
	ServerSystemEnum.ServerSystem,
	ServerSystemEnum.AttrServerSystem,
	ServerSystemEnum.BuffServerSystem,
	ServerSystemEnum.TaskServerSystem,
	ServerSystemEnum.SettingServerSystem,
	ServerSystemEnum.IllustrateServerSystem,
	ServerSystemEnum.StoryStageServerSystem,
	ServerSystemEnum.BattleEventServerSystem,
	ServerSystemEnum.BuildingServerSystem,
	ServerSystemEnum.AreaServerSystem,
	ServerSystemEnum.MobServerSystem,
	ServerSystemEnum.EnvServerSystem,
	ServerSystemEnum.LivingServerSystem,
	ServerSystemEnum.PhaseServerSystem,
	ServerSystemEnum.FeatureServerSystem,
	# ServerSystemEnum.CombatCoreServerSystem,
	ServerSystemEnum.GunServerSystem,
	ServerSystemEnum.BulletServerSystem,
	ServerSystemEnum.DamageServerSystem,
	ServerSystemEnum.MeleeServerSystem,
	ServerSystemEnum.MeleeAttackServerSystem,
	ServerSystemEnum.ArmorServerSystem,
	ServerSystemEnum.DialogueServerSystem,
	ServerSystemEnum.CarServerSystem,
	ServerSystemEnum.ItemsServerSystem,
	ServerSystemEnum.BlocksServerSystem,
	ServerSystemEnum.MolangServerSystem,
	ServerSystemEnum.BuildStructServerSystem,
	ServerSystemEnum.LadarServerSystem,
	ServerSystemEnum.EntityServerSystem,
	ServerSystemEnum.ElectricServerSystem,
	ServerSystemEnum.NPCServerSystem,
	ServerSystemEnum.RandomEventServerSystem,
]

EditorServerSystemList = [
	ServerSystemEnum.EditorServerSystem
]

ClientSystemList = [
	ClientSystemEnum.ClientSystem,
	ClientSystemEnum.DisplayClientSystem,
	ClientSystemEnum.CameraClientSystem,
	ClientSystemEnum.AttrClientSystem,
	ClientSystemEnum.BuffClientSystem,
	ClientSystemEnum.StoryStageClientSystem,
	ClientSystemEnum.TaskClientSystem,
	ClientSystemEnum.SettingClientSystem,
	ClientSystemEnum.IllustrateClientSystem,
	ClientSystemEnum.EnvClientSystem,
	ClientSystemEnum.BlocksClientSystem,
	ClientSystemEnum.PhaseClientSystem,
	ClientSystemEnum.DamageIndicatorClientSystem,
	ClientSystemEnum.GunClientSystem,
	ClientSystemEnum.BulletClientSystem,
	ClientSystemEnum.CombatCoreClientSystem,
	ClientSystemEnum.MeleeClientSystem,
	ClientSystemEnum.ArmorClientSystem,
	ClientSystemEnum.DialogueClientSystem,
	ClientSystemEnum.CarClientSystem,
	ClientSystemEnum.ItemsClientSystem,
	ClientSystemEnum.MolangClientSystem,
	ClientSystemEnum.BuildStructClientSystem,
	ClientSystemEnum.LadarClientSystem,
	ClientSystemEnum.ElectricClientSystem,
	ClientSystemEnum.EffectClientSystem,
	ClientSystemEnum.EntityClientSystem,
]

# SystemEvent
ServerChatEvent = 'ServerChatEvent'

# ClientEvent
OnUiInitFinishedEvent = "OnUiInitFinishedEvent"


class ModEventEnum(object):
	GHAST_DIE = 0


CheckVillageDis = 20.0

WeaponIdentifierPrefixes = [
	ModNameSpace + ':gun_',
	ModNameSpace + ':melee_',
]

NPCIdentifierPrefix = ModNameSpace + ':npc_'
ChestIdentifierPrefix = ModNameSpace + ':chest_pool'
MonsterPoolIdentifierPrefix = ModNameSpace + ':monster_pool'
