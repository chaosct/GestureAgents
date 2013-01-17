# -*- coding: utf-8 -*-

from GestureAgentsDemo.Render import Update


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
