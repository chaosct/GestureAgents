# coding: utf-8
from GestureAgents.Recognizer import Recognizer
from GestureAgents.Recognizer import newHypothesis
from GestureAgents.Events import Event
from GestureAgents.Agent import Agent
from GestureAgents.AppRecognizer import FakeAgent
from copy import deepcopy


class FakeRecognizer(Recognizer):
    def init(self, system, original_recognizer):
        super(FakeRecognizer, self).__init__(system)
        self.original_recognizer = original_recognizer
        self.register_event(self.system.newAgent(original_recognizer), FakeRecognizer.newAgent)

    @newHypothesis
    def newAgent(self, agent):
        self.agent = FakeAgent(agent, self)
        self.system.newAgent()
        if not self.agent.is_someone_subscribed():
            self.fail("Noone interested")


def class_FeatureGesture(feature):
    class FeatureGesture(Recognizer):
        newAgent = Event()

        def __init__(self, system):
            super(FeatureGesture, self).__init__(system)
            self.new_agents = {}  # dict of fake NewAgent events
            self.__failed = False   # flag preventing double failing
            self.feature = feature(self)  # the gesture definition
            # feature.gesture = self  # we assign the parent
            self.register_event(self.feature.newAgent,
                                FeatureGesture.EventNewFeatureAgent)
            self.agent = Agent([], self)  #legacy, for finishing

        @newHypothesis
        def EventnewAgent(self, agent):
            "Handle newAgent events"
            event = self.sourceevents[agent.newAgent]
            # if event.empty():
            #     self.fail("Noone interested")
            event(agent)

        def EventNewFeatureAgent(self, agent):
            self.newAgent(agent)

        def newAgent(self, recognizer):
            if recognizer not in self.new_agents:
                if recognizer is TuioCursorEvents:
                    self.new_agents[recognizer] = TuioCursorEvents.newAgent
                else:
                    self.new_agents[recognizer] = Event()
                    self.recognizers.append(recognizer(self))
            return self.new_agents[recognizer]

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

    # import GestureAgents.Gestures as Gestures
    # Gestures.load_recognizer(FeatureGesture)
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

        #For now we assume that self.gesture *is* the featuregestue
        self.gesture.finish()
        super(Feature, self).finish()
        pass

    def copy_to(self, d):
        for event, f in self.registers.iteritems():
            if event in self.gesture.sourceevents.itervalues():
                oevent = [o for o, ff in self.gesture.sourceevents.iteritems() if ff is event][0]
                d.register_event(d.getNewAgent(oevent), f)
            else:
                d.register_event(event, f)
    
