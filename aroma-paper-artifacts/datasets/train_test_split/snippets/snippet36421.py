import os
from math import log
from os.path import join, expanduser
from joblib import Parallel
from modl.decomposition.fmri import fMRIDictFact, rfMRIDictionaryScorer
from modl.input_data.fmri.rest import get_raw_rest_data
from sklearn.externals.joblib import delayed
from sklearn.model_selection import train_test_split
import numpy as np


def compute_components(n_components, batch_size, learning_rate, positive, reduction, alpha, method, n_epochs, verbose, smoothing_fwhm, n_jobs, raw_dir, output_dir):
    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    info = {}
    (masker, data) = get_raw_rest_data(raw_dir)
    (train_imgs, test_imgs) = train_test_split(data, train_size=None, test_size=1, random_state=0)
    train_imgs = train_imgs['filename'].values
    test_imgs = test_imgs['filename'].values
    cb = rfMRIDictionaryScorer(test_imgs, info=info, artifact_dir=output_dir)
    dict_fact = fMRIDictFact(method=method, mask=masker, smoothing_fwhm=smoothing_fwhm, verbose=verbose, n_epochs=n_epochs, n_jobs=n_jobs, random_state=1, n_components=n_components, positive=positive, learning_rate=learning_rate, batch_size=batch_size, reduction=reduction, alpha=alpha, callback=cb)
    dict_fact.fit(train_imgs)
    dict_fact.components_img_.to_filename(join(output_dir, 'components.nii.gz'))
