import os
from os import path, mkdir
import numpy as np
import random
import timeit
import cv2
from tqdm import tqdm
from skimage import measure
from multiprocessing import Pool
import lightgbm as lgb
from sklearn.model_selection import KFold, GroupShuffleSplit
from sklearn.neighbors import KDTree
from skimage.morphology import watershed
import warnings
import os


def check_id(id: str):
    labels = cv2.imread(path.join(masks_folder, (('mask_' + '_'.join(id[:(- 4)].split('_')[(- 2):])) + '.tif')), cv2.IMREAD_UNCHANGED)
    if (np.max(labels) > 255):
        print('FUCK', str(np.max(labels)))
    mask = cv2.imread(os.path.join(train_pred_folder, id), cv2.IMREAD_COLOR)[(..., 0)]
    return (id if ((np.max(labels) > 1) and (np.sum(mask) > (200 * 255))) else None)
