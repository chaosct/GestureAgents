#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from GestureAgents.AppRecognizer import AppRecognizer
from RecognizerDT_Test import build_and_register_DT
from RecognizerTT_Test import build_and_register_TT
from RecognizerT_Test import RecognizerT_Test
from recognizer_testing import run_apps
from recognizer_testing import test_events
from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap


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


def test_regognizer(recognizer_class, events2listen, fake_events, events_expected):
    class GenericRecognizerTestCase(unittest.TestCase):
        def setUp(self):
            self.appt1 = AppTestGeneric(recognizer_class, events2listen)

        def runTest(self):
            run_apps(test_events(fake_events))
            self.assertEqual(self.appt1.received, events_expected)

        def tearDown(self):
            self.appt1.unregister()
    return GenericRecognizerTestCase

TapTestCase = test_regognizer(RecognizerTap, ("newTap",), events_3tap, 3)


class DoubleTapTestCase(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 1)

    def tearDown(self):
        self.appt1.unregister()


class TripleTapTestCase(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTT()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 1)

    def tearDown(self):
        self.appt1.unregister()


class TapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTap2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 3)

    def tearDown(self):
        self.appt1.unregister()


class DoubleTapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 1)

    def tearDown(self):
        self.appt1.unregister()


class TripleTapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestTT2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 1)

    def tearDown(self):
        self.appt1.unregister()


class TripleTapWinsOverDoubleTapTestCase(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT()
        self.appt2 = AppTestTT()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 0)
        self.assertEqual(self.appt2.received, 1)

    def tearDown(self):
        self.appt1.unregister()
        self.appt2.unregister()


class TripleTapWinsOverDoubleTapTestCase2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT2()
        self.appt2 = AppTestTT2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 0)
        self.assertEqual(self.appt2.received, 1)

    def tearDown(self):
        self.appt1.unregister()
        self.appt2.unregister()


class TripleTapWinsOverDoubleTapTestCaseMixed1(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT()
        self.appt2 = AppTestTT2()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 0)
        self.assertEqual(self.appt2.received, 1)

    def tearDown(self):
        self.appt1.unregister()
        self.appt2.unregister()


class TripleTapWinsOverDoubleTapTestCaseMixed2(unittest.TestCase):
    def setUp(self):
        self.appt1 = AppTestDT2()
        self.appt2 = AppTestTT()

    def runTest(self):
        run_apps(test_events(events_3tap))
        self.assertEqual(self.appt1.received, 0)
        self.assertEqual(self.appt2.received, 1)

    def tearDown(self):
        self.appt1.unregister()
        self.appt2.unregister()


if __name__ == '__main__':
    unittest.main()

