import warnings
import matplotlib.pyplot as plt
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
import torch
from mmcv.parallel import collate, scatter
from mmcv.runner import load_checkpoint
from mmdet.core import get_classes
from mmdet.datasets.pipelines import Compose
from mmdet.models import build_detector


def show_result(img, result, class_names, score_thr=0.3, wait_time=0, show=True, out_file=None):
    'Visualize the detection results on the image.\n\n    Args:\n        img (str or np.ndarray): Image filename or loaded image.\n        result (tuple[list] or list): The detection result, can be either\n            (bbox, segm) or just bbox.\n        class_names (list[str] or tuple[str]): A list of class names.\n        score_thr (float): The threshold to visualize the bboxes and masks.\n        wait_time (int): Value of waitKey param.\n        show (bool, optional): Whether to show the image with opencv or not.\n        out_file (str, optional): If specified, the visualization result will\n            be written to the out file instead of shown in a window.\n\n    Returns:\n        np.ndarray or None: If neither `show` nor `out_file` is specified, the\n            visualized image is returned, otherwise None is returned.\n    '
    assert isinstance(class_names, (tuple, list))
    img = mmcv.imread(img)
    img = img.copy()
    if isinstance(result, tuple):
        (bbox_result, segm_result) = result
    else:
        (bbox_result, segm_result) = (result, None)
    bboxes = np.vstack(bbox_result)
    labels = [np.full(bbox.shape[0], i, dtype=np.int32) for (i, bbox) in enumerate(bbox_result)]
    labels = np.concatenate(labels)
    if (segm_result is not None):
        segms = mmcv.concat_list(segm_result)
        inds = np.where((bboxes[:, (- 1)] > score_thr))[0]
        np.random.seed(42)
        color_masks = [np.random.randint(0, 256, (1, 3), dtype=np.uint8) for _ in range((max(labels) + 1))]
        for i in inds:
            i = int(i)
            color_mask = color_masks[labels[i]]
            mask = maskUtils.decode(segms[i]).astype(np.bool)
            img[mask] = ((img[mask] * 0.5) + (color_mask * 0.5))
    mmcv.imshow_det_bboxes(img, bboxes, labels, class_names=class_names, score_thr=score_thr, show=show, wait_time=wait_time, out_file=out_file)
    if (not (show or out_file)):
        return img