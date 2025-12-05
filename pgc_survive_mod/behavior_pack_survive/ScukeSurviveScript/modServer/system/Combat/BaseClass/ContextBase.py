# -*- coding: utf-8 -*-


class ContextBase(object):
    def __init__(self, up_context=None):
        super(ContextBase, self).__init__()
        self.up_context = up_context

    def GetUpContext(self):
        return self.up_context

    @classmethod
    def GetContextByClassName(cls, context_instance, class_name):
        max_depth = 10
        temp_context = context_instance

        while temp_context is not None and max_depth > 0:
            max_depth -= 1

            temp_context_class_name = type(temp_context).__name__
            if temp_context_class_name == class_name:
                return temp_context
            if hasattr(temp_context, 'up_context'):
                temp_context = temp_context.up_context
        return None

    def GetCurrentContextName(self):
        return type(self).__name__
