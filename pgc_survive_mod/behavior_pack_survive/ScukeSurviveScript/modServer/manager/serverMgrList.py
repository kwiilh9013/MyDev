# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modServer.manager.datasetMgrGas import DatasetManagerGas
from ScukeSurviveScript.modServer.manager.lobbyMgrGas import LobbyManagerGas
from ScukeSurviveScript.ScukeCore.common.manager.eventManager import EventMgr

ServerManagerList = [
	LobbyManagerGas,
	DatasetManagerGas,
	EventMgr,
]
