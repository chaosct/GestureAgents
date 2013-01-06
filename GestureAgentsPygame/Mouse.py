#!/usr/bin/env python
# -*- coding: utf-8 -*-


from GestureAgentsTUIO.Tuio import TuioAgentGenerator
import GestureAgentsPygame.Screen as Screen

from pygame.locals import *


class MouseAsTuioAgentGenerator(object):
    def __init__(self):
        self.pressed = False
        self.myagent = None
        self.sid = -1
        self.screensize = Screen.size

    def event(self, e):
        if e.type == MOUSEBUTTONDOWN:
            self.pressed = True
            self.myagent = TuioAgentGenerator.makeCursorAgent()
            self._updateAgent(self.myagent, e)
            self.myagent.newAgent(self.myagent)
            self.myagent.newCursor(self.myagent)
        elif e.type == MOUSEBUTTONUP:
            self.pressed = False
            self._updateAgent(self.myagent, e)
            self.myagent.removeCursor(self.myagent)
            self.myagent.finish()
            self.myagent = None
        elif e.type == MOUSEMOTION:
            if self.pressed:
                self._updateAgent(self.myagent, e)
                self.myagent.updateCursor(self.myagent)

    def _updateAgent(self, a, e):
        a.pos = e.pos
        a.posx = e.pos[0]
        a.posy = e.pos[1]
        a.sessionid = self.sid
        a.xmot = 0
        a.ymot = 0
        a.mot_accel = 0
