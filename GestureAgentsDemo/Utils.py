# -*- coding: utf-8 -*-

from GestureAgentsDemo.Render import Update, drawBatch
from pyglet.text import Label
from pyglet.clock import schedule_once


class DynamicValue(object):
    """docstring for DynamicValue"""
    def __init__(self, value=0):
        self.value = value
        self.target = value
        self.time = 0

    def __call__(self, target=None, time=0):
        if target is None:
            return self.value
        if time <= 0:
            self.value = target
        else:
            self.time = time
            self.target = target
            Update.register(DynamicValue._update_cb, self)

    def _update_cb(self, dt):
        step = dt * (self.target - self.value) / self.time
        self.time -= dt
        if self.time <= 0:
            Update.unregister(self)
            self.value = self.target
        else:
            self.value += step


class TextAlert(object):
    def __init__(self, pos, text, group=None, timeout=5,
                color=(255, 100, 100, 255), font_size=8, **kwargs):
        x, y = pos
        self.text = Label(text=text, x=x, y=y, font_size=font_size,
                            group=group, batch=drawBatch,
                            color=color, **kwargs)
        schedule_once(self.kill, timeout)

    def kill(self, dt=0):
        self.text.delete()
        self.text = None
