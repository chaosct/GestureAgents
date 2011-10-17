#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, math
import sys
sys.path.append('../..')

import GestureAgents.Screen as Screen
#from GestureAgents.Gestures import RecognizerStick, RecognizerPaint, RecognizerDoubleTap, RecognizerTap
from GestureAgents.AppRecognizer import AppRecognizer
from RecognizerMove import RecognizerMove
from RecognizerZoomRotate import RecognizerZoomRotate
import GestureAgents.Render
import numpy as np
import transformations as tr
import pygame.image
import OpenGL.GL as GL

def loadImage(image):
    textureSurface = pygame.image.load(image)
 
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
 
    width = textureSurface.get_width()
    height = textureSurface.get_height()
 
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA,
        GL.GL_UNSIGNED_BYTE, textureData)
    
    return texture, width, height

class MapApp:
    def __init__(self):
        Screen.ScreenDraw.register(MapApp.draw,self)
        AppRecognizer(RecognizerMove).newAgent.register(MapApp.newAgentMove,self)
        AppRecognizer(RecognizerZoomRotate).newAgent.register(MapApp.newAgentZoomRotate,self)
        self.texname = "earth-map-big.jpg"
        self.texture = None
        self.tmatrix = tr.identity_matrix()
        self.Move = None
    
    def load_texture(self):
        self.texture, self.texturew, self.textureh = loadImage(self.texname)
    
    def draw(self):
        if not self.texture:
            self.load_texture()
        
        GL.glPushMatrix()
        GL.glMultMatrixf(self.tmatrix)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glBegin(GL.GL_QUADS)
     
        # Bottom Left Of The Texture and Quad
        GL.glTexCoord2f(0, 1); GL.glVertex2f(0, 0)
     
        # Top Left Of The Texture and Quad
        GL.glTexCoord2f(0, 0); GL.glVertex2f(0, self.textureh)
     
        # Top Right Of The Texture and Quad
        GL.glTexCoord2f(1, 0); GL.glVertex2f( self.texturew,  self.textureh)
     
        # Bottom Right Of The Texture and Quad
        GL.glTexCoord2f(1, 1); GL.glVertex2f(self.texturew, 0)
        GL.glEnd()
        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glPopMatrix()

    
    def newAgentMove(self,Move):
        #if not self.Move:
        Move.newMove.register(MapApp.newMove,self)
    
    def newAgentZoomRotate(self,ZRotate):
        ZRotate.newZoomRotate.register(MapApp.newZoomRotate,self)
    
    def newMove(self,Move):
        self.Move = Move
        Move.newTranslation.register(MapApp.newTranslation,self)
        Move.endMove.register(MapApp.endMove,self)
    
    def newZoomRotate(self,ZRotate):
        ZRotate.newScale.register(MapApp.newScale,self)
        #ZRotate.newRotation.register(MapApp.newRotation,self)
        #ZRotate.endZoom.register(MapApp.newRotation,self)
    
    def endMove(self,MZoom):
        #if MZoom == self.Move:
        self.Move = None
    
    def newTranslation(self,MZoom):
        #print MZoom.translation
        #self.tmatrix = tr.concatenate_matrices(tr.translation_matrix(list(MZoom.translation)+[0]),self.tmatrix)
        self.tmatrix = tr.translation_matrix(list(MZoom.translation)+[0]).transpose().dot(self.tmatrix)
    
    def newScale(self,MZoom):
        print "rotate"

from GestureAgents.Agent import Agent        
@Agent.compatibility_policy.rule(0)
def zoom_over_move(r1,r2):
    if type(r1) == RecognizerMove and type(r2) == RecognizerZoomRotate:
        return True

if __name__ == "__main__":
    import GestureAgents
    RecognizerMove()
    RecognizerZoomRotate()
    app = MapApp()
    GestureAgents.run_apps()
