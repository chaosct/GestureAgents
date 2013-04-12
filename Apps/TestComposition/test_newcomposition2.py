
from newcomposition2 import AppRecognizer2

from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap
from recognizer_testing import t_r

events_tap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    # ('f', 2, (0.5, 0.5), (
    #  (0.3, 'in'),
    #  (0.4, 'out'))),
]

events_2tap = [
    ('f', 1, (0.5, 0.5), (
     (0, 'in'),
     (0.1, 'out'))),
    ('f', 2, (0.5, 0.5), (
     (0.3, 'in'),
     (0.4, 'out'))),
]


class FeatureTapTestCase1(t_r(
        events_tap,
        RecognizerTap,
        ("newTap",), 1,
        AppRecognizerClass=AppRecognizer2)):
    pass


class FeatureTapTestCase2(t_r(
        events_2tap,
        RecognizerTap,
        ("newTap",), 2,
        AppRecognizerClass=AppRecognizer2)):
    pass
