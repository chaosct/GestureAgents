#!/usr/bin/env python
# -*- coding: utf-8 -*-


from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Events import Event
from GestureAgents.Tuio import TuioCursorEvents
from GestureAgents.Agent import Agent


class RecognizerMove(Recognizer):
    newAgent = Event()
    def __init__(self):
        Recognizer.__init__(self)
        self.register_event(TuioCursorEvents.newAgent,RecognizerMove.EventnewAgent)
        self.cursor = None
        self.cursorpos = None
    
    @newHypothesis
    def EventnewAgent(self,Cursor):
        self.agent = self.makeAgentMove()
        self.agent.pos = Cursor.pos
        self.newAgent(self.agent)
        if not self.agent.is_someone_subscribed():
            self.fail("Noone interested")
        self.unregister_all()
        if Cursor.recycled:
            self.register_event(Cursor.finishAgent,RecognizerMove.EventRecycledFail)
            self.EventNewCursor(Cursor)
        else:
            self.register_event(Cursor.newCursor,RecognizerMove.EventNewCursor)
    
    def EventRecycledFail(self,Cursor):
        self.fail("Zombie event")
    
    def EventNewCursor(self,Cursor):
        self.cursor = Cursor
        self.acquire(self.cursor)
        self.complete()
        
    def execute(self):
        self.register_event(self.cursor.updateCursor,RecognizerMove.EventUpdateCursor)
        self.register_event(self.cursor.removeCursor,RecognizerMove.EventRemoveCursor)
        self.cursorpos = self.cursor.pos
        self.agent.newMove(self.agent)
    
    def EventUpdateCursor(self,Cursor):
        dx = Cursor.pos[0]-self.cursorpos[0]
        dy = Cursor.pos[1]-self.cursorpos[1]
        self.agent.translation = (dx,dy)
        self.agent.newTranslation(self.agent)
        self.cursorpos = Cursor.pos
    
    def EventRemoveCursor(self,Cursor):
        self.cursor = None
        self.agent.endMove(self.agent)
        self.finish()
    
    def makeAgentMove(self):
        events = ("newMove","newTranslation","endMove")
        a = Agent(events,self)
        a.owners.append(self)
        return a
    
    def duplicate(self):
        d = RecognizerMove()
        Recognizer.copy_to(self,d)
        d.cursor = self.cursor
        d.cursorpos = self.cursorpos
        return d
