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


def track_tube_overlaps(bboxes1, bboxes2):
    lt = np.maximum(np.minimum(bboxes1[(:, :, :2)], bboxes1[(:, :, 2:)]), np.minimum(bboxes2[(:, :2)], bboxes2[(:, 2:)]))
    rb = np.minimum(np.maximum(bboxes1[(:, :, 2:)], bboxes1[(:, :, :2)]), np.maximum(bboxes2[(:, 2:)], bboxes2[(:, :2)]))
    wh = np.clip((rb - lt), 0, None)
    overlap = (wh[(:, :, 0)] * wh[(:, :, 1)])
    return overlap
