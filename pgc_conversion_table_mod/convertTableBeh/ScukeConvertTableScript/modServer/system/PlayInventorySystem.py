# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ScukeConvertTableScript.ScukeCore.server.system.BaseServerSystem import BaseServerSystem
from ScukeConvertTableScript.ScukeCore.utils.eventWrapper import EngineEvent, AddonEvent
from ScukeConvertTableScript.modCommon.cfg import ItemEMCConfig,ItemSortConfig
from ScukeConvertTableScript.modCommon import modConfig
from ScukeConvertTableScript.ScukeCore.server import engineApiGas
from ScukeConvertTableScript.ScukeCore.server.api import serverApiMgr
from ScukeConvertTableScript.ScukeCore.common.api.commonApiMgr import DeepCopy

compFactory = serverApi.GetEngineCompFactory()
EntityTypeEnum = serverApi.GetMinecraftEnum().EntityType
ItemTypeEnum = serverApi.GetMinecraftEnum().ItemPosType


class PlayInventorySystem(BaseServerSystem):
    def __init__(self, namespace, systemName):
        super(PlayInventorySystem,self).__init__(namespace, systemName)
        self._ItemSortMapDic = {t: i for i, t in enumerate(ItemSortConfig._ItemSort)}

    @AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
    def SortPlayInventory(self, args):
        """
        对背包进行整理，支持竖直和水平；默认整理背包，可选是否要整理快捷栏
        """
        playerId, isVerticalkey = args['playerId'], args['isVerticalkey']

        # 判断是否存在排序表映射，没有则构造
        if not self._ItemSortMapDic:
            self._ItemSortMapDic = {t: i for i, t in enumerate(ItemSortConfig._ItemSort)}
        playerAllItemList = compFactory.CreateItem(playerId).GetPlayerAllItems(ItemTypeEnum.INVENTORY, True)
        playerBagItemList = playerAllItemList[9:]
        playerBagItemList = self.FormatItemInfoList(playerBagItemList)
        playerBagItemList = self.MergeBagItemList(playerBagItemList)
        playerBagItemSortedList = self.SortBagItemList(playerBagItemList)
        SetInvItemNum = compFactory.CreateItem(playerId).SetInvItemNum
        SetPlayerAllItems = compFactory.CreateItem(playerId).SetPlayerAllItems
        # 玩家背包物品栏枚举
        Inventory = ItemTypeEnum.INVENTORY
        i = 9
        # 竖向排序槽位映射
        verticalIndex = {9: 9, 10: 18, 11: 27, 12: 10, 13: 19, 14: 28, 15: 11, 16: 20, 17: 29, 18: 12, 19: 21, 20: 30,
                         21: 13, 22: 22, 23: 31, 24: 14, 25: 23, 26: 32, 27: 15, 28: 24, 29: 33, 30: 16, 31: 25, 32: 34,
                         33: 17, 34: 26, 35: 35}
        # 需要设置的玩家背包物品列表
        SetItemDic = {}
        for itemDict in playerBagItemSortedList:
            if itemDict == None:
                break
            solt = i
            if isVerticalkey:
                solt = verticalIndex[i]
            SetItemDic[(Inventory, solt)] = itemDict
            i += 1
        for i in range(9, 36):
            SetInvItemNum(i, 0)
        SetPlayerAllItems(SetItemDic)
        self.NotifyToClient(playerId, "RefreshInventory", {"data": None})
        self.SendMsgToClient(playerId, "SortInventory", {"sortType": isVerticalkey})

    # region 一键整理零件方法
    def FormatItemInfoList(self,ItemList):
        """清除玩家背包物品字典多余数据"""
        FormatItemInfo = serverApiMgr.itemApi.FormatItemInfo
        newItemList = []
        for item in ItemList:
            if item:
                item = FormatItemInfo(item)
            newItemList.append(item)
        return newItemList
    
    def MergeBagItemList(self,itemList):
        """合并物品列表中相同物品"""
        def makeHashable(obj):
            """
            将字典或其他复杂结构转换为可哈希形式。
            """
            if isinstance(obj, dict):
                # 字典转化为元组，键按顺序排序以确保哈希的一致性
                return tuple((key, makeHashable(value)) for key, value in sorted(obj.items()))
            elif isinstance(obj, list):
                # 列表转化为元组
                return tuple(makeHashable(item) for item in obj)
            elif isinstance(obj, (str, int, float, type(None))):
                # 基本类型直接返回
                return obj
            else:
                # 其他类型直接转字符串表示（可根据需求调整）
                return str(obj)
            
        GetItemMaxStackSize = serverApiMgr.GetItemMaxStackSize
        itemCountMap = {} # key:count 注意count是有可能超过64，方便之后做分堆
        # 物品合并操作
        for itemDic in itemList:
            if itemDic != None:
                newItemName,newAuxValue = itemDic['newItemName'],itemDic['newAuxValue']
                # 生成该物品key
                keyList = []
                for info in itemDic:
                    infoValue = itemDic[info]
                    if info == 'count':
                        continue
                    elif info == 'userData':
                        keyList.append(makeHashable(infoValue))
                        continue
                    if type(infoValue) == type([]):
                        keyList.append(tuple(infoValue))
                    else:
                        keyList.append(infoValue)
                key = tuple(keyList)
                # if GetItemMaxStackSize(newItemName,newAuxValue) != 1:
                if key in itemCountMap:
                    itemCountMap[key] += itemDic['count']
                else:
                    itemCountMap[key] = itemDic['count']
            
                        
        # 物品分堆操作
        newItemList = []
        # 记录已经处理过的物品字典key，保证同一种物品只执行一次
        itemSet = set()
        for itemDic in itemList:
            # 如果为None则直接添加
            if itemDic is None:
                newItemList.append(None)
                continue
            # 该物品的堆叠上限
            newItemName,newAuxValue = itemDic['newItemName'],itemDic['newAuxValue']
            itemMaxStackSize = GetItemMaxStackSize(newItemName,newAuxValue)
            # 生成该物品key
            keyList = []
            for info in itemDic:
                infoValue = itemDic[info]
                if info == 'count':
                    continue
                elif info == 'userData':
                    keyList.append(makeHashable(infoValue))
                    continue
                if type(infoValue) == type([]):
                    keyList.append(tuple(infoValue))
                else:
                    keyList.append(infoValue)
            key = tuple(keyList)
            if key not in itemSet:
                if key in itemCountMap:
                    totalCount = itemCountMap[key]
                    # 该物品的数量总和大于其堆叠上限，进行分堆
                    if totalCount > itemMaxStackSize:
                        while totalCount > itemMaxStackSize:
                            newItemDic = DeepCopy(itemDic)
                            newItemDic['count'] = itemMaxStackSize
                            newItemList.append(newItemDic)
                            totalCount -= itemMaxStackSize
                            if totalCount<=itemMaxStackSize:
                                newItemDic = DeepCopy(itemDic)
                                newItemDic['count'] = totalCount
                                newItemList.append(newItemDic)
                                break
                    else:
                        itemDic['count'] = totalCount
                        newItemList.append(itemDic)
                else:
                    newItemList.append(itemDic)
            itemSet.add(key)
        return newItemList

    def SortBagItemList(self,ItemList):
        """
        根据排序表对背包物品进行排序
        ItemList = [itemDic , None]
        """
        ItemInSortCofigList = []
        ItemNotSortCofigList = []
        ItemSortMapDic = self._ItemSortMapDic
        # 对附魔书单独排序一次
        # 提取出附魔书列表
        enchantedBookList = [item for item in ItemList if item and item.get('newItemName') == 'minecraft:enchanted_book' and item.get('newAuxValue') == 0]
        # 对字典进行排序，排序依据是 'enchantData' 中的元组
        if enchantedBookList:
            enchantedBookList.sort(key = lambda x: (x['userData']['ench'][0]['id']['__value__'], x['userData']['ench'][0]['lvl']['__value__']))
            # 将排序后的附魔书合并到原始列表中，保持 'None' 的位置
            resultList = []
            idx = 0  # 用来指示中当前处理到的字典
            for item in ItemList:
                if item and item.get('newItemName') == 'minecraft:enchanted_book' and item.get('newAuxValue') == 0:
                    resultList.append(enchantedBookList[idx])
                    idx += 1
                else:
                    # 不是附魔书的字典或者是 None，直接添加到结果中
                    resultList.append(item)
            ItemList = resultList

        for idx, item in enumerate(ItemList):
            if item is not None:
                key = (item['newItemName'], item['newAuxValue'])
                if key in ItemSortMapDic:
                    ItemInSortCofigList.append((item, ItemSortMapDic[key]))
                else:
                    ItemNotSortCofigList.append((item, idx))
        # 对于在排序表中物品按照排序表索引排序
        ItemInSortCofigList = [item for item, _ in sorted(ItemInSortCofigList, key=lambda x: x[1])]
        # 不在排序表中物品保持原有排序
        ItemNotSortCofigList = [item for item, _ in ItemNotSortCofigList]
        if ItemNotSortCofigList:
            print '==========列表中物品不在排序表中，请检查排序表===========',ItemNotSortCofigList
        # 合并结果，并在末尾补回 None
        newItemList = ItemInSortCofigList + ItemNotSortCofigList + [None] * ItemList.count(None)
        return newItemList
    # endregion
