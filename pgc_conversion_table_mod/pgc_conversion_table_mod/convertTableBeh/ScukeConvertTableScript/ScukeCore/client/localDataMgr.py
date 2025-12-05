# -*- coding: utf-8 -*-
Flags = frozenset(('__tuple__', '__set__', '__frozenset__'))


def ConvertGet(data):
    if isinstance(data, dict):
        return {ConvertGet(key): ConvertGet(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        if data and isinstance(data[-1], unicode) and data[-1] in Flags:
            flag = data.pop()
            if flag == '__tuple__':
                return tuple(ConvertGet(data))
            elif flag == '__set__':
                return set(ConvertGet(data))
            elif flag == '__frozenset__':
                return frozenset(ConvertGet(data))
        return [ConvertGet(element) for element in data]
    # 从json读取的话，应该需要转换成utf-8的，否则开发者获取的字符串会有u前缀
    elif isinstance(data, unicode):
        return data.encode('utf-8')
    else:
        return data


def ConvertSet(data):
    if isinstance(data, dict):
        return {ConvertSet(key): ConvertSet(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [ConvertSet(element) for element in data]
    elif isinstance(data, tuple):
        return tuple(ConvertSet(element) for element in data) + ('__tuple__',)
    elif isinstance(data, set):
        return [ConvertSet(element) for element in data] + ['__set__']
    elif isinstance(data, frozenset):
        return [ConvertSet(element) for element in data] + ['__frozenset__']
    else:
        return data
