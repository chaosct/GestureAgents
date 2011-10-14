#!/usr/bin/env python
# -*- coding: utf-8 -*-


from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Events import Event
from GestureAgents.Tuio import TuioCursorEvents
from GestureAgents.Agent import Agent


class RecognizerMoveZoom(Recognizer):
    newAgent = Event()
    def __init__(self):
        Recognizer.__init__(self)
        self.register_event(TuioCursorEvents.newAgent,RecognizerMoveZoom.EventnewAgent)
        self.cursor1 = None
        self.cursor1pos = None
    
    @newHypothesis
    def EventnewAgent(self,Cursor):
        self.agent = self.makeAgentMoveZoom()
        self.agent.pos = Cursor.pos
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail()
        self.unregister_all()
        self.register_event(Cursor.newCursor,RecognizerMoveZoom.EventNewCursor)
    
    def EventNewCursor(self,Cursor):
        self.cursor1 = Cursor
        self.acquire(self.cursor1)
        self.complete()
        
    def execute(self):
        self.register_event(self.cursor1.updateCursor,RecognizerMoveZoom.EventUpdateCursor)
        self.register_event(self.cursor1.removeCursor,RecognizerMoveZoom.EventRemoveCursor)
        self.cursor1pos = self.cursor1.pos
        self.agent.newMoveZoom(self.agent)
    
    def EventUpdateCursor(self,Cursor):
        #for now we translate
        dx = Cursor.pos[0]-self.cursor1pos[0]
        dy = Cursor.pos[1]-self.cursor1pos[1]
        self.agent.translation = (dx,dy)
        self.agent.newTranslation(self.agent)
        self.cursor1pos = Cursor.pos
    
    def EventRemoveCursor(self,Cursor):
        self.cursor1 = None
        self.agent.endMoveZoom(self.agent)
        self.finish()
    
    def makeAgentMoveZoom(self):
        events = ("newMoveZoom","newTranslation","newZoom","newRotation","endMoveZoom")
        a = Agent(events)
        a.owners.append(self)
        return a
    
    def duplicate(self):
        d = RecognizerMoveZoom()
        Recognizer.copy_to(self,d)
        d.cursor1 = self.cursor1
        d.cursor1pos = self.cursor1pos
        return d
