#!/usr/bin/env python
# -*- coding: utf-8 -*-


#DEPRECATED!!

from Events import Event
from Agent import Agent
from pygame.locals import *

class MouseEvents:
    newCursor = Event()
    moveCursor = Event()
    removeCursor = Event()

class MouseAgentGenerator:
    def __init__(self):
        self.pressed = False
    def event(self,e):
        if e.type == MOUSEBUTTONDOWN:
            self.pressed = True
            self.myagent = Agent()
            self.myagent.pos = e.pos
            MouseEvents.newCursor.call(self.myagent)
        elif e.type == MOUSEBUTTONUP:
            self.pressed = False
            self.myagent.pos = e.pos
            MouseEvents.removeCursor.call(self.myagent)
            self.myagent = None
        elif e.type == MOUSEMOTION:
            if self.pressed:
                self.myagent.pos = e.pos
                MouseEvents.moveCursor.call(self.myagent)
