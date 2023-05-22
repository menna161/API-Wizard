import csv
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from tqdm import tqdm
from scipy.spatial.transform import Rotation
from skimage.io import imread
import numpy as np
from tadataka.camera import CameraModel, CameraParameters, FOV
from tadataka.dataset.frame import Frame
from tadataka.dataset.base import BaseDataset
from tadataka.pose import Pose


def __init__(self, dataset_root, condition='daylight'):
    self.camera_model = CameraModel(CameraParameters(focal_length=[615, 615], offset=[320, 240]), distortion_model=None)
    groundtruth_dir = Path(dataset_root, 'groundtruth')
    illumination_dir = Path(dataset_root, 'illumination')
    pose_path = Path(groundtruth_dir, 'camera_track.txt')
    self.baseline_length = 10.0
    (self.rotations, self.positions) = load_poses(pose_path)
    depth_dir = Path(groundtruth_dir, 'depth_maps')
    depth_cache_dir = Path(groundtruth_dir, 'depth_cache')
    if (not depth_cache_dir.exists()):
        generate_depth_cache(depth_dir, depth_cache_dir)
    self.depth_L_paths = sorted(Path(depth_cache_dir, 'left').glob('*.npy'))
    self.depth_R_paths = sorted(Path(depth_cache_dir, 'right').glob('*.npy'))
    image_dir = Path(illumination_dir, condition)
    image_cache_dir = Path(illumination_dir, (condition + '_cache'))
    if (not image_cache_dir.exists()):
        generate_image_cache(image_dir, image_cache_dir)
    self.image_L_paths = sorted(Path(image_cache_dir, 'left').glob('*.npy'))
    self.image_R_paths = sorted(Path(image_cache_dir, 'right').glob('*.npy'))
    assert (len(self.depth_L_paths) == len(self.depth_R_paths) == len(self.image_L_paths) == len(self.image_R_paths) == len(self.rotations) == len(self.positions))
    for i in range(len(self.positions)):
        DL = self.depth_L_paths[i].name
        DR = self.depth_R_paths[i].name
        IL = self.image_L_paths[i].name
        IR = self.image_R_paths[i].name
        assert (DL[(- 8):] == DR[(- 8):] == IL[(- 8):] == IR[(- 8):])
