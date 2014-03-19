#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import pygame
import pygame.locals
import pygame.draw
import random
import math
#import sys
#sys.path.append('../..')

import GestureAgentsPygame.Screen as Screen
from GestureAgentsTUIO.Gestures2D.RecognizerStick import RecognizerStick
from GestureAgentsTUIO.Gestures2D.RecognizerDoubleTap import RecognizerDoubleTap
from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap
from GestureAgents.AppRecognizer import AppRecognizer
import GestureAgentsPygame.Render as Render
from GestureAgentsTUIO.Tuio import TuioCursorEvents


class ErasingApp:
    def __init__(self,system):
        Screen.ScreenDraw.register(ErasingApp.draw, self)
        AppRecognizer(system, RecognizerDoubleTap).newAgent.register(
            ErasingApp.newAgentDoubleTap, self)
        self.button = (400, 400)
        self.buttoncolor = (0, 100, 255)
        self.buttonrad = 50
        self.surface = PaintingApp.instance.surface
        
    def newAgentDoubleTap(self, agent):
        #context here
        if self.dist(agent.pos, self.button) < self.buttonrad:
            agent.newDoubleTap.register(ErasingApp.event_new_dtap, self)

    def event_new_dtap(self, Tap):
        #pygame.draw.circle(self.surface, (0,255,100) , map(int,Tap.pos), 10, 0)
        self.buttoncolor = [random.randint(100, 255) for _ in self.buttoncolor]
        self.surface.fill(0)

    def draw(self):
        pygame.draw.circle(
            self.surface, self.buttoncolor, self.button, self.buttonrad, 3)

    @staticmethod
    def dist(a, b):
        dx, dy = (a[0] - b[0], a[1] - b[1])
        return math.sqrt(dx ** 2 + dy ** 2)


class PaintingApp:
    def __init__(self, system):
        PaintingApp.instance = self
        Screen.ScreenDraw.register(PaintingApp.draw, self)
        self.surface = pygame.Surface(
            Screen.size, flags=pygame.locals.SRCALPHA)
        AppRecognizer(system, RecognizerStick).newAgent.register(
            PaintingApp.newAgentStick, self)
        AppRecognizer(system, TuioCursorEvents).newAgent.register(
            PaintingApp.newAgentPaint, self)
        AppRecognizer(system,
            RecognizerTap).newAgent.register(PaintingApp.newAgentTap, self)

    def newAgentTap(self, agent):
        agent.newTap.register(PaintingApp.event_new_tap, self)

    def newAgentPaint(self, agent):
        #context here
        agent.updateCursor.register(PaintingApp.event_painting, self)

    def newAgentStick(self, agent):
        #context here
        agent.newStick.register(PaintingApp.event_finish_stick, self)

    def draw(self):
        Render.drawT(self.surface)

    def event_finish_stick(self, Stick):
        pygame.draw.line(
            self.surface, (255, 255, 255), Stick.pos1, Stick.pos2, 5)

    def event_painting(self, Point):
        pygame.draw.circle(
            self.surface, (255, 100, 100), map(int, Point.pos), 10, 0)

    def event_new_tap(self, Tap):
        pygame.draw.circle(
            self.surface, (0, 100, 200), map(int, Tap.pos), 10, 0)

if __name__ == "__main__":
    from GestureAgentsPygame import System
    s = System()
    app = PaintingApp(s)
    app2 = ErasingApp(s)
    s.run_apps()
