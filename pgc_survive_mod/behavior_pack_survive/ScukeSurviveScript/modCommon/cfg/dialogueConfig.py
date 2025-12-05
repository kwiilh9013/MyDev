# -*- encoding: utf-8 -*-
Config = {
	'scuke_survive:npc_golden_creeper': {
		'nodes': {
			'1000110': '!@HasTamed',
			'1000120': '@HasTamed',
		}
	},
	'scuke_survive:npc_igniter': {
		'nodes': {
			'1000210': '@PlanetBoosterValid && !@PlanetBoosterActivated && @PhasePlanetBoosterActivated<1 && @HasNpcConsumeTask',
			'1000213': '@PlanetBoosterValid && !@PlanetBoosterActivated && @PhasePlanetBoosterActivated<1 && !@HasNpcConsumeTask && @HasNpcConsumeCreeperTask',
			'1000215': '@PlanetBoosterValid && !@PlanetBoosterActivated && @PhasePlanetBoosterActivated<1 && !@HasNpcConsumeTask && !@HasNpcConsumeCreeperTask && @HasGuardPlanetBoosterTask && @PlanetBoosterHasCreeper',
			'1000260': '@PlanetBoosterValid && !@PlanetBoosterActivated && @PhasePlanetBoosterActivated<1 && !@HasNpcConsumeTask && !@HasNpcConsumeCreeperTask && @HasGuardPlanetBoosterTask && !@PlanetBoosterHasCreeper',
			'1000250': '@PlanetBoosterValid && !@PlanetBoosterActivated && @PhasePlanetBoosterActivated<1 && !@HasGuardPlanetBoosterTask',
			'1000220': '@PlanetBoosterValid && @PlanetBoosterActivated',
			'1000230': '!@PlanetBoosterValid',
			'1000240': '!@PlanetBoosterActivated && @PhasePlanetBoosterActivated>0',
		}
	},
	'scuke_survive:npc_keke': {
		'nodes': {
			'1000310': True,
		}
	},
	'scuke_survive:npc_zhanjing': {
		'nodes': {
			'1000410': True,
		}
	},
	'scuke_survive:npc_wheelchair_man': {
		'nodes': {
			'1000510': True,
		}
	},
}