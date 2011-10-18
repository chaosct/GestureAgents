#!/usr/bin/env python
# -*- coding: utf-8 -*-


from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Events import Event
from GestureAgents.Tuio import TuioCursorEvents
from GestureAgents.Agent import Agent
import math

class RecognizerZoomRotate(Recognizer):
    newAgent = Event()
    def __init__(self):
        Recognizer.__init__(self)
        self.register_event(TuioCursorEvents.newAgent,RecognizerZoomRotate.EventnewAgent1)
        self.cursor1 = None
        self.cursor1pos = None
        self.cursor2 = None
        self.cursor2pos = None
        
    @newHypothesis
    def EventnewAgent1(self,Cursor):
        self.agent = self.makeAgentZoomRotate()
        self.agent.pos1 = Cursor.pos
        self.agent.pos2 = Cursor.pos
        self.agent.pos = self.agent.pos1
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail()
        self.unregister_all()
        self.register_event(Cursor.newCursor,RecognizerZoomRotate.EventNewCursor1)
    
    def EventNewCursor1(self,Cursor):
        self.cursor1 = Cursor
        self.acquire(self.cursor1)
        self.register_event(TuioCursorEvents.newAgent,RecognizerZoomRotate.EventnewAgent2)
        self.register_event(self.cursor1.removeCursor,RecognizerZoomRotate.EventRemoveCursorpre)
        
    @newHypothesis
    def EventnewAgent2(self,Cursor):
        self.agent.pos1 = self.cursor1.pos
        self.agent.pos2 = Cursor.pos
        self.agent.pos = self.agent.pos2
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail()
        self.unregister_all()
        self.register_event(Cursor.newCursor,RecognizerZoomRotate.EventNewCursor2) 
        
    def EventNewCursor2(self,Cursor):
        self.cursor2 = Cursor
        self.acquire(self.cursor2)
        self.register_event(self.cursor2.removeCursor,RecognizerZoomRotate.EventRemoveCursorpre)
        self.complete()
        self.fail_all_others()
        
    def execute(self):
        self.unregister_all()
        self.register_event(self.cursor1.updateCursor,RecognizerZoomRotate.EventUpdateCursor)
        self.register_event(self.cursor2.updateCursor,RecognizerZoomRotate.EventUpdateCursor)
        self.register_event(self.cursor1.removeCursor,RecognizerZoomRotate.EventRemoveCursor)
        self.register_event(self.cursor2.removeCursor,RecognizerZoomRotate.EventRemoveCursor)
        self.cursor1pos = self.cursor1.pos
        self.cursor2pos = self.cursor2.pos
        self.agent.pos1 = self.cursor1pos
        self.agent.pos2 = self.cursor2pos
        self.agent.newZoomRotate(self.agent)
    
    def EventRemoveCursorpre(self,Cursor):
        self.cursor1 = None
        self.cursor2 = None
        self.fail()
    
    def EventUpdateCursor(self,Cursor):
        cursor1npos = self.cursor1pos
        cursor2npos = self.cursor2pos
        if Cursor == self.cursor1:
            cursor1npos = Cursor.pos
            self.agent.pivot = cursor2npos
        elif Cursor == self.cursor2:
            cursor2npos = Cursor.pos
            self.agent.pivot = cursor1npos
        dx,dy = [self.cursor2pos[n] - self.cursor1pos[n] for n in (0,1)]
        ndx,ndy = [cursor2npos[n] - cursor1npos[n] for n in (0,1)]
        a = math.atan2(dy,dx)
        na = math.atan2(ndy,ndx)
        dist = math.sqrt(dx*dx+dy*dy)
        ndist = math.sqrt(ndx*ndx+ndy*ndy)
        
        
        self.agent.rotation = (na-a)
        self.agent.scale = (ndist/dist)
        
        self.agent.newRotation(self.agent)
        self.agent.newScale(self.agent)
        
        self.cursor1pos = cursor1npos
        self.cursor2pos = cursor2npos
    
    def EventRemoveCursor(self,Cursor):
        self.cursor1 = None
        self.cursor2 = None
        self.agent.endZoomRotate(self.agent)
        self.finish()
    
    def makeAgentZoomRotate(self):
        events = ("newZoomRotate","newRotation","newScale","endZoomRotate")
        a = Agent(events)
        a.owners.append(self)
        return a
    
    def duplicate(self):
        d = RecognizerZoomRotate()
        Recognizer.copy_to(self,d)
        d.cursor1 = self.cursor1
        d.cursor1pos = self.cursor1pos
        d.cursor2 = self.cursor2
        d.cursor2pos = self.cursor2pos
        return d
