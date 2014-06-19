from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap
from recognizer_testing import t_r

events_tap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
]


class TUIOTapTestCase1(t_r(events_tap, RecognizerTap, ("newTap",), 1)):
    pass


events_2tap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.05, 'in'),
     (0.15, 'out'))),
]


class TUIOTapTestCase2(t_r(events_2tap, RecognizerTap, ("newTap",), 2)):
    pass


events_notap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.7, 'out'))),
]


class TUIOTapTestCase3(t_r(events_notap, RecognizerTap, ("newTap",), 0)):
    pass


events_dtap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.2, 'in'),
     (0.3, 'out'))),
]


class TUIOTapTestCase4(t_r(events_dtap, RecognizerTap, ("newTap",), 2)):
    pass


from GestureAgentsTUIO.Gestures2D.RecognizerDoubleTap import RecognizerDoubleTap


class TUIODoubleTapTestCase1(t_r(events_dtap,
                                 RecognizerDoubleTap,
                                 ("newDoubleTap",), 1)):
    pass


class TUIODoubleTapTestCase2(t_r(events_2tap,
                                 RecognizerDoubleTap,
                                 ("newDoubleTap",), 0)):
    pass


events_nodtap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.8, 'in'),
     (0.9, 'out'))),
]


class TUIODoubleTapTestCase3(t_r(events_nodtap,
                                 RecognizerDoubleTap,
                                 ("newDoubleTap",), 0)):
    pass


events_nodtap2 = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.8, 0.8), (
     (0.2, 'in'),
     (0.3, 'out'))),
]


class TUIODoubleTapTestCase4(t_r(events_nodtap2,
                                 RecognizerDoubleTap,
                                 ("newDoubleTap",), 0)):
    pass


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


class TUIODoubleTapTestCase4(t_r(events_3tap,
                                 RecognizerDoubleTap,
                                 ("newDoubleTap",), 1)):
    pass


events_2dtap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.2, 'in'),
     (0.3, 'out'))),
    ('f', 3, (0.5, 0.5), (
     (0.4, 'in'),
     (0.5, 'out'))),
    ('f', 4, (0.5, 0.5), (
     (0.6, 'in'),
     (0.7, 'out'))),
]


class TUIODoubleTapTestCase5(t_r(events_2dtap,
                                 RecognizerDoubleTap,
                                 ("newDoubleTap",), 2)):
    pass
