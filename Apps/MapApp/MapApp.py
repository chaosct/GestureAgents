#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('../..')

import GestureAgentsPygame.Screen as Screen
from GestureAgentsTUIO.Gestures2D.RecognizerStick import RecognizerStick
from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap
from GestureAgents.AppRecognizer import AppRecognizer
from RecognizerMove import RecognizerMove
from RecognizerZoomRotate import RecognizerZoomRotate
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
        AppRecognizer(RecognizerStick).newAgent.register(MapApp.newAgentStick,self)
        AppRecognizer(RecognizerTap).newAgent.register(MapApp.newAgentTap,self)
        self.texname = "earth-map-big.jpg"
        self.texture = None
        self.tmatrix = tr.identity_matrix()
        self.Move = None
        self.points_of_interest = []
    
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
        
        for x,y in self.points_of_interest:
            GL.glBegin(GL.GL_QUADS)
            for xx, yy in [(x+dx,y+dy) for dx,dy in ((10,10),(10,-10),(-10,-10),(-10,10))]:
                GL.glVertex2f(xx,yy)
            GL.glEnd()
        
        GL.glPopMatrix()

    
    def newAgentMove(self,Move):
        #if not self.Move:
        Move.newMove.register(MapApp.newMove,self)
    
    def newAgentZoomRotate(self,ZRotate):
        ZRotate.newZoomRotate.register(MapApp.newZoomRotate,self)
    
    def newAgentStick(self,Stick):
        Stick.newStick.register(MapApp.newStick,self)
        
    def newAgentTap(self,Tap):
        posinmap = tr.inverse_matrix(self.tmatrix).transpose().dot(Tap.pos+(0,1))
        if 0 < posinmap[0] < self.texturew and 0 < posinmap[1] < self.textureh:
            Tap.newTap.register(MapApp.newTap,self)
    
    def newTap(self,Tap):
        posinmap = tr.inverse_matrix(self.tmatrix).transpose().dot(Tap.pos+(0,1))
        self.points_of_interest.append(posinmap[0:2])
    
    def newStick(self,Stick):
        self.tmatrix = tr.identity_matrix()
    
    def newMove(self,Move):
        self.Move = Move
        Move.newTranslation.register(MapApp.newTranslation,self)
        Move.endMove.register(MapApp.endMove,self)
    
    def newZoomRotate(self,ZRotate):
        ZRotate.newScale.register(MapApp.newScale,self)
        ZRotate.newRotation.register(MapApp.newRotation,self)
        #ZRotate.endZoom.register(MapApp.newRotation,self)
    
    def endMove(self,MZoom):
        #if MZoom == self.Move:
        self.Move = None
    
    def newTranslation(self,MZoom):
        self.tmatrix = self.tmatrix.dot(tr.translation_matrix(list(MZoom.translation)+[0]).transpose())
    
    def newRotation(self,MZoom):
        pivot = list(MZoom.pivot)+[0]
        self.tmatrix = self.tmatrix.dot(tr.rotation_matrix(MZoom.rotation,[0, 0, 1],pivot).transpose())
    
    def newScale(self,MZoom):
        pivot = list(MZoom.pivot)+[0]
        self.tmatrix = self.tmatrix.dot(tr.scale_matrix(MZoom.scale,pivot).transpose())

from GestureAgents.Agent import Agent        
@Agent.compatibility_policy.rule(0)
def zoom_over_move(r1,r2):
    if type(r1) == RecognizerMove and type(r2) == RecognizerZoomRotate:
        return True
      
@Agent.compatibility_policy.rule(0)
def zoom_over_stick(r1,r2):
    if type(r1) == RecognizerStick and type(r2) == RecognizerZoomRotate:
        return True

if __name__ == "__main__":
    import GestureAgentsPygame
    app = MapApp()
    GestureAgentsPygame.run_apps()
