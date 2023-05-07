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


def get_shape_diff(track_boxes, tube_boxes):
    track_boxes = np.atleast_3d(track_boxes).astype(np.float)
    tube_boxes = np.atleast_2d(tube_boxes).astype(np.float)
    track_height = (track_boxes[(:, :, 2)] - track_boxes[(:, :, 0)])
    track_width = (track_boxes[(:, :, 3)] - track_boxes[(:, :, 1)])
    tube_height = (tube_boxes[(:, 2)] - tube_boxes[(:, 0)])
    tube_width = (tube_boxes[(:, 3)] - tube_boxes[(:, 1)])
    diff = ((np.abs((track_height - tube_height)) / (track_height + tube_height)) + (np.abs((track_width - tube_width)) / (track_width + tube_width)))
    return np.exp((1.5 * (- diff)))
