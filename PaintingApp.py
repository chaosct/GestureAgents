#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Screen
import pygame
import pygame.locals
import pygame.draw
from RecognizerStick import RecognizerStick
from RecognizerPaint import RecognizerPaint

class PaintingApp:
    def __init__(self,screen):
        Screen.ScreenDraw.register(PaintingApp.draw,self)
        self.surface = pygame.Surface(Screen.size,flags=pygame.locals.SRCALPHA)
        self.screen = screen
        #pygame.draw.line(self.surface, (255,255,255) , (50,50), (100,100), 5)
        RecognizerStick.E_finishStick.register(PaintingApp.event_finish_stick,self)
        RecognizerPaint.E_Painting.register(PaintingApp.event_painting,self)
        RecognizerPaint.E_NewPaint.register(PaintingApp.event_new_paint,self)
    
    def draw(self):
        self.screen.blit(self.surface,(0,0))
        
    def event_finish_stick(self,Stick):
        pygame.draw.line(self.surface, (255,255,255) , Stick.pos1, Stick.pos2, 5)
    
    def event_painting(self,Point):
        pygame.draw.circle(self.surface, (255,100,100) , Point.pos, 10, 0)
    
    def event_new_paint(self,Paint):
        for p in Paint.previousPoints:
            pygame.draw.circle(self.surface, (255,100,100) , p, 10, 0)
