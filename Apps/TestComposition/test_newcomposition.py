
from newcomposition import class_FeatureGesture

from RecognizerFeatureT import class_FeatureTap
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

'''
class FeatureTapTestCase1(t_r(
        events_tap,
        class_FeatureGesture(class_FeatureTap()),
        ("newTap",), 1)):
    pass


class FeatureTapTestCase2(t_r(
        events_2tap,
        class_FeatureGesture(class_FeatureTap()),
        ("newTap",), 2)):
    pass
'''