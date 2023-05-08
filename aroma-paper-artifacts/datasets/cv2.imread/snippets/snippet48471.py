from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
from .ddd_utils import compute_box_3d, project_to_image, draw_box_3d
import matplotlib.pyplot as plt
import sys


def compose_vis_add(self, img_path, dets, calib, center_thresh, pred, bev, img_id='out'):
    self.imgs[img_id] = cv2.imread(img_path)
    (h, w) = pred.shape[:2]
    (hs, ws) = ((self.imgs[img_id].shape[0] / h), (self.imgs[img_id].shape[1] / w))
    self.imgs[img_id] = cv2.resize(self.imgs[img_id], (w, h))
    self.add_blend_img(self.imgs[img_id], pred, img_id)
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
                    box_2d[(:, 0)] /= hs
                    box_2d[(:, 1)] /= ws
                    self.imgs[img_id] = draw_box_3d(self.imgs[img_id], box_2d, cl)
    self.imgs[img_id] = np.concatenate([self.imgs[img_id], self.imgs[bev]], axis=1)