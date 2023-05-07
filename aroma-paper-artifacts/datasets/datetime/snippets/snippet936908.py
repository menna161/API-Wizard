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


def adjust_poi_tubes(tubes, poi_tubes):

    def adjust_single_frame(tubes, poi_tubes):
        tubes_end_mask = (tubes[(:, 5)] > tubes[(:, 0)])
        trans_x_end = (((tubes[tubes_end_mask][(:, 6)] + tubes[tubes_end_mask][(:, 8)]) / 2) - ((tubes[tubes_end_mask][(:, 1)] + tubes[tubes_end_mask][(:, 3)]) / 2))
        trans_y_end = (((tubes[tubes_end_mask][(:, 7)] + tubes[tubes_end_mask][(:, 9)]) / 2) - ((tubes[tubes_end_mask][(:, 2)] + tubes[tubes_end_mask][(:, 4)]) / 2))
        trans_x_end = (trans_x_end / (tubes[tubes_end_mask][(:, 5)] - tubes[tubes_end_mask][(:, 0)]))
        trans_y_end = (trans_y_end / (tubes[tubes_end_mask][(:, 5)] - tubes[tubes_end_mask][(:, 0)]))
        mean_trans_x_end = np.mean((trans_x_end / (tubes[tubes_end_mask][(:, 7)] - tubes[tubes_end_mask][(:, 9)])))
        mean_trans_y_end = np.mean((trans_y_end / (tubes[tubes_end_mask][(:, 7)] - tubes[tubes_end_mask][(:, 9)])))
        poi_tubes[(:, [6, 8])] += ((mean_trans_x_end * (poi_tubes[(:, 5)] - poi_tubes[(:, 0)])) * (poi_tubes[(:, 7)] - poi_tubes[(:, 9)]))[(:, None)]
        poi_tubes[(:, [7, 9])] += ((mean_trans_y_end * (poi_tubes[(:, 5)] - poi_tubes[(:, 0)])) * (poi_tubes[(:, 7)] - poi_tubes[(:, 9)]))[(:, None)]
        tubes_start_mask = (tubes[(:, 10)] < tubes[(:, 0)])
        trans_x_start = (((tubes[tubes_start_mask][(:, 11)] + tubes[tubes_start_mask][(:, 13)]) / 2) - ((tubes[tubes_start_mask][(:, 1)] + tubes[tubes_start_mask][(:, 3)]) / 2))
        trans_y_start = (((tubes[tubes_start_mask][(:, 12)] + tubes[tubes_start_mask][(:, 14)]) / 2) - ((tubes[tubes_start_mask][(:, 2)] + tubes[tubes_start_mask][(:, 4)]) / 2))
        trans_x_start = (trans_x_start / (tubes[tubes_start_mask][(:, 10)] - tubes[tubes_start_mask][(:, 0)]))
        trans_y_start = (trans_y_start / (tubes[tubes_start_mask][(:, 10)] - tubes[tubes_start_mask][(:, 0)]))
        mean_trans_x_start = np.mean((trans_x_start / (tubes[tubes_start_mask][(:, 12)] - tubes[tubes_start_mask][(:, 14)])))
        mean_trans_y_start = np.mean((trans_y_start / (tubes[tubes_start_mask][(:, 12)] - tubes[tubes_start_mask][(:, 14)])))
        poi_tubes[(:, [11, 13])] += ((mean_trans_x_start * (poi_tubes[(:, 10)] - poi_tubes[(:, 0)])) * (poi_tubes[(:, 12)] - poi_tubes[(:, 14)]))[(:, None)]
        poi_tubes[(:, [12, 14])] += ((mean_trans_y_start * (poi_tubes[(:, 10)] - poi_tubes[(:, 0)])) * (poi_tubes[(:, 12)] - poi_tubes[(:, 14)]))[(:, None)]
        return poi_tubes
    frame_idxs = np.unique(tubes[(:, 0)])
    for frame_idx in frame_idxs:
        poi_tubes[(poi_tubes[(:, 0)] == frame_idx)] = adjust_single_frame(tubes[(tubes[(:, 0)] == frame_idx)], poi_tubes[(poi_tubes[(:, 0)] == frame_idx)])
    return poi_tubes
