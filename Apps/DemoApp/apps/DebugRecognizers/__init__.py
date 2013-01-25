# -*- coding: utf-8 -*-

from ..Map.RecognizerMove import RecognizerMove
from ..Map.RecognizerZoomRotate import RecognizerZoomRotate
from GestureAgentsDemo.Render import Update
from pyglet.clock import schedule_interval, schedule_once
import gc
import weakref
from GestureAgentsDemo.Geometry import Circle, Ring, Rectangle
from GestureAgentsDemo.Utils import DynamicValue, TextAlert


class GraphicAlert(object):
    def __init__(self, pos, group):
        self.figure = Rectangle(5, 5, group=group, color=(255, 0, 0))
        self.figure.getCentered(pos)
        self.figure.updateDisplay()
        schedule_once(self.kill, 1)

    def kill(self, dt=0):
        self.figure = None


class RecognizerParticle(object):
    spacing = 30
    positions = [(x * spacing + 10, y * spacing + 10)
                for x in range(10) for y in range(10)]

    def __init__(self, recognizer, group=None, color=(200, 0, 0)):
        self.recognizer = weakref.ref(recognizer)
        self.group = group
        self.circle = Circle(10, 20, group=group, color=color)
        self.pos = (x, y) = RecognizerParticle.positions.pop(0)
        self.x = DynamicValue(0)
        self.y = DynamicValue(0)
        self.x(x, 0.1)
        self.y(y, 0.1)
        self.ring = None
        self.nrfail = 0
        Update.register(RecognizerParticle.update, self)
        f = self.recognizer().fail
        self.recognizer().fail = lambda *l, **kw: (self.rfail(*l, **kw), f(*l, **kw))

    def rfail(self, cause="Cause unknown"):
        x, y = self.pos
        y = y - 8 * self.nrfail
        self.nrfail += 1
        # x, y = (x + randrange(-5, 5), y + randrange(-5, 5))
        # GraphicAlert((x, y), self.group)
        # if cause:
        TextAlert((x, y), text=cause, group=self.group)
        print self.recognizer(), cause

    def update(self, dt=0):
        if self.isdead():
            Update.unregister(self)
            # self.circle.clear()
        else:
            dx = dy = 0
            if self.recognizer().executed:
                dx = randrange(-5, 5)
                dy = randrange(-5, 5)
            if self.recognizer().is_pristine() and not self.ring:
                self.ring = Ring(10, 3, 20, group=self.group)
            elif not self.recognizer().is_pristine() and self.ring:
                self.ring = None
            for f in (self.circle, self.ring):
                if f:
                    f.getCentered((dx + self.x(), dy + self.y()))
                    f.updateDisplay()

    def __del__(self):
        # GraphicAlert(self.pos, self.group)
        RecognizerParticle.positions.append(self.pos)

    def isdead(self):
        return self.recognizer() is None


from random import randrange


class ColorDict(dict):
    def get(self, key):
        if key not in self:
            self[key] = (randrange(255), randrange(255), randrange(255))
        return self[key]
rcolors = ColorDict()


class DebugRecognizer(object):
    DebugApp = True

    def __init__(self, group=None):
        self.group = group
        self.types = (RecognizerMove, RecognizerZoomRotate)
        self.recognizers = weakref.WeakKeyDictionary()
        # Update.register(DebugRecognizer.update, self)
        schedule_interval(self.update, 1)

    def update(self, dt):
        gc.collect()
        for type in self.types:
            listrecog = [obj for obj in gc.get_objects() if isinstance(obj, type)]
            for r in listrecog:
                if r not in self.recognizers:
                    self.recognizers[r] = RecognizerParticle(r, group=self.group, color=rcolors.get(type))
            # for r, rp in list(self.recognizers.iteritems()):
            #     if rp.isdead():
            #         del self.recognizers[r]
