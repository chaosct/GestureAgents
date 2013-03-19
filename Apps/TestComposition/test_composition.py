#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GestureAgents.AppRecognizer import AppRecognizer
import GestureAgents.Gestures as Gestures
from RecognizerDT_Test import build_and_register_DT
from GestureAgents.Agent import Agent
import GestureAgents.Reactor as Reactor


events_3tap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.2, 'in'),
     (0.3, 'out'))),
    ('f', 3, (0.5, 0.5), (
     (0.4, 'in'),
     (0.5, 'out'))),
]


def printf(s):
    print s


def test_events(evlist):
    from GestureAgentsTUIO.Tuio import TuioAgentGenerator
    maxtime = 0
    for entry in evlist:
        t = entry[0]
        if t == 'f':
            sid, pos, events = entry[1:]
            a = TuioAgentGenerator.makeCursorAgent()
            a.pos = pos
            a.posx = pos[0]
            a.posy = pos[1]
            a.sessionid = sid
            a.xmot = 0
            a.ymot = 0
            a.mot_accel = 0
            for e in events:
                time, ev_type = e[:2]
                maxtime = max(maxtime, time)
                if ev_type == 'in':
                    f = lambda s, a=a: (a.newAgent(a), a.newCursor(a))
                elif ev_type == 'out':
                    f = lambda s, a=a: (a.removeCursor(a), a.finish())
                else:
                    raise NotImplementedError
                Reactor.schedule_after(time, None, f)
    return maxtime+1

# Test Composition sharing sub-gestures
#Test 1: 2 recognizers share a sub recognzer (Tap)


RecognizerDT1 = build_and_register_DT()


class AppTestComposition1(object):
    def __init__(self):
        AppRecognizer(RecognizerDT1).newAgent.register(AppTestComposition1.newAgent2Tap, self)
        self.dtaps = 0

    def newAgent2Tap(self, agent):
        agent.newDoubleTap.register(AppTestComposition1.DT, self)

    def DT(self, agent):
        self.dtaps += 1


#super simple Loop

def run_apps(maxtime):
    if Gestures.recognizers_loaded:
        print "Loaded %d gesture recognizers:" % len(Gestures.recognizers)
        for r in Gestures.recognizers:
            print "\t%s" % str(r)

    print "=" * 5 + "Agent.completion_policy Policy rules:" + "=" * 5
    print Agent.completion_policy
    running = [True]

    def stop(a):
        running[0] = False
    Reactor.schedule_after(maxtime, None, stop)
    while running[0]:
        Reactor.run_all_now()

if __name__ == '__main__':
    appt1 = AppTestComposition1()
    run_apps(test_events(events_3tap))
    assert appt1.dtaps == 1
    appt1 = AppTestComposition1()
    run_apps(test_events(events_3tap))
    assert appt1.dtaps == 1

