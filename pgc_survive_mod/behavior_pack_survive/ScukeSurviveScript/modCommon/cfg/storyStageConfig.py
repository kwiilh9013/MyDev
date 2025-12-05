# -*- encoding: utf-8 -*-
from ScukeSurviveScript.modCommon.cfg.buildings.markers.scuke_planet_booster import Config as Scuke_planetBooster

Config = {
	'SendGoldenCreeper': {
		'player': {
			'forbidControl': True,
			'immune': True,
		},
		'posTransformer': {
			'type': 'building',
			'identifier': Scuke_planetBooster['identifier'],
			'filter': 'closest'
		},
		'duration': 4.3,
		'lines': [
			{
				'type': 'cameraMoving', 'offset': 0.2, 'duration': 2, 'stayTime': 0.1,
				'fov': 70,
				'pos': [(245.0, 14.7, 233.0), (245.0, 14.7, 233.0), (245.0, 14.7, 233.0)],
				'rot': [(3.6, 73.4, 0.0), (-8.0, 91.8, 0.0), (-32.2, 92.1, 0.0)],
			},
			{
				'type': 'entityMoving', 'offset': 0, 'duration': 2, 'targets': '@creepers',
				'pos': [
					(234, 13, 232),
					(234, 19, 231)
				],
				'rot': [
					(0, 270, 0),
					(0, 270, 0)
				],
			},
			{'type': 'sendCreeper', 'offset': 2, 'duration': 0, 'targets': '@creepers', 'identifier': Scuke_planetBooster['identifier']},
			{
				'type': 'cameraMoving', 'offset': 2.3, 'duration': 2, 'stayTime': 0.1,
				'fov': 70,
				'pos': [(245.0, 14.7, 233.0), (245.0, 14.7, 233.0), (245.0, 14.7, 233.0), (245.0, 14.7, 233.0), (245.0, 14.7, 233.0), (245.0, 14.7, 233.0), (245.0, 14.7, 233.0)],
				'rot': [(-32.2, 92.1, 0.0), (-10.0, 100.1, 0.0), (-6.0, 154.1, 0.0), (-3.1, 270, 0.0), (-2, 280, 0.0), (-1.7, 421.6, 0.0), (-2.3, 430, 0.0)],
			},
		]
	},
	'ActivatePlanetBooster': {
		'player': {
			'forbidControl': True,
			'immune': True,
		},
		'posTransformer': {
			'type': 'building',
			'identifier': Scuke_planetBooster['identifier'],
			'filter': 'closest'
		},
		'duration': 8.2,
		'lines': [
			{
				'type': 'cameraMoving', 'offset': 0.2, 'duration': 7, 'stayTime': 1,
				'fov': 70,
				'pos': [(267.0, 16.3, 232), (290.0, 18.5, 232), (324.7, 32.7, 232), (372.2, 56.1, 232)],
				'rot': [(2.9, 90.0, -0.0), (4.8, 90.0, -0.0), (1.3, 90.0, -0.0), (-14.3, 90.0, -0.0)],
			},
			{'type': 'activatePlanetBooster', 'offset': 5, 'duration': 0, 'identifier': Scuke_planetBooster['identifier'], 'killArea': [(180, 0, 180), (280, 100, 280)]}
		]
	}
}
