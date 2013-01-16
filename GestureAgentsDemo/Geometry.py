#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pi, sin, cos
from GestureAgentsDemo.Render import drawBatch
from pyglet.gl import GL_TRIANGLES


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
        self.vertexlist.delete()
        self.vertexlist = None


class Circle(Figure):
    def __init__(self, radius, nodes, **kw):
        self.radius = radius
        angles = [2.0 * pi * n / nodes for n in range(0, nodes)]
        vertices = [(radius * cos(
            a), radius * sin(a)) for a in angles for f in (cos, sin)]
        vtriangles = [c for (v1, v2) in zip(vertices, [vertices[-1]] + vertices[:-1])
                      for xy in (v1, (0, 0), v2) for c in xy]
        super(Circle, self).__init__(vtriangles, **kw)
