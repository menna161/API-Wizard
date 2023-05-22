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


def extrudeLine_cell_thickness(self, line, cell_thickness=0.04, growth=1.05, divisions=1, direction=3):
    (x, y) = list(zip(*line))
    x = np.array(x)
    y = np.array(y)
    if (direction == 3):
        (spacing, _) = self.spacing_cell_thickness(cell_thickness=cell_thickness, growth=growth, divisions=divisions)
        normals = self.curveNormals(x, y)
        for i in range(1, len(spacing)):
            xo = (x + (spacing[i] * normals[(:, 0)]))
            yo = (y + (spacing[i] * normals[(:, 1)]))
            line = list(zip(xo.tolist(), yo.tolist()))
            self.addLine(line)
    elif (direction == 4):
        (spacing, _) = self.spacing_cell_thickness(cell_thickness=cell_thickness, growth=growth, divisions=divisions)
        normals = self.curveNormals(x, y)
        normalx = normals[(:, 0)].mean()
        normaly = normals[(:, 1)].mean()
        for i in range(1, len(spacing)):
            xo = (x + (spacing[i] * normalx))
            yo = (y + (spacing[i] * normaly))
            line = list(zip(xo.tolist(), yo.tolist()))
            self.addLine(line)
