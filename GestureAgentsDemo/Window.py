from pyglet.window import Window, key, NoSuchConfigException
from pyglet.gl import Config, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pyglet.clock

from GestureAgentsTUIO import Tuio
from GestureAgents import Reactor

from Mouse import MouseAsTuioAgentGenerator
import Render


class DemoWindow(Window):
    """docstring for DemoWindow"""
    def __init__(self):
        try:
            # Try and create a window with multisampling (antialiasing)
            config = Config(sample_buffers=1, samples=4,
                            depth_size=16, double_buffer=True,)
            super(DemoWindow, self).__init__(resizable=True, config=config)
        except NoSuchConfigException:
            # Fall back to no multisampling for old hardware
            super(DemoWindow, self).__init__(resizable=True)
        self.initdisplay()
        self.tuiomouse = MouseAsTuioAgentGenerator()
        self.sensors = (
            Tuio.TuioAgentGenerator(self.get_size(), inverse_y=True),
            self.tuiomouse)
        pyglet.clock.schedule(self.update)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Render.drawBatch.draw()

    def update(self, dt):
        Render.Update(dt)
        Reactor.run_all_now()
        for s in self.sensors:
            if hasattr(s, 'update'):
                s.update()

    def initdisplay(self):
        w, h = Render.windowsize
        self.set_size(w, h)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.F:
            self.set_fullscreen(not self.fullscreen)
        else:
            Render.basegroup.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.tuiomouse.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.tuiomouse.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.tuiomouse.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
