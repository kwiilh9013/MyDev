# -*- coding: utf-8 -*-
from ScukeSurviveScript.modServer.system.Combat.BaseClass.SkillBase import SkillBase
import ScukeSurviveScript.modCommon.cfg.mc_skill_cfg as SkillConfig

from ScukeSurviveScript.modServer.system.Combat.Context.SkillBasicContext import SkillBasicContext
from ScukeSurviveScript.modServer.system.Combat.Mgr.Processor.CDProcessor import CDProcessor


class SkillServerMgr(object):
    def __init__(self, serverSystem):
        super(SkillServerMgr, self).__init__()
        self.serverSystem = serverSystem
        self.compFactory = self.serverSystem.engineApi.GetEngineCompFactory()
        self.skillMap = {}

        self._CDProcessor = CDProcessor(self)

    def CastSkill(self, entityId, skillId):
        config = None
        if skillId in SkillConfig.data:
            config = SkillConfig.data[skillId]
        else:
            print "SkillServerMgr CastSkill error, skillId:", skillId, "not found."
            return

        sourcePosComp = self.compFactory.CreatePos(entityId)
        sourceRotComp = self.compFactory.CreateRot(entityId)

        context = SkillBasicContext()
        context.skill_id = skillId
        context.source_entity_id = entityId
        context.target_entity_id = None
        context.source_entity_pos = sourcePosComp.GetPos()
        context.source_entity_foot_pos = sourcePosComp.GetFootPos()
        context.source_entity_rot = sourceRotComp.GetRot()

        SkillInfoDict = {
            'skill_id': skillId,
            'context': context,
        }

        # 后续添加能否释放技能（状态冲突，CD，等）逻辑
        # self.CanCastSkill(context)

        # 后续添加的更新CD逻辑
        # self.ColdTimeProcessor.Update(context)

        # 索敌逻辑，补充context.target_entity_id
        # self.TargetFilterPorcessor.FindTarget(config, context)

        # 广播技能准备，其他系统根据技能添加额外的Context
        print "PreCastSkill", skillId
        self.serverSystem.BroadcastEvent('PreCastSkill', SkillInfoDict)
        testNextContext = SkillBasicContext.GetContextByClassName(SkillInfoDict['context'], 'TestNextContext')


        skill = SkillBase(self.serverSystem, context)
        skill.InitSkill(config)
        self.skillMap[entityId] = skill

        skill.DoSkill()

        self.serverSystem.BroadcastEvent('PostCastSkill', SkillInfoDict)

    def SkillFinish(self, entityId):
        if entityId in self.skillMap:
            del self.skillMap[entityId]