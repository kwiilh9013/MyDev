# -*- encoding: utf-8 -*-
Config = {
	'Cutscene00': {
		'type': 'words',
		'lines': [
			{'type': 'typing', 'speed': 0.2, 'duration': 0.2, 'align': 'center', 'text': '“没有人的文明，§z§z§z§z§z就像腌黄瓜没放酱料，没有任何意义”§z§z§z§z§z'},
			{'type': 'text', 'duration': 0.3, 'align': 'right', 'text': '§l——老黄瓜'},
		],
		'duration': 1.0
	},
	'Cutscene01': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/01',
		'moveY': (-5, 5),
		'text': [
			{'offset': 0, 'text': "当太阳内部的氢燃料耗尽，它不再散发生命所需的热量。", 'text2': "When the sun's hydrogen fuel runs out, it stops emitting the heat needed for life."},
			{'offset': 5.5, 'text': "地球随之进入了前所未有的寒冷期，大地逐渐被冰雪覆盖。", 'text2': "Earth enters an unprecedented ice age, with the land gradually covered in ice and snow."},
		],
		'duration': 10.5,
		'fadein': 0.6,
		'fadeout': 0.2,
		'playMusic': 'scuke_survive.cutscene.start',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words01_1'},
			{'offset': 5.5, 'name': 'scuke_survive.cutscene.words01_2'},
		]
	},
	'Cutscene02': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/02',
		'moveY': (-5, 5),
		'text': [
			{'offset': 0, 'text': "面对这冰冷的现实，人类建造巨型发动机，开始启航寻找新的家园。", 'text2': "Faced with this cold reality, humans build giant engines and set sail to find a new home."},
		],
		'duration': 6.5,
		'fadein': 0.2,
		'fadeout': 0.2,
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words02_1'},
		]
	},
	'Cutscene03': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/03',
		'moveY': (5, -5),
		'scale': (100, 105),
		'text': [
			{'offset': 0, 'text': "然而，当地球的稳定轨迹被强行改变，自然灾害频发。", 'text2': "However, as Earth's stable orbit is forcibly altered, natural disasters become frequent."},
			{'offset': 6, 'text': "人类才意识到自己有多渺小和无助。", 'text2': "Humans realize how small and helpless they are."},
			{'offset': 9.5, 'text': "随着陨石一同坠入地球的，还有一种未知的病毒，会让生物丧失理智...",
			 'text2': "With the meteorites that crash into Earth comes an unknown virus that causes creatures to lose their sanity..."},
		],
		'duration': 15.7,
		'fadein': 0.2,
		'fadeout': 0.2,
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words03_1'},
			{'offset': 6, 'name': 'scuke_survive.cutscene.words03_2'},
			{'offset': 9.5, 'name': 'scuke_survive.cutscene.words03_3'},
		]
	},
	'Cutscene04': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/04',
		'moveY': (5, -5),
		'moveX': (-5, 5),
		'scale': 110,
		'text': [
			{'offset': 0, 'text': "但别担心，总有这样一群人。", 'text2': "But don't worry, there are always people."},
			{'offset': 2.5, 'text': "他们背负着拯救地球的使命，勇敢地踏上了这条充满挑战的征途。",
			 'text2': "They carry the mission of saving the Earth, bravely embarking on this challenging journey."},
		],
		'duration': 8.5,
		'fadein': 0.2,
		'fadeout': 0.2,
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words04_1'},
			{'offset': 2.5, 'name': 'scuke_survive.cutscene.words04_2'},
		]
	},
	'Cutscene05': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/05',
		'moveY': (-5, 5),
		'text': [
			{'offset': 0, 'text': "这些英雄们日夜不休，不断点燃和维护那些巨大的星球发动机。", 'text2': "These heroes work day and night to ignite and maintain those huge planetary engines."},
			{'offset': 6.5, 'text': "以确保地球能够在宇宙航行中保持动力，继续前行。",
			 'text2': "To ensure Earth's continued propulsion and journey through the cosmos."},
		],
		'duration': 11.3,
		'fadein': 0.2,
		'fadeout': 0.2,
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words05_1'},
			{'offset': 6.5, 'name': 'scuke_survive.cutscene.words05_2'},
		]
	},
	'Cutscene06': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/06',
		'moveY': (-5, 5),
		'text': [
			{'offset': 0, 'text': "而你，我的朋友，你才是真正的英雄。", 'text2': "And you, my friend, are the true hero."},
			{'offset': 4.5, 'text': "你的每一份努力和坚持，都是这场伟大迁徙的一部分。",
			 'text2': "Your every effort and persistence are part of this great migration."},
		],
		'duration': 9.0,
		'fadein': 0.2,
		'fadeout': 0.2,
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words06_1'},
			{'offset': 4.5, 'name': 'scuke_survive.cutscene.words06_2'},
		]
	},
	'Cutscene07': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/07',
		'moveX': (5, -5),
		'scale': 110,
		'text': [
			{'offset': 0, 'text': "在这部史诗中，我们共同见证了一场人类与宇宙的伟大抗争。", 'text2': "In this epic, we witness a great struggle between mankind and the universe."},
			{'offset': 6.2,
			 'text': "记录下这一段充满挑战和希望的历史篇章。",
			 'text2': "Recording this historical chapter full of challenges and hopes."},
			{'offset': 13, 'showLogo': True}
		],
		'duration': 18.0,
		'fadein': 0.2,
		'fadeout': 1,
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.words07_1'},
			{'offset': 6.2, 'name': 'scuke_survive.cutscene.words07_2'},
		]
	},
	'Cutscene08': {
		'type': 'movie',
		'texture': '',
		'text': [],
		'duration': 2.0,
	},
	'Cutscene09': {
		'type': 'words',
		'lines': [
			{'type': 'typing', 'speed': 0.1, 'duration': 0.2, 'align': 'center', 'text': '§l§c警告！§z§z警告！§z§z'},
			{'type': 'typing', 'speed': 0.1, 'duration': 0.3, 'align': 'center', 'text': '§l我们被拉入火星轨道……§z！§z！§z！'},
		],
		'duration': 0.1,
		'playMusic': 'scuke_survive.cutscene.warning',
	},
	'Cutscene10': {
		'type': 'wakeup',
		'duration': 0.1
	},
	'MissionSuccess100010': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/ms100010',
		'moveY': (5, -5),
		'text': [
			{'offset': 0, 'text': "经过全人类的努力，我们成功逃离了火星的引力轨道，再次迎来了希望。", 'text2': "但是前方，未知的旅途，还等待着我们。"},
		],
		'duration': 10.0,
		'fadein': 0.5,
		'fadeout': 1.0,
		'playMusic': 'scuke_survive.cutscene.success',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.ms100010_words_1'},
		]
	},
	'MissionFailed100010': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/mf100010',
		'moveY': (-5, 5),
		'text': [
			{'offset': 0, 'text': "火星轨道的陨石从天而降，这就是真正的天灾吗？天空撕裂...大地崩坏...", 'text2': "人类真是如此渺小和脆弱...但我们并没有放弃希望，这样的灾难是无法打倒人类伟大征途的！"},
		],
		'duration': 16.3,
		'fadein': 0.5,
		'fadeout': 1.0,
		'playMusic': 'scuke_survive.cutscene.failed',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.mf100010_words_1'},
			{'offset': 8.3, 'name': 'scuke_survive.cutscene.mf100010_words_2'},
		]
	},
	'MissionSuccess100020': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/ms100020',
		'moveY': (-5, 5),
		'text': [
			{'offset': 0, 'text': "我们又一次成功逃脱了毁灭性的打击，穿过小行星带。", 'text2': "我们将抵达逃离太阳系最重要的中转站...木星！"},
		],
		'duration': 9.0,
		'fadein': 0.5,
		'fadeout': 1.0,
		'playMusic': 'scuke_survive.cutscene.success',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.ms100020_words_1'},
		]
	},
	'MissionFailed100020': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/mf100020',
		'moveY': (5, -5),
		'text': [
			{'offset': 0, 'text': "星空被黑暗遮蔽，无数陨石悉数坠落...大地裂变，史无前例的海啸地震，袭击了我们。", 'text2': "但...我们并没有失败...这只是我们将历经100代人，伟大征途中的一个挫折。我们选择希望。"},
		],
		'duration': 18.3,
		'fadein': 0.5,
		'fadeout': 1.0,
		'playMusic': 'scuke_survive.cutscene.failed',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.mf100020_words_1'},
			{'offset': 9.8, 'name': 'scuke_survive.cutscene.mf100020_words_2'},
		]
	},
	'MissionSuccess100030': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/ms100030',
		'moveY': (-10, 10),
		'sizeY': 72,
		'text': [
			{'offset': 0, 'text': "人类的赞歌就是勇气的赞歌！人类的伟大就是勇气的伟大！", 'text2': "通过全人类的饱和式救援和牺牲，我们成功脱离了木星轨道！加速脱离太阳系！...未完待续"},
		],
		'duration': 14.5,
		'fadein': 0.5,
		'fadeout': 1.0,
		'playMusic': 'scuke_survive.cutscene.success',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.ms100030_words_1'},
			{'offset': 6.0, 'name': 'scuke_survive.cutscene.ms100030_words_2'},
		]
	},
	'MissionFailed100030': {
		'type': 'movie',
		'texture': 'textures/ui/scuke_survive/cutscenes/mf100030',
		'moveY': (10, -10),
		'sizeY': 83,
		'text': [
			{'offset': 0, 'text': "巨大的木星眼凝视着我们，越来越近...我们会被无情的吞噬吗...", 'text2': "希望，是我们这个时代像钻石一样珍贵的东西。不到最后一刻，我们不会放弃...未完待续"},
		],
		'duration': 13.5,
		'fadein': 0.5,
		'fadeout': 1.0,
		'playMusic': 'scuke_survive.cutscene.failed',
		'sounds': [
			{'offset': 0, 'name': 'scuke_survive.cutscene.mf100030_words_1'},
			{'offset': 5.5, 'name': 'scuke_survive.cutscene.mf100030_words_2'},
		]
	},
}
