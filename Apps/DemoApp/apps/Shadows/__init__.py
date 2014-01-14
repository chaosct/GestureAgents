# -*- coding: utf-8 -*-

from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgentsDemo.Geometry import Ring, Circle
from GestureAgentsDemo.Render import drawBatch
from GestureAgents.Recognizer import Recognizer
import pyglet.clock
from pyglet.sprite import Sprite
from pyglet.resource import Loader
from GestureAgents.AppRecognizer import AppRecognizer
from weakref import WeakKeyDictionary
from math import sin, cos, pi
from unipath import Path


def notifier(fnotified, function):
    def notifierfunction(*args, **kwargs):
        function(*args, **kwargs)
        fnotified(*args, **kwargs)
    return notifierfunction


rcolors = {
    'RecognizerZoomRotate' : (0, 255, 0),
    'RecognizerMove' : (0, 0, 255)
}

ICONPATH = Path(Path(__file__).parent, "icons")
loader = Loader([ICONPATH])


class customSprite(object):
    def __init__(self, image):
        self.image = image

    def getCentered(self, pos):
        self.image.x, self.image.y = pos

    def updateDisplay(self):
        pass


def create_recognizer_icon(r, group):
    print Path(ICONPATH, r + ".png")
    if Path(ICONPATH, r + ".png").exists():
        t = loader.image(r + ".png")
        sprite = Sprite(t, batch=drawBatch, group=group)
        sprite.scale = 0.25
        return customSprite(sprite)
    else:
        color = rcolors.get(r, (255, 255, 255))
        return Circle(5, 20, group=group, color=color)


class FingerFollower(object):
    DebugApp = True

    def __init__(self, agent, group=None):
        self.agent = agent
        self.ring = None
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
        if not self.ring:
            self.ring = Ring(10, 4, 20, group=self.group, color=(255, 0, 0))
        self.ring.getCentered(self.pos())
        self.ring.updateDisplay()
        cx, cy = self.pos()
        for n, c in enumerate(self.recognizersymbols.itervalues()):
            x = cx + 20 * cos(n * pi / 5)
            y = cy + 20 * sin(n * pi / 5)
            c.getCentered((x, y))
            c.updateDisplay()

    def removeCursor(self, a):
        self.ring = None

    def finishAgent(self, a):
        self.dead = True
        self.agent.newCursor.unregister(self)
        self.agent.updateCursor.unregister(self)
        self.agent.removeCursor.unregister(self)
        self.agent.finishAgent.unregister(self)

    def update(self, dt=0):
        actuals = set(apprecognizers_subscribed(self.agent))
        anteriors = set(self.recognizersymbols)
        pending = actuals - anteriors
        for r in pending:
            name = r.original_recognizer.__name__
            self.recognizersymbols[r] = create_recognizer_icon(name, self.group)
        if pending:
            self.updateCursor(None)


class FingerShadow(object):
    DebugApp = True

    def __init__(self, system, group=None):
        self.group = group
        TuioCursorEvents.newAgent.register(FingerShadow.newAgentCursor, self)
        self.curshadows = WeakKeyDictionary()
        # Update.register(FingerShadow.update, self)
        pyglet.clock.schedule_interval(self.update, .1)
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
        if not isinstance(r, Recognizer):
            continue
        if r.failed:
            continue
        if type(r) is AppRecognizer:
            yield r
        else:
            agent = r.agent
            if agent not in a_process:
                a_process.add(agent)
                for rr in apprecognizers_subscribed(agent, a_process):
                    yield rr


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
