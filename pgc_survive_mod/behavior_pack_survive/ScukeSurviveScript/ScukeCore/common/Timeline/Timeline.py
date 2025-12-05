# -*- coding: utf-8 -*-


class TimelineNode(object):
    """timeline关键帧节点"""
    def __init__(self, frame, notifyFunc, nodeArgs=None):
        # 关键帧
        self.frame = frame
        # 关键帧回调
        self.notifyFunc = notifyFunc
        # 关键帧回调函数的参数
        self.nodeArgs = nodeArgs

    def Destroy(self):
        self.notifyFunc = None
        self.nodeArgs = None
        del self

    def Run(self):
        """执行回调"""
        if self.notifyFunc:
            if self.nodeArgs:
                self.notifyFunc(self.nodeArgs)
            else:
                self.notifyFunc()
        pass


class Timeline(object):
    """
    timeline, 可重复使用
        1秒30帧
        调用Start启动
        最后一个关键帧执行完即结束
    """
    def __init__(self, endFrame, loop=False, endFunction=None):
        self.currentFrame = 0
        self.endFrame = endFrame
        self.endFunction = endFunction
        self.frame2nodeMap = {}
        self.loop = loop
        self.runState = False
        pass

    def Destroy(self):
        for _, nodes in self.frame2nodeMap.iteritems():
            for node in nodes:
                node.Destroy()
            del nodes
        self.frame2nodeMap = None
        self.endFunction = None
        del self

    def addNode(self, frame, notifyFunc, nodeArgs=None):
        """添加关键帧节点"""
        node = TimelineNode(frame, notifyFunc, nodeArgs)
        if frame not in self.frame2nodeMap:
            self.frame2nodeMap[frame] = []
        self.frame2nodeMap[frame].append(node)

    def Start(self):
        """启动timeline"""
        self.runState = True
        # 如果有第0帧，则立即执行一次
        self.RunCurrentNodes(0)
        pass

    def Update(self):
        """更新timeline, 1秒30帧"""
        if not self.runState:
            return

        self.currentFrame += 1
        self.RunCurrentNodes(self.currentFrame)

        if self.currentFrame >= self.endFrame:
            self.End()
        pass

    def End(self):
        """结束timeline"""
        self.runState = False
        # 重置为初始状态，等待下一次使用
        self.currentFrame = 0
        if self.endFunction:
            self.endFunction()
        pass

    def RunCurrentNodes(self, frame):
        if frame in self.frame2nodeMap:
            for node in self.frame2nodeMap[frame]:
                node.Run()
        pass

    def GetRunState(self):
        return self.runState
    
    # def pause(self):
    #     self._can_update = False

    # def resume(self):
    #     self._can_update = True
