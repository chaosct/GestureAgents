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
from Render import initializeDisplay,calibrate,drawT,copyT,saveCalibration,ConfKey

pygame.init()

initializeDisplay()

tscreen = pygame.Surface(Screen.size,flags=SRCALPHA)

app = PaintingApp.PaintingApp(tscreen)

mouse = Mouse.MouseAgentGenerator()
RecognizerStick()
RecognizerPaint()

def input(events): 
    global running
    for event in events: 
        if event.type == QUIT: 
            running = False 
        else: 
            mouse.event(event)
            ConfKey(event)



running = True

while running: 
    calibrate()
    input(pygame.event.get())
    Reactor.run_all_now()
    Screen.ScreenDraw.call()
    #screen.blit(tscreen,(0,0))
    drawT(tscreen)
    pygame.display.flip()

saveCalibration()
