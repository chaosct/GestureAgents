# coding: utf-8
from GestureAgents.Recognizer import Recognizer
from GestureAgents.Recognizer import newHypothesis
from GestureAgents.Events import Event
from copy import deepcopy


def class_FeatureGesture(feature):
    class FeatureGesture(Recognizer):
        newAgent = Event()

        def __init__(self):
            super(FeatureGesture, self).__init__()
            self.sourceevents = {}  # dict of fake NewAgent events
            self.__failed = False   # flag preventing double failing
            self.feature = feature(self)  # the gesture definition
            # feature.gesture = self  # we assign the parent
            self.register_event(self.feature.newAgent,
                                FeatureGesture.EventNewFeatureAgent)

        @newHypothesis
        def EventnewAgent(self, agent):
            "Handle newAgent events"
            event = self.sourceevents[agent.newAgent]
            # if event.empty():
            #     self.fail("Noone interested")
            event(agent)

        def EventNewFeatureAgent(self, agent):
            self.newAgent(agent)

        def getNewAgent(self, na):
            if na not in self.sourceevents:
                self.sourceevents[na] = Event()
                self.register_event(na, FeatureGesture.EventnewAgent)
            return self.sourceevents[na]

        def fail(self, cause):
            print "FeatureGesture.fail({})".format(cause)
            if self.__failed:
                return
            self.__failed = True
            self.feature.safe_fail(cause)
            super(FeatureGesture, self).fail(cause)

        def execute(self):
            self.feature.execute()

        def duplicate(self):
            d = self.get_copy()
            for se in self.sourceevents:
                d.getNewAgent(se)
            d.__failed = self.__failed
            # import ipdb
            # ipdb.set_trace()
            d.feature.unregister_all()
            d.feature = self.feature.duplicate(d)
            d.register_event(d.feature.newAgent,
                             FeatureGesture.EventNewFeatureAgent)
            return d

    import GestureAgents.Gestures as Gestures
    Gestures.load_recognizer(FeatureGesture)
    return FeatureGesture


class Feature(Recognizer):
    def __init__(self, parent):
        super(Feature, self).__init__()
        self.gesture = parent
        self.__failed = False

    def getNewAgent(self, na):
        return self.gesture.getNewAgent(na)

    def fail(self, cause):
        if self.__failed:
            return
        self.__failed = True
        self.gesture.fail(cause)
        super(Feature, self).fail(cause)

    def acquire(self, agent):
        self.gesture.acquire(agent)

    def complete(self, caller):
        if caller is not self:
            caller.execute()
        self.gesture.complete()

    def finish(self):
        #for every agent acquired fake recycling
        #that means tracking acquired agents per feature
        #and making agent envelops simply faking the recycled flag
        pass

    def copy_to(self, d):
        for event, f in self.registers.iteritems():
            if event in self.gesture.sourceevents.itervalues():
                oevent = [o for o, f in self.gesture.sourceevents.iteritems() if f is event][0]
                d.register_event(d.getNewAgent(oevent), f)
            else:
                d.register_event(event, f)
    
