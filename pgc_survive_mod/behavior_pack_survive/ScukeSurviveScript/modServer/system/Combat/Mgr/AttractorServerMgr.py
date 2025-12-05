# -*- coding: utf-8 -*-

from ScukeSurviveScript.modCommon import modConfig

from ScukeSurviveScript.modServer.system.Combat.Context.SkillBasicContext import SkillBasicContext
from ScukeSurviveScript.modServer.system.Combat.Mgr.Processor.CDProcessor import CDProcessor


class AttractorServerMgr(object):
    def __init__(self, serverSystem):
        super(AttractorServerMgr, self).__init__()
        self.serverSystem = serverSystem
        self.serverApi = serverSystem.engineApi
        self.compFactory = self.serverSystem.engineApi.GetEngineCompFactory()

        self.serverSystem.ListenForEvent(self.serverApi.GetEngineNamespace(), self.serverApi.GetEngineSystemName(),
                                         "AddEntityServerEvent", self, self.AddEntityServerEvent)
        self.serverSystem.ListenForEvent(self.serverApi.GetEngineNamespace(), self.serverApi.GetEngineSystemName(),
                                         "DamageEvent", self, self.DamageEvent)
        self.serverSystem.ListenForEvent(self.serverApi.GetEngineNamespace(), self.serverApi.GetEngineSystemName(),
                                         "AddEffectServerEvent", self, self.AddEffectServerEvent)
        self.serverSystem.ListenForEvent(self.serverApi.GetEngineNamespace(), self.serverApi.GetEngineSystemName(),
                                         "RemoveEffectServerEvent", self, self.RemoveEffectServerEvent)
        self.serverSystem.ListenForEvent(modConfig.ModName, modConfig.ServerSystemEnum.GunServerSystem,
                                         "OnGunShootBullet", self, self.OnGunShootBullet)

        self.AttractorTimer = {}

    def Update(self):
        for key in list(self.AttractorTimer.keys()):
            duration = self.AttractorTimer[key]
            duration = duration - 1
            self.AttractorTimer[key] = duration
            if duration <= 0:
                self.serverSystem.DestroyEntity(key)
                self.AttractorTimer.pop(key)


    def ProjectileDoHitEffectEvent(self, args):
        x = args['x']
        y = args['y']
        z = args['z']
        id = args['id']
        comp = self.serverApi.GetEngineCompFactory().CreateEngineType(id)
        if comp.GetEngineTypeStr() == "minecraft:arrow":
            entityId = self.serverSystem.CreateEngineEntityByTypeStr("scuke_survive:attractor", (x, y, z), (0, 0), 0)
            self.AttractorTimer[entityId] = 10*30
            pushableComp = self.serverApi.GetEngineCompFactory().CreateActorPushable(entityId)
            pushableComp.SetActorPushable(0)

    def AddEntityServerEvent(self, args):
        engineTypeStr = args['engineTypeStr']
        id = args['id']
        if engineTypeStr == 'scuke_survive:attractor':
            comp = self.serverApi.GetEngineCompFactory().CreateTag(id)
            comp.AddEntityTag("Attractor")

    def DamageEvent(self, args):
        entityId = args['entityId']
        comp = self.serverApi.GetEngineCompFactory().CreateEngineType(entityId)
        if comp.GetEngineTypeStr() == "scuke_survive:attractor":
            args['knock'] = False

    def OnGunShootBullet(self, args):
        eid = args['eid']
        comp = self.serverApi.GetEngineCompFactory().CreateEffect(eid)
        comp.AddEffectToEntity("scuke_survive:effect_highlight", 10, 1, False)

    def AddEffectServerEvent(self, args):
        entityId = args['entityId']
        effectName = args['effectName']
        if effectName == "scuke_survive:effect_highlight":
            comp = self.serverApi.GetEngineCompFactory().CreateTag(entityId)
            print comp.AddEntityTag("Highlight")

    def RemoveEffectServerEvent(self, args):
        entityId = args['entityId']
        effectName = args['effectName']
        if effectName == "scuke_survive:effect_highlight":
            comp = self.serverApi.GetEngineCompFactory().CreateTag(entityId)
            print comp.RemoveEntityTag("Highlight")
