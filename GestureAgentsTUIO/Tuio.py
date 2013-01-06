#!/usr/bin/env python
# -*- coding: utf-8 -*-

import GestureAgentsTUIO.tuio as tuio
from GestureAgents.Events import Event
from GestureAgents.Agent import Agent


class TuioCursorEvents:
    newAgent = Event()


class TuioAgentGenerator:
    def __init__(self, screensize):
        self.tracking = tuio.Tracking()
        self.cursors = {}
        self.agents = {}
        self.screensize = screensize

    def update(self):
        self.tracking.update()
        cursors = {}
        for cur in self.tracking.cursors():
            cursors[cur.sessionid] = self._genCurDict(cur)
        #send removeCursor
        for c in dict(self.cursors):
            if c not in cursors:
                del self.cursors[c]
                a = self.agents[c]
                a.removeCursor.call(a)
                a.finish()
                del self.agents[c]
        #send new info
        for c, content in cursors.iteritems():
            if c not in self.cursors:
                #newCursor
                a = self.makeCursorAgent()
                self._updateAgent(a, content)
                a.ontable = False
                self.cursors[c] = content
                self.agents[c] = a
                TuioCursorEvents.newAgent.call(a)
                a.ontable = True
                a.newCursor.call(a)
            elif content != self.cursors[c]:
                #updateCursor
                a = self.agents[c]
                self._updateAgent(a, content)
                self.cursors[c] = content
                a.updateCursor.call(a)

    def __del__(self):
        self.tracking.stop()

    @staticmethod
    def _genCurDict(cur):
        d = dict()
        for member in ("sessionid", "xpos", "ypos", "xmot", "ymot", "mot_accel"):
            d[member] = getattr(cur, member)
        return d

    def _updateAgent(self, agent, dcur):
        for member, value in dcur.iteritems():
            setattr(agent, member, value)
        #pos is legacy as Mouse emulator
        agent.pos = (
            agent.xpos * self.screensize[0], agent.ypos * self.screensize[1])

    @staticmethod
    def makeCursorAgent():
        evts = ('newCursor', 'updateCursor', 'removeCursor')
        return Agent(evts, TuioCursorEvents)
