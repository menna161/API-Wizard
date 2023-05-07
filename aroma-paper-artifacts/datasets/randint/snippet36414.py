import os
import sys
from os import path
from os.path import join
import numpy as np
from sacred import Experiment
from sacred.observers import FileStorageObserver
from sklearn.externals.joblib import Parallel
from sklearn.externals.joblib import delayed
from sklearn.utils import check_random_state
from modl.utils.system import get_output_dir
from exps.exp_decompose_fmri import exp as single_exp


@exp.automain
def run(n_seeds, n_jobs, _run, _seed):
    seed_list = check_random_state(_seed).randint(np.iinfo(np.uint32).max, size=n_seeds)
    exps = []
    exps += [{'method': 'sgd', 'step_size': step_size} for step_size in np.logspace((- 7), (- 7), 1)]
    exps += [{'method': 'gram', 'reduction': reduction} for reduction in [12]]
    rundir = join(basedir, str(_run._id), 'run')
    if (not os.path.exists(rundir)):
        os.makedirs(rundir)
    Parallel(n_jobs=n_jobs, verbose=10)((delayed(single_run)(config_updates, rundir, i) for (i, config_updates) in enumerate(exps)))
