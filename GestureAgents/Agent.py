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
    completion_policy = PolicyRuleset()
    def __init__(self,eventnames):
        "eventnames is a list of names that will become member events. finishAgent will allways be created."
        #TODO: newEvent when done
        self.recognizers_acquired = []
        self.recognizer_complete = None
        self.events = {}
        self.owners = []
        for ename in list(eventnames)+["finishAgent"]:
            self.events[ename]=Event()
            setattr(self,ename,self.events[ename])
        
    def acquire(self,Recognizer):
        if self.recognizer_complete and not self.recognizers_acquired:
            return False
        else:
            self.recognizers_acquired.append(Recognizer)
            return True
    
    def finish(self):
        "The owner of the event will not generate more events"
        self.finishAgent(self)
            
    def discard(self,Recognizer):
        #print "Agent discard", Recognizer
        if Recognizer == self.recognizer_complete:
            print "DISCARD"
            import traceback
            traceback.print_stack()
            self.recognizer_complete = None
            #print "WARNING: discarding a confirmed recognizer. That shouldn't happen"
        elif Recognizer in self.recognizers_acquired:
            self.recognizers_acquired.remove(Recognizer)
            if not self.recognizers_acquired and self.recognizer_complete:
                self.recognizer_complete.confirm(self)
        
    def _complete(self,Recognizer):
        assert(Recognizer is not self.recognizer_complete)
        # According to the policy we choose the best Recognizer
        print "CCC", self, type(Recognizer), type(self.recognizer_complete)
        if self.completion_policy.result(self.recognizer_complete,Recognizer) == False:
            #Policy doesn't accept change
            Recognizer.safe_fail()
            return
        elif self.recognizer_complete:
            self.recognizer_complete.safe_fail()
            print "COMPLETED BY SOMEONE"
            self.recognizer_complete = None
        
        self.recognizer_complete = Recognizer
        if Recognizer in self.recognizers_acquired:
            self.recognizers_acquired.remove(Recognizer)
        if not self.recognizers_acquired:
            self.recognizer_complete.confirm(self)
            
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
        from Recognizer import Recognizer
        l = set([r[1] for ename,event in self.events.iteritems() for r in event.registered])
        #print "Agent failed, killing %d things:" % len(l)
        for r in l:
            if isinstance(r,Recognizer):
                r.safe_fail()
    
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
def accept_if_none(recognizer1,recognizer2):
    "Accept First"
    if recognizer1 == None:
        return True
    
