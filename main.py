#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys,os
from pygame.locals import *
import Mouse
from RecognizerStick import RecognizerStick
from RecognizerPaint import RecognizerPaint
import Screen
import Reactor
import PaintingApp



pygame.init()

window = pygame.display.set_mode(Screen.size) 
screen = pygame.display.get_surface() 

app = PaintingApp.PaintingApp(screen)

mouse = Mouse.MouseAgentGenerator()
RecognizerStick()
RecognizerPaint()

def input(events): 
   for event in events: 
      if event.type == QUIT: 
         sys.exit(0) 
      else: 
         mouse.event(event)

while True: 
   input(pygame.event.get())
   Reactor.run_all_now()
   Screen.ScreenDraw.call()
   pygame.display.flip()
