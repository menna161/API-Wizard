import copy
import functions.setting.setting_utils as su
from joblib import Parallel, delayed
import json
import logging
import multiprocessing
import numpy as np
import os
import time


def shuffled_indices_from_chunk_patch_seq(setting, dvf_list=None, torso_list=None, stage_sequence=None, semi_epoch=None, chunk=None, samples_per_image=None, log_header='', chunk_length_force_to_multiple_of=None):
    margin = setting['Margin']
    class_balanced = setting['ClassBalanced']
    indices = {}
    for c in range(len(class_balanced)):
        indices[('class' + str(c))] = []
    start_time = time.time()
    if setting['ParallelSearching']:
        num_cores = (multiprocessing.cpu_count() - 2)
        results = Parallel(n_jobs=num_cores)((delayed(search_indices_seq)(dvf_label=dvf_list[i], c=c, class_balanced=class_balanced, margin=margin, torso=torso_list[i]['stage1']) for i in range(len(dvf_list)) for c in range(0, len(class_balanced))))
        for iresults in range(0, len(results)):
            i_dvf = (iresults // len(class_balanced))
            c = (iresults % len(class_balanced))
            if len(results[iresults]):
                if (len(indices[('class' + str(c))]) == 0):
                    indices[('class' + str(c))] = np.array(np.c_[(results[iresults], (i_dvf * np.ones(len(results[iresults]), dtype=np.int32)))])
                else:
                    indices[('class' + str(c))] = np.concatenate((indices[('class' + str(c))], np.array(np.c_[(results[iresults], (i_dvf * np.ones(len(results[iresults]), dtype=np.int32)))])), axis=0)
        del results
        end_time = time.time()
        if setting['verbose']:
            logging.debug((log_header + ' Parallel searching for {} classes is Done in {:.2f}s'.format(len(class_balanced), (end_time - start_time))))
    samples_per_chunk = (samples_per_image * len(dvf_list))
    sample_per_chunk_per_class = np.round((samples_per_chunk / len(class_balanced)))
    number_samples_class = np.empty(len(class_balanced), dtype=np.int32)
    random_state = np.random.RandomState((((semi_epoch * 10000) + (chunk * 100)) + stage_sequence[0]))
    selected_indices = np.array([])
    for (c, k) in enumerate(indices.keys()):
        number_samples_class[c] = min((sample_per_chunk_per_class * setting['ClassBalancedWeight'][c]), np.shape(indices[k])[0])
        if (np.shape(indices[('class' + str(c))])[0] > 0):
            i1 = random_state.randint(0, high=np.shape(indices[('class' + str(c))])[0], size=number_samples_class[c])
            if ((c == 0) or (len(selected_indices) == 0)):
                selected_indices = np.concatenate((indices[('class' + str(c))][(i1, :)], (c * np.ones([len(i1), 1], dtype=np.int32))), axis=1).astype(np.int32)
            else:
                selected_indices = np.concatenate((selected_indices, np.concatenate((indices[('class' + str(c))][(i1, :)], (c * np.ones([len(i1), 1], dtype=np.int32))), axis=1)), axis=0)
        logging.info((log_header + ': {} of samples in class {} for SemiEpoch = {}, Chunk = {} '.format(number_samples_class[c], c, semi_epoch, chunk)))
    if setting['verbose']:
        logging.debug((log_header + ': samplesPerChunk is {} for SemiEpoch = {}, Chunk = {} '.format(sum(number_samples_class), semi_epoch, chunk)))
    shuffled_index = np.arange(0, len(selected_indices))
    random_state.shuffle(shuffled_index)
    if (chunk_length_force_to_multiple_of is not None):
        remainder = (len(shuffled_index) % chunk_length_force_to_multiple_of)
        if (remainder != 0):
            shuffled_index = shuffled_index[0:(len(shuffled_index) - remainder)]
    return selected_indices[shuffled_index]
