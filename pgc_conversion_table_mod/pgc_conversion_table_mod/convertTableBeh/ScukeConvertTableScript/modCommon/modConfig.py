# -*- coding: utf-8 -*-


ModName = "ScukeConvertTable"
ModScriptName = "ScukeConvertTableScript"
ModVersion = '0.0.1'
ModNameSpace = "scuke_convert_table"

DefaultGameType = 0
DefaultGameDifficulty = 2  # Normal

ServerSystemPath = "%s.modServer.system" % ModScriptName
ClientSystemPath = "%s.modClient.system" % ModScriptName


class ServerSystemEnum(object):
	ServerSystem = "ServerSystem"
	PlayInventorySystem = "PlayInventorySystem"
	EditorServerSystem = "EditorServerSystem"
	TableMainServer = "TableMainServer"
	TableTeamServer = "TableTeamServer"
	LinkServer = "LinkServer"


class ClientSystemEnum(object):
	ClientSystem = "ClientSystem"
	TableMainClient = "TableMainClient"
	TableTeamClient = "TableTeamClient"
	VisualUIClient = "VisualUIClient"


ServerSystemList = [
	ServerSystemEnum.ServerSystem,
	ServerSystemEnum.PlayInventorySystem,
	ServerSystemEnum.TableMainServer,
	ServerSystemEnum.TableTeamServer,
	ServerSystemEnum.LinkServer
]

EditorServerSystemList = [
	ServerSystemEnum.EditorServerSystem
]

ClientSystemList = [
	ClientSystemEnum.ClientSystem,
	ClientSystemEnum.TableMainClient,
	ClientSystemEnum.TableTeamClient,
	ClientSystemEnum.VisualUIClient
]

# SystemEvent
ServerChatEvent = 'ServerChatEvent'

# ClientEvent
OnUiInitFinishedEvent = "OnUiInitFinishedEvent"
