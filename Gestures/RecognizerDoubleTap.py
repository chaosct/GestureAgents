#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Recognizer import Recognizer, newHypothesis
from Events import Event
from RecognizerTap import RecognizerTap
import Reactor
from Agent import Agent
import math

class RecognizerDoubleTap(Recognizer):
    newAgent = Event()
    def __init__(self):
        Recognizer.__init__(self)
        self.agent = None
        self.firstap = None
        self.secondtap = None
        self.register_event(RecognizerTap.newAgent,RecognizerDoubleTap.EventNewAgent)
        self.time = 0.3
        self.maxd = 10
        
    @newHypothesis
    def EventNewAgent(self,Tap):
        self.agent = self.make_DoubleTapAgent()
        self.agent.pos = Tap.pos
        self.newAgent.call(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail()
        else:
            self.unregister_event(RecognizerTap.newAgent)
            self.register_event(Tap.newTap,RecognizerDoubleTap.FirstTap)
        
    def FirstTap(self,Tap):
        self.firstap = Tap
        self.unregister_event(Tap.newTap)
        self.register_event(RecognizerTap.newAgent,RecognizerDoubleTap.EventNewAgent2)
        Reactor.schedule_after(self.time,self,RecognizerDoubleTap.timeout)
        self.acquire(Tap)
    
    
    @newHypothesis
    def EventNewAgent2(self,Tap):
        if self.dist(Tap.pos,self.firstap.pos) > self.maxd:
            self.fail()
        else:
            self.unregister_event(RecognizerTap.newAgent)
            self.register_event(Tap.newTap,RecognizerDoubleTap.SecondTap)
        
    def SecondTap(self,Tap):
        if self.dist(Tap.pos,self.firstap.pos) > self.maxd:
            self.fail()
        else:
            self.secondtap = Tap
            self.unregister_event(Tap.newTap)
            Reactor.cancel_schedule(self)
            self.acquire(Tap)
            self.complete()
            self.fail_all_others()

    
    def timeout(self):
        self.fail()
    
    def execute(self):
        self.agent.pos = self.secondtap.pos
        self.agent.newDoubleTap(self.agent)
        self.finish()
    
    def duplicate(self):
        d = RecognizerDoubleTap()
        Recognizer.copy_to(self,d)
        d.firstap = self.firstap
        d.secondtap = self.secondtap
        return d
    
    @staticmethod
    def dist(a,b):
        dx,dy = (a[0]-b[0],a[1]-b[1])
        return math.sqrt(dx**2 + dy**2)
    
    def make_DoubleTapAgent(self):
        a =  Agent(("newDoubleTap",))
        a.owners.append(self)
        return a
