#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Recognizer import Recognizer, newHypothesis
import copy
from Agent import Agent
from Events import Event

class FakeAgent(Agent):
    def __init__(self,original):
        self.original_agent = original
        Agent.__init__(self,list(original.events))
        
    def __getattr__(self,attrname):
        return getattr(self.original_agent,attrname)
        

class AppRecognizer(Recognizer):
    def __init__(self,recognizer):
        Recognizer.__init__(self)

        self.recognizer = recognizer
        self.newAgent = Event()
        self.eventqueue = []
        self.register_event(recognizer.newAgent,AppRecognizer._eventNewAgent)
        self.willenqueue = True
    
    @newHypothesis
    def _eventNewAgent(self,agent):
        self.unregister_event(self.recognizer.newAgent)
        self.agent = self._makeAgentAgent(agent)
        self.newAgent(self.agent)
        self.otheragent = agent
        if not self.agent.is_someone_subscribed():
            self.fail()
        else:
            for ename,event in agent.events.iteritems():
                ffff = lambda self,a,eventname=ename: self.enqueueEvent(a,eventname)
                self.register_event(event,ffff )
    
    def enqueueEvent(self,a,e):
        if not self.eventqueue:
            self.acquire(a)
            self.complete()
        if self.willenqueue:
            copyagent = copy.copy(self.agent)
            copyagent.original_agent = copy.copy(copyagent.original_agent)
            self.eventqueue.append((e,copyagent))
        else:
            if e == "finishAgent":
                self.finish()
            else:
                self.agent.events[e](self.agent)

    def execute(self):
        self.willenqueue = False
        for event_name,agent in self.eventqueue:
            if event_name == "finishAgent":
                self.finish()
            else:
                self.agent.events[event_name](agent)
    
    def _makeAgentAgent(self,agent):
        a =  FakeAgent(agent)
        a.owners.append(self)
        return a
    
    def duplicate(self):
        d = AppRecognizer(self.recognizer)
        d.newAgent = self.newAgent
        Recognizer.copy_to(self,d)
            
