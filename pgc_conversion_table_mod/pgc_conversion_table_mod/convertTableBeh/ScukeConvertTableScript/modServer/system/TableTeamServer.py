# -*- coding: utf-8 -*-
from ScukeConvertTableScript.ScukeCore.common import config
from ScukeConvertTableScript.ScukeCore.server.system.BaseServerSystem import (
    BaseServerSystem,
)
from ScukeConvertTableScript.ScukeCore.common.api import itemApi
from ScukeConvertTableScript.ScukeCore.common.api.commonApiMgr import DeepCopy
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.ScukeCore.server import engineApiGas
from ScukeConvertTableScript.ScukeCore.server.api import serverApiMgr
import mod.server.extraServerApi as serverApi

compFactory = serverApi.GetEngineCompFactory()

class TableTeamServer(BaseServerSystem):
    def __init__(self, namespace, systemName):
        super(TableTeamServer, self).__init__(namespace, systemName)
        # 玩家组队信息；{队长id：[队员id]}，玩家处于队员状态时只会出现在[队员List]中，当玩家一个人时默认为队长
        self._allPlayerTeam = {}
        # 玩家名称，用于在离线时获取玩家名称
        self._allPlayerName = {}
        self._teamNameConfigKey = "ScukeConvertTableTeamNameKey"
        self._teamConfigKey = "ScukeConvertTableTeamKey"
    # region 方法
    def SaveWorldTeamConfig(self):
        """存档当前世界的组队和玩家姓名信息"""
        serverApiMgr.SetExtraData(self.mLevelId, self._teamConfigKey, self._allPlayerTeam)
        serverApiMgr.SetExtraData(self.mLevelId, self._teamNameConfigKey, self._allPlayerName)
        serverApiMgr.compFactory.CreateExtraData(self.mLevelId).SaveExtraData()

    def GetWorldTeamConfig(self):
        """获取当前世界的组队信息"""
        ExtraData = serverApiMgr.GetExtraData(self.mLevelId, self._teamConfigKey)
        return ExtraData
    def GetWorldTeamNameConfig(self):
        """获取当前世界的玩家姓名信息"""
        data = serverApiMgr.GetExtraData(self.mLevelId, self._teamNameConfigKey)
        if not data:
            data = {}
        return data
    def GetPlayerName(self, pid):
        """获取玩家名字"""
        return compFactory.CreateName(pid).GetName()
    def UpdatePlayerUI(self, pid):
        """刷新指定玩家的组队UI"""
        self.SendMsgToClient(pid,"GetPlayerTeam",{"teamDic": self._allPlayerTeam, "allPlayerName": self._allPlayerName})

    def UpdateAllUI(self):
        """刷新全部玩家的组队UI"""
        self.SendMsgToAllClient("GetPlayerTeam",{"teamDic": self._allPlayerTeam, "allPlayerName": self._allPlayerName})

    def FindOwner(self, tpid):
        """
        寻找某个玩家的队长
        return 队长id/None
        """
        for opid in self._allPlayerTeam:
            memberPlayerList = self._allPlayerTeam[opid]
            if memberPlayerList:
                for pid in memberPlayerList:
                    if tpid == pid:
                        return opid
        return None
    
    def IsUsedData(self,pid):
        """判断玩家数据是否有用，作为有队员的队长或队员时代表数据有用"""
        if (pid in self._allPlayerTeam and self._allPlayerTeam[pid]) or self.FindOwner(pid):
            return True
        return False
    # endregion

    # region 事件
    @EngineEvent()
    def AddServerPlayerEvent(self, args):
        """玩家加入游戏时"""
        pid = args["id"]
        self._allPlayerTeam = self.GetWorldTeamConfig()
        self._allPlayerName = self.GetWorldTeamNameConfig()
        self._allPlayerName[pid] = self.GetPlayerName(pid)
        if self._allPlayerTeam:
            if pid in self._allPlayerTeam:
                # 说明是队长
                self.UpdateAllUI()
                self.SaveWorldTeamConfig()
                self.BroadcastEvent("HasUpdateAllPlayerTeam", {"allPlayerTeam": self._allPlayerTeam})
                return
            for opid in self._allPlayerTeam:
                tList = self._allPlayerTeam[opid]
                if tList:
                    for id in tList:
                        if id == pid:
                            # 说明是成员
                            self.UpdateAllUI()
                            self.SaveWorldTeamConfig()
                            self.BroadcastEvent("HasUpdateAllPlayerTeam", {"allPlayerTeam": self._allPlayerTeam})
                            return
            # 其他情况说明没有组队
            self._allPlayerTeam[pid] = []
            self.SaveWorldTeamConfig()
        else:
            self._allPlayerTeam = {}
            self._allPlayerTeam[pid] = []
            self.SaveWorldTeamConfig()
        self.UpdateAllUI()
        self.BroadcastEvent("HasUpdateAllPlayerTeam", {"allPlayerTeam": self._allPlayerTeam})

    @EngineEvent()
    def PlayerIntendLeaveServerEvent(self, args):
        """玩家退出游戏时"""
        playerId = args["playerId"]
        if self.IsUsedData(playerId):
            if self._allPlayerName:
                self._allPlayerName[playerId] = self.GetPlayerName(playerId)
        else:
            for item in (self._allPlayerName, self._allPlayerTeam):
                if playerId in item:
                    item.pop(playerId)
        self.SaveWorldTeamConfig()
        self.UpdateAllUI()
        self.BroadcastEvent("HasUpdateAllPlayerTeam", {"allPlayerTeam": self._allPlayerTeam})
        self.SendMsgToAllClient('PlayerLeaveGame',{'pid':playerId})
    # endregion

    # region 客户端事件
    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryPushTableTeamUI(self, args):
        """尝试Push出管理界面UI"""
        pid = args["pid"]
        self.SendMsgToClient(pid,"PushTableTeamUI",{"teamDic": self._allPlayerTeam, "allPlayerName": self._allPlayerName})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryGetPlayerTeam(self, args):
        """获取到所有玩家当前组队信息"""
        pid = args["pid"]
        self.UpdatePlayerUI(pid)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryInviteTeam(self, args):
        """邀请玩家进入团队"""
        opid, tpid = args["opid"], args["tpid"]
        if opid in self._allPlayerTeam:
            self.SendMsgToClient(tpid, "InviteTeam", {"opid": opid})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryAcceptInvite(self, args):
        """接受邀请"""
        opid, tpid = args["opid"], args["tpid"]
        if opid not in self._allPlayerTeam:
            return
        # 当邀请人没有队员且发送邀请后成功拥有组员后，给邀请人回调：用于清除邀请人被其他人邀请的相关数据
        if not self._allPlayerTeam[opid]:
            self.SendMsgToClient(opid, "HasAcceptInvite", {"opid": opid})
        # opid邀请人，tpid被邀请人
        if opid in self._allPlayerTeam:
            self._allPlayerTeam[opid].append(tpid)
        if tpid in self._allPlayerTeam:
            self._allPlayerTeam.pop(tpid)
        self.UpdateAllUI()
        # 向EMC管理服务端发送成功接受邀请
        self.BroadcastEvent("AcceptInvite",{"tpid": tpid, "opid": opid, "allPlayerTeam": self._allPlayerTeam})
        # 隐藏队员的CD显示与CD重置
        self.SendMsgToClient(opid, "InviteTeamBarUI", {"opid": None, "pid": opid})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryLeaveTeam(self, args):
        """离开团队"""
        opid, tpid = args["opid"], args["tpid"]
        # 队长情况，默认第一个是新的队长
        if tpid in self._allPlayerTeam:
            tList = self._allPlayerTeam[opid]
            if not tList:
                return
            newopid = tList[0]
            self._allPlayerTeam[newopid] = tList[1:]
            self._allPlayerTeam[opid] = []
            self.UpdateAllUI()
            self.SaveWorldTeamConfig()
            self.BroadcastEvent("LeaveTeam",{"tpid": tpid, "opid": opid,"newopid": newopid,"allPlayerTeam": self._allPlayerTeam})
        else:
            # 队员情况
            for pid in list(self._allPlayerTeam.keys()):
                tList = self._allPlayerTeam[pid]
                if tList:
                    for id in tList:
                        if id == tpid:
                            tList.remove(id)
                            self._allPlayerTeam[pid] = tList
                            self._allPlayerTeam[tpid] = []
                            self.UpdateAllUI()
                            self.SaveWorldTeamConfig()
                            self.BroadcastEvent("LeaveTeam",{"tpid": tpid,"opid": pid,"allPlayerTeam": self._allPlayerTeam})
                        else:
                            continue
                        

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryKickTeam(self, args):
        """踢出团队成员"""
        opid, tpid = args["opid"], args["tpid"]
        # opid团队队长id，被踢出的团队队员id
        tList = self._allPlayerTeam[opid]
        for id in tList:
            if tpid == id:
                tList.remove(tpid)
                self._allPlayerTeam[opid] = tList
                # 如果玩家在线则新建玩家数据
                if tpid in serverApi.GetPlayerList():
                    self._allPlayerTeam[tpid] = []
                else:
                # 不在线则删除储存名字数据
                    if tpid in self._allPlayerName:
                        self._allPlayerName.pop(tpid)
                break
            else:
                continue
        self.UpdateAllUI()
        self.SaveWorldTeamConfig()
        self.BroadcastEvent("KickTeam",{"tpid": tpid, "opid": opid, "allPlayerTeam": self._allPlayerTeam})

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def TryTransferTeam(self, args):
        """转让队长"""
        # tpid是转让后的新队长
        opid, tpid = args["opid"], args["tpid"]
        tList = self._allPlayerTeam[opid]
        if not tList:
            return
        for id in tList:
            if tpid == id:
                tList.remove(id)
                tList.append(opid)
                break
            else:
                continue
        self._allPlayerTeam.pop(opid)
        self._allPlayerTeam[tpid] = tList
        self.UpdatePlayerUI(tpid)
        for pid in tList:
            self.UpdatePlayerUI(pid)
        self.SaveWorldTeamConfig()
        self.BroadcastEvent("TransferTeam",{"tpid": tpid, "opid": opid, "allPlayerTeam": self._allPlayerTeam})

    # endregion 