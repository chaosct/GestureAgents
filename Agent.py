#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Reactor

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
    def __init__(self):
        self.recognizers_acquired = []
        self.recognizer_complete = None
        
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
        Reactor.run_after(lambda : self._complete(Recognizer) )
