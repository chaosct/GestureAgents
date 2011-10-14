#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, math
import sys
sys.path.append('../..')

import GestureAgents.Screen as Screen
#from GestureAgents.Gestures import RecognizerStick, RecognizerPaint, RecognizerDoubleTap, RecognizerTap
from GestureAgents.AppRecognizer import AppRecognizer
from RecognizerMoveZoom import RecognizerMoveZoom
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
        #self.surface = pygame.Surface(GestureAgents.Screen.size,flags=pygame.locals.SRCALPHA)
        #pygame.draw.line(self.surface, (255,255,255) , (50,50), (100,100), 5)
        #AppRecognizer(RecognizerStick).newAgent.register(MapApp.newAgentStick,self)
        #AppRecognizer(RecognizerPaint).newAgent.register(MapApp.newAgentPaint,self)
        #AppRecognizer(RecognizerDoubleTap).newAgent.register(MapApp.newAgentDoubleTap,self)
        #AppRecognizer(RecognizerTap).newAgent.register(MapApp.newAgentTap,self)
        #AppRecognizer(TuioCursorEvents).newAgent.register(MapApp.newAgentCursor,self)
        AppRecognizer(RecognizerMoveZoom).newAgent.register(MapApp.newAgentMoveZoom,self)
        #self.button = (400,400)
        #self.buttoncolor = (0,100,255)
        self.texname = "earth-map-big.jpg"
        self.texture = None
        self.tmatrix = tr.identity_matrix()
        self.movezoom = None
    
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

    
    def newAgentMoveZoom(self,MZoom):
        #if not self.movezoom:
        print 'eee'
        MZoom.newMoveZoom.register(MapApp.newMoveZoom,self)
    
    def newMoveZoom(self,MZoom):
        self.movezoom = MZoom
        MZoom.newTranslation.register(MapApp.newTranslation,self)
        MZoom.endMoveZoom.register(MapApp.endMoveZoom,self)
        print 'aaa'
    
    def endMoveZoom(self,MZoom):
        #if MZoom == self.movezoom:
        print 'bbb'
        self.movezoom = None
    
    def newTranslation(self,MZoom):
        #print MZoom.translation
        #self.tmatrix = tr.concatenate_matrices(tr.translation_matrix(list(MZoom.translation)+[0]),self.tmatrix)
        self.tmatrix = tr.translation_matrix(list(MZoom.translation)+[0]).transpose().dot(self.tmatrix)
        
        
if __name__ == "__main__":
    import GestureAgents
    RecognizerMoveZoom()
    app = MapApp()
    GestureAgents.run_apps()
