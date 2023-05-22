import mmcv
import numpy as np
from terminaltables import AsciiTable
from .bbox_overlaps import bbox_overlaps
from .class_names import get_classes


def average_precision(recalls, precisions, mode='area'):
    "Calculate average precision (for single or multiple scales).\n\n    Args:\n        recalls (ndarray): shape (num_scales, num_dets) or (num_dets, )\n        precisions (ndarray): shape (num_scales, num_dets) or (num_dets, )\n        mode (str): 'area' or '11points', 'area' means calculating the area\n            under precision-recall curve, '11points' means calculating\n            the average precision of recalls at [0, 0.1, ..., 1]\n\n    Returns:\n        float or ndarray: calculated average precision\n    "
    no_scale = False
    if (recalls.ndim == 1):
        no_scale = True
        recalls = recalls[(np.newaxis, :)]
        precisions = precisions[(np.newaxis, :)]
    assert ((recalls.shape == precisions.shape) and (recalls.ndim == 2))
    num_scales = recalls.shape[0]
    ap = np.zeros(num_scales, dtype=np.float32)
    if (mode == 'area'):
        zeros = np.zeros((num_scales, 1), dtype=recalls.dtype)
        ones = np.ones((num_scales, 1), dtype=recalls.dtype)
        mrec = np.hstack((zeros, recalls, ones))
        mpre = np.hstack((zeros, precisions, zeros))
        for i in range((mpre.shape[1] - 1), 0, (- 1)):
            mpre[(:, (i - 1))] = np.maximum(mpre[(:, (i - 1))], mpre[(:, i)])
        for i in range(num_scales):
            ind = np.where((mrec[(i, 1:)] != mrec[(i, :(- 1))]))[0]
            ap[i] = np.sum(((mrec[(i, (ind + 1))] - mrec[(i, ind)]) * mpre[(i, (ind + 1))]))
    elif (mode == '11points'):
        for i in range(num_scales):
            for thr in np.arange(0, (1 + 0.001), 0.1):
                precs = precisions[(i, (recalls[(i, :)] >= thr))]
                prec = (precs.max() if (precs.size > 0) else 0)
                ap[i] += prec
            ap /= 11
    else:
        raise ValueError('Unrecognized mode, only "area" and "11points" are supported')
    if no_scale:
        ap = ap[0]
    return ap
