#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GestureAgents.Recognizer import Recognizer, newHypothesis
import copy
from GestureAgents.Agent import Agent
from GestureAgents.Events import Event


class FakeAgent(Agent):
    def __init__(self, original, creator):
        self.original_agent = original
        Agent.__init__(self, creator, list(original.events))

    def __getattr__(self, attrname):
        return getattr(self.original_agent, attrname)


class AppRecognizer(Recognizer):
    ninstances = 0

    def __init__(self, system, recognizer):
        Recognizer.__init__(self, system, Event())

        self.recognizer = recognizer
        self.eventqueue = []
        self.register_event(self.system.newAgent(recognizer), AppRecognizer._eventNewAgent)
        self.willenqueue = True
        self.name = "AppRecognizer(%s) %d" % (str(recognizer.__name__), AppRecognizer.ninstances)
        AppRecognizer.ninstances += 1

    @newHypothesis
    def _eventNewAgent(self, agent):
        self.unregister_event(self.system.newAgent(self.recognizer))
        self.agent = self._makeAgentAgent(agent)
        self.newAgent(self.agent)
        self.otheragent = agent
        if not self.agent.is_someone_subscribed():
            self.fail("Noone interested")
        else:
            for ename, event in agent.events.iteritems():
                ffff = lambda self, a, eventname=ename: self.enqueueEvent(
                    a, eventname)
                self.register_event(event, ffff)

    def enqueueEvent(self, a, e):
        if not self.eventqueue:
            self.acquire(a)
            self.complete()
        if self.willenqueue:
            #copyagent = copy.copy(self.agent)
            original_agent = copy.copy(a)
            self.eventqueue.append((e, original_agent))
        else:
            self.agent.original_agent = a
            if e == "finishAgent":
                self.finish()
            else:
                self.agent.events[e](self.agent)

    def execute(self):
        self.willenqueue = False
        for event_name, agent in self.eventqueue:
            self.agent.original_agent = agent
            if event_name == "finishAgent":
                self.finish()
            else:
                self.agent.events[event_name](self.agent)

    def _makeAgentAgent(self, agent):
        a = FakeAgent(agent, self)
        return a

    def duplicate(self):
        d = self.get_copy(self.system, self.recognizer)
        d.newAgent = self.newAgent

    def __repr__(self):
        return self.name


#policy
@Agent.completion_policy.rule(-60)
def AppRecognizer_loses(recognizer1, recognizer2):
    "AppRecognizer always looses"
    if type(recognizer1) == AppRecognizer:
        return True
    if type(recognizer2) == AppRecognizer:
        return False
