from PyQt4 import QtGui, QtCore
import sys
import ui_main
import numpy as np
import pylab
import time


def update(self):
    t1 = time.time()
    points = 100
    X = np.arange(points)
    Y = np.sin(((((np.arange(points) / points) * 3) * np.pi) + time.time()))
    C = pylab.cm.jet(((time.time() % 10) / 10))
    self.matplotlibwidget.axes.plot(X, Y, ms=100, color=C, lw=10, alpha=0.8)
    self.matplotlibwidget.axes.grid()
    self.matplotlibwidget.axes.get_figure().tight_layout()
    self.matplotlibwidget.draw()
    print(('update took %.02f ms' % ((time.time() - t1) * 1000)))
    if self.chkMore.isChecked():
        QtCore.QTimer.singleShot(10, self.update)
