#!/usr/bin/env 

import pyglet
from pyglet.gl import Config
from pyglet.window import Window, key
import pyglet.app

from GestureAgentsTUIO import Tuio
from GestureAgents import Reactor, Gestures, Agent
from Mouse import MouseAsTuioAgentGenerator
        
class DemoWindow(Window):
    """docstring for DemoWindow"""
    def __init__(self):
        try:
            # Try and create a window with multisampling (antialiasing)
            config = Config(sample_buffers=1, samples=4, 
                            depth_size=16, double_buffer=True,)
            super(DemoWindow, self).__init__(resizable=True, config=config)
        except pyglet.window.NoSuchConfigException:
            # Fall back to no multisampling for old hardware
            super(DemoWindow, self).__init__(resizable=True)
        self.tuiomouse = MouseAsTuioAgentGenerator()
        self.sensors = (Tuio.TuioAgentGenerator(self.get_size()),self.tuiomouse)
        pyglet.clock.schedule(self.update)
    def on_draw(self):
        pass
    def update(self,dt):
        Reactor.run_all_now()
        for s in self.sensors:
            if hasattr(s,'update'):
                s.update()
    def initdisplay(self):
        self.set_size(800,600)
    def on_key_press(self,symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.F:
            self.set_fullscreen(not self.fullscreen)
        else:
            print "key", symbol, "!"
    def on_mouse_press(self,x, y, button, modifiers):
        self.tuiomouse.on_mouse_press(x,y,button,modifiers)
    def on_mouse_release(self,x, y, button, modifiers):
        self.tuiomouse.on_mouse_release(x,y,button,modifiers)
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        self.tuiomouse.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


def run_apps(debugMem=False):

    if Gestures.recognizers_loaded:
        print "Loaded %d gesture recognizers:" % len(Gestures.recognizers)
        for r in Gestures.recognizers:
            print "\t%s" % str(r)

    # def input(events): 
    #     global running
    #     for event in events: 
    #         else:
    #             for s in sensors:
    #                 if hasattr(s,'event'):
    #                     s.event(event)
    #             ConfKey(event)
    
    print "="*5 + " Agent.completion_policy Policy rules " + "="*5
    print Agent.Agent.completion_policy
    print "="*5 + " Agent.compatibility_policy Policy rules " + "="*5
    print Agent.Agent.compatibility_policy
    
    # if debugMem:
    #     MemSummary().digest()

    # while running: 
    #     calibrate()
    #     input(pygame.event.get())
    #     Screen.ScreenDraw.call()
    #     pygame.display.flip()
    #     clock.tick_busy_loop(30)
    window = DemoWindow()
    pyglet.app.run()

def run():
    run_apps()

if __name__ == '__main__':
    run()