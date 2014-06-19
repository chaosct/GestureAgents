# -*- coding: utf-8 -*-
from GestureAgentsDemo.Geometry import Ring
from GestureAgentsDemo.Render import windowsize, drawBatch, basegroup, Update
from GestureAgentsDemo.Utils import TextAlert
from pyglet.gl import GL_LINES


class CalibratorApp(object):
    def __init__(self, system, group=None):
        self.group = group
        self.ring1 = None
        self.label = None
        Update.register(CalibratorApp.update, self)

    def creategeometry(self):
        group = self.group
        self.ring1 = Ring(windowsize[1] / 2.0, 5, 50, group=group)
        self.ring1.getCentered((windowsize[0] / 2, windowsize[1] / 2))
        self.ring1.updateDisplay()
        self.ring2 = Ring(windowsize[1] / 3.0, 5, 50, group=group)
        self.ring2.getCentered((windowsize[0] / 2, windowsize[1] / 2))
        self.ring2.updateDisplay()
        self.ring3 = Ring(windowsize[1] / 6.0, 5, 50, group=group)
        self.ring3.getCentered((windowsize[0] / 2, windowsize[1] / 2))
        self.ring3.updateDisplay()
        vertices = [(x * windowsize[0], y * windowsize[1])
                    for x in (v / 8.0 for v in range(0, 9)) for y in (0, 1)]
        vertices += [(x * windowsize[0], y * windowsize[1])
                    for y in (v / 6.0 for v in range(0, 7)) for x in (0, 1)]
        vvertices = [c[i] for c in vertices for i in (0, 1)]
        self.lines = drawBatch.add(
            len(vertices),
            GL_LINES,
            group,
            ('v2f/static', vvertices),
            ('c3B/static', [255, 255, 255] * len(vertices))
            )

    def destroygeometry(self):
        self.ring1 = None
        self.ring2 = None
        self.ring3 = None
        self.lines.delete()
        self.lines = None

    def update(self, dt=0):
        configurator = basegroup.get_configurator()
        if not self.ring1 and configurator:
            self.creategeometry()
        elif self.ring1 and not configurator:
            self.destroygeometry()
        if configurator and self.label != configurator['name']:
            self.label = configurator['name']
            TextAlert((windowsize[0] / 2, windowsize[1] / 2),
                        text=self.label,
                        group=self.group,
                        timeout=1,
                        font_size=32,
                        anchor_x='center')
