#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Reactor
from Events import Event
from Recognizer import Recognizer

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
    def __init__(self,eventnames):
        "eventnames is a list of names that will become member events"
        #TODO: newEvent when done
        self.recognizers_acquired = []
        self.recognizer_complete = None
        self.events = {}
        for ename in eventnames:
            self.events[ename]=Event()
            setattr(self,ename,self.events[ename])
        
    def acquire(self,Recognizer):
        #print "Agent acquire", Recognizer
        if self.recognizer_complete and not self.recognizers_acquired:
            return False
        else:
            self.recognizers_acquired.append(Recognizer)
            return True
            
    def discard(self,Recognizer):
        #print "Agent discard", Recognizer
        if Recognizer == self.recognizer_complete:
            self.recognizer_complete = None
            #print "WARNING: discarding a confirmed recognizer. That shouldn't happen"
        elif Recognizer in self.recognizers_acquired:
            self.recognizers_acquired.remove(Recognizer)
            if not self.recognizers_acquired and self.recognizer_complete:
                self.recognizer_complete.confirm(self)
        
    def _complete(self,Recognizer):
        #print "Agent complete", Recognizer
        if self.recognizer_complete:
            #which one is preferable?
            self.recognizer_complete.fail()
            self.recognizer_complete = None
        self.recognizer_complete = Recognizer
        if Recognizer in self.recognizers_acquired:
            self.recognizers_acquired.remove(Recognizer)
        if not self.recognizers_acquired:
            self.recognizer_complete.confirm(self)
            
    def complete(self,Recognizer):
        if Recognizer not in self.recognizers_acquired:
            if not self.acquire(Recognizer): return
        Reactor.run_after(lambda Recognizer=Recognizer, self=self: self._complete(Recognizer) )
    
    def is_someone_subscribed(self):
        for ename,event in self.events.iteritems():
            if event.registered:
                return True
        return False
    
    def fail(self):
        "The Recognizer owner of this agent fails before really existing, so All the recognizers based on it must fail"
        l = set([r for ename,event in self.events.iteritems() for r in event.registered])
        print "Agent failed, killing %d things" % len(l)
        for r in l:
            if isinstance(r,Recognizer):
                r.fail()
    
    def fail_all_others(self,winner):
        Reactor.run_after(lambda winner=winner,self=self: self._fail_all_others(winner))
                
    def _fail_all_others(self,winner):
        #assert(self.recognizer_complete is winner) we are all consenting adults here
        target = type(winner)
        for r in list(self.recognizers_acquired):
            if type(r) == target and r is not winner:
                r.fail()
        
        
