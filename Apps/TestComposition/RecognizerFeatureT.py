# -*- coding: utf-8 -*-
from newcomposition import Feature
from GestureAgents.Events import Event
from GestureAgentsTUIO import Tuio
import math
from GestureAgents.Agent import Agent


def class_FeatureTap():
    class FeatureTap(Feature):
        newAgent = Event()

        def __init__(self, parent):
            print "FeatureTap.__init__"
            self.finger = None
            super(FeatureTap, self).__init__(parent)
            self.cursorEvents = Tuio.TuioCursorEvents
            self.register_event(self.getNewAgent(self.cursorEvents.newAgent),
                                FeatureTap.EventNewAgent)
            self.maxd = 10
            self.time = 0.5
            self.origin = None

        def EventNewAgent(self, Cursor):
            print "FeatureTap.EventNewAgent"
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
                self.unregister_event(
                    self.getNewAgent(self.cursorEvents.newAgent))
                self.register_event(Cursor.newCursor,
                                    FeatureTap.EventNewCursor)

        def EventNewCursor(self, Cursor):
            print "FeatureTap.EventMoveCursor"
            self.finger = Cursor
            self.unregister_event(Cursor.newCursor)
            self.register_event(Cursor.updateCursor,
                                FeatureTap.EventMoveCursor)
            self.register_event(
                Cursor.removeCursor, FeatureTap.EventRemoveCursor)
            self.expire_in(self.time)
            self.origin = Cursor.pos
            self.acquire(Cursor)

        def EventMoveCursor(self, Cursor):
            print "FeatureTap.EventMoveCursor"
            if self.dist(Cursor.pos, self.origin) > self.maxd:
                self.fail("Cursor moved")

        def EventRemoveCursor(self, Cursor):
            print "FeatureTap.EventRemoveCursor"
            self.cancel_expire()
            self.unregister_event(Cursor.updateCursor)
            self.unregister_event(Cursor.removeCursor)
            self.complete(self)

        def execute(self):
            print "FeatureTap.execute"
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

    return FeatureTap
