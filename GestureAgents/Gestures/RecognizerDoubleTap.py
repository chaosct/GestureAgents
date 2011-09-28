#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Events import Event
from RecognizerTap import RecognizerTap
from GestureAgents.Agent import Agent
import math

class RecognizerDoubleTap(Recognizer):
    newAgent = Event()
    rtotal = 0
    def __init__(self):
        Recognizer.__init__(self)
        self.agent = None
        self.firstap = None
        self.secondtap = None
        self.register_event(RecognizerTap.newAgent,RecognizerDoubleTap.EventNewAgent)
        self.time = 0.3
        self.maxd = 10
        self.name = "RecognizerDoubleTap %d" % RecognizerDoubleTap.rtotal
        RecognizerDoubleTap.rtotal+=1
        
    @newHypothesis
    def EventNewAgent(self,Tap):
        self.agent = self.make_DoubleTapAgent()
        self.agent.pos = Tap.pos
        self.newAgent.call(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail(cause="Noone Interested")
        else:
            self.unregister_event(RecognizerTap.newAgent)
            self.register_event(Tap.newTap,RecognizerDoubleTap.FirstTap)
        
    def FirstTap(self,Tap):
        self.firstap = Tap
        self.unregister_event(Tap.newTap)
        self.register_event(RecognizerTap.newAgent,RecognizerDoubleTap.EventNewAgent2)
        self.expire_in(self.time)
        self.acquire(Tap)
    
    
    @newHypothesis
    def EventNewAgent2(self,Tap):
        if self.dist(Tap.pos,self.firstap.pos) > self.maxd:
            self.fail(cause="Max distance")
        else:
            self.unregister_event(RecognizerTap.newAgent)
            self.register_event(Tap.newTap,RecognizerDoubleTap.SecondTap)
        
    def SecondTap(self,Tap):
        if self.dist(Tap.pos,self.firstap.pos) > self.maxd:
            self.fail(cause="Max distance")
        else:
            self.secondtap = Tap
            self.unregister_event(Tap.newTap)
            self.cancel_expire()
            self.acquire(Tap)
            self.complete()
            #print "I win",self
            #print self.agent.newDoubleTap.registered
            #import pdb; pdb.set_trace()
            self.fail_all_others()
 
    def execute(self):
        #print "I execute",self
        self.agent.pos = self.secondtap.pos
        #print self.agent.newDoubleTap.registered
        self.agent.newDoubleTap(self.agent)
        self.finish()
    
    def duplicate(self):
        d = RecognizerDoubleTap()
        Recognizer.copy_to(self,d)
        d.firstap = self.firstap
        d.secondtap = self.secondtap
        return d
    
    #def fail(self, cause="Unknown"):
    #    print "RecognizerDoubleTap(",self,") fail, cause="+cause
    #    #raise Exception("RecognizerDoubleTap fail")
    #    Recognizer.fail(self)
    
    @staticmethod
    def dist(a,b):
        dx,dy = (a[0]-b[0],a[1]-b[1])
        return math.sqrt(dx**2 + dy**2)
    
    def make_DoubleTapAgent(self):
        a =  Agent(("newDoubleTap",))
        a.owners.append(self)
        return a
        
    def __repr__(self):
        return self.name
