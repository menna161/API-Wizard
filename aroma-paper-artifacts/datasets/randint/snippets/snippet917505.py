import argparse
import numpy as np
import os
import random
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from joblib import dump
import multiprocessing as mp
from multiprocessing import Manager
import plasclass_utils as utils


def get_start_inds(seq_names, seq_lengths, num_frags, length):
    ' Randomly simulate fragments of a specific length from the sequences\n    '
    filtered_seq_names = [seq_names[i] for (i, v) in enumerate(seq_lengths) if (v > (0.85 * length))]
    filtered_seq_lengths = [l for l in seq_lengths if (l > (0.85 * length))]
    tot_seq_len = sum(filtered_seq_lengths)
    length_fractions = [(float(l) / float(tot_seq_len)) for l in filtered_seq_lengths]
    inds_dict = {}
    for name in filtered_seq_names:
        inds_dict[name] = []
    for i in range(num_frags):
        seq_ind = np.random.choice(len(filtered_seq_names), p=length_fractions)
        seq_len = filtered_seq_lengths[seq_ind]
        seq_name = filtered_seq_names[seq_ind]
        if (seq_len < length):
            inds_dict[seq_name].append(0)
        else:
            start_ind = random.randint(0, (seq_len - 1))
            inds_dict[seq_name].append(start_ind)
    return inds_dict
