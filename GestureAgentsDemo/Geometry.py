#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pi, sin, cos
from GestureAgentsDemo.Render import drawBatch
from pyglet.gl import GL_TRIANGLES


def MovingWindowIterator(it, group, loop=True):
    seq = list(it)
    if loop:
        seq = seq + seq[:group - 1:]
    chunk = []
    while len(chunk) < group:
        chunk.append(seq.pop(0))
    yield chunk
    while seq:
        chunk.pop(0)
        chunk.append(seq.pop(0))
        yield chunk


class Figure(object):
    """docstring for Figure"""
    def __init__(self, vertices=(), geometry_type=GL_TRIANGLES,
                group=None, color=(255, 255, 255), texturevertices=None):
        self.vertices = vertices
        self.geometry_type = geometry_type
        self.vertexlist = None
        self.transformed_vertices = self.vertices
        self.color = list(color)
        self.group = group
        self.texturevertices = texturevertices
        self.updateDisplay()

    def getCentered(self, xy):
        self.transformed_vertices = [v + xy[n % len(
            xy)] for n, v in enumerate(self.vertices)]

    def updateDisplay(self):
        if not self.vertexlist:
            nvertices = len(self.transformed_vertices) / 2
            arrays = []
            arrays.append(('v2f/dynamic', self.transformed_vertices))
            color = self.color
            if len(color) == 3:
                color = color * nvertices
            arrays.append(('c3B/dynamic', color))
            if self.texturevertices:
                arrays.append(('t2f/dynamic', self.texturevertices))
            self.vertexlist = drawBatch.add(
                nvertices,
                self.geometry_type,
                self.group,  # group2d,
                *arrays
                )
        else:
            self.vertexlist.vertices = self.transformed_vertices

    def clear(self):
        if self.vertexlist:
            self.vertexlist.delete()
        self.vertexlist = None

    def __del__(self):
        self.clear()


class Circle(Figure):
    def __init__(self, radius, nodes, **kw):
        self.radius = radius
        angles = [2.0 * pi * n / nodes for n in range(0, nodes)]
        vertices = [(radius * cos(a), radius * sin(a)) for a in angles]
        vtriangles = [c for (v1, v2) in MovingWindowIterator(vertices, 2, True)
                      for xy in (v1, (0, 0), v2) for c in xy]
        super(Circle, self).__init__(vtriangles, **kw)


class Rectangle(Figure):
    def __init__(self, w, h, texture=False, **kw):
        self.w = w
        self.h = h
        vertices = [(0, 0), (w, 0), (w, h), (0, h)]
        indices = (0, 1, 2, 2, 3, 0)
        vtriangles = [c for i in indices for c in vertices[i]]
        vtexture = None
        if texture:
            tvertices = texture.tex_coords
            print tvertices
            vtexture = [c for i in indices
                        for c in (tvertices[i * 3], tvertices[i * 3 + 1])]
        super(Rectangle, self).__init__(vtriangles, texturevertices=vtexture, **kw)
