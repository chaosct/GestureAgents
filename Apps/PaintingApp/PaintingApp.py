#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame.locals
import pygame.draw
import random, math
import sys
sys.path.append('../..')

import GestureAgents.Screen
from GestureAgents.Gestures import RecognizerStick, RecognizerPaint, RecognizerDoubleTap, RecognizerTap
from GestureAgents.AppRecognizer import AppRecognizer
import GestureAgents.Render

class PaintingApp:
    def __init__(self):
        GestureAgents.Screen.ScreenDraw.register(PaintingApp.draw,self)
        self.surface = pygame.Surface(GestureAgents.Screen.size,flags=pygame.locals.SRCALPHA)
        #pygame.draw.line(self.surface, (255,255,255) , (50,50), (100,100), 5)
        AppRecognizer(RecognizerStick).newAgent.register(PaintingApp.newAgentStick,self)
        AppRecognizer(RecognizerPaint).newAgent.register(PaintingApp.newAgentPaint,self)
        AppRecognizer(RecognizerDoubleTap).newAgent.register(PaintingApp.newAgentDoubleTap,self)
        AppRecognizer(RecognizerTap).newAgent.register(PaintingApp.newAgentTap,self)
        self.button = (400,400)
        self.buttoncolor = (0,100,255)
    
    def newAgentDoubleTap(self,agent):
        #context here
        if self.dist(agent.pos,self.button) < 50:
            agent.newDoubleTap.register(PaintingApp.event_new_dtap,self)
    
    def newAgentTap(self,agent):
        agent.newTap.register(PaintingApp.event_new_tap,self)
        
    def newAgentPaint(self,agent):
        #context here
        agent.newPaint.register(PaintingApp.event_new_paint,self)
        agent.updatePaint.register(PaintingApp.event_painting,self)
    
    def newAgentStick(self,agent):
        #context here
        agent.newStick.register(PaintingApp.event_finish_stick,self)
    
    def draw(self):
        pygame.draw.circle(self.surface, self.buttoncolor , self.button , 50, 3)
        GestureAgents.Render.drawT(self.surface)
        
        
    def event_finish_stick(self,Stick):
        pygame.draw.line(self.surface, (255,255,255) , Stick.pos1, Stick.pos2, 5)
    
    def event_painting(self,Point):
        pygame.draw.circle(self.surface, (255,100,100) , map(int,Point.pos), 10, 0)
    
    def event_new_paint(self,Paint):
        for p in Paint.previousPoints:
            pygame.draw.circle(self.surface, (255,100,100) , map(int,p), 10, 0)
    
    def event_new_dtap(self,Tap):
        #pygame.draw.circle(self.surface, (0,255,100) , map(int,Tap.pos), 10, 0)
        self.buttoncolor = [random.randint(0,255) for i in self.buttoncolor]
        self.surface.fill(0)
    
    def event_new_tap(self,Tap):
        pygame.draw.circle(self.surface, (0,100,200) , map(int,Tap.pos), 10, 0)
        
    @staticmethod
    def dist(a,b):
        dx,dy = (a[0]-b[0],a[1]-b[1])
        return math.sqrt(dx**2 + dy**2)
        
if __name__ == "__main__":
    import GestureAgents
    app = PaintingApp()
    GestureAgents.run_apps()
