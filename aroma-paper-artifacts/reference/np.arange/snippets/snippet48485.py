from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
import random


def draw_dense_reg(regmap, heatmap, center, value, radius, is_offset=False):
    diameter = ((2 * radius) + 1)
    gaussian = gaussian2D((diameter, diameter), sigma=(diameter / 6))
    value = np.array(value, dtype=np.float32).reshape((- 1), 1, 1)
    dim = value.shape[0]
    reg = (np.ones((dim, ((diameter * 2) + 1), ((diameter * 2) + 1)), dtype=np.float32) * value)
    if (is_offset and (dim == 2)):
        delta = (np.arange(((diameter * 2) + 1)) - radius)
        reg[0] = (reg[0] - delta.reshape(1, (- 1)))
        reg[1] = (reg[1] - delta.reshape((- 1), 1))
    (x, y) = (int(center[0]), int(center[1]))
    (height, width) = heatmap.shape[0:2]
    (left, right) = (min(x, radius), min((width - x), (radius + 1)))
    (top, bottom) = (min(y, radius), min((height - y), (radius + 1)))
    masked_heatmap = heatmap[((y - top):(y + bottom), (x - left):(x + right))]
    masked_regmap = regmap[(:, (y - top):(y + bottom), (x - left):(x + right))]
    masked_gaussian = gaussian[((radius - top):(radius + bottom), (radius - left):(radius + right))]
    masked_reg = reg[(:, (radius - top):(radius + bottom), (radius - left):(radius + right))]
    if ((min(masked_gaussian.shape) > 0) and (min(masked_heatmap.shape) > 0)):
        idx = (masked_gaussian >= masked_heatmap).reshape(1, masked_gaussian.shape[0], masked_gaussian.shape[1])
        masked_regmap = (((1 - idx) * masked_regmap) + (idx * masked_reg))
    regmap[(:, (y - top):(y + bottom), (x - left):(x + right))] = masked_regmap
    return regmap
