import numpy as np
import random
import copy


def load_data(data_path, subjects, actions):
    nactions = len(actions)
    (sampled_data_set, complete_data) = ({}, [])
    for subj in subjects:
        for action_idx in np.arange(len(actions)):
            action = actions[action_idx]
            for subact in [1, 2]:
                print('Reading subject {0}, action {1}, subaction {2}'.format(subj, action, subact))
                filename = '{0}/S{1}/{2}_{3}.txt'.format(data_path, subj, action, subact)
                action_sequence = read_txt_as_data(filename)
                (t, d) = action_sequence.shape
                even_indices = range(0, t, 2)
                sampled_data_set[(subj, action, subact, 'even')] = action_sequence[(even_indices, :)]
                if (len(complete_data) == 0):
                    complete_data = copy.deepcopy(action_sequence)
                else:
                    complete_data = np.append(complete_data, action_sequence, axis=0)
    return (sampled_data_set, complete_data)
