#!/usr/bin/env

import pyglet.app
from GestureAgents import Gestures, Agent
from Window import DemoWindow
import GestureAgents.System
from GestureAgentsTUIO.Tuio import TuioCursorEvents

class System(GestureAgents.System.System, DemoWindow):
    def __init__(self):
        sources = [TuioCursorEvents]
        GestureAgents.System.System.__init__(self, sources)
        DemoWindow.__init__(self)

    def run_apps(self, debugMem=False):
        # if Gestures.recognizers_loaded:
        #     print "Loaded %d gesture recognizers:" % len(Gestures.recognizers)
        #     for r in Gestures.recognizers:
        #         print "\t%s" % str(r)

        print "=" * 5 + " Agent.completion_policy Policy rules " + "=" * 5
        print Agent.Agent.completion_policy
        print "=" * 5 + " Agent.compatibility_policy Policy rules " + "=" * 5
        print Agent.Agent.compatibility_policy

        # self.window = DemoWindow()
        pyglet.app.run()

    def stop(self):
        pyglet.app.exit()

    def update(self, dt):
        DemoWindow.update(self, dt)        

