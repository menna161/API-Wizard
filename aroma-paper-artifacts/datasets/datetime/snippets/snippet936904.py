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


def update_tracks_fast(tracks, tube, arg):
    mid_frame = tube[0].astype(np.int)
    mid_box = tube[1:5]
    end_frame = tube[5].astype(np.int)
    end_box = tube[6:10]
    start_frame = tube[10].astype(np.int)
    start_box = tube[11:15]
    score = tube[15]

    def get_center(box):
        return np.array((((box[0] + box[2]) / 2), ((box[1] + box[3]) / 2)))
    back_frames = np.arange(start_frame, mid_frame)
    front_frames = np.arange((mid_frame + 1), (end_frame + 1))
    all_tube_frames = np.arange(start_frame, (end_frame + 1))
    back_start_coef = ((mid_frame - back_frames) / (mid_frame - start_frame))
    back_mid_coef = ((back_frames - start_frame) / (mid_frame - start_frame))
    front_mid_coef = ((end_frame - front_frames) / (end_frame - mid_frame))
    front_end_coef = ((front_frames - mid_frame) / (end_frame - mid_frame))
    back_frame_boxes = (np.outer(back_start_coef, start_box) + np.outer(back_mid_coef, mid_box))
    front_frame_boxes = (np.outer(front_end_coef, end_box) + np.outer(front_mid_coef, mid_box))
    tube_boxes = np.concatenate((back_frame_boxes, mid_box[None], front_frame_boxes))
    tube_frame_num = len(all_tube_frames)
    depth_divider = 8
    tube_direction = np.zeros(3)
    tube_direction[:2] = (get_center(end_box) - get_center(start_box))
    tube_direction[2] = (np.max(all_tube_frames) - np.min(all_tube_frames))
    tube_direction[2] /= depth_divider
    if (len(tracks) == 0):
        new_track = Track()
        new_track.update_frames(all_tube_frames, tube_boxes, mid_frame, mid_box, score, tube_direction)
        tracks.append(new_track)
        return
    all_has_frame = np.zeros((len(tracks), tube_frame_num), dtype=np.bool)
    all_track_boxes = np.zeros((len(tracks), *tube_boxes.shape))
    track_direction = np.zeros((len(tracks), 3))
    for (track_idx, track) in enumerate(tracks):
        if (track.prev_direction is not None):
            track_direction[(track_idx, :)] = track.prev_direction
        for (i, frame) in enumerate(all_tube_frames):
            if (frame not in track.frames):
                continue
            all_has_frame[(track_idx, i)] = True
            all_track_boxes[(track_idx, i, :)] = (track.frames[frame][0] / track.frames[frame][1])
    track_direction[(:, 2)] /= depth_divider
    has_overlap = (np.sum(all_has_frame, axis=1) > 0)
    all_iou = np.zeros(all_has_frame.shape, dtype=np.float)
    shape_diff = np.zeros(all_has_frame.shape, dtype=np.float)
    all_iou[has_overlap] = track_tube_iou(all_track_boxes[has_overlap], tube_boxes)
    shape_diff[has_overlap] = get_shape_diff(all_track_boxes[has_overlap], tube_boxes)
    mean_all_iou = np.zeros(has_overlap.shape, dtype=np.float)
    mean_all_iou[has_overlap] = (np.sum(all_iou[has_overlap], axis=1) / np.sum(all_has_frame[has_overlap], axis=1))
    angle_cos = np.ones_like(mean_all_iou)
    norm_mul = (np.linalg.norm(track_direction, axis=1) * np.linalg.norm(tube_direction))
    cos_mask = np.logical_and(has_overlap, (norm_mul > 0))
    angle_cos[cos_mask] = (np.dot(track_direction[cos_mask], tube_direction) / norm_mul[cos_mask])
    mean_all_iou = (mean_all_iou * (1 + (arg.cos_weight * angle_cos)))
    max_idx = np.argmax(mean_all_iou)
    if (mean_all_iou[max_idx] > arg.linking_min_iou):
        tracks[max_idx].update_frames(all_tube_frames, tube_boxes, mid_frame, mid_box, score, tube_direction)
    else:
        new_track = Track()
        new_track.update_frames(all_tube_frames, tube_boxes, mid_frame, mid_box, score, tube_direction)
        tracks.append(new_track)
