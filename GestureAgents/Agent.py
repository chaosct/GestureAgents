#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Reactor
from Events import Event
from Policy import PolicyRuleset



class Agent:
    """This class represents something that generates Events.
    
    When receiving an event with an Agent associated,
    call acquire to show your interest. If you are an 
    application, you may call complete directly.
    
    If you are a recognizer call complete when you have
    fully recognized a gesture. For symbolic gestures 
    this means at the end of the recognition. For continuous
    gestures, you may call complete directly instead of
    acquire, as you know that anything is ypur gesture.
    
    Whenever you feel that you don't need this agent
    anymore, call discard AS EARLY AS POSSIBLE.
    
    Recognizers must call these through their own helpers
    in the class Recognizer.
    """
    #Policy on whenever a confirmed recognizer can be failed by a new recognizer confirming
    completion_policy = PolicyRuleset()
    #Policy on whenever one gesture can be confirmed while another can be aquired (for instance when a continuous gesture can
    #finish another gesture to complete.
    compatibility_policy = PolicyRuleset()
    
    def __init__(self,eventnames,creator):
        """eventnames is a list of names that will become member events.
        creator is a class or instance with newAgent event to be called when recycling this agent."""
        self.recognizers_acquired = []
        self.recognizer_complete = None
        self.events = {}
        self.owners = []
        self.newAgent = creator.newAgent
        #is this agent having a confirmed recognizer?
        self.completed = False
        #is this agent recycled?
        self.recycled = False
        self.finished = False
        for ename in list(eventnames)+["finishAgent"]:
            self.events[ename]=Event()
            setattr(self,ename,self.events[ename])
        
    def acquire(self,Recognizer):
        "The recognizer is interested on this agent"
        #can we acquire even if there is someone confirmed?
        if self.completed and self.compatibility_policy.result(self.recognizer_complete,Recognizer) != True:
            return False
        else:
            self.recognizers_acquired.append(Recognizer)
            return True
    
    def finish(self):
        "The owner of the event will not generate more events"
        self.finishAgent(self)
            
    def discard(self,Recognizer):
        """The recognizer is no longer interested in this agent.
        This should occur after acquiring the agent. If it happens
        after confirming, the agent will be recycled."""
        if Recognizer == self.recognizer_complete:
            print "DISCARD"
            import traceback
            #traceback.print_stack()
            self.recognizer_complete = None
            if self.completed and not self.finished:
                self.completed = False
                self.recycled = True
                print "Recycling!:",type(Recognizer)
                for r in self._get_recognizers_subscribed():
                    r.safe_fail()
                self.newAgent(self)
                
            #print "WARNING: discarding a confirmed recognizer. That shouldn't happen"
        elif Recognizer in self.recognizers_acquired:
            self.recognizers_acquired.remove(Recognizer)
            if self._can_confirm():
                self.recognizer_complete.confirm(self)
                self.completed = True
        
    
    def _can_confirm(self):
        "Decides if self.recognizer_complete can be confirmed"
        if not self.recognizer_complete: return False
        if self.completed: return False
        if not self.recognizers_acquired: return True
        for r in self.recognizers_acquired:
            if self.compatibility_policy.result(self.recognizer_complete,r) != True \
            and self.compatibility_policy.result(r, self.recognizer_complete) != True:
                return False
        return True
        
    def _complete(self,Recognizer):
        assert(Recognizer is not self.recognizer_complete)
        # According to the policy we choose the best Recognizer
        #print "CCC", self, type(Recognizer), type(self.recognizer_complete)
        if self.completion_policy.result(self.recognizer_complete,Recognizer) == False:
            #Policy doesn't accept change
            Recognizer.safe_fail()
            return
        elif self.recognizer_complete:
            self.recognizer_complete.safe_fail("Displaced by another recognizer: "+str(Recognizer))
            self.recognizer_complete = None
            self.completed = False
        
        self.recognizer_complete = Recognizer
        if Recognizer in self.recognizers_acquired:
            self.recognizers_acquired.remove(Recognizer)
        #According to the policy we remove acquisitions
        if self._can_confirm():
            self.recognizer_complete.confirm(self)
            self.completed = True
            
    def complete(self,Recognizer):
        assert(Recognizer in self.recognizers_acquired)
        Reactor.run_after(lambda Recognizer=Recognizer, self=self: self._complete(Recognizer) )
    
    def is_someone_subscribed(self):
        for ename,event in self.events.iteritems():
            if event.registered:
                return True
        return False
    
    def fail(self):
        "The Recognizer owner of this agent fails before really existing, so All the recognizers based on it must fail"
        if self.finished: return
        for r in self._get_recognizers_subscribed():
            r.safe_fail()
    
    def _get_recognizers_subscribed(self):
        from Recognizer import Recognizer
        return [r for r in set([r[1] for ename,event in self.events.iteritems() for r in event.registered]) if isinstance(r,Recognizer)]
    
    def fail_all_others(self,winner):
        Reactor.run_after(lambda winner=winner,self=self: self._fail_all_others(winner))
                
    def _fail_all_others(self,winner):
        #assert(self.recognizer_complete is winner) we are all consenting adults here
        target = type(winner)
        #print "fail_all_others :",winner,"wants to fail",target
        for r in list(self.recognizers_acquired):
            if type(r) == target and r is not winner:
                #print "fail_all_others by",winner,":", r, "is target"
                r.safe_fail(cause="Fail all others by %s"%str(winner))
            else:
                #print "fail_all_others :", r, "is not target"
                pass
        

#default policies

@Agent.completion_policy.rule(-100)
def _accept_if_none(recognizer1,recognizer2):
    "Accept First"
    if recognizer1 == None:
        return True

@Agent.completion_policy.rule(-99)
def _accept_if_compatible(recognizer1,recognizer2):
    "Use compatibility_policy to accept completion one over another"
    if Agent.compatibility_policy.result(recognizer1,recognizer2) == True:
        return True
    
@Agent.compatibility_policy.rule(100)
def _never_accept(recognizer_confirmed,recognizer_acquiring):
    "Never accept acquire when confirmed"
    return False
