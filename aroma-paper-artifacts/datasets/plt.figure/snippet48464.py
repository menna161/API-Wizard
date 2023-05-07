from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
from .ddd_utils import compute_box_3d, project_to_image, draw_box_3d
import matplotlib.pyplot as plt
import sys


def show_all_imgs(self, pause=False, time=0):
    if (not self.ipynb):
        for (i, v) in self.imgs.items():
            cv2.imshow('{}'.format(i), v)
        if (cv2.waitKey((0 if pause else 1)) == 27):
            import sys
            sys.exit(0)
    else:
        self.ax = None
        nImgs = len(self.imgs)
        fig = self.plt.figure(figsize=((nImgs * 10), 10))
        nCols = nImgs
        nRows = (nImgs // nCols)
        for (i, (k, v)) in enumerate(self.imgs.items()):
            fig.add_subplot(1, nImgs, (i + 1))
            if (len(v.shape) == 3):
                self.plt.imshow(cv2.cvtColor(v, cv2.COLOR_BGR2RGB))
            else:
                self.plt.imshow(v)
        self.plt.show()
