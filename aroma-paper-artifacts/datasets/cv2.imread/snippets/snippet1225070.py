import numpy as np
import torch
from datasets.BaseDataset import BaseDataset
import os
import cv2
import io
from config import config
from io import BytesIO
from config import config


def _fetch_data(self, img_path, hha_path, label_weight_path, mapping_path, gt_path, dtype=None):
    from config import config
    img = np.array(cv2.imread(img_path), dtype=np.float32)
    hha = np.array(cv2.imread(hha_path), dtype=np.float32)
    tsdf = np.load(label_weight_path)['arr_0'].astype(np.float32).reshape(1, 60, 36, 60)
    label_weight = np.load(label_weight_path)['arr_1'].astype(np.float32)
    depth_mapping_3d = np.load(mapping_path)['arr_0'].astype(np.int64)
    gt = np.load(gt_path)['arr_0'].astype(np.int64)
    sketch_gt = np.load(gt_path.replace('Label', 'sketch3D').replace('npz', 'npy')).astype(np.int64)
    return (img, hha, tsdf, label_weight, depth_mapping_3d, gt, sketch_gt)
