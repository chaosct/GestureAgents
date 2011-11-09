#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Events import Event, EventClient
import Reactor

class RecognizerFailedException(Exception):
    pass

class Recognizer(EventClient):
    
    def __init__(self):
        EventClient.__init__(self)
        self.agentsAcquired = []
        self.agentsConfirmed = []
        #TODO: replace self.failed with self.died and self.failed to indicate different things?
        self.failed = False
        self.agent = None
        self.executed = False
        #self.parent = False
    
    def finish(self):
        assert(self.failed==False)
        self.failed=True
        self.unregister_all()
        #we die but not fail
        assert(not self.agentsAcquired)
        for a in self.agentsConfirmed:
            a.discard(self)
        self.agent.owners.remove(self) #removing a complex reference cycle preventing gc
        self.agent.finish()
        
    def unregister_all(self):
        EventClient.unregister_all(self)
        Reactor.cancel_schedule(self)
    
    #def fail(self):
    #    self.failed=True
    #    Reactor.run_after(lambda self=self: self._fail())
        
    def fail(self,cause="Unknown"):
        assert(self.failed==False)
        self.failed=True
        for a in self.agentsAcquired+self.agentsConfirmed:
            a.discard(self)
        self.agentsAcquired = []
        self.agentsConfirmed = []
        self.unregister_all()
        # we have to fail only if we are the solely owner of self.agent.
        if self.agent:
            self.agent.owners.remove(self)
            if not self.agent.owners:
                self.agent.fail()
            self.agent = None
        raise RecognizerFailedException()
    
    def acquire(self,agent):
        #TODO: define a way to release agents also
        if self.failed: return 
        if agent.acquire(self):
            self.agentsAcquired.append(agent)
        else:
            self.fail("Acquire failed")
            
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
            self.executed = True
        
    def copy_to(self,d):
        if self.failed: print "WARNING: copying a failed Recognizer!"
        if self.agentsConfirmed and not self.executed: print "WARNING: copying a Recognizer in confirmation!"
        d.unregister_all()
        for a in self.agentsAcquired:
            d.acquire(a)
        EventClient.copy_to(self,d)
        Reactor.duplicate_instance(self,d)
        #we duplicate agents
        if self.agent:
            d.agent = self.agent
            self.agent.owners.append(d)
        d.executed = self.executed
        #d.parent = self.parent
    
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
    
    def safe_fail(self,cause="Unknown"):
        try:
            self.fail(cause=cause)
        except RecognizerFailedException:
            pass
    
    def expire_in(self,s):
        l = lambda self: self.safe_fail(cause="Timeout")
        Reactor.schedule_after(s,self,l)
    
    def cancel_expire(self):
        Reactor.cancel_schedule(self)
        
def newHypothesis(f):
    "Decorator to create a new hypothesis every time that is called"
    def newHipothesisAndRun(self,*args,**kwargs):
        if self.is_someone_interested():
            d = self.duplicate()
            #self.parent = d
            f(self,*args,**kwargs)
        elif not self.is_pristine():
            self.safe_fail("Noone interested")
    return newHipothesisAndRun
    
    
from Agent import Agent
#policies for comparison between Recognizers

@Agent.completion_policy.rule(100)
def last_to_enter_wins(recognizer1,recognizer2):
    "Last to enter wins"
    return True

@Agent.completion_policy.rule(-50)
def completed_win(recognizer1,recognizer2):
    "Completed win"
    if recognizer1.executed and not recognizer2.executed:
        return False
    if not recognizer1.executed and recognizer2.executed:
        return True

@Agent.completion_policy.rule(-49)
def completed_win(recognizer1,recognizer2):
    "Wins the recognizer with more agents"
    la1 = len(recognizer1.agentsAcquired)
    lr1 = len(recognizer1.agentsConfirmed)
    la2 = len(recognizer2.agentsAcquired)
    lr2 = len(recognizer2.agentsConfirmed)
    if la1+lr1 > la2+lr2:
        return False
    elif la1+lr1 < la2+lr2:
        return True

