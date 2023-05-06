from __future__ import division
import numpy as np
import chainer
from testcases.elichika_tests.chainercv_model import transforms


def mask_to_segm(mask, bbox, segm_size, index=None):
    'Crop and resize mask.\n\n    This function requires cv2.\n\n    Args:\n        mask (~numpy.ndarray): See below.\n        bbox (~numpy.ndarray): See below.\n        segm_size (int): The size of segm :math:`S`.\n        index (~numpy.ndarray): See below. :math:`R = N` when\n            :obj:`index` is :obj:`None`.\n\n    Returns:\n        ~numpy.ndarray: See below.\n\n    .. csv-table::\n        :header: name, shape, dtype, format\n\n        :obj:`mask`, ":math:`(N, H, W)`", :obj:`bool`, --\n        :obj:`bbox`, ":math:`(R, 4)`", :obj:`float32`,         ":math:`(y_{min}, x_{min}, y_{max}, x_{max})`"\n        :obj:`index` (optional), ":math:`(R,)`", :obj:`int32`, --\n        :obj:`segms` (output), ":math:`(R, S, S)`", :obj:`float32`,         ":math:`[0, 1]`"\n\n    '
    pad = 1
    (_, H, W) = mask.shape
    bbox = chainer.backends.cuda.to_cpu(bbox)
    padded_segm_size = (segm_size + (pad * 2))
    expand_scale = (padded_segm_size / segm_size)
    bbox = _expand_bbox(bbox, expand_scale)
    resize_size = padded_segm_size
    bbox = _integerize_bbox(bbox)
    segm = []
    if (index is None):
        index = np.arange(len(bbox))
    else:
        index = chainer.backends.cuda.to_cpu(index)
    for (i, bb) in zip(index, bbox):
        y_min = max(bb[0], 0)
        x_min = max(bb[1], 0)
        y_max = max(min(bb[2], H), 0)
        x_max = max(min(bb[3], W), 0)
        if ((y_max <= y_min) or (x_max <= x_min)):
            segm.append(np.zeros((segm_size, segm_size), dtype=np.float32))
            continue
        bb_height = (bb[2] - bb[0])
        bb_width = (bb[3] - bb[1])
        cropped_m = np.zeros((bb_height, bb_width), dtype=np.bool)
        y_offset = (y_min - bb[0])
        x_offset = (x_min - bb[1])
        cropped_m[(y_offset:((y_offset + y_max) - y_min), x_offset:((x_offset + x_max) - x_min))] = chainer.backends.cuda.to_cpu(mask[(i, y_min:y_max, x_min:x_max)])
        with chainer.using_config('cv_resize_backend', 'cv2'):
            sgm = transforms.resize(cropped_m[None].astype(np.float32), (resize_size, resize_size))[0].astype(np.int32)
        segm.append(sgm[(pad:(- pad), pad:(- pad))])
    return np.array(segm, dtype=np.float32)
