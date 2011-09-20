#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tuio
from Recognizer import Recognizer, newHypothesis
from Agent import Agent
from Events import Event

class RecognizerPaint(Recognizer):
    allr = 0
    E_NewPaint = Event()
    E_Painting = Event()
    def __init__(self):
        self.finger = None
        RecognizerPaint.allr += 1
        print "new RecognizerPaint, we are", RecognizerPaint.allr
        Recognizer.__init__(self)
        self.cursorEvents = Tuio.TuioCursorEvents
        self.register_event(self.cursorEvents.newCursor,RecognizerPaint.EventNewCursor)
        self.agent = Agent()
        self.previousPoints = []
        self.events = ( self.E_NewPaint, self.E_Painting)
        
    @newHypothesis    
    def EventNewCursor(self,Cursor):
        if not self.finger:
            self.finger = Cursor
            self.unregister_event(self.cursorEvents.newCursor)
            self.register_event(self.cursorEvents.moveCursor,RecognizerPaint.EventMoveCursorTemporary)
            self.register_event(self.cursorEvents.removeCursor,RecognizerPaint.EventRemoveCursor)
            self.acquire(Cursor)
            self.complete()
            return True
    
    
    def EventMoveCursorTemporary(self, Cursor):
        if Cursor == self.finger:
            self.previousPoints.append(Cursor.pos)
        
    def execute(self):
        self.unregister_event(self.cursorEvents.moveCursor)
        self.register_event(self.cursorEvents.moveCursor,RecognizerPaint.EventMoveCursorConfirmed)
        self.agent.previousPoints = list(self.previousPoints)
        RecognizerPaint.E_NewPaint.call(self.agent)
        print "Start painting!"
        
    def EventMoveCursorConfirmed(self, Cursor):
        if Cursor == self.finger:
            self.agent.pos = Cursor.pos
            RecognizerPaint.E_Painting.call(self.agent)
            print "Painting",Cursor.pos
        
    def EventRemoveCursor(self, Cursor):
        if Cursor == self.finger:
            self.fail()
            
    def __del__(self):
        RecognizerPaint.allr -= 1
        
    def duplicate(self):
        d = RecognizerPaint()
        Recognizer.copy_to(self,d)
        d.finger = self.finger
        d.previousPoints = list(self.previousPoints)
        if not self.is_pristine():
            d.agent = self.agent
        return d
