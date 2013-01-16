# -*- coding: utf-8 -*-

from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgentsDemo.Geometry import Ring
from GestureAgentsDemo.Render import Update


class FingerFollower(object):
    DebugApp = True

    def __init__(self, agent, group=None):
        self.agent = agent
        self.circle = None
        self.dead = False
        self.group = group
        self.agent.newCursor.register(FingerFollower.newCursor, self)
        self.agent.updateCursor.register(FingerFollower.updateCursor, self)
        self.agent.removeCursor.register(FingerFollower.removeCursor, self)
        self.agent.finishAgent.register(FingerFollower.finishAgent, self)
        # if self.agent.recycled:
        #     self.newCursor(self.agent)

    def newCursor(self, a):
        self.updateCursor(a)

    def updateCursor(self, a):
        if not self.circle:
            self.circle = Ring(10, 4, 20, group=self.group, color=(255, 0, 0))
        self.circle.getCentered(self.agent.pos)
        self.circle.updateDisplay()

    def removeCursor(self, a):
        self.circle = None

    def finishAgent(self, a):
        self.dead = True
        self.agent.newCursor.unregister(self)
        self.agent.updateCursor.unregister(self)
        self.agent.removeCursor.unregister(self)
        self.agent.finishAgent.unregister(self)


class FingerShadow(object):
    DebugApp = True

    def __init__(self, group=None):
        self.group = group
        TuioCursorEvents.newAgent.register(FingerShadow.newAgentCursor, self)
        self.curshadows = {}
        Update.register(FingerShadow.update, self)

    def newAgentCursor(self, A):
        if A not in self.curshadows:
            ff = FingerFollower(A, group=self.group)
            self.curshadows[A] = ff

    def update(self, dt=0):
        for a in list(self.curshadows.itervalues()):
            if a.dead:
                del self.curshadows[a.agent]
