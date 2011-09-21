#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys,os
from pygame.locals import *
import Mouse
from RecognizerStick import RecognizerStick
from RecognizerPaint import RecognizerPaint
from RecognizerTap import RecognizerTap
from RecognizerDoubleTap import RecognizerDoubleTap
import Screen
import Reactor
import PaintingApp
from Render import initializeDisplay,calibrate,drawT,copyT,saveCalibration,ConfKey
import Tuio

pygame.init()

initializeDisplay()

tscreen = pygame.Surface(Screen.size,flags=SRCALPHA)

app = PaintingApp.PaintingApp(tscreen)

#mouse = Mouse.MouseAgentGenerator()

#sensors = (Mouse.MouseAgentGenerator(),Tuio.TuioAgentGenerator())
sensors = (Tuio.TuioAgentGenerator(),)

RecognizerStick()
RecognizerPaint()
RecognizerTap()
RecognizerDoubleTap()

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

class MemSummary:
    def digest(self):
        import gc
        from Recognizer import Recognizer
        from collections import Counter
        counter = Counter(type(obj) for obj in gc.get_objects() if isinstance(obj, Recognizer))
        print "===========MEMORY=========="
        for t,c in counter.most_common():
            print t,":",c
        
        print
          
        print "%d Failed" % len([obj for obj in gc.get_objects() if isinstance(obj, Recognizer) and obj.failed])
        print "="*30
        Reactor.schedule_after(2,self,MemSummary.digest)
        

    

running = True

MemSummary().digest()

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
