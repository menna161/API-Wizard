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


def distribute(self, direction='u', number=0, type='constant'):
    if (direction == 'u'):
        line = np.array(self.getULines()[number])
    elif (direction == 'v'):
        line = np.array(self.getVLines()[number])
    (tck, u) = interpolate.splprep(line.T, s=0, k=1)
    if (type == 'constant'):
        t = np.linspace(0.0, 1.0, num=len(line))
    if (type == 'transition'):
        first = np.array(self.getULines()[0])
        last = np.array(self.getULines()[(- 1)])
        (tck_first, u_first) = interpolate.splprep(first.T, s=0, k=1)
        (tck_last, u_last) = interpolate.splprep(last.T, s=0, k=1)
        if (number < 0.0):
            number = len(self.getVLines())
        v = (float(number) / float(len(self.getVLines())))
        t = (((1.0 - v) * u_first) + (v * u_last))
    line = interpolate.splev(t, tck, der=0)
    line = list(zip(line[0].tolist(), line[1].tolist()))
    if (direction == 'u'):
        self.getULines()[number] = line
    elif (direction == 'v'):
        for (i, uline) in enumerate(self.getULines()):
            self.getULines()[i][number] = line[i]
