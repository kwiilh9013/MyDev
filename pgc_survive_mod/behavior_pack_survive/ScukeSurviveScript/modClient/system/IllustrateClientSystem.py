# -*- coding: utf-8 -*-
from ScukeSurviveScript.ScukeCore.common.log.logManager import LogManager
from ScukeSurviveScript.ScukeCore.client.system.BaseClientSystem import BaseClientSystem
from ScukeSurviveScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeSurviveScript.modClient.manager.singletonGac import Instance
from ScukeSurviveScript.modClient.ui.uiDef import UIDef
import ScukeSurviveScript.modCommon.cfg.illustration.illustrateMergeCfg as Illustrate
from ScukeSurviveScript.modCommon import modConfig
import mod.client.extraClientApi as clientApi

LevelId = clientApi.GetLevelId()
WORLD = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
MyPid = clientApi.GetLocalPlayerId()
CreatingItem = clientApi.GetEngineCompFactory().CreateItem


class IllustrateClientSystem(BaseClientSystem):
    def __init__(self, namespace, systemName):
        super(IllustrateClientSystem, self).__init__(namespace, systemName)
        self._memoryList = []
        self.hasUnlockList = []
        self.InitializeIllustration()

    def InitializeIllustration(self):
        Dict = Illustrate.GetAllData()
        valueList = Dict.values()
        mergeList = reduce(lambda x, y: x + y, valueList)
        for i in mergeList:
            if i and type(i) == dict and "id" in i:
                self._memoryList.append(i['id'])

    @EngineEvent()
    def UiInitFinished(self, args=None):
        pass

    @AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.IllustrateServerSystem)
    def UpdateUnlockList(self, args):
        self.hasUnlockList = args['list']

    @AddonEvent(modConfig.ModName, modConfig.ServerSystemEnum.IllustrateServerSystem)
    def UnlockIllustrate(self, args):
        Name = args['name']
        Type = args['type']
        ItemDict = CreatingItem(LevelId).GetItemBasicInfo(Name)
        if ItemDict:
            ZhName = ItemDict['itemName']
        else:
            ZhName = WORLD.GetChinese("entity.{}.name".format(Name))
        headIcon = 'random'
        if Type == "mob":
            if Name.startswith("scuke_survive:"):
                headIcon = Name.replace("_survive:", "_")
        Instance.mUIManager.ShowSnackBar({
            'icon': "textures/ui/scuke_survive/head_icon/{}".format(headIcon),
            'title': '解锁图鉴',
            'content': ZhName,
            'duration': 3.0,
            "type": Type,
            'name': Name
        })
        self.hasUnlockList.append(Name)

