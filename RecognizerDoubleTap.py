#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Recognizer import Recognizer, newHypothesis
from Events import Event
from RecognizerTap import RecognizerTap
import Reactor
from Agent import Agent
import math

class RecognizerDoubleTap(Recognizer):
    allr = 0
    E_NewDoubleTap = Event()
    def __init__(self):
        RecognizerDoubleTap.allr += 1
        print "new RecognizerDoubleTap, we are",RecognizerDoubleTap.allr
        Recognizer.__init__(self)
        self.agent = Agent()
        self.events = (self.E_NewDoubleTap,)
        self.firstap = None
        self.secondtap = None
        self.register_event(RecognizerTap.E_NewTap,RecognizerDoubleTap.FirstTap)
        self.time = 0.5
        self.maxd = 10
        
    @newHypothesis
    def FirstTap(self,Tap):
        print "firsttap"
        self.firstap = Tap
        self.unregister_event(RecognizerTap.E_NewTap)
        self.register_event(RecognizerTap.E_NewTap,RecognizerDoubleTap.SecondTap)
        Reactor.schedule_after(self.time,self,RecognizerDoubleTap.timeout)
        self.acquire(Tap)
        return True
    
    @newHypothesis
    def SecondTap(self,Tap):
        print "secondtap"
        if self.dist(Tap.pos,self.firstap.pos) < self.maxd:
            self.secondtap = Tap
            self.unregister_event(RecognizerTap.E_NewTap)
            Reactor.cancel_schedule(self)
            self.acquire(Tap)
            self.complete()
            return True
    
    def timeout(self):
        print "dying..."
        self.fail()
    
    def execute(self):
        self.agent.pos = self.secondtap.pos
        self.E_NewDoubleTap.call(self.agent)
        self.fail()
    
    def __del__(self):
        RecognizerDoubleTap.allr -= 1
    
    def duplicate(self):
        d = RecognizerDoubleTap()
        Recognizer.copy_to(self,d)
        d.firstap = self.firstap
        d.secondtap = self.secondtap
        if not self.is_pristine():
            d.agent = self.agent
        return d
    
    @staticmethod
    def dist(a,b):
        dx,dy = (a[0]-b[0],a[1]-b[1])
        return math.sqrt(dx**2 + dy**2)
