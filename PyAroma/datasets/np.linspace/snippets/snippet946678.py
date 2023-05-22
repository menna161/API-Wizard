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


def TunnelMesh(self, name='', tunnel_height=2.0, divisions_height=100, ratio_height=10.0, dist='symmetric', smoothing_algorithm='simple', smoothing_iterations=10, smoothing_tolerance=0.001):
    block_tunnel = BlockMesh(name=name)
    self.tunnel_height = tunnel_height
    line = self.block_te.getVLines()[(- 1)]
    line.reverse()
    del line[(- 1)]
    line += self.block_airfoil.getULines()[(- 1)]
    del line[(- 1)]
    line += self.block_te.getVLines()[0]
    block_tunnel.addLine(line)
    p1 = np.array((block_tunnel.getULines()[0][0][0], tunnel_height))
    p2 = np.array((0.0, tunnel_height))
    p3 = np.array((0.0, (- tunnel_height)))
    p4 = np.array((block_tunnel.getULines()[0][(- 1)][0], (- tunnel_height)))
    line = list()
    vec = (p2 - p1)
    for t in np.linspace(0.0, 1.0, 10):
        p = (p1 + (t * vec))
        line.append(p.tolist())
    del line[(- 1)]
    for phi in np.linspace(90.0, 270.0, 200):
        phir = np.radians(phi)
        x = (tunnel_height * np.cos(phir))
        y = (tunnel_height * np.sin(phir))
        line.append((x, y))
    del line[(- 1)]
    vec = (p4 - p3)
    for t in np.linspace(0.0, 1.0, 10):
        p = (p3 + (t * vec))
        line.append(p.tolist())
    line = np.array(line)
    (tck, _) = interpolate.splprep(line.T, s=0, k=1)
    if (dist == 'symmetric'):
        ld = (- 1.3)
        ud = 1.3
    if (dist == 'lower'):
        ld = (- 1.2)
        ud = 1.5
    if (dist == 'upper'):
        ld = (- 1.5)
        ud = 1.2
    xx = np.linspace(ld, ud, len(block_tunnel.getULines()[0]))
    t = ((np.tanh(xx) + 1.0) / 2.0)
    (xs, ys) = interpolate.splev(t, tck, der=0)
    line = list(zip(xs.tolist(), ys.tolist()))
    block_tunnel.addLine(line)
    p5 = np.array(block_tunnel.getULines()[0][0])
    p6 = np.array(block_tunnel.getULines()[0][(- 1)])
    vline1 = BlockMesh.makeLine(p5, p1, divisions=divisions_height, ratio=ratio_height)
    vline2 = BlockMesh.makeLine(p6, p4, divisions=divisions_height, ratio=ratio_height)
    boundary = [block_tunnel.getULines()[0], block_tunnel.getULines()[(- 1)], vline1, vline2]
    block_tunnel.transfinite(boundary=boundary)
    ulines = list()
    old_ulines = block_tunnel.getULines()
    for (j, uline) in enumerate(block_tunnel.getULines()):
        if ((j == 0) or (j == (len(block_tunnel.getULines()) - 1))):
            ulines.append(uline)
            continue
        line = list()
        (xo, yo) = list(zip(*old_ulines[0]))
        xo = np.array(xo)
        yo = np.array(yo)
        normals = BlockMesh.curveNormals(xo, yo)
        for (i, point) in enumerate(uline):
            if ((i == 0) or (i == (len(uline) - 1))):
                line.append(point)
                continue
            pt = np.array(old_ulines[j][i])
            pto = np.array(old_ulines[0][i])
            vec = (pt - pto)
            dist = (np.dot(vec, normals[i]) / np.linalg.norm(normals[i]))
            pn = (pto + (dist * normals[i]))
            v = (float(j) / float(len(block_tunnel.getULines())))
            exp = 0.6
            pnew = (((1.0 - (v ** exp)) * pn) + ((v ** exp) * pt))
            line.append((pnew.tolist()[0], pnew.tolist()[1]))
        ulines.append(line)
    block_tunnel = BlockMesh(name=name)
    for uline in ulines:
        block_tunnel.addLine(uline)
    ij = [0, 30, 0, (len(block_tunnel.getULines()) - 1)]
    block_tunnel.transfinite(ij=ij)
    ij = [(len(block_tunnel.getVLines()) - 31), (len(block_tunnel.getVLines()) - 1), 0, (len(block_tunnel.getULines()) - 1)]
    block_tunnel.transfinite(ij=ij)
    if (smoothing_algorithm == 'simple'):
        smooth = Smooth(block_tunnel)
        nodes = smooth.selectNodes(domain='interior')
        block_tunnel = smooth.smooth(nodes, iterations=1, algorithm='laplace')
        ij = [1, 30, 1, (len(block_tunnel.getULines()) - 2)]
        nodes = smooth.selectNodes(domain='ij', ij=ij)
        block_tunnel = smooth.smooth(nodes, iterations=2, algorithm='laplace')
        ij = [(len(block_tunnel.getVLines()) - 31), (len(block_tunnel.getVLines()) - 2), 1, (len(block_tunnel.getULines()) - 2)]
        nodes = smooth.selectNodes(domain='ij', ij=ij)
        block_tunnel = smooth.smooth(nodes, iterations=3, algorithm='laplace')
    elif (smoothing_algorithm == 'elliptic'):
        smoother = Elliptic.Elliptic(block_tunnel.getULines())
        new_ulines = smoother.smooth(iterations=smoothing_iterations, tolerance=smoothing_tolerance, bnd_type=None, verbose=True)
        block_tunnel.setUlines(new_ulines)
    elif (smoothing_algorithm == 'angle_based'):
        smoother = SmoothAngleBased(block_tunnel, data_source='block')
        smoothed_vertices = smoother.smooth(iterations=smoothing_iterations, tolerance=smoothing_tolerance, verbose=True)
        new_ulines = smoother.mapToUlines(smoothed_vertices)
        block_tunnel.setUlines(new_ulines)
    self.block_tunnel = block_tunnel
    self.blocks.append(block_tunnel)
