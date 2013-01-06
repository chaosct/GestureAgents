#!/usr/bin/env

import pyglet.app


from GestureAgents import Gestures, Agent
from Window import DemoWindow


def run_apps(debugMem=False):
    global window
    if Gestures.recognizers_loaded:
        print "Loaded %d gesture recognizers:" % len(Gestures.recognizers)
        for r in Gestures.recognizers:
            print "\t%s" % str(r)

    print "=" * 5 + " Agent.completion_policy Policy rules " + "=" * 5
    print Agent.Agent.completion_policy
    print "=" * 5 + " Agent.compatibility_policy Policy rules " + "=" * 5
    print Agent.Agent.compatibility_policy

    window = DemoWindow()
    pyglet.app.run()


def run():
    run_apps()

if __name__ == '__main__':
    run()
