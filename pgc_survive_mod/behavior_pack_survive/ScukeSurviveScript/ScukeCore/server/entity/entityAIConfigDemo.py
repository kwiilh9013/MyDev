# -*- coding: UTF-8 -*-
from ScukeSurviveScript.ScukeCore.server.entity.component.meleeAttackComp import MeleeAttackComp
from ScukeSurviveScript.ScukeCore.server.entity.enum.actionEnum import ActionEnum


"""
这里是用做config格式参考的文件, 不允许导入、运行该文件。
"""


# region 实体AI配置


_EntityAIDict = {
    # 实体类型id
    "minecraft:zombie": {
        # 实体的攻击力，需配置在行为包json中，在初始化时会通过api获取

        # === 这部分是自定义的字段，任意添加 ===
        # 攻击距离判定
        "attack_dist": 3,
        # 瞬移距离判定
        "teleport_start_dist": 16,
        "teleport_end_dist": 6,
        # === end ====

        # === 这部分是组件配置，可选 ===
        "components": {
            # 组件id，可任意填写，需保证该实体的组件中唯一
            "attack_1": {
                # 指定组件的逻辑处理类，默认使用ComponentBase
                # 如果执行的action在ComponentBas里有，则可以不指定
                "type": MeleeAttackComp,
                # 格式: key=帧数(1秒30帧), 
                # value=关键帧配置，执行时会将value作为参数，根据action的具体逻辑来填写(需要什么就填什么)。value可填空，即表示什么都不做，用于标记timeline的结束
                # 使用的action，需在组件类、或者ComponentBas里有，才能执行到
                "timeline": {
                    0: {"type": ActionEnum.SetMolang, "molang": {"query.mod.attack": 1}, },
                    10: {"type": ActionEnum.AreaAttack, "radius": 1, },
                    15: {"type": ActionEnum.SetMolang, "molang": {"query.mod.attack": 0}, },
                },
                # 除此外，可以新增任意字段
            },
            "attack_2": {
                # 直接执行行为，而不是执行timeline。会在Start时执行里面的所有行为，执行完成后就调用End
                "actions": [
                    {"type": ActionEnum.SetMolang, "molang": {"query.mod.teleport": 1}, },
                ],
            },

            # 其他类型，包括被动，根据自己的情况调整配置格式
        },
        # === end ====
    },
}
def GetEntityAIConfig(engineTypeStr):
    """获取实体ai 配置信息"""
    return _EntityAIDict.get(engineTypeStr)
# endregion

