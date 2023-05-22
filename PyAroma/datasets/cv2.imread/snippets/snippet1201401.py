import argparse
from multiprocessing.pool import Pool
import numpy as np
from cv2 import cv2
import os


def ensemble_image(params):
    (file, dirs, ensembling_dir, strategy) = params
    images = []
    for dir in dirs:
        file_path = os.path.join(dir, file)
        images.append(cv2.imread(file_path, cv2.IMREAD_COLOR))
    images = np.array(images)
    if (strategy == 'average'):
        ensembled = average_strategy(images)
    elif (strategy == 'hard_voting'):
        ensembled = hard_voting(images)
    else:
        raise ValueError('Unknown ensembling strategy')
    cv2.imwrite(os.path.join(ensembling_dir, file), ensembled)
