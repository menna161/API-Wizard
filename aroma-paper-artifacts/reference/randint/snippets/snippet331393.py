import numpy as np
import pandas as pd
from mahal_dist import mahal_dist
from mahal_dist_variant import mahal_dist_variant


def generate_dataset(seed):
    rdg = np.random.RandomState(seed)
    row = rdg.randint(8000, 10000)
    col = rdg.randint(30, 35)
    contamination = rdg.uniform(0.015, 0.025)
    outlier_num = int((row * contamination))
    inlier_num = (row - outlier_num)
    inliers = rdg.randn(inlier_num, col)
    row_1 = ((outlier_num // 2) if np.mod(outlier_num, 2) else int((outlier_num / 2)))
    row_2 = (outlier_num - row_1)
    outliers_sub_1 = rdg.gamma(shape=2, scale=0.5, size=(row_1, col))
    outliers_sub_2 = rdg.exponential(1.5, size=(row_2, col))
    outliers = np.r_[(outliers_sub_1, outliers_sub_2)]
    dataset = np.r_[(inliers, outliers)]
    outliers_indices = range(len(dataset))[inlier_num:]
    return dataset
