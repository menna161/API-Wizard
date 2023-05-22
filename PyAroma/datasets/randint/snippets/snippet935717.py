from collections import Sequence
import matplotlib.pyplot as plt
import mmcv
import numpy as np
import torch


def random_scale(img_scales, mode='range'):
    'Randomly select a scale from a list of scales or scale ranges.\n\n    Args:\n        img_scales (list[tuple]): Image scale or scale range.\n        mode (str): "range" or "value".\n\n    Returns:\n        tuple: Sampled image scale.\n    '
    num_scales = len(img_scales)
    if (num_scales == 1):
        img_scale = img_scales[0]
    elif (num_scales == 2):
        if (mode == 'range'):
            img_scale_long = [max(s) for s in img_scales]
            img_scale_short = [min(s) for s in img_scales]
            long_edge = np.random.randint(min(img_scale_long), (max(img_scale_long) + 1))
            short_edge = np.random.randint(min(img_scale_short), (max(img_scale_short) + 1))
            img_scale = (long_edge, short_edge)
        elif (mode == 'value'):
            img_scale = img_scales[np.random.randint(num_scales)]
    else:
        if (mode != 'value'):
            raise ValueError('Only "value" mode supports more than 2 image scales')
        img_scale = img_scales[np.random.randint(num_scales)]
    return img_scale
