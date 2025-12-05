# -*- coding: utf-8 -*-
""""gameRenderTick模块的config"""
from ..modCommon import modConfig

# mod根路径
_ModPath = modConfig.ModScriptName


# system相关
SystemNameSpace = "scuke_game_render_tick"
SystemName = "game_render_tick_client_system"
SystemPath = "%s.gameRenderTick.GameRenderTickClientSystem.GameRenderTickClientSystem" % _ModPath


# UI相关
UIKey = "ScukeGameRenderTickUI"
UIClassPath = "%s.gameRenderTick.gameRenderTickUI.GameRenderTickUI" % _ModPath
UINamespace = "scuke_game_render_tick_ui.main"


