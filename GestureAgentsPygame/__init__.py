#!/usr/bin/env python
# -*- coding: utf-8 -*-

import GestureAgentsPygame.Screen as Screen
import pygame
import sys
import os
from pygame.locals import *
import GestureAgents.Reactor as Reactor
from GestureAgentsPygame.Render import initializeDisplay, calibrate, ConfKey
import GestureAgentsTUIO.Tuio as Tuio
from GestureAgentsPygame.Mouse import MouseAsTuioAgentGenerator
import GestureAgents.Gestures as Gestures
import pygame.display
import GestureAgents.Agent as Agent
from pygame.time import Clock
import GestureAgents.System
from GestureAgentsTUIO.Tuio import TuioCursorEvents


class MemSummary:
    def digest(self):
        import gc
        gc.collect()
        from GestureAgents.Recognizer import Recognizer
        from collections import Counter
        counter = Counter(type(
            obj) for obj in gc.get_objects() if isinstance(obj, Recognizer))
        print "===========MEMORY=========="
        for t, c in counter.most_common():
            print t, ":", c
            if c > 100:
                import pdb
                pdb.set_trace()

        print
        lfailed = [obj for obj in gc.get_objects(
        ) if isinstance(obj, Recognizer) and obj.failed]
        print "%d Failed" % len(lfailed)
        print "=" * 30
        #lfailed = None
        #l = [obj for obj in gc.get_objects() if isinstance(obj, Recognizer)]
        #import objgraph
        #objgraph.show_backrefs(l, filename='failed.png',max_depth=5)
        #for obj in l:
        #    print obj
        #    print obj.__dict__
        Reactor.schedule_after(2, self, MemSummary.digest)




class System(GestureAgents.System.System):

    def __init__(self):
        sources = [TuioCursorEvents]
        GestureAgents.System.System.__init__(self, sources)
        self.sensors = None
        self.clock = None

    def print_info(self, debugMem=False):
        if self.recognizers:
            print "Loaded %d gesture recognizers:" % len(self.recognizers)
            for r in self.recognizers:
                print "\t%s" % str(r)

        print "=" * 5 + " Agent.completion_policy Policy rules " + "=" * 5
        print Agent.Agent.completion_policy
        print "=" * 5 + " Agent.compatibility_policy Policy rules " + "=" * 5
        print Agent.Agent.compatibility_policy

        if debugMem:
            MemSummary().digest()


    def run_apps(self, debugMem=False):
        pygame.init()
        initializeDisplay()
        tscreen = pygame.Surface(Screen.size, flags=SRCALPHA)
        self.sensors = (
            Tuio.TuioAgentGenerator(Screen.size), MouseAsTuioAgentGenerator())

        self.clock = Clock()

        self.print_info(debugMem)

        GestureAgents.System.System.run_apps(self)

    def update(self):
        calibrate()
        for s in self.sensors:
            if hasattr(s, 'update'):
                s.update()
        Screen.ScreenDraw.call()
        pygame.display.flip()
        self.clock.tick_busy_loop(30)
        self.input(pygame.event.get())

    def input(self, events):
        for event in events:
            if event.type == QUIT:
                self.stop()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.stop()
            if event.type == KEYDOWN and event.key == K_f:
                pygame.display.toggle_fullscreen()
            else:
                for s in self.sensors:
                    if hasattr(s, 'event'):
                        s.event(event)
                ConfKey(event)