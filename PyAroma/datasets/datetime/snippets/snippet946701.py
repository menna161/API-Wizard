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


def extrudeLine(self, line, direction=0, length=0.1, divisions=1, ratio=1.00001, constant=False):
    (x, y) = list(zip(*line))
    x = np.array(x)
    y = np.array(y)
    if (constant and (direction == 0)):
        x.fill(length)
        line = list(zip(x.tolist(), y.tolist()))
        self.addLine(line)
    elif (constant and (direction == 1)):
        y.fill(length)
        line = list(zip(x.tolist(), y.tolist()))
        self.addLine(line)
    elif (direction == 3):
        spacing = self.spacing(divisions=divisions, ratio=ratio, length=length)
        normals = self.curveNormals(x, y)
        for i in range(1, len(spacing)):
            xo = (x + (spacing[i] * normals[(:, 0)]))
            yo = (y + (spacing[i] * normals[(:, 1)]))
            line = list(zip(xo.tolist(), yo.tolist()))
            self.addLine(line)
    elif (direction == 4):
        spacing = self.spacing(divisions=divisions, ratio=ratio, length=length)
        normals = self.curveNormals(x, y)
        normalx = normals[(:, 0)].mean()
        normaly = normals[(:, 1)].mean()
        for i in range(1, len(spacing)):
            xo = (x + (spacing[i] * normalx))
            yo = (y + (spacing[i] * normaly))
            line = list(zip(xo.tolist(), yo.tolist()))
            self.addLine(line)
