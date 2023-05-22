import copy
import functions.setting.setting_utils as su
from joblib import Parallel, delayed
import json
import logging
import multiprocessing
import numpy as np
import os
import time


def select_im_from_semiepoch(setting, im_info_list_full=None, semi_epoch=None, chunk=None, number_of_images_per_chunk=None):
    im_info_list_full = copy.deepcopy(im_info_list_full)
    random_state = np.random.RandomState(semi_epoch)
    if setting['Randomness']:
        random_indices = random_state.permutation(len(im_info_list_full))
    else:
        random_indices = np.arange(len(im_info_list_full))
    lower_range = (chunk * number_of_images_per_chunk)
    upper_range = ((chunk + 1) * number_of_images_per_chunk)
    if (upper_range >= len(im_info_list_full)):
        upper_range = len(im_info_list_full)
    indices_chunk = random_indices[lower_range:upper_range]
    im_info_list = [im_info_list_full[i] for i in indices_chunk]
    return im_info_list
