#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Events import Event, EventClient
import Reactor

class Recognizer(EventClient):
    
    def __init__(self):
        EventClient.__init__(self)
        self.agentsAcquired = []
        self.agentsConfirmed = []
        #TODO: replace self.failed with self.died and self.failed to indicate different things?
        self.failed = False
        self.agent = None
    
    def finish(self):
        self.failed=True
        #we die but not fail
        assert(not self.agentsAcquired)
        for a in self.agentsConfirmed:
            #TODO: that shouldn't do discard, it should recover the agent for further use bu another Recognizer
            #using newAgent
            a.discard(self)
        self.unregister_all()
        
    def unregister_all(self):
        EventClient.unregister_all(self)
        Reactor.cancel_schedule(self)
    
    def fail(self):
        self.failed=True
        Reactor.run_after(lambda self=self: self._fail())
        
    def _fail(self):
        self.failed=True
        for a in self.agentsAcquired+self.agentsConfirmed:
            a.discard(self)
        self.agentsAcquired = []
        self.agentsConfirmed = []
        self.unregister_all()
        if self.agent:
            self.agent.fail()
            self.agent = None
    
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
        d.unregister_all()
        for a in self.agentsAcquired:
            d.acquire(a)
        EventClient.copy_to(self,d)
        Reactor.duplicate_instance(self,d)
    
    def is_pristine(self):
        return ( len(self.agentsAcquired) + len(self.agentsConfirmed) ) == 0
    
    def is_someone_interested(self):
        for f,i in self.newAgent.registered:
            if not isinstance(i,Recognizer):
                return True
            elif i.is_someone_interested():
                return True
        return False
    
    def fail_all_others(self):
        for a in self.agentsAcquired+self.agentsConfirmed:
            a.fail_all_others(self)
        
def newHypothesis(f):
    "Decorator to create a new hypothesis every time that is called"
    def newHipothesisAndRun(self,*args,**kwargs):
        if self.is_someone_interested():
            d = self.duplicate()
            f(self,*args,**kwargs)
        elif not self.is_pristine():
            self.fail()
    return newHipothesisAndRun
