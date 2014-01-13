#!/usr/bin/env python
# -*- coding: utf-8 -*-


import GestureAgentsTUIO.Tuio as Tuio
from math import sqrt, fabs
from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Events import Event
from GestureAgents.Agent import Agent


class AgentStick(Agent):
    eventnames = ("newStick",)


class RecognizerStick (Recognizer):

    def __init__(self, system):
        Recognizer.__init__(self, system)
        self.finger = None
        self.cursorEvents = Tuio.TuioCursorEvents
        self.register_event(
            system.newAgent(self.cursorEvents), RecognizerStick.EventNewAgent)
        self.positions = []
        self.newAgent = system.newAgent(RecognizerStick)

    @newHypothesis
    def EventNewAgent(self, Cursor):
        if Cursor.recycled:
            self.fail(cause="Agent is recycled")
        self.agent = AgentStick(self)
        self.agent.pos = Cursor.pos
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail(cause="Noone interested")
        else:
            self.unregister_all()
            self.register_event(
                Cursor.newCursor, RecognizerStick.EventNewCursor)

    def EventNewCursor(self, Cursor):
        #cursor is an Agent
        self.finger = Cursor
        self.positions.append(Cursor.pos)
        self.unregister_event(Cursor.newCursor)
        self.register_event(
            Cursor.updateCursor, RecognizerStick.EventMoveCursor)
        self.register_event(
            Cursor.removeCursor, RecognizerStick.EventRemoveCursor)
        #acquire should be the last thing to do
        self.acquire(Cursor)

    def EventMoveCursor(self, Cursor):
        self.positions.append(Cursor.pos)
        if not self.is_line():
            self.fail(cause="Is not line")

    def is_line(self):
        first = self.positions[0]
        last = self.positions[-1]
        dist = sqrt((last[0] - first[0]) ** 2 + (last[1] - first[1]) ** 2)
        if dist < 50:
            return True
        maxdist = dist / 20.0
        for p in self.positions:
            d = self.pdis(first, last, p)
            if abs(d) > maxdist:
                return False
        return True

    def EventRemoveCursor(self, Cursor):
        self.unregister_event(Cursor.updateCursor)
        self.unregister_event(Cursor.removeCursor)
        first = self.positions[0]
        last = self.positions[-1]
        dist = sqrt((last[0] - first[0]) ** 2 + (last[1] - first[1]) ** 2)
        if self.is_line() and dist > 30:
            self.complete()
        else:
            self.fail(cause="Is not line")

    def duplicate(self):
        d = self.get_copy(self.system)
        d.finger = self.finger
        d.positions = list(self.positions)
        return d

    def execute(self):
        self.agent.pos1 = self.positions[0]
        self.agent.pos2 = self.positions[-1]

        self.agent.newStick.call(self.agent)
        self.finish()

    # def make_StickAgent(self):
    #     a = Agent(("newStick",), self)
    #     return a

    @staticmethod
    def pdis(a, b, c):
        t = b[0] - a[0], b[1] - a[1]           # Vector ab
        dd = sqrt(t[0] ** 2 + t[1] ** 2)         # Length of ab
        t = t[0] / dd, t[1] / dd               # unit vector of ab
        n = -t[1], t[0]                    # normal unit vector to ab
        ac = c[0] - a[0], c[1] - a[1]          # vector ac
        return fabs(ac[0] * n[0] + ac[1] * n[1])  # Projection of ac to n (the minimum distance)


