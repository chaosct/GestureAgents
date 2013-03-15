# coding: utf-8
from GestureAgents import Recognizer
from GestureAgentsTUIO import Tuio
from GestureAgents.Recognizer import newHypothesis
from GestureAgents.Events import Event
from GestureAgents.Agent import Agent
import math


class FeatureGesture(Recognizer):
    def __init__(self, feature):
        self.feature = feature
        feature.gesture = self
        self.sourceevents = {}
        self.__failed = False

    @newHypothesis
    def EventnewAgent(self, agent):
        event = self.sourceevents[agent.newAgent]
        if event.empty():
            self.fail("Noone interested")
        event(agent)

    def getNewAgent(self, na):
        if na not in self.sourceevents:
            self.sourceevents[na] = Event()
            self.register_event(na, self.EventnewAgent)
        return self.sourceevents[na]

    def fail(self, cause):
        if self.__failed:
            return
        self.__failed = True
        self.feature.safe_fail(cause)
        super(FeatureGesture, self).fail(cause)


class Feature(Recognizer):
    def __init__(self):
        self.__failed = False

    def getNewAgent(self, na):
        return self.gesture.getNewAgent(na)

    def fail(self, cause):
        if self.__failed:
            return
        self.__failed = True
        self.gesture.fail()
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


class FeatureTap(Feature):
    newAgent = Event()

    def __init__(self):
        self.finger = None
        super(FeatureTap, self).__init__()
        self.cursorEvents = Tuio.TuioCursorEvents
        self.register_event(self.getNewAgent(self.cursorEvents.newAgent), FeatureTap.EventNewAgent)
        self.maxd = 10
        self.time = 0.5
        self.origin = None

    def EventNewAgent(self, Cursor):
        # Am I interested on this Agent?
        # We don't want recycled Agents
        if Cursor.recycled:
            self.fail("Cursor is recycled")
        # Let's ask our subscribbers
        self.agent = self.make_TapAgent()
        self.agent.pos = Cursor.pos
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail("Noone interested")
        else:
            self.unregister_event(self.getNewAgent(self.cursorEvents.newAgent))
            self.register_event(Cursor.newCursor, FeatureTap.EventNewCursor)

    def EventNewCursor(self, Cursor):
        self.finger = Cursor
        self.unregister_event(Cursor.newCursor)
        self.register_event(Cursor.updateCursor, FeatureTap.EventMoveCursor)
        self.register_event(
            Cursor.removeCursor, FeatureTap.EventRemoveCursor)
        self.expire_in(self.time)
        self.origin = Cursor.pos
        self.acquire(Cursor)

    def EventMoveCursor(self, Cursor):
        if self.dist(Cursor.pos, self.origin) > self.maxd:
            self.fail("Cursor moved")

    def EventRemoveCursor(self, Cursor):
        self.cancel_expire()
        self.unregister_event(Cursor.updateCursor)
        self.unregister_event(Cursor.removeCursor)
        self.complete(self)

    def execute(self):
        self.agent.pos = self.origin
        self.agent.newTap(self.agent)
        self.finish()

    @staticmethod
    def dist(a, b):
        dx, dy = (a[0] - b[0], a[1] - b[1])
        return math.sqrt(dx ** 2 + dy ** 2)

    def duplicate(self):
        d = self.get_copy()
        d.finger = self.finger
        d.origin = self.origin
        return d

    def make_TapAgent(self):
        a = Agent(("newTap",), self)
        return a
