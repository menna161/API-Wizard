import copy
import numpy as np
from scipy import interpolate
from PySide6 import QtGui, QtCore
from Utils import Utils
import GraphicsItemsCollection as gic
import GraphicsItem
import logging


def getCamberThickness(self, spline_data, le_id):
    u_le = spline_data[1][(le_id - 3)]
    upper = np.linspace(u_le, 0.0, 300)
    lower = np.linspace(u_le, 1.0, 300)
    tck = spline_data[5]
    coo_upper = interpolate.splev(upper, tck, der=0)
    coo_lower = interpolate.splev(lower, tck, der=0)
    camber = (0.5 * (np.array(coo_upper) + np.array(coo_lower)))
    thickness = (np.array(coo_upper) - np.array(coo_lower))
    max_camber = np.max(camber[1])
    pos_camber = np.where((camber[1] == max_camber))
    max_camber_pos = camber[0][pos_camber][0]
    max_thickness = np.max(thickness)
    pos_thickness = np.where((thickness == max_thickness))[1]
    max_thickness_pos = coo_upper[0][pos_thickness][0]
    logger.info('Maximum thickness: {:5.2f} % at {:5.2f} % chord'.format((max_thickness * 100.0), (max_thickness_pos * 100.0)))
    logger.info('Maximum camber: {:5.2f} % at {:5.2f} % chord'.format((max_camber * 100.0), (max_camber_pos * 100.0)))
    return camber
