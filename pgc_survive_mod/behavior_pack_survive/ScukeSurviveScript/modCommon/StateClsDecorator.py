# -*- coding: utf-8 -*-


class StateMachineFactory(object):
	# 所有类型
	_all_state_cls_dict = {}

	@classmethod
	def get_all_state_cls_info(cls):
		return cls._all_state_cls_dict

	@classmethod
	def register_cls(cls, game_type, status, state_cls):
		add_dict = cls._get_map(game_type)
		if status not in add_dict:
			add_dict[status] = state_cls
		# else:
		# 	raise RuntimeError, 'duplicate sub state cls : game_type:%s statue:%s' % (game_type, status)

	@classmethod
	def get_state_cls(cls, game_type, status):
		state_dict = cls._get_map(game_type)
		if status in state_dict:
			return state_dict[status]
		return None

	@classmethod
	def _get_map(cls, game_type):
		return cls._all_state_cls_dict.setdefault(game_type, {})


def register_machine_state_cls(game_type, status):
	def decorator(cls):
		StateMachineFactory.register_cls(game_type, status, cls)
		return cls
	return decorator
