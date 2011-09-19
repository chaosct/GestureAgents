#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from OpenGL.GL import *
from OpenGL.GLU import *
import Screen
import pygame

width, height = Screen.size

CALIBRATION_FILE = 'calibration.json'

#default calibration
calibration = {}
calibration['x']=0
calibration['y']=0
calibration['z']=0
calibration['w']=1
calibration['h']=1
calibration['ax']=0
calibration['ay']=0
calibration['az']=0

try:
    fcalibration = open(CALIBRATION_FILE)
    calibration.update(json.load(fcalibration))
    print "Loaded "+CALIBRATION_FILE
except IOError:
    pass
    

def initializeDisplay():
    global texture
    w,h = Screen.size
    pygame.display.set_mode(Screen.size, pygame.OPENGL|pygame.DOUBLEBUF)
 
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity();
    gluPerspective(45,float(w)/float(h),0.5,150)
    glMatrixMode(GL_MODELVIEW)
 
    # set up texturing
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    texture = glGenTextures(1)

def copyT(textureSurface):
    width, height = Screen.size
    
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
        GL_UNSIGNED_BYTE, textureData)

def drawT(textureSurface):
    glEnable(GL_TEXTURE_2D)
    copyT(textureSurface)
    
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
 
    # Bottom Left Of The Texture and Quad
    glTexCoord2f(0, 1); glVertex2f(0, 0)
 
    # Top Left Of The Texture and Quad
    glTexCoord2f(0, 0); glVertex2f(0, 1)
 
    # Top Right Of The Texture and Quad
    glTexCoord2f(1, 0); glVertex2f( 1,  1)
 
    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1, 1); glVertex2f(1, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def calibrate():
    global calibration
    if configurators[configurator] and keyPressed :configurators[configurator][keyPressed]()
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glScale(1,-1,1)
    
    
    glTranslate(calibration['x'],calibration['y'],calibration['z'])
    glRotate(calibration['ax'],1,0,0)
    glRotate(calibration['ay'],0,1,0)
    glRotate(calibration['az'],0,0,1)
    glScale(calibration['w'],calibration['h'],1)
    
    glTranslate(-0.5,-0.5,-1)
    
    #glTranslate(1,0,0)
    glBegin(GL_QUADS)
    glVertex2f(-0.01, 0.01)
    glVertex2f(-0.01, -0.01)
    glVertex2f(0.01, -0.01)
    glVertex2f(0.01, 0.01)
    glEnd()



def saveCalibration():
    print "Saving "+CALIBRATION_FILE
    fcalibration = open(CALIBRATION_FILE,'w')
    json.dump(calibration,fcalibration,sort_keys=True, indent=4)
    
    

s = 0.01
sd = 1

def c_change(k,v):
    global calibration
    calibration[k]+=v


CMove = {pygame.K_w:lambda: c_change('y',-s),
         pygame.K_s:lambda: c_change('y',s),
         pygame.K_a:lambda: c_change('x',-s),
         pygame.K_d:lambda: c_change('x',s),
         'name': "Move center"}

CZoom = {pygame.K_w:lambda: c_change('h',s),
         pygame.K_s:lambda: c_change('h',-s),
         pygame.K_a:lambda: c_change('w',-s),
         pygame.K_d:lambda: c_change('w',s),
         'name': "Zoom"}
         
CParal = {pygame.K_w:lambda: c_change('ay',sd),
          pygame.K_s:lambda: c_change('ay',-sd),
          pygame.K_a:lambda: c_change('ax',-sd),
          pygame.K_d:lambda: c_change('ax',sd),
          'name': "Lateral angles"}

CRota = {pygame.K_w:lambda: c_change('z',sd),
         pygame.K_s:lambda: c_change('z',-sd),
         pygame.K_a:lambda: c_change('az',-s),
         pygame.K_d:lambda: c_change('az',s),
         'name': "Rotation and Z"}

configurators = (None,CMove,CZoom,CParal,CRota)
configurator = 0
keyPressed = None

def ConfKey(event):
    global configurator, keyPressed
    if configurators[configurator] and event.type == pygame.KEYDOWN and event.key in configurators[configurator]:
        keyPressed = event.key
    elif event.type == pygame.KEYUP and event.key == keyPressed:
        keyPressed = None
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
        configurator = (configurator+1) % len(configurators)
        if configurators[configurator]:
            print "Configurator: "+ configurators[configurator]['name']
        else:
            print "No Configurator"
