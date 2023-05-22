from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
from .ddd_utils import compute_box_3d, project_to_image, draw_box_3d
import matplotlib.pyplot as plt
import sys


def show_img(self, pause=False, imgId='default'):
    cv2.imshow('{}'.format(imgId), self.imgs[imgId])
    if pause:
        cv2.waitKey()
