import numpy as np
from PySide6 import QtGui, QtCore
import GraphicsItemsCollection as gic
import GraphicsItem
import logging


def makeChord(self):
    line = gic.GraphicsCollection()
    color = QtGui.QColor(52, 235, 122, 255)
    line.pen.setColor(color)
    line.pen.setWidthF(2.5)
    line.pen.setCosmetic(True)
    line.pen.setStyle(QtCore.Qt.CustomDashLine)
    stroke = 10
    dot = 1
    space = 5
    line.pen.setDashPattern([stroke, space, dot, space])
    index_min = np.argmin(self.raw_coordinates[0])
    index_max = np.argmax(self.raw_coordinates[0])
    x1 = self.raw_coordinates[0][index_min]
    y1 = self.raw_coordinates[1][index_min]
    x2 = self.raw_coordinates[0][index_max]
    y2 = self.raw_coordinates[1][index_max]
    line.Line(x1, y1, x2, y2)
    self.chord = GraphicsItem.GraphicsItem(line)
    self.chord.setZValue(99)
    self.chord.setAcceptHoverEvents(False)
