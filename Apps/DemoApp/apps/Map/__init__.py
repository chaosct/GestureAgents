# -*- coding: utf-8 -*-

from GestureAgentsDemo.Geometry import Rectangle
from pyglet.graphics import OrderedGroup, TextureGroup, Group
from GestureAgentsDemo import transformations as tr
import pyglet.image
import os.path
from OpenGL.GL import glPushMatrix, glPopMatrix, glMultMatrixf

from GestureAgents.AppRecognizer import AppRecognizer
from RecognizerMove import RecognizerMove
from RecognizerZoomRotate import RecognizerZoomRotate


class GroupTransform(Group):
    def __init__(self, *args, **kwargs):
        self.matrix = tr.identity_matrix()
        super(GroupTransform, self).__init__(*args, **kwargs)

    def set_state(self):
        glPushMatrix()
        glMultMatrixf(self.matrix)

    def unset_state(self):
        glPopMatrix()


class DemoMapApp(object):
    def __init__(self, group=None):
        self.tgroup = GroupTransform(parent=group)
        self.fggroup = OrderedGroup(1, parent=self.tgroup)
        self.bggroup = OrderedGroup(0, parent=self.tgroup)
        self.texfile = os.path.join(os.path.dirname(__file__), "earth-map-big.jpg")
        self.mapimage = pyglet.image.load(self.texfile)
        self.maptexture = self.mapimage.get_texture()
        self.map = Rectangle(self.mapimage.width, self.mapimage.height,
            group=TextureGroup(self.maptexture, parent=self.bggroup),
            texture=self.maptexture)
        AppRecognizer(
            RecognizerMove).newAgent.register(DemoMapApp.newAgentMove, self)
        AppRecognizer(RecognizerZoomRotate).newAgent.register(
            DemoMapApp.newAgentZoomRotate, self)

    def newAgentMove(self, Move):
        #TODO: check if inside
        Move.newMove.register(DemoMapApp.newMove, self)

    def newMove(self, Move):
        self.Move = Move
        Move.newTranslation.register(DemoMapApp.newTranslation, self)
        Move.endMove.register(DemoMapApp.endMove, self)

    def newTranslation(self, MZoom):
        self.tgroup.matrix = self.tgroup.matrix.dot(
            tr.translation_matrix(list(MZoom.translation) + [0]).transpose())

    def endMove(self, MZoom):
        self.Move = None

    def newAgentZoomRotate(self, ZRotate):
        ZRotate.newZoomRotate.register(DemoMapApp.newZoomRotate, self)

    def newZoomRotate(self, ZRotate):
        ZRotate.newScale.register(DemoMapApp.newScale, self)
        ZRotate.newRotation.register(DemoMapApp.newRotation, self)
        #ZRotate.endZoom.register(DemoMapApp.newRotation,self)

    def newRotation(self, MZoom):
        pivot = list(MZoom.pivot) + [0]
        self.tgroup.matrix = self.tgroup.matrix.dot(
            tr.rotation_matrix(MZoom.rotation, [0, 0, 1], pivot).transpose())

    def newScale(self, MZoom):
        pivot = list(MZoom.pivot) + [0]
        self.tgroup.matrix = self.tgroup.matrix.dot(
            tr.scale_matrix(MZoom.scale, pivot).transpose())


from GestureAgents.Agent import Agent


@Agent.compatibility_policy.rule(0)
def zoom_over_move(r1, r2):
    if type(r1) == RecognizerMove and type(r2) == RecognizerZoomRotate:
        return True


# @Agent.compatibility_policy.rule(0)
# def zoom_over_stick(r1, r2):
#     if type(r1) == RecognizerStick and type(r2) == RecognizerZoomRotate:
#         return True
