import os
from tqdm import tqdm
import argparse
from argparse import RawTextHelpFormatter
import glob
import numpy as np
from sklearn.neighbors import BallTree
import open3d
import torch
import shutil
from termcolor import colored
import time
from typing import Tuple
import sys
from clear_folder import clear_folder
from pretty_print import pretty_print_arguments


def get_sampling_positions(original_vertices: np.ndarray, stride: float) -> Tuple[(np.ndarray, np.ndarray)]:
    'returns center points of uniform sampling with certain stride length along the ground plane\n\n    Arguments:\n        original_vertices {np.ndarray} -- 3D coordinates of vertices\n        stride {float} -- distance between center points of sampling\n\n    Returns:\n        Tuple[np.ndarray, np.ndarray] -- returns sampling positions in x and y direction (always full height!)\n    '
    mins_xyz = original_vertices[(:, :3)].min(axis=0)
    maxs_xyz = original_vertices[(:, :3)].max(axis=0)
    sampling_positions_x = np.arange(mins_xyz[0], maxs_xyz[0], stride)
    offset_x = ((maxs_xyz[0] - sampling_positions_x[(- 1)]) / 2)
    sampling_positions_x = (sampling_positions_x + offset_x)
    sampling_positions_y = np.arange(mins_xyz[1], maxs_xyz[1], stride)
    offset_y = ((maxs_xyz[1] - sampling_positions_y[(- 1)]) / 2)
    sampling_positions_y = (sampling_positions_y + offset_y)
    return (sampling_positions_x, sampling_positions_y)
