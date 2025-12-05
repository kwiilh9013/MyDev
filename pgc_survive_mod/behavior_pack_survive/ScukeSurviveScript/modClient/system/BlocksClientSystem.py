# -*- coding: utf-8 -*-
import math
import mod.client.extraClientApi as clientApi
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import AddonEvent, EngineEvent
from ScukeSurviveScript.ScukeCore.client import engineApiGac
from ScukeSurviveScript.ScukeCore.common.api import commonApiMgr
from ScukeSurviveScript.ScukeCore.client.api import clientApiMgr
from ScukeSurviveScript.modCommon import modConfig
from ScukeSurviveScript.modCommon import eventConfig
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef

compFactory = clientApi.GetEngineCompFactory()


class BlocksClientSystem(BaseClientSystem):
    """功能方块 客户端"""

    def __init__(self, namespace, systemName):
        super(BlocksClientSystem, self).__init__(namespace, systemName)
        self.clicking = False
        # 当前交互的方块
        self.presentPos = (0, 0, 0)
        self.presentDim = 0
        self.presentOwner = None
        # 是否在蓄力使用引爆器
        self.usingDetonator = False
        self.usingTime = 0
        self.detonatorTimer = None
        # 保存自己放置的炸弹方块信息
        self.c4BombList = []
        # 注册订阅
        Instance.mEventMgr.RegisterEvent(eventConfig.TimeBombSetTimeEvent, self.TimeBombSetTimeEvent)

    def Destroy(self):
        Instance.mEventMgr.UnRegisterEvent(eventConfig.TimeBombSetTimeEvent, self.TimeBombSetTimeEvent)
        super(BlocksClientSystem, self).Destroy()

    def ResetClick(self):
        self.clicking = False

    @EngineEvent()
    def ClientBlockUseEvent(self, args):
        if self.clicking: return
        self.clicking = True
        engineApiGac.AddTimer(0.03, self.ResetClick)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BlocksServerSystem)
    def OpenTimeBombScreenEvent(self, args):
        self.presentDim, self.presentPos, self.presentOwner = args["dim"], args["pos"], args["owner"]
        """打开定时炸弹设置界面"""
        Instance.mUIManager.PushUI(UIDef.UI_TimeBomb, {})

    def TimeBombSetTimeEvent(self, args):
        param = {
            "totalTime": args["value"],
            "dim": self.presentDim,
            "pos": self.presentPos,
            "owner": self.presentOwner
        }
        self.NotifyToServer(eventConfig.TimeBombSetTimeEvent, param)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BlocksServerSystem)
    def TimeBombSyncStatusEvent(self, args):
        if args["dim"] != clientApiMgr.GetCurrentDimension(): return
        t = args["time"]
        if t <= 10:
            p = min(12 - t, 4) if t > 4 else 5
            c = 1.0 / float(p)
            for i in range(1, p):
                dt = c * (i - 1)
                engineApiGac.AddTimer(dt, self.PlayLeftTimeSound, args["pos"])
        else:
            self.PlayLeftTimeSound(args["pos"])

    def PlayLeftTimeSound(self, pos):
        clientApiMgr.PlayCustomMusic("scuke_survive.block.time_bomb_left_time", pos, 0.5, 1.0)

    @EngineEvent()
    def StopUsingItemClientEvent(self, args):
        self.usingDetonator = False
        self.usingTime = -1
        engineApiGac.CancelTimer(self.detonatorTimer)
        self.detonatorTimer = None
        ui = Instance.mUIManager.GetUI(UIDef.UI_C4Bomb)
        ui.SetBar(0, False)
        engineApiGac.AddTimer(0.01, setattr, self, "usingTime", 0)

    @EngineEvent()
    def StartUsingItemClientEvent(self, args):
        if self.usingTime == -1:
            return
        if self.IsUsingDetonator(args):
            self.usingDetonator = True
            if self.IsInDistance():
                self.DetonatorTimer()
            else:
                engineApiGac.SetTipMessage("§c您未在附近放置C4炸弹")

    def IsInDistance(self):
        # 如果附近没有炸弹，就不启动
        i = 0
        dim = clientApiMgr.GetCurrentDimension()
        pos = engineApiGac.GetEntityPos(self.mPlayerId)
        while i < len(self.c4BombList):
            p, d = self.c4BombList[i]
            if d == dim:
                dist = sum((a - b) ** 2 for a, b in zip(p, pos))
                if dist < 2500:
                    return True
            i += 1
        return False

    def IsUsingDetonator(self, args):
        pid = args["playerId"]
        if pid != self.mPlayerId: return False
        item = args["itemDict"]
        name = item["newItemName"]
        if name == "scuke_survive:c4_detonator":
            return True
        return False

    def DetonatorTimer(self):
        if not self.usingDetonator:
            self.usingTime = 0
            return
        t = 3 - self.usingTime
        # UI进度条
        ui = Instance.mUIManager.GetUI(UIDef.UI_C4Bomb)
        ui.SetBar(self.usingTime / 3.0, True)
        if t == 0:
            self.usingTime = 0
            self.Ignite()
            ui.SetBar(0.0, False)
            return
        self.usingTime += 0.5
        self.detonatorTimer = engineApiGac.AddTimer(0.5, self.DetonatorTimer)

    def Ignite(self):
        if not self.IsInDistance():
            engineApiGac.SetTipMessage("§c附近没有可引爆的炸弹")
            return
        param = {"igniter": self.mPlayerId, "dim": clientApiMgr.GetCurrentDimension()}
        self.NotifyToServer(eventConfig.C4BombIgniteEvent, param)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BlocksServerSystem)
    def C4BombPlaceEvent(self, args):
        """自己放置的C4初始化完成触发"""
        bd = args.get("blockData")
        if bd:
            self.c4BombList.append(bd)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BlocksServerSystem)
    def C4BombRemoveEvent(self, args):
        """自己放置的C4销毁触发"""
        bd = args.get("blockData")
        if bd in self.c4BombList:
            self.c4BombList.remove(bd)

    @AddonEvent(modConfig.ModNameSpace, modConfig.ServerSystemEnum.BlocksServerSystem)
    def ShowBlockInfo(self, args):
        if args['type'] == 'followHud':
            active = args['active']
            followHudUI = Instance.mUIManager.GetUI(UIDef.UI_FollowHud)
            if followHudUI:
                if active:
                    followHudUI.ShowPosTalk(args['pos'], args['dim'], {'text': args['msg']}, args.get('offset'))
                else:
                    followHudUI.HidePosTalk(args['pos'], args['dim'])
