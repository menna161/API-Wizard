from __future__ import print_function
import torch
import torch.backends.cudnn as cudnn
import numpy as np
import cv2
import os
import pandas as pd
import copy
import time
import torchvision
from face_detect_lib.models.retinaface import RetinaFace
from face_detect_lib.layers.functions.prior_box import PriorBox
from face_detect_lib.utils.box_utils import decode_batch, decode_landm_batch, decode, decode_landm
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from functools import partial
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from torch.nn import init
import torch.nn as nn
import math
import re
import math
import collections
from functools import partial
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import model_zoo
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from torch.nn import init
import torch.nn as nn
import math
import torch
import torchvision.models.resnet as resnet


def detect_video_face(img_list, detect_record):
    num_frames = len(img_list)
    num_faces = 0
    face_count = {}
    (img_h, img_w) = (img_list[0].shape[0], img_list[0].shape[1])
    face_list = []
    detect_tmp_begin = time.time()
    dets_list = detect_face(img_list, detect_record)
    detect_tmp_end = time.time()
    detect_face_time = (detect_tmp_end - detect_tmp_begin)
    global DETECT_FACE_TIME
    DETECT_FACE_TIME += detect_face_time
    print('detect face time:', detect_face_time)
    align_begin = time.time()
    for (idx, img_raw) in enumerate(img_list):
        dets = dets_list[idx][np.where((dets_list[idx][(:, 4)] >= pipeline_cfg.vis_thres))][(:, :4)].astype(np.int64)
        face_list.append(dets)
        if (len(dets) not in face_count):
            face_count[len(dets)] = 0
        face_count[len(dets)] += 1
    face_align_begin = time.time()
    max_count = 0
    for num in face_count:
        if (face_count[num] > max_count):
            num_faces = num
            max_count = face_count[num]
    if (num_faces <= 0):
        return (None, (- 1))
    active_faces = None
    face_tubes = []
    for frame_idx in range(num_frames):
        cur_faces = face_list[frame_idx]
        if (len(cur_faces) <= 0):
            continue
        if (active_faces is not None):
            ious = vanilla_bbox_iou_overlaps(cur_faces, active_faces)
            (max_iou, max_idx) = (np.max(ious, axis=1), np.argmax(ious, axis=1))
            mark = [False for _ in range(len(active_faces))]
        else:
            (max_iou, max_idx) = (None, None)
        for face_idx in range(len(cur_faces)):
            if ((max_iou is None) or (max_iou[face_idx] < 0.5)):
                face = copy.deepcopy(cur_faces[face_idx])
                if (active_faces is None):
                    active_faces = face[(np.newaxis, :)]
                else:
                    active_faces = np.concatenate((active_faces, face[(np.newaxis, :)]), axis=0)
                face_tubes.append([[frame_idx, face_idx]])
            else:
                correspond_idx = max_idx[face_idx]
                if mark[correspond_idx]:
                    continue
                mark[correspond_idx] = True
                active_faces[correspond_idx] = cur_faces[face_idx]
                face_tubes[correspond_idx].append([frame_idx, face_idx])
    face_tubes.sort(key=(lambda tube: len(tube)), reverse=True)
    if (len(face_tubes) < num_faces):
        num_faces = len(face_tubes)
    num_faces = min(num_faces, 2)
    face_tubes = face_tubes[:num_faces]
    (aligned_faces_img_256, aligned_faces_img_299, aligned_faces_img_320) = ([], [], [])
    for face_idx in range(num_faces):
        (cur_face_list, source_frame_list) = ([], [])
        (tube_idx, max_size) = (0, 0)
        for frame_idx in range(num_frames):
            cur_face = face_tubes[face_idx][tube_idx]
            next_face = (None if (tube_idx == (len(face_tubes[face_idx]) - 1)) else face_tubes[face_idx][(tube_idx + 1)])
            if ((next_face is not None) and (abs((cur_face[0] - frame_idx)) > abs((next_face[0] - frame_idx)))):
                tube_idx += 1
                cur_face = next_face
            face = copy.deepcopy(face_list[cur_face[0]][cur_face[1]])
            cur_face_list.append(face)
            source_frame_list.append(cur_face[0])
            (_, _, size) = get_boundingbox(face, img_w, img_h)
            if (size > max_size):
                max_size = size
        max_size = ((max_size // 2) * 2)
        max_size = min(max_size, img_w, img_h)
        (cur_faces_img_256, cur_faces_img_299, cur_faces_img_320) = ([], [], [])
        for frame_idx in range(num_frames):
            (x1, y1, size) = adjust_boundingbox(cur_face_list[frame_idx], img_w, img_h, max_size)
            img = img_list[source_frame_list[frame_idx]][(y1:(y1 + size), x1:(x1 + size), :)]
            img_256 = cv2.resize(img, (256, 256), interpolation=cv2.INTER_LINEAR)
            cur_faces_img_256.append(img_256)
            img_299 = cv2.resize(img, (299, 299), interpolation=cv2.INTER_LINEAR)
            cur_faces_img_299.append(img_299)
        cur_faces_numpy_256 = np.stack(cur_faces_img_256, axis=0)
        cur_faces_numpy_299 = np.stack(cur_faces_img_299, axis=0)
        aligned_faces_img_256.append(cur_faces_numpy_256)
        aligned_faces_img_299.append(cur_faces_numpy_299)
    aligned_faces_numpy_256 = np.stack(aligned_faces_img_256, axis=0)
    aligned_faces_numpy_299 = np.stack(aligned_faces_img_299, axis=0)
    align_end = time.time()
    print('align_time:256 299', (align_end - align_begin))
    return ([aligned_faces_numpy_256, aligned_faces_numpy_299], 1)
