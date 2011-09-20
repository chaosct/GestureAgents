#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Events import Event, EventClient
import Reactor

class Recognizer(EventClient):
    
    def __init__(self):
        EventClient.__init__(self)
        self.agentsAcquired = []
        self.agentsConfirmed = []
        self.failed = False
    
    def fail(self):
        Reactor.run_after(lambda: self._fail())
        
    def _fail(self):
        #if self.failed: return
        for a in self.agentsAcquired+self.agentsConfirmed:
            a.discard(self)
        self.agentsAcquired = []
        self.agentsConfirmed = []
        self.unregister_all()
        #force fail depending registers as they ar recognizing
        #unexisting agents
    
    def acquire(self,agent):
        if self.failed: return 
        if agent.acquire(self):
            self.agentsAcquired.append(agent)
        else:
            self.failed = True
            self.fail()
            
    def complete(self):
        if self.failed: return
        for a in self.agentsAcquired:
            a.complete(self)
            
    def confirm(self,agent):
        if self.failed: return
        self.agentsAcquired.remove(agent)
        self.agentsConfirmed.append(agent)
        if not self.agentsAcquired:
            self.execute()

    def copy_to(self,d):
        if self.failed: print "WARNING: copying a failed Recognizer!"
        if self.agentsConfirmed: print "WARNING: copying a Recognizer in confirmation!"
        for a in self.agentsAcquired:
            d.acquire(a)
        EventClient.copy_to(self,d)
        Reactor.duplicate_instance(self,d)
    
    def is_pristine(self):
        return ( len(self.agentsAcquired) + len(self.agentsConfirmed) ) == 0
    
    def is_someone_interested(self):
        for e in self.events:
            for f,i in e.registered:
                if not isinstance(i,Recognizer):
                    return True
                elif i.is_someone_interested():
                    return True
        return False
        
def newHypothesis(f):
    "Decorator to create a new hypothesis every time that is called"
    def newHipothesisAndRun(self,*args,**kwargs):
        if self.is_someone_interested():
            d = self.duplicate()
            f(self,*args,**kwargs):
        elif not self.is_pristine():
            self.fail()
    return newHipothesisAndRun
