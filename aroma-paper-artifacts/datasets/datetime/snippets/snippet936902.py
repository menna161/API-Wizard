import torch
import cv2
import os
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from network.utils import bbox_iou
from datetime import datetime
import multiprocessing
from scipy.optimize import linear_sum_assignment


def track_tube_iou(track_boxes, tube_boxes):
    track_boxes = np.atleast_3d(track_boxes).astype(np.float)
    tube_boxes = np.atleast_2d(tube_boxes).astype(np.float)

    def track_tube_overlaps(bboxes1, bboxes2):
        lt = np.maximum(np.minimum(bboxes1[(:, :, :2)], bboxes1[(:, :, 2:)]), np.minimum(bboxes2[(:, :2)], bboxes2[(:, 2:)]))
        rb = np.minimum(np.maximum(bboxes1[(:, :, 2:)], bboxes1[(:, :, :2)]), np.maximum(bboxes2[(:, 2:)], bboxes2[(:, :2)]))
        wh = np.clip((rb - lt), 0, None)
        overlap = (wh[(:, :, 0)] * wh[(:, :, 1)])
        return overlap
    overlap = track_tube_overlaps(track_boxes, tube_boxes)
    area1 = ((track_boxes[(:, :, 2)] - track_boxes[(:, :, 0)]) * (track_boxes[(:, :, 3)] - track_boxes[(:, :, 1)]))
    area1 = np.abs(area1)
    area2 = ((tube_boxes[(:, 2)] - tube_boxes[(:, 0)]) * (tube_boxes[(:, 3)] - tube_boxes[(:, 1)]))
    area2 = np.abs(area2)
    ious = (overlap / ((area1 + area2) - overlap))
    return ious
