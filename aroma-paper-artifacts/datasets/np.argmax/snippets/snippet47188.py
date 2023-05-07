import tensorflow as tf
import numpy as np
import collections
from matplotlib.colors import to_rgb
import matplotlib.pyplot as plt
from matplotlib import animation
from dps import cfg
from dps.utils import Param, square_subplots
from dps.utils.tf import build_gradient_train_op, apply_mask_and_group_at_front, build_scheduled_value, FIXED_COLLECTION
from dps.tf.updater import DataManager, Evaluator, TensorRecorder, VideoUpdater as _VideoUpdater
from dps.train import Hook


def mAP(pred_boxes, gt_boxes, n_classes, recall_values=None, iou_threshold=None):
    ' Calculate mean average precision on a dataset.\n\n    Averages over:\n        classes, recall_values, iou_threshold\n\n    pred_boxes: [[class, conf, y_min, y_max, x_min, x_max] * n_boxes] * n_images\n    gt_boxes: [[class, y_min, y_max, x_min, x_max] * n_boxes] * n_images\n\n    '
    if (recall_values is None):
        recall_values = np.linspace(0.0, 1.0, 11)
    if (iou_threshold is None):
        iou_threshold = np.linspace(0.5, 0.95, 10)
    ap = []
    for c in range(n_classes):
        _ap = []
        for iou_thresh in iou_threshold:
            predicted_list = []
            n_positives_gt = 0
            for (pred, gt) in zip(pred_boxes, gt_boxes):
                pred_c = sorted([b for (cls, *b) in pred if (cls == c)], key=(lambda k: (- k[0])))
                area = [((ymax - ymin) * (xmax - xmin)) for (_, ymin, ymax, xmin, xmax) in pred_c]
                pred_c = [(*b, a) for (b, a) in zip(pred_c, area)]
                gt_c = [b for (cls, *b) in gt if (cls == c)]
                n_positives_gt += len(gt_c)
                if (not gt_c):
                    predicted_list.extend(((conf, 0) for (conf, *_) in pred_c))
                    continue
                gt_c = np.array(gt_c)
                gt_c_area = ((gt_c[(:, 1)] - gt_c[(:, 0)]) * (gt_c[(:, 3)] - gt_c[(:, 2)]))
                gt_c = np.concatenate([gt_c, gt_c_area[(..., None)]], axis=1)
                used = ([0] * len(gt_c))
                for (conf, *box) in pred_c:
                    iou = compute_iou(box, gt_c)
                    best_idx = np.argmax(iou)
                    best_iou = iou[best_idx]
                    if ((best_iou > iou_thresh) and (not used[best_idx])):
                        predicted_list.append((conf, 1.0))
                        used[best_idx] = 1
                    else:
                        predicted_list.append((conf, 0.0))
            if (not predicted_list):
                ap.append(0.0)
                continue
            predicted_list = np.array(sorted(predicted_list, key=(lambda k: (- k[0]))), dtype=np.float32)
            cs = np.cumsum(predicted_list[(:, 1)])
            precision = (cs / (np.arange(predicted_list.shape[0]) + 1))
            recall = (cs / n_positives_gt)
            for r in recall_values:
                p = precision[(recall >= r)]
                _ap.append((0.0 if (p.size == 0) else p.max()))
        ap.append((np.mean(_ap) if _ap else 0.0))
    return np.mean(ap)
