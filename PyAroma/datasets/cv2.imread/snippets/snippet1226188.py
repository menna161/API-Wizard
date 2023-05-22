from __future__ import division
import os
import numpy as np
import cv2
from libs import utils
from torch.utils.data import Dataset
import json
from PIL import Image


def make_img_gt_mask_pair(self, idx):
    '\n        Make the image-ground-truth pair\n        '
    prev_round_mask_tmp = self.prevmasks_list[idx]
    if (self.seq_name is None):
        obj_id = self.all_seqs_list[idx][0]
        img_path = self.img_list[self.all_seqs_list[idx][1]]
        label_path = self.labels[self.all_seqs_list[idx][1]]
    else:
        obj_id = self.obj_id
        img_path = self.img_list[idx]
        label_path = self.labels[idx]
    seq_name = img_path.split('/')[(- 2)]
    n_obj = (1 if isinstance(obj_id, int) else len(obj_id))
    img = cv2.imread(os.path.join(self.db_root_dir, img_path))
    img = np.array(img, dtype=np.float32)
    if self.rgb:
        img = img[(:, :, [2, 1, 0])]
    if (label_path is not None):
        label = Image.open(os.path.join(self.db_root_dir, label_path))
    elif self.batch_gt:
        gt = np.zeros(np.append(img.shape[:(- 1)], n_obj), dtype=np.float32)
    else:
        gt = np.zeros(img.shape[:(- 1)], dtype=np.float32)
    if (label_path is not None):
        gt_tmp = np.array(label, dtype=np.uint8)
        if self.batch_gt:
            gt = np.zeros(np.append(n_obj, gt_tmp.shape), dtype=np.float32)
            for (ii, k) in enumerate(obj_id):
                gt[(ii, :, :)] = (gt_tmp == k)
            gt = gt.transpose((1, 2, 0))
        else:
            gt = (gt_tmp == obj_id).astype(np.float32)
    if self.batch_gt:
        prev_round_mask = np.zeros(np.append(img.shape[:(- 1)], n_obj), dtype=np.float32)
        for (ii, k) in enumerate(obj_id):
            prev_round_mask[(:, :, ii)] = (prev_round_mask_tmp == k)
    else:
        prev_round_mask = (prev_round_mask_tmp == obj_id).astype(np.float32)
    return (img, gt, prev_round_mask)
