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


def MeshQuality(self, crit='k2inf'):
    (vertices, connectivity) = self.mesh
    if (crit == 'k2inf'):
        v12 = (vertices[connectivity[(:, 1)]] - vertices[connectivity[(:, 0)]])
        v23 = (vertices[connectivity[(:, 2)]] - vertices[connectivity[(:, 1)]])
        v34 = (vertices[connectivity[(:, 3)]] - vertices[connectivity[(:, 2)]])
        v41 = (vertices[connectivity[(:, 0)]] - vertices[connectivity[(:, 3)]])
        a = np.linalg.norm(v12)
        b = np.linalg.norm(v23)
        c = np.linalg.norm(v34)
        d = np.linalg.norm(v41)
        p = (0.5 * (((a + b) + c) + d))
        q2 = np.sqrt(((((a ** 2) + (b ** 2)) + (c ** 2)) + (d ** 2)))
        alpha = Utils.angle_between(v12, (- v41))
        beta = Utils.angle_between(v23, (- v12))
        gamma = Utils.angle_between(v34, (- v23))
        delta = Utils.angle_between(v41, (- v12))
        theta = (0.5 * (alpha + gamma))
        A = np.sqrt((((((p - a) * (p - b)) * (p - c)) * (p - d)) - ((((a * b) * c) * d) * np.cos(theta))))
        ka = (((a ** 2) + (d ** 2)) / ((a * d) * np.sin(alpha)))
        kb = (((a ** 2) + (b ** 2)) / ((a * b) * np.sin(beta)))
        kc = (((b ** 2) + (c ** 2)) / ((b * c) * np.sin(gamma)))
        kd = (((c ** 2) + (d ** 2)) / ((c * d) * np.sin(delta)))
        k = np.stack((ka, kb, kc, kd))
        quality = (np.max(k, axis=0) / 2.0)
    self.mesh.quality = quality
    return self.mesh.quality
