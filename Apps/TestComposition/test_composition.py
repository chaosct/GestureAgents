#!/usr/bin/env python
# -*- coding: utf-8 -*-

from RecognizerDT_Test import build_and_register_DT
from RecognizerTT_Test import build_and_register_TT
from RecognizerT_Test import RecognizerT_Test
from recognizer_testing import t_r, t_rs
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


# Test Composition sharing sub-gestures
#Test 1: 2 recognizers share a sub recognzer (Tap)


RecognizerDT1 = build_and_register_DT()
RecognizerTT1 = build_and_register_TT()
RecognizerDT2 = build_and_register_DT(RecognizerT_Test)
RecognizerTT2 = build_and_register_TT(RecognizerT_Test)


class TapTestCase(t_r(events_3tap, RecognizerTap, ("newTap",), 3)):
    pass


class DoubleTapTestCase(t_r(events_3tap, RecognizerDT1, ("newDoubleTap",), 1)):
    pass


class TripleTapTestCase(t_r(events_3tap, RecognizerTT1, ("newTripleTap",), 1)):
    pass


class DoubleTapTestCase2(t_r(events_3tap, RecognizerDT2, ("newDoubleTap",), 1)):
    pass


class TripleTapTestCase2(t_r(events_3tap, RecognizerTT2, ("newTripleTap",), 1)):
    pass


class TripleTapWinsOverDoubleTapTestCase(t_rs(events_3tap,
                                         [(RecognizerDT1, ("newDoubleTap",), 0),
                                          (RecognizerTT1, ("newTripleTap",), 1)])):
    pass


class TripleTapWinsOverDoubleTapTestCase2(t_rs(events_3tap,
                                          [(RecognizerDT2, ("newDoubleTap",), 0),
                                           (RecognizerTT2, ("newTripleTap",), 1)])):
    pass


class TripleTapWinsOverDoubleTapTestCaseMixed1(t_rs(events_3tap,
                                               [(RecognizerDT1, ("newDoubleTap",), 0),
                                                (RecognizerTT2, ("newTripleTap",), 1)])):
    pass


class TripleTapWinsOverDoubleTapTestCaseMixed1b(t_rs(events_3tap,
                                               [(RecognizerTT2, ("newTripleTap",), 1),
                                                (RecognizerDT1, ("newDoubleTap",), 0)])):
    pass


class TripleTapWinsOverDoubleTapTestCaseMixed2(t_rs(events_3tap,
                                               [(RecognizerDT2, ("newDoubleTap",), 0),
                                                (RecognizerTT1, ("newTripleTap",), 1)])):
    pass

class TripleTapWinsOverDoubleTapTestCaseMixed2b(t_rs(events_3tap,
                                               [(RecognizerTT1, ("newTripleTap",), 1),
                                                (RecognizerDT2, ("newDoubleTap",), 0)])):
    pass


events_nodtap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.8, 'in'),
     (0.9, 'out'))),
]


class DoubleTapTestCase3(t_r(events_nodtap,
                         RecognizerDT1,
                         ("newDoubleTap",), 0)):
    pass


events_nodtap2 = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.7, 0.7), (
     (0.2, 'in'),
     (0.3, 'out'))),
]


class DoubleTapTestCase4(t_r(events_nodtap2,
                         RecognizerDT1,
                         ("newDoubleTap",), 0)):
    pass

if __name__ == '__main__':
    import unittest
    unittest.main()
