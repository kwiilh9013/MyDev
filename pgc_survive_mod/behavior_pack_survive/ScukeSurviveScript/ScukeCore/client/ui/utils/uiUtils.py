# -*- coding: utf-8 -*-

from functools import wraps
import mod.client.extraClientApi as clientApi

def touch_filter(touchType):
    def touchFilter(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
            touchEvent = args[1]["TouchEvent"]
            if touchType == "up":
                if touchEvent == touchEventEnum.TouchUp:
                    value = func(*args, **kwargs)
                    return value
            if touchType == "down":
                if touchEvent == touchEventEnum.TouchDown:
                    value = func(*args, **kwargs)
                    return value
            if touchType == "cancel":
                if touchEvent == touchEventEnum.TouchCancel:
                    value = func(*args, **kwargs)
                    return value
            if touchType == "move":
                if touchEvent == touchEventEnum.TouchMove:
                    value = func(*args, **kwargs)
                    return value

        return decorated

    return touchFilter


# 按钮点击时透明度变化
def button_touch(touchType):
    def touchFilter(func):
        def wrapper(*args, **kwargs):
            if touchType == 'down':
                uiNode = args[0]
                buttonPath = args[1]['ButtonPath']
                uiNode and uiNode.SetAlpha("{}/pressed".format(buttonPath), 0.5)
            elif touchType == 'up':
                pass
            value = func(*args, **kwargs)
            return value

        return wrapper

    return touchFilter
