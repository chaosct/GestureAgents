# -*- coding: utf-8 -*-
from pyglet.graphics import OrderedGroup
from pyglet.gl import glPushMatrix, glPopMatrix, glScalef
from GestureAgentsDemo.Utils import DynamicValue


class ShellAppGroup(OrderedGroup):
    """docstring for ShellAppGroup"""
    def __init__(self, order, parent=None):
        super(ShellAppGroup, self).__init__(order, parent=parent)
        self.scale = DynamicValue(1)

    def set_state(self):
        glPushMatrix()
        glScalef(self.scale(), self.scale(), 1)

    def unset_state(self):
        glPopMatrix()

from GestureAgents.AppRecognizer import AppRecognizer

from GestureAgentsTUIO.Gestures2D.RecognizerDoubleTap import RecognizerDoubleTap


class ShellApp(object):
    """docstring for ShellApp"""
    def __init__(self):
        self.possible_apps = [DemoApp]
        self.running = {}
        self.maxid = 0
        AppRecognizer(RecognizerDoubleTap).newAgent.register(
            ShellApp.newAgentDoubleTap, self)
        self.minimized = False

    def launch(self, App):
        id = self.maxid
        group = ShellAppGroup(id)
        self.maxid += 1
        app = App(group=group)
        self.running[app] = dict(id=id, group=group, program=App, instance=app)

    def newAgentDoubleTap(self, agent):
        agent.newDoubleTap.register(ShellApp.newDoubleTap, self)

    def newDoubleTap(self, DTap):
        self.minimized = not self.minimized
        s = .5 if self.minimized else 1
        for app in self.running.itervalues():
            app["group"].scale(s, 1)


from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgentsDemo.Geometry import Circle


class DemoApp(object):
    """docstring for DemoApp"""
    def __init__(self, group=None):
        AppRecognizer(
            TuioCursorEvents).newAgent.register(DemoApp.newAgentPaint, self)
        self.circles = {}
        self.displaygroup = group

    def newAgentPaint(self, agent):
        agent.updateCursor.register(DemoApp.event_move, self)
        agent.newCursor.register(DemoApp.event_new, self)
        agent.removeCursor.register(DemoApp.event_remove, self)

    def event_move(self, Point):
        self.circles[Point.sessionid].getCentered(Point.pos)
        self.circles[Point.sessionid].updateDisplay()

    def event_new(self, Point):
        self.circles[Point.sessionid] = Circle(25, 20, group=self.displaygroup)
        self.event_move(Point)

    def event_remove(self, Point):
        self.circles[Point.sessionid].clear()
        del self.circles[Point.sessionid]


if __name__ == '__main__':
    import GestureAgentsDemo
    from apps.Map import DemoMapApp
    from apps.Shadows import FingerShadow
    from apps.DebugRecognizers import DebugRecognizer
    shell = ShellApp()
    shell.launch(DemoMapApp)
    shell.launch(FingerShadow)
    shell.launch(DebugRecognizer)
    # shell.launch(DemoApp)
    GestureAgentsDemo.run_apps()
