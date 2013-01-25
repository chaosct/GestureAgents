# -*- coding: utf-8 -*-

import pyglet.graphics
import GestureAgents.Events
import json

drawBatch = pyglet.graphics.Batch()
Update = GestureAgents.Events.Event()
windowsize = (1024, 768)


class DistortGroup(pyglet.graphics.Group):
    CALIBRATION_FILE = 'calibration.json'

    def __init__(self, parent=None):

        #default calibration
        self.calibration = {
            'x': 0,
            'y': 0,
            'z': 0,
            'w': 1,
            'h': 1,
            'ax': 0,
            'ay': 0,
            'az': 0,
        }

        try:
            fcalibration = open(self.CALIBRATION_FILE)
            self.calibration.update(json.load(fcalibration))
            print "Loaded " + self.CALIBRATION_FILE
        except IOError:
            pass

        def c_change(k, v):
            self.calibration[k] += v

        from pyglet.window import key
        s = 0.01
        sd = 1
        CMove = {key.W: lambda: c_change('y', -s),
                 key.S: lambda: c_change('y', s),
                 key.A: lambda: c_change('x', -s),
                 key.D: lambda: c_change('x', s),
                 'name': "Move center"}

        CZoom = {key.W: lambda: c_change('h', s),
                 key.S: lambda: c_change('h', -s),
                 key.A: lambda: c_change('w', -s),
                 key.D: lambda: c_change('w', s),
                 'name': "Zoom"}

        CParal = {key.W: lambda: c_change('ax', sd),
                  key.S: lambda: c_change('ax', -sd),
                  key.A: lambda: c_change('ay', -sd),
                  key.D: lambda: c_change('ay', sd),
                  'name': "Lateral angles"}

        CRota = {key.W: lambda: c_change('z', s),
                 key.S: lambda: c_change('z', -s),
                 key.A: lambda: c_change('az', -sd),
                 key.D: lambda: c_change('az', sd),
                 'name': "Rotation and Z"}

        self.configurators = (None, CMove, CZoom, CParal, CRota)
        self.configurator = 0

        super(DistortGroup, self).__init__(parent=parent)

    def set_state(self):
        from pyglet.gl import *
        w, h = windowsize
        calibration = self.calibration
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPerspective(45, 1, 0, 150)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(calibration['x'], calibration['y'], calibration['z'] - 1)
        glRotatef(calibration['ax'], 1, 0, 0)
        glRotatef(calibration['ay'], 0, 1, 0)
        glRotatef(calibration['az'], 0, 0, 1)
        glScalef(calibration['w'], calibration['h'], 1)
        glScalef(1.0 / w, 1.0 / h, 1)
        glTranslatef(-w / 2, -h / 2, 0)

    def unset_state(self):
        from pyglet.gl import glPopMatrix, glMatrixMode, GL_PROJECTION, GL_MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key
        if self.configurator and symbol in self.get_configurator():
            self.get_configurator()[symbol]()
        if symbol == key.SPACE:
            self.configurator = (self.configurator + 1) % len(self.configurators)
            if self.get_configurator():
                print "Configurator: " + self.get_configurator()['name']
            else:
                print "No Configurator"
                print "Saving " + self.CALIBRATION_FILE
                fcalibration = open(self.CALIBRATION_FILE, 'w')
                json.dump(self.calibration, fcalibration, sort_keys=True, indent=4)

    def get_configurator(self):
        return self.configurators[self.configurator]

basegroup = DistortGroup()
