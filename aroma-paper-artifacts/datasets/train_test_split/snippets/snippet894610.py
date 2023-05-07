import os
import numpy as np
import sys
from loss_functions import *
import nibabel as nib
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import *
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import *
from keras.callbacks import *
from glob import glob
from keras.callbacks import *


def read_all_slices(in_paths, path_image, rescale=True):
    cur_vol = np.concatenate([np.transpose(nib.load(c_path).get_data())[(:, ::DS_FACT, ::DS_FACT)] for c_path in in_paths], 0)
    cur_vol_mask = np.concatenate([np.transpose(nib.load(c_path).get_data())[(:, ::DS_FACT, ::DS_FACT)] for c_path in path_image], 0)
    s_id = check_arr_nan(cur_vol, cur_vol_mask)
    num_bleed = range(0, len(cur_vol))
    num_bleed = np.setdiff1d(num_bleed, s_id)
    num_no_bleed = 544
    indices = np.random.choice(num_bleed.shape[0], num_no_bleed, replace=True)
    s_id = np.concatenate([s_id, num_bleed[indices]])
    cur_vol_mask = mask_preprocess(cur_vol_mask)
    (cur_vol, cur_vol_mask) = (cur_vol[s_id], cur_vol_mask[s_id])
    if rescale:
        cur_vol = ((cur_vol.astype(np.float32) - np.mean(cur_vol.astype(np.float32))) / np.std(cur_vol.astype(np.float32)))
        return (cur_vol, cur_vol_mask)
    else:
        return (cur_vol, cur_vol_mask)
