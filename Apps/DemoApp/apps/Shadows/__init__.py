# -*- coding: utf-8 -*-

from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgentsDemo.Geometry import Ring, Circle
from GestureAgentsDemo.Render import Update
from GestureAgents.AppRecognizer import AppRecognizer
from weakref import WeakKeyDictionary
from math import sin, cos, pi


def notifier(fnotified, function):
    def notifierfunction(*args, **kwargs):
        function(*args, **kwargs)
        fnotified(*args, **kwargs)
    return notifierfunction


rcolors = {
    'RecognizerZoomRotate' : (0, 255, 0),
    'RecognizerMove' : (0, 0, 255)
}


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
        self.recognizersymbols = WeakKeyDictionary()

    def pos(self):
        return self.agent.pos

    def newCursor(self, a):
        self.updateCursor(a)

    def updateCursor(self, a):
        if not self.circle:
            self.circle = Ring(10, 4, 20, group=self.group, color=(255, 0, 0))
        self.circle.getCentered(self.pos())
        self.circle.updateDisplay()
        cx, cy = self.pos()
        for n, c in enumerate(self.recognizersymbols.itervalues()):
            x = cx + 20 * cos(n * pi / 5)
            y = cy + 20 * sin(n * pi / 5)
            c.getCentered((x, y))
            c.updateDisplay()

    def removeCursor(self, a):
        self.circle = None

    def finishAgent(self, a):
        self.dead = True
        self.agent.newCursor.unregister(self)
        self.agent.updateCursor.unregister(self)
        self.agent.removeCursor.unregister(self)
        self.agent.finishAgent.unregister(self)

    def update(self, dt=0):
        actuals = set(apprecognizers_subscribed(self.agent))
        anteriors = set(self.recognizersymbols)
        for r in actuals - anteriors:
            name = r.recognizer.__name__
            color = rcolors.get(name, (255, 255, 255))
            self.recognizersymbols[r] = Circle(5, 20, group=self.group, color=color)


class FingerShadow(object):
    DebugApp = True

    def __init__(self, group=None):
        self.group = group
        TuioCursorEvents.newAgent.register(FingerShadow.newAgentCursor, self)
        self.curshadows = WeakKeyDictionary()
        Update.register(FingerShadow.update, self)
        # self.apprecognizerlist = WeakSet()
        # AppRecognizer.acquire = notifier(self.NewAppRecognizer, AppRecognizer.acquire)

    def newAgentCursor(self, A):
        if A not in self.curshadows:
            ff = FingerFollower(A, group=self.group)
            self.curshadows[A] = ff

    def update(self, dt=0):
        for a in list(self.curshadows.itervalues()):
            if a.dead:
                del self.curshadows[a.agent]
            else:
                a.update()
        # print len(self.apprecognizerlist)

    def NewAppRecognizer(self, *args, **kwargs):
        print args[0]


def recognizers_subscribed(agent):
    recognizers = set()
    for event in agent.events.itervalues():
        recognizers = recognizers.union(event.lookupf.iterkeys())
    return recognizers


def apprecognizers_subscribed(agent, a_process=None):
    if a_process is None:
        a_process = set()
    for r in recognizers_subscribed(agent):
        if type(r) is AppRecognizer:
            yield r
        else:
            agent = r.agent
            if agent not in a_process:
                a_process.add(agent)
                for r in apprecognizers_subscribed(agent, a_process):
                    yield r


def getSourceAgents(recog):
    pendent = [recog]
    for r in pendent:
        try:
            for a in recog.get_agents_acquired_or_confirmed():
                if TuioCursorEvents in a.owners:
                    yield a
                pendent.extend(a.owners)
        except AttributeError:
            pass
