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
import Tuio

pygame.init()

initializeDisplay()

tscreen = pygame.Surface(Screen.size,flags=SRCALPHA)

app = PaintingApp.PaintingApp(tscreen)

mouse = Mouse.MouseAgentGenerator()

sensors = (Mouse.MouseAgentGenerator(),Tuio.TuioAgentGenerator())

RecognizerStick()
RecognizerPaint()

def input(events): 
    global running
    for event in events: 
        if event.type == QUIT: 
            running = False 
        else:
            for s in sensors:
                if hasattr(s,'event'):
                    s.event(event)
            ConfKey(event)



running = True

while running: 
    calibrate()
    input(pygame.event.get())
    Reactor.run_all_now()
    for s in sensors:
        if hasattr(s,'update'):
            s.update()
    Screen.ScreenDraw.call()
    #screen.blit(tscreen,(0,0))
    drawT(tscreen)
    pygame.display.flip()

saveCalibration()
