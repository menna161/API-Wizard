import copy
import functions.setting.setting_utils as su
from joblib import Parallel, delayed
import json
import logging
import multiprocessing
import numpy as np
import os
import time


def shuffled_indices_from_chunk_patch(setting, dvf_list=None, torso_list=None, im_info_list=None, stage=None, semi_epoch=None, chunk=None, samples_per_image=None, log_header=''):
    for single_dict in setting['DataExpDict']:
        iclass_folder = su.address_generator(setting, 'IClassFolder', data=single_dict['data'], deform_exp=single_dict['deform_exp'], stage=stage)
        if (not os.path.isdir(iclass_folder)):
            os.makedirs(iclass_folder)
    margin = setting['Margin']
    class_balanced = setting['ClassBalanced']
    indices = {}
    for c in range(len(class_balanced)):
        indices[('class' + str(c))] = []
    start_time = time.time()
    if setting['ParallelSearching']:
        num_cores = (multiprocessing.cpu_count() - 2)
        results = (([None] * len(dvf_list)) * len(class_balanced))
        count_iclass_loaded = 0
        for (i_dvf, im_info) in enumerate(im_info_list):
            for c in range(len(class_balanced)):
                iclass_address = su.address_generator(setting, 'IClass', data=im_info['data'], deform_exp=im_info['deform_exp'], cn=im_info['cn'], type_im=im_info['type_im'], dsmooth=im_info['dsmooth'], c=c, stage=stage)
                if os.path.isfile(iclass_address):
                    results[((i_dvf * len(class_balanced)) + c)] = np.load(iclass_address)
                    count_iclass_loaded += 1
        if (count_iclass_loaded != len(results)):
            logging.debug((log_header + ': not all I1 found. start calculating... SemiEpoch = {}, Chunk = {}, stage={}'.format(semi_epoch, chunk, stage)))
            results = Parallel(n_jobs=num_cores)((delayed(search_indices)(dvf=dvf_list[i], torso=torso_list[i], c=c, class_balanced=class_balanced, margin=margin, dim_im=setting['Dim']) for i in range(0, len(dvf_list)) for c in range(0, len(class_balanced))))
            for (i_dvf, im_info) in enumerate(im_info_list):
                for c in range(0, len(class_balanced)):
                    iclass_address = su.address_generator(setting, 'IClass', data=im_info['data'], deform_exp=im_info['deform_exp'], cn=im_info['cn'], type_im=im_info['type_im'], dsmooth=im_info['dsmooth'], c=c, stage=stage)
                    np.save(iclass_address, results[((i_dvf * len(class_balanced)) + c)])
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
    else:
        for (i_dvf, im_info) in enumerate(im_info_list):
            mask = np.zeros(np.shape(dvf_list[i_dvf])[:(- 1)], dtype=np.bool)
            mask[(margin:(- margin), margin:(- margin), margin:(- margin))] = True
            if (torso_list[i_dvf] is not None):
                mask = (mask & torso_list[i_dvf])
            for c in range(len(class_balanced)):
                iclass_address = su.address_generator(setting, 'IClass', data=im_info['data'], deform_exp=im_info['deform_exp'], cn=im_info['cn'], type_im=im_info['type_im'], dsmooth=im_info['dsmooth'], c=c, stage=stage)
                if os.path.isfile(iclass_address):
                    i1 = np.load(iclass_address)
                else:
                    if (c == 0):
                        i1 = np.ravel_multi_index(np.where((np.all((np.abs(dvf_list[i_dvf]) < class_balanced[c]), axis=3) & mask)), np.shape(dvf_list[i_dvf])[:(- 1)]).astype(np.int32)
                    if ((c > 0) & (c < len(class_balanced))):
                        if (setting['Dim'] == 2):
                            i1 = np.ravel_multi_index(np.where(((np.all((np.abs(dvf_list[i_dvf]) < class_balanced[c]), axis=3) & np.any((np.abs(dvf_list[i_dvf]) >= class_balanced[(c - 1)]), axis=3)) & mask)), np.shape(dvf_list[i_dvf])[:(- 1)]).astype(np.int32)
                        if (setting['Dim'] == 3):
                            i1 = np.ravel_multi_index(np.where(((np.all((np.abs(dvf_list[i_dvf]) < class_balanced[c]), axis=3) & np.all((np.abs(dvf_list[i_dvf]) >= class_balanced[(c - 1)]), axis=3)) & mask)), np.shape(dvf_list[i_dvf])[:(- 1)]).astype(np.int32)
                    np.save(iclass_address, i1)
                if (len(i1) > 0):
                    if (len(indices[('class' + str(c))]) == 0):
                        indices[('class' + str(c))] = np.array(np.c_[(i1, (i_dvf * np.ones(len(i1), dtype=np.int32)))])
                    else:
                        indices[('class' + str(c))] = np.concatenate((indices[('class' + str(c))], np.array(np.c_[(i1, (i_dvf * np.ones(len(i1), dtype=np.int32)))])), axis=0)
                if setting['verbose']:
                    logging.debug((log_header + ': Finding classes done for i = {}, c = {} '.format(i_dvf, c)))
        del i1
        end_time = time.time()
        if setting['verbose']:
            logging.debug((log_header + ': Searching for {} classes is Done in {:.2f}s'.format((len(class_balanced) + 1), (end_time - start_time))))
    samples_per_chunk = (samples_per_image * len(dvf_list))
    sample_per_chunk_per_class = np.round((samples_per_chunk / len(class_balanced)))
    number_samples_class = np.empty(len(class_balanced), dtype=np.int32)
    random_state = np.random.RandomState((((semi_epoch * 10000) + (chunk * 100)) + stage))
    selected_indices = np.array([])
    for (c, k) in enumerate(indices.keys()):
        number_samples_class[c] = min(sample_per_chunk_per_class, np.shape(indices[k])[0])
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
    return selected_indices[shuffled_index]
