#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from GestureAgents.AppRecognizer import AppRecognizer
import GestureAgents.Gestures as Gestures
from RecognizerDT_Test import build_and_register_DT
from GestureAgents.Agent import Agent
import GestureAgents.Reactor as Reactor
from RecognizerTT_Test import build_and_register_TT
from RecognizerT_Test import RecognizerT_Test


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


def enter_debug():
    return
    import pdb
    pdb.set_trace()


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
                    f = lambda s, a=a: (enter_debug(), a.removeCursor(a), a.finish())
                else:
                    raise NotImplementedError
                Reactor.schedule_after(time, None, f)
    return maxtime+1


def run_apps(maxtime, debug=False):
    if debug:
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


class AppTestGeneric(object):
    def __init__(self, recognizer, events):
        self.ar = AppRecognizer(recognizer)
        self.ar.newAgent.register(AppTestGeneric.newAgentTap, self)
        self.received = 0
        self.events = events

    def newAgentTap(self, agent):
        for event in self.events:
            getattr(agent, event).register(AppTestGeneric.cb, self)

    def cb(self, agent):
        self.received += 1

    def unregister(self):
        self.ar.newAgent.unregister(self)

# Test Composition sharing sub-gestures
#Test 1: 2 recognizers share a sub recognzer (Tap)


RecognizerDT1 = build_and_register_DT()
RecognizerTT1 = build_and_register_TT()
RecognizerDT2 = build_and_register_DT(RecognizerT_Test)
RecognizerTT2 = build_and_register_TT(RecognizerT_Test)


def AppTestTap():
    from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap
    return AppTestGeneric(RecognizerTap, ("newTap",))


def AppTestDT():
    return AppTestGeneric(RecognizerDT1, ("newDoubleTap",))


def AppTestTT():
    return AppTestGeneric(RecognizerTT1, ("newTripleTap",))


def AppTestTap2():
    return AppTestGeneric(RecognizerT_Test, ("newTap",))


def AppTestDT2():
    return AppTestGeneric(RecognizerDT2, ("newDoubleTap",))


def AppTestTT2():
    return AppTestGeneric(RecognizerTT2, ("newTripleTap",))


class TapTestCase(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTap()

    def runTest(self):
        run_apps(test_events(events_3tap))
        assert self.appt1.received == 3

    def tearDown(self):
        self.appt1.unregister()


class DoubleTapTestCase(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT()

    def runTest(self):
        run_apps(test_events(events_3tap))
        assert self.appt1.received == 1

    def tearDown(self):
        self.appt1.unregister()


class TripleTapTestCase(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTT()

    def runTest(self):
        run_apps(test_events(events_3tap))
        assert self.appt1.received == 1

    def tearDown(self):
        self.appt1.unregister()

class TapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTap2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        assert self.appt1.received == 3

    def tearDown(self):
        self.appt1.unregister()


class DoubleTapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        assert self.appt1.received == 1

    def tearDown(self):
        self.appt1.unregister()


class TripleTapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTT2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        assert self.appt1.received == 1

    def tearDown(self):
        self.appt1.unregister()

if __name__ == '__main__':
    unittest.main()

