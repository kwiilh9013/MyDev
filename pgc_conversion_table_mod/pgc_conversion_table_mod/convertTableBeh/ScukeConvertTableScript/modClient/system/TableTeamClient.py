# -*- coding: utf-8 -*-
from ScukeConvertTableScript.ScukeCore.client.system.BaseClientSystem import (
    BaseClientSystem,
)
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
import mod.client.extraClientApi as clientApi
from ScukeConvertTableScript.ScukeCore.client import engineApiGac
from ScukeConvertTableScript.modClient.manager.singletonGac import Instance
from ScukeConvertTableScript.modCommon import modConfig

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
getConfigData = compFactory.CreateConfigClient(levelId).GetConfigData
setConfigData = compFactory.CreateConfigClient(levelId).SetConfigData


class TableTeamClient(BaseClientSystem):
    def __init__(self, namespace, systemName):
        super(TableTeamClient, self).__init__(namespace, systemName)

        self._invitePlayerId = None
        self._inviteBarCD = {}
        self._inviteBarObj = {}

        self._inviteKey = "ScukeConvertTableInvite" + self.mPlayerId
        inviteId = engineApiGac.GetConfigData(self._inviteKey)
        if inviteId:
            self._invitePlayerId = inviteId

    def Destroy(self):
        super(TableTeamClient, self).Destroy()

    def Update(self):
        for pid in list(self._inviteBarCD.keys()):
            if self._inviteBarCD[pid] > 0:
                self._inviteBarCD[pid] -= 1
            else:
                self._inviteBarCD[pid] = 0

    # region 服务端事件
    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def InviteTeam(self, args):
        """被邀请事件，储存邀请人后广播UI"""
        opid = args["opid"]
        self._invitePlayerId = opid
        engineApiGac.SetConfigData(self._inviteKey, self._invitePlayerId)
        self.BroadcastEvent("InviteTeamUI", {"opid": opid, "pid": self.mPlayerId})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.TableTeamServer)
    def HasAcceptInvite(self, args):
        """成功邀请别人时清除邀请自己的相关数据"""
        self._invitePlayerId = None
        engineApiGac.SetConfigData(self._inviteKey, self._invitePlayerId)
        self.BroadcastEvent("InviteTeamUI", {"opid": None, "pid": self.mPlayerId})

    # endregion

    # region 客户端同端事件
    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def SaveinviteBarCD(self, args):
        if args["pid"] == self.mPlayerId:
            self._inviteBarCD, self._inviteBarObj = args["inviteBarCD"],args["inviteBarObj"]

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def GetinviteBarCD(self, args):
        if self._inviteBarCD and args["pid"] == self.mPlayerId:
            self.BroadcastEvent("GetinviteBarCDUI",{"pid": self.mPlayerId,"inviteBarCD": self._inviteBarCD,"inviteBarObj": self._inviteBarObj})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def NoInvite(self, args):
        """邀请结束，清除邀请人储存"""
        if args["pid"] == self.mPlayerId:
            opid = args["opid"]
            if self._invitePlayerId == opid:
                self._invitePlayerId = None
                engineApiGac.SetConfigData(self._inviteKey, self._invitePlayerId)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def GetInvite(self, args):
        """初始化UI时，获得邀请状态"""
        if args["pid"] == self.mPlayerId:
            self.BroadcastEvent("InviteTeamUI", {"opid": self._invitePlayerId, "pid": self.mPlayerId})

    # endregion
