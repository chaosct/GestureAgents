#!/usr/bin/env python
# -*- coding: utf-8 -*-

import GestureAgentsPygame.Screen as Screen
import pygame, sys,os
from pygame.locals import *
import GestureAgents.Reactor as Reactor
from GestureAgentsPygame.Render import initializeDisplay,calibrate,ConfKey
import GestureAgentsTUIO.Tuio as Tuio
from GestureAgentsPygame.Mouse import MouseAsTuioAgentGenerator
import GestureAgents.Gestures as Gestures
import pygame.display
import GestureAgents.Agent as Agent
from pygame.time import Clock

class MemSummary:
    def digest(self):
        import gc
        gc.collect()
        from GestureAgents.Recognizer import Recognizer
        from collections import Counter
        counter = Counter(type(obj) for obj in gc.get_objects() if isinstance(obj, Recognizer))
        print "===========MEMORY=========="
        for t,c in counter.most_common():
            print t,":",c
            if c > 100: import pdb; pdb.set_trace()
        
        print
        lfailed = [obj for obj in gc.get_objects() if isinstance(obj, Recognizer) and obj.failed]
        print "%d Failed" % len(lfailed)
        print "="*30
        #lfailed = None
        #l = [obj for obj in gc.get_objects() if isinstance(obj, Recognizer)]
        #import objgraph
        #objgraph.show_backrefs(l, filename='failed.png',max_depth=5)
        #for obj in l:
        #    print obj
        #    print obj.__dict__
        Reactor.schedule_after(2,self,MemSummary.digest)
        

running = False

def run_apps(debugMem=False):
    global running
    pygame.init()
    initializeDisplay()
    tscreen = pygame.Surface(Screen.size,flags=SRCALPHA)
    sensors = (Tuio.TuioAgentGenerator(Screen.size),MouseAsTuioAgentGenerator())

    clock = Clock()

    if Gestures.recognizers_loaded:
        print "Loaded %d gesture recognizers:" % len(Gestures.recognizers)
        for r in Gestures.recognizers:
            print "\t%s" % str(r)

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
    
    print "="*5 + " Agent.completion_policy Policy rules " + "="*5
    print Agent.Agent.completion_policy
    print "="*5 + " Agent.compatibility_policy Policy rules " + "="*5
    print Agent.Agent.compatibility_policy
    
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
        clock.tick_busy_loop(30)
