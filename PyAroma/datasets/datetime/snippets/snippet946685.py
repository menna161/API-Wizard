import os
import copy
from datetime import date
import locale
import numpy as np
from scipy import interpolate
import meshio
from PySide6 import QtGui, QtCore, QtWidgets
import PyAero
import GraphicsItemsCollection as gic
import GraphicsItem
import Elliptic
import Connect
from Smooth_angle_based import SmoothAngleBased
from Utils import Utils
from Settings import OUTPUTDATA
import logging


def makeBoundaries(self):
    'A boundary edge is an edge that belongs only to one cell'
    (vertices, _) = self.mesh
    vertices = np.array(vertices)
    edges = self.edges
    seen = set()
    unique = list()
    doubles = set()
    for edge in edges:
        if (edge not in seen):
            seen.add(edge)
            unique.append(edge)
        else:
            doubles.add(edge)
    self.boundary_edges = [edge for edge in unique if (edge not in doubles)]
    self.boundary_tags = {'airfoil': [], 'inlet': [], 'outlet': []}
    for edge in self.boundary_edges:
        x = vertices[edge[0]][0]
        y = vertices[edge[0]][1]
        if ((x > (- 0.1)) and (x < 1.1) and (y < 0.5) and (y > (- 0.5))):
            self.boundary_tags['airfoil'].append(edge)
        elif (x == np.max(vertices[(:, 0)])):
            self.boundary_tags['outlet'].append(edge)
        else:
            self.boundary_tags['inlet'].append(edge)
    return
