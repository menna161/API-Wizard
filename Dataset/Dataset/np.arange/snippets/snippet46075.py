import numpy as np
import random
import copy
import os


def get_srnn_gts(actions, data_set, data_mean, data_std, dim_to_ignore, source_seq_len, target_seq_len, input_size, to_euler=True):
    srnn_gts = {}
    for action in actions:
        srnn_gt = []
        (encoder_inputs, decoder_inputs, targets) = srnn_sample(data_set, action, source_seq_len, target_seq_len, input_size)
        for i in np.arange(targets.shape[0]):
            target = targets[(i, :, :)]
            if to_euler:
                for j in np.arange(target.shape[0]):
                    for k in np.arange(0, 115, 3):
                        target[(j, k:(k + 3))] = rotmat2euler(expmap2rotmat(target[(j, k:(k + 3))]))
            srnn_gt.append(target)
        srnn_gts[action] = srnn_gt
    return srnn_gts
