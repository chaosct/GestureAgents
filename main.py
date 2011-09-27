#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Screen
import pygame, sys,os
from pygame.locals import *
import Mouse
import Reactor
import PaintingApp
from Render import initializeDisplay,calibrate,ConfKey
import Tuio
import Gestures
import pygame.display

class MemSummary:
    def digest(self):
        import gc
        from Recognizer import Recognizer
        from collections import Counter
        counter = Counter(type(obj) for obj in gc.get_objects() if isinstance(obj, Recognizer))
        print "===========MEMORY=========="
        for t,c in counter.most_common():
            print t,":",c
            if c > 100: import pdb; pdb.set_trace()
        
        print
          
        print "%d Failed" % len([obj for obj in gc.get_objects() if isinstance(obj, Recognizer) and obj.failed])
        print "="*30
        Reactor.schedule_after(2,self,MemSummary.digest)

running = False

def run_apps(debugMem=False):
    global running
    pygame.init()
    initializeDisplay()
    tscreen = pygame.Surface(Screen.size,flags=SRCALPHA)
    #app = PaintingApp.PaintingApp(tscreen)
    #mouse = Mouse.MouseAgentGenerator()
    #sensors = (Mouse.MouseAgentGenerator(),Tuio.TuioAgentGenerator())
    sensors = (Tuio.TuioAgentGenerator(),)

    if Gestures.recognizers:
        print "Found %d gesture recognizers:" % len(Gestures.recognizers)
        for r in Gestures.recognizers:
            print "\t%s" % str(r)
    Gestures.load_all()

    def input(events): 
        global running
        for event in events: 
            if event.type == QUIT: 
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == KEYDOWN and event.key == K_f:
                pygame.display.toggle_fullscreen()
            else:
                for s in sensors:
                    if hasattr(s,'event'):
                        s.event(event)
                ConfKey(event)
    running = True

    if debugMem:
        MemSummary().digest()

    while running: 
        calibrate()
        input(pygame.event.get())
        Reactor.run_all_now()
        for s in sensors:
            if hasattr(s,'update'):
                s.update()
        Screen.ScreenDraw.call()
        pygame.display.flip()

