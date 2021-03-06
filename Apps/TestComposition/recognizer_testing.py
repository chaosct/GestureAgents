# -*- coding: utf-8 -*-
from GestureAgentsTUIO.Tuio import TuioAgentGenerator
import GestureAgents.Reactor as Reactor
import GestureAgents.Gestures as Gestures
from GestureAgents.Agent import Agent
from GestureAgents.AppRecognizer import AppRecognizer
import unittest
from GestureAgents.Events import Event
from GestureAgentsTUIO.Tuio import TuioCursorEvents


def test_events(evlist):
    """Program a series of input events for testing:
    [(type, arg1, arg2, [(timestamp1, event1 ),
                         (timestamp2, event2 ), ...] ),...]
    returns the total duration of the events + 1 seconds
    """
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


class AppTestGeneric(object):
    "Generic application to test recognizers"
    def __init__(self, recognizer, events, system, AppRecognizerClass=AppRecognizer):
        self.ar = AppRecognizerClass(system, recognizer)
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


def test_recognizer(fake_events, recognizer_class, events2listen, events_expected, **kwargs):
    "Create a unit test for a recognizer using a series of events"
    return test_recognizers(fake_events, [(recognizer_class, events2listen, events_expected)], **kwargs)


class TestSystem(object):
    def __init__(self):
        self.new_agents = {}
        self.recognizers = []
        self.sources = [TuioCursorEvents]

    def newAgent(self, recognizer):
        if recognizer not in self.new_agents:
            if recognizer is TuioCursorEvents:
                self.new_agents[recognizer] = TuioCursorEvents.newAgent
            else:
                self.new_agents[recognizer] = Event()
                self.recognizers.append(recognizer(self))
        return self.new_agents[recognizer]

    def run_apps(self, maxtime, debug=False, faketime=True):
        "Minimal reactor loop for the event system to work"
        import datetime
        olddatetime = datetime.datetime

        class newdatetime(olddatetime):
            faketime = olddatetime.now()

            @classmethod
            def now(cls):
                return cls.faketime

        if faketime:
            datetime.datetime = newdatetime

        if debug:
            if self.recognizers:
                print "Loaded %d gesture recognizers:" % len(self.recognizers)
                for r in self.recognizers:
                    print "\t%s" % str(r)

            print "=" * 5 + "Agent.completion_policy Policy rules:" + "=" * 5
            print Agent.completion_policy
        running = [True]

        def stop(a):
            running[0] = False
        Reactor.schedule_after(maxtime, None, stop)
        while running[0]:
            Reactor.run_all_now()
            if faketime and Reactor.scheduled_tasks:
                nextfaketime = Reactor.scheduled_tasks[0][0]
                datetime.datetime.faketime = nextfaketime

        if faketime:
            datetime.datetime = olddatetime


def test_recognizers(fake_events, testing_entries, AppRecognizerClass=AppRecognizer):
    "Create a unit test for several recognizers using a series of events"
    class GenericRecognizerTestCase(unittest.TestCase):
        def setUp(self):
            self.apps = []
            self.system = TestSystem()
            for entry in testing_entries:
                recognizer_class, events2listen, events_expected = entry
                d = {"app": AppTestGeneric(recognizer_class, events2listen, self.system, AppRecognizerClass),
                     "expected": events_expected}
                self.apps.append(d)

        def runTest(self):
            self.system.run_apps(test_events(fake_events))
            for app in self.apps:
                self.assertEqual(app['app'].received, app['expected'])

        def tearDown(self):
            for app in self.apps:
                app['app'].unregister()
            Reactor.cancel_all_tasks()
    return GenericRecognizerTestCase


def t_r(*args, **kargs):
    return test_recognizer(*args, **kargs)


def t_rs(*args, **kargs):
    return test_recognizers(*args, **kargs)
