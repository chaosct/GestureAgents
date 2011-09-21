#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tuio
from Recognizer import Recognizer, newHypothesis
from Agent import Agent
from Events import Event

class RecognizerPaint(Recognizer):
    allr = 0
    newAgent = Event()
    def __init__(self):
        self.finger = None
        RecognizerPaint.allr += 1
        print "new RecognizerPaint, we are", RecognizerPaint.allr
        Recognizer.__init__(self)
        self.cursorEvents = Tuio.TuioCursorEvents
        self.register_event(self.cursorEvents.newAgent,RecognizerPaint.EventNewAgent)
        self.previousPoints = []
        self.confirmed = False
        
    @newHypothesis
    def EventNewAgent(self,Cursor):
        if Cursor.ontable:
            self.fail()
        self.agent = self.make_PaintAgent()
        self.agent.pos = Cursor.pos
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail()
        else:
            self.unregister_event(self.cursorEvents.newAgent)
            self.register_event(Cursor.newCursor,RecognizerPaint.EventNewCursor)
        
          
    def EventNewCursor(self,Cursor):
        self.finger = Cursor
        self.unregister_event(Cursor.newCursor)
        self.register_event(Cursor.updateCursor,RecognizerPaint.EventMoveCursorTemporary)
        self.register_event(Cursor.removeCursor,RecognizerPaint.EventRemoveCursor)
        self.acquire(Cursor)
        self.complete()
    
    
    def EventMoveCursorTemporary(self, Cursor):
        self.previousPoints.append(Cursor.pos)
        
    def execute(self):
        self.confirmed = True
        self.unregister_event(self.finger.updateCursor)
        self.register_event(self.finger.updateCursor,RecognizerPaint.EventMoveCursorConfirmed)
        self.agent.previousPoints = list(self.previousPoints)
        self.agent.newPaint(self.agent)
        print "Start painting!"
        
    def EventMoveCursorConfirmed(self, Cursor):
        self.agent.pos = Cursor.pos
        self.agent.updatePaint(self.agent)
        #print "Painting",Cursor.pos
        
    def EventRemoveCursor(self, Cursor):
        if not self.confirmed:
            self.fail()
        else:
            self.finish()
            
    def __del__(self):
        RecognizerPaint.allr -= 1
        
    def duplicate(self):
        d = RecognizerPaint()
        Recognizer.copy_to(self,d)
        d.finger = self.finger
        d.previousPoints = list(self.previousPoints)
        #if not self.is_pristine():
        d.agent = self.agent
        return d
    
    @staticmethod
    def make_PaintAgent():
        return Agent(("newPaint","updatePaint"))
