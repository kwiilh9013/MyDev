# -*- encoding: utf-8 -*-

from ScukeSurviveScript.modCommon.defines.monsterEnum import MonsterEnum
from ScukeSurviveScript.modCommon.cfg.gunConfig import GetConfig as GetGunConfig
from ScukeSurviveScript.modCommon.cfg.meleeConfig import GetConfig as GetMeleeConfig
from ScukeSurviveScript.modCommon.cfg.entity.entityAIConfig import GetEntityConfig

EntityPreloadWeapons = {}
# 直接读取aiconfig，获取手持武器的id
_weaponEntityList = (
	MonsterEnum.RebelRagman,
	MonsterEnum.RebelVagrant,
	MonsterEnum.RebelSoilder,
	MonsterEnum.RebelLeader,
)
for engineType in _weaponEntityList:
	cfg = GetEntityConfig(engineType)
	if cfg and 'item_pool' in cfg:
		itemPool = cfg['item_pool']
		weaponList = []
		for item in itemPool:
			if 'itemName' in item:
				weaponList.append(item['itemName'])
		if weaponList:
			EntityPreloadWeapons[engineType] = {'display': weaponList}
	pass

# 初始化从id映射到config
for itemValue in EntityPreloadWeapons.itervalues():
	displayIdentifiers = itemValue.get('display', None)
	if displayIdentifiers:
		displayConfigs = []
		for identifier in displayIdentifiers:
			config = GetGunConfig(identifier)
			if config:
				displayConfigs.append(config['display'])
				continue
			config = GetMeleeConfig(identifier)
			if config:
				displayConfigs.append(config['display'])
				continue
		itemValue['display'] = displayConfigs
