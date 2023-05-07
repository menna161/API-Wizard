import numpy as np
from skimage import exposure
from skimage.color import rgb2gray
import pandas as pd
from tadataka.feature import Matcher
from tadataka.flow_estimation.image_curvature import extract_curvature_extrema, compute_image_curvature
from tadataka.flow_estimation.flow_estimation import estimate_affine_transform
from tadataka.flow_estimation.extrema_tracker import ExtremaTracker
from tadataka.triangulation import TwoViewTriangulation
from tadataka.utils import is_in_image_range
from functools import reduce


def create_keypoint_frame(start_id, keypoints):
    N = keypoints.shape[0]
    ids = np.arange(start_id, (start_id + N))
    return create_keypoint_frame_(ids, keypoints)
