import copy
import functions.setting.setting_utils as su
from joblib import Parallel, delayed
import json
import logging
import multiprocessing
import numpy as np
import os
import time


def shuffled_indices_from_chunk(setting, dvf_list=None, torso_list=None, im_info_list=None, stage=None, stage_sequence=None, semi_epoch=None, chunk=None, samples_per_image=None, log_header='', full_image=None, seq_mode=False, chunk_length_force_to_multiple_of=None):
    if full_image:
        ishuffled = np.arange(len(dvf_list))
    elif seq_mode:
        ishuffled = shuffled_indices_from_chunk_patch_seq(setting, dvf_list=dvf_list, torso_list=torso_list, stage_sequence=stage_sequence, semi_epoch=semi_epoch, chunk=chunk, samples_per_image=samples_per_image, log_header=log_header, chunk_length_force_to_multiple_of=chunk_length_force_to_multiple_of)
    else:
        ishuffled = shuffled_indices_from_chunk_patch(setting, dvf_list=dvf_list, torso_list=torso_list, im_info_list=im_info_list, stage=stage, semi_epoch=semi_epoch, chunk=chunk, samples_per_image=samples_per_image, log_header=log_header)
    return ishuffled
