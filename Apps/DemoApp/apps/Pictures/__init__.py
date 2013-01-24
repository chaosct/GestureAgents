# -*- coding: utf-8 -*-

from pyglet.resource import Loader
from pyglet.sprite import Sprite
from GestureAgentsDemo.Render import drawBatch
from unipath import Path
from random import randrange
from GestureAgents.AppRecognizer import AppRecognizer
from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap
from math import sqrt
from GestureAgentsDemo.Render import windowsize, Update
from GestureAgentsDemo.Utils import DynamicValue
IMAGESPATH = "/home/carles/Imatges/songexplorer-video"
loader = Loader([IMAGESPATH])


class AppPictureBrowser(object):
    def __init__(self, group=None):
        self.group = group
        dir = Path(IMAGESPATH)
        files = [f.name for f in list(dir.listdir("*.png"))]
        self.pictures = []
        for f in files[:20]:
            self.pictures.append(Picture(f, group=group))


def dist(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return sqrt(dx * dx + dy * dy)


class Picture(object):
    def __init__(self, image, group=None):
        self.texture = loader.image(image)
        self.texture.anchor_x = self.texture.width / 2
        self.texture.anchor_y = self.texture.height / 2
        self.sprite = Sprite(self.texture, batch=drawBatch, group=group)
        w, h = windowsize
        self.x = DynamicValue(randrange(100, w - 100))
        self.y = DynamicValue(randrange(100, h - 100))
        self.sprite.scale = 0.1
        AppRecognizer(RecognizerTap).newAgent.register(Picture.newTapAgent, self)
        Update.register(Picture.update, self)

    def newTapAgent(self, agent):
        # print "oh?", dist(agent.pos, (self.sprite.x, self.sprite.y))
        if dist(agent.pos, (self.sprite.x, self.sprite.y)) < 10:
            agent.newTap.register(Picture.newTap, self)

    def newTap(self, tap):
        w, h = windowsize
        self.x(randrange(100, w - 100), .5)
        self.y(randrange(100, h - 100), .5)

    def update(self, dt=0):
        self.sprite.x = self.x()
        self.sprite.y = self.y()
