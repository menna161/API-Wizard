from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
from .ddd_utils import compute_box_3d, project_to_image, draw_box_3d
import matplotlib.pyplot as plt
import sys


def add_3d_detection(self, image_or_path, dets, calib, show_txt=False, center_thresh=0.5, img_id='det'):
    if isinstance(image_or_path, np.ndarray):
        self.imgs[img_id] = image_or_path
    else:
        self.imgs[img_id] = cv2.imread(image_or_path)
    for cat in dets:
        for i in range(len(dets[cat])):
            cl = self.colors[((cat - 1), 0, 0)].tolist()
            if (dets[cat][(i, (- 1))] > center_thresh):
                dim = dets[cat][(i, 5:8)]
                loc = dets[cat][(i, 8:11)]
                rot_y = dets[cat][(i, 11)]
                if (loc[2] > 1):
                    box_3d = compute_box_3d(dim, loc, rot_y)
                    box_2d = project_to_image(box_3d, calib)
                    self.imgs[img_id] = draw_box_3d(self.imgs[img_id], box_2d, cl)
