from __future__ import division
import itertools
import time
import warnings
from math import log, sqrt
from os.path import join
import numpy as np
from joblib import dump
from nibabel.filebasedimages import ImageFileError
from nilearn._utils import CacheMixin
from nilearn._utils import check_niimg
from nilearn.input_data import NiftiMasker
from sklearn.base import TransformerMixin
from sklearn.externals.joblib import Memory
from sklearn.externals.joblib import Parallel
from sklearn.externals.joblib import delayed
from sklearn.utils import check_random_state
from ..input_data.fmri.base import BaseNilearnEstimator
from .dict_fact import DictFact, Coder


def _compute_components(masker, imgs, step_size=1, confounds=None, dict_init=None, alpha=1, positive=False, reduction=1, learning_rate=1, n_components=20, batch_size=20, n_epochs=1, method='masked', verbose=0, random_state=None, callback=None, n_jobs=1):
    methods = {'masked': {'G_agg': 'masked', 'Dx_agg': 'masked'}, 'dictionary only': {'G_agg': 'full', 'Dx_agg': 'full'}, 'gram': {'G_agg': 'masked', 'Dx_agg': 'masked'}, 'average': {'G_agg': 'average', 'Dx_agg': 'average'}, 'reducing ratio': {'G_agg': 'masked', 'Dx_agg': 'masked'}}
    masker._check_fitted()
    dict_init = _check_dict_init(dict_init, mask_img=masker.mask_img_, n_components=n_components)
    if (dict_init is not None):
        n_components = dict_init.shape[0]
    random_state = check_random_state(random_state)
    if (method == 'sgd'):
        optimizer = 'sgd'
        G_agg = 'full'
        Dx_agg = 'full'
        reduction = 1
    else:
        method = methods[method]
        G_agg = method['G_agg']
        Dx_agg = method['Dx_agg']
        optimizer = 'variational'
    if verbose:
        print('Scanning data')
    n_records = len(imgs)
    if (confounds is None):
        confounds = itertools.repeat(None)
    data_list = list(zip(imgs, confounds))
    (n_samples_list, dtype) = _lazy_scan(imgs)
    indices_list = np.zeros((len(imgs) + 1), dtype='int')
    indices_list[1:] = np.cumsum(n_samples_list)
    n_samples = (indices_list[(- 1)] + 1)
    n_voxels = np.sum((check_niimg(masker.mask_img_).get_data() != 0))
    if verbose:
        print('Learning...')
    dict_fact = DictFact(n_components=n_components, code_alpha=alpha, code_l1_ratio=0, comp_l1_ratio=1, comp_pos=positive, reduction=reduction, Dx_agg=Dx_agg, optimizer=optimizer, step_size=step_size, G_agg=G_agg, learning_rate=learning_rate, batch_size=batch_size, random_state=random_state, n_threads=n_jobs, verbose=0)
    dict_fact.prepare(n_samples=n_samples, n_features=n_voxels, X=dict_init, dtype=dtype)
    cpu_time = 0
    io_time = 0
    if (n_records > 0):
        if verbose:
            verbose_iter_ = np.linspace(0, (n_records * n_epochs), verbose)
            verbose_iter_ = verbose_iter_.tolist()
        current_n_records = 0
        for i in range(n_epochs):
            if verbose:
                print(('Epoch %i' % (i + 1)))
            if ((method == 'gram') and (i == 5)):
                dict_fact.set_params(G_agg='full', Dx_agg='average')
            if (method == 'reducing ratio'):
                reduction = (1 + ((reduction - 1) / sqrt((i + 1))))
                dict_fact.set_params(reduction=reduction)
            record_list = random_state.permutation(n_records)
            for record in record_list:
                if (verbose and verbose_iter_ and (current_n_records >= verbose_iter_[0])):
                    print(('Record %i' % current_n_records))
                    if (callback is not None):
                        callback(masker, dict_fact, cpu_time, io_time)
                    verbose_iter_ = verbose_iter_[1:]
                t0 = time.perf_counter()
                (img, these_confounds) = data_list[record]
                masked_data = masker.transform(img, confounds=these_confounds)
                masked_data = masked_data.astype(dtype)
                io_time += (time.perf_counter() - t0)
                t0 = time.perf_counter()
                permutation = random_state.permutation(masked_data.shape[0])
                if (method in ['average', 'gram']):
                    sample_indices = np.arange(indices_list[record], indices_list[(record + 1)])
                    sample_indices = sample_indices[permutation]
                else:
                    sample_indices = None
                masked_data = masked_data[permutation]
                dict_fact.partial_fit(masked_data, sample_indices=sample_indices)
                current_n_records += 1
                cpu_time += (time.perf_counter() - t0)
    components = _flip(dict_fact.components_)
    return components
