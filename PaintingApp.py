#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Screen
import pygame
import pygame.locals
import pygame.draw
from RecognizerStick import RecognizerStick
from RecognizerPaint import RecognizerPaint
from RecognizerDoubleTap import RecognizerDoubleTap

class PaintingApp:
    def __init__(self,screen):
        Screen.ScreenDraw.register(PaintingApp.draw,self)
        self.surface = pygame.Surface(Screen.size,flags=pygame.locals.SRCALPHA)
        self.screen = screen
        #pygame.draw.line(self.surface, (255,255,255) , (50,50), (100,100), 5)
        RecognizerStick.newAgent.register(PaintingApp.newAgentStick,self)
        RecognizerPaint.newAgent.register(PaintingApp.newAgentPaint,self)
        RecognizerDoubleTap.newAgent.register(PaintingApp.newAgentDoubleTap,self)
    
    def newAgentDoubleTap(self,agent):
        #context here
        agent.newDoubleTap.register(PaintingApp.event_new_tap,self)
        
    def newAgentPaint(self,agent):
        #context here
        agent.newPaint.register(PaintingApp.event_new_paint,self)
        agent.updatePaint.register(PaintingApp.event_painting,self)
    
    def newAgentStick(self,agent):
        #context here
        agent.newStick.register(PaintingApp.event_finish_stick,self)
    
    def draw(self):
        self.screen.blit(self.surface,(0,0))
        
    def event_finish_stick(self,Stick):
        pygame.draw.line(self.surface, (255,255,255) , Stick.pos1, Stick.pos2, 5)
    
    def event_painting(self,Point):
        pygame.draw.circle(self.surface, (255,100,100) , map(int,Point.pos), 10, 0)
    
    def event_new_paint(self,Paint):
        for p in Paint.previousPoints:
            pygame.draw.circle(self.surface, (255,100,100) , map(int,p), 10, 0)
    
    def event_new_tap(self,Tap):
        pygame.draw.circle(self.surface, (0,255,100) , map(int,Tap.pos), 10, 0)
