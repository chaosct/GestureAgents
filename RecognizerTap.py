#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tuio
from Recognizer import Recognizer, newHypothesis
from Events import Event
from Agent import Agent
import math
import Reactor

class RecognizerTap(Recognizer):
    #for debugging porpuses we have a count of instances
    newAgent = Event()
    def __init__(self):
        self.finger = None
        Recognizer.__init__(self)
        self.cursorEvents = Tuio.TuioCursorEvents
        self.register_event(self.cursorEvents.newAgent,RecognizerTap.EventNewAgent)
        self.maxd = 10
        self.time = 0.5
        self.origin = None
    
    @newHypothesis
    def EventNewAgent(self,Cursor):
        # Am I interested on this Agent?
        # We don't want recycled Agents
        if Cursor.ontable:
            self.fail()
        # Let's ask our subscribbers
        self.agent = self.make_TapAgent()
        self.agent.pos = Cursor.pos
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail()
        else:
            self.unregister_event(self.cursorEvents.newAgent)
            self.register_event(Cursor.newCursor,RecognizerTap.EventNewCursor)
        
    def EventNewCursor(self,Cursor):
        self.finger = Cursor
        self.unregister_event(Cursor.newCursor)
        self.register_event(Cursor.updateCursor,RecognizerTap.EventMoveCursor)
        self.register_event(Cursor.removeCursor,RecognizerTap.EventRemoveCursor)
        Reactor.schedule_after(self.time,self,RecognizerTap.fail)
        self.origin = Cursor.pos
        self.acquire(Cursor)

    
    def EventMoveCursor(self,Cursor):
        if self.dist(Cursor.pos,self.origin) > self.maxd:
            self.fail()
    
    def EventRemoveCursor(self,Cursor):
        Reactor.cancel_schedule(self)
        self.unregister_event(Cursor.updateCursor)
        self.unregister_event(Cursor.removeCursor)
        self.complete()
            
    def execute(self):
        self.agent.pos = self.origin
        self.agent.newTap.call(self.agent)
        print "Tap!"
        self.finish()
    
    @staticmethod
    def dist(a,b):
        dx,dy = (a[0]-b[0],a[1]-b[1])
        return math.sqrt(dx**2 + dy**2)
    
    def duplicate(self):
        d = RecognizerTap()
        Recognizer.copy_to(self,d)
        d.finger = self.finger
        d.origin = self.origin
        #if not self.is_pristine():
        d.agent = self.agent
        return d
        
    @staticmethod
    def make_TapAgent():
        return Agent(("newTap",))
