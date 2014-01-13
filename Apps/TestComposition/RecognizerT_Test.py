#!/usr/bin/env python
# -*- coding: utf-8 -*-

import GestureAgentsTUIO.Tuio as Tuio
from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Agent import Agent
import math


class RecognizerT_Test(Recognizer):

    def __init__(self, system):
        self.finger = None
        Recognizer.__init__(self, system)
        self.cursorEvents = Tuio.TuioCursorEvents
        self.register_event(
            self.system.newAgent(self.cursorEvents), RecognizerT_Test.EventNewAgent)
        self.maxd = 10
        self.time = 0.5
        self.origin = None
        self.newAgent = self.system.newAgent(RecognizerT_Test)

    @newHypothesis
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
            self.unregister_event(self.system.newAgent(self.cursorEvents))
            self.register_event(Cursor.newCursor, RecognizerT_Test.EventNewCursor)

    def EventNewCursor(self, Cursor):
        self.finger = Cursor
        self.unregister_event(Cursor.newCursor)
        self.register_event(Cursor.updateCursor, RecognizerT_Test.EventMoveCursor)
        self.register_event(
            Cursor.removeCursor, RecognizerT_Test.EventRemoveCursor)
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
        self.complete()

    def execute(self):
        self.agent.pos = self.origin
        self.agent.newTap(self.agent)
        self.finish()

    @staticmethod
    def dist(a, b):
        dx, dy = (a[0] - b[0], a[1] - b[1])
        return math.sqrt(dx ** 2 + dy ** 2)

    def duplicate(self):
        d = self.get_copy(self.system)
        d.finger = self.finger
        d.origin = self.origin
        return d

    def make_TapAgent(self):
        a = Agent(self,("newTap",))
        return a
