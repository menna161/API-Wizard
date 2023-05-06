from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
import random


def draw_msra_gaussian(heatmap, center, sigma):
    tmp_size = (sigma * 3)
    mu_x = int((center[0] + 0.5))
    mu_y = int((center[1] + 0.5))
    (w, h) = (heatmap.shape[0], heatmap.shape[1])
    ul = [int((mu_x - tmp_size)), int((mu_y - tmp_size))]
    br = [int(((mu_x + tmp_size) + 1)), int(((mu_y + tmp_size) + 1))]
    if ((ul[0] >= h) or (ul[1] >= w) or (br[0] < 0) or (br[1] < 0)):
        return heatmap
    size = ((2 * tmp_size) + 1)
    x = np.arange(0, size, 1, np.float32)
    y = x[(:, np.newaxis)]
    x0 = y0 = (size // 2)
    g = np.exp(((- (((x - x0) ** 2) + ((y - y0) ** 2))) / (2 * (sigma ** 2))))
    g_x = (max(0, (- ul[0])), (min(br[0], h) - ul[0]))
    g_y = (max(0, (- ul[1])), (min(br[1], w) - ul[1]))
    img_x = (max(0, ul[0]), min(br[0], h))
    img_y = (max(0, ul[1]), min(br[1], w))
    heatmap[(img_y[0]:img_y[1], img_x[0]:img_x[1])] = np.maximum(heatmap[(img_y[0]:img_y[1], img_x[0]:img_x[1])], g[(g_y[0]:g_y[1], g_x[0]:g_x[1])])
    return heatmap
