import numpy as np
import random
import copy
import os


def load_data(data_path, actions):
    nactions = len(actions)
    (sampled_data_set, complete_data) = ({}, [])
    for action_idx in np.arange(nactions):
        action = actions[action_idx]
        path = '{}/{}'.format(data_path, action)
        count = 0
        for fn in os.listdir(path):
            count = (count + 1)
        for examp_index in np.arange(count):
            filename = '{}/{}/{}_{}.txt'.format(data_path, action, action, (examp_index + 1))
            action_sequence = read_txt_as_data(filename)
            (t, d) = action_sequence.shape
            even_indices = range(0, t, 2)
            sampled_data_set[(action, (examp_index + 1), 'even')] = action_sequence[(even_indices, :)]
            if (len(complete_data) == 0):
                complete_data = copy.deepcopy(action_sequence)
            else:
                complete_data = np.append(complete_data, action_sequence, axis=0)
    return (sampled_data_set, complete_data)
