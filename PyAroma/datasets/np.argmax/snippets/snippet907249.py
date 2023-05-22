import pandas as pd
from mlopt.problem import Problem
import mlopt.settings as stg
from mlopt.learners import LEARNER_MAP, installed_learners
from mlopt.sampling import Sampler
from mlopt.strategy import encode_strategies
from mlopt.filter import Filter
import mlopt.error as e
from mlopt.utils import n_features, accuracy, suboptimality
import mlopt.utils as u
from mlopt.kkt import create_kkt_matrix, factorize_kkt_matrix
from mlopt.utils import pandas2array
from cvxpy import Minimize, Maximize
import numpy as np
import os
from glob import glob
import tempfile
import tarfile
import pickle as pkl
from joblib import Parallel, delayed
from tqdm.auto import tqdm
from time import time


def choose_best(self, problem_data, labels, parallel=False, batch_size=stg.JOBLIB_BATCH_SIZE, use_cache=True):
    '\n        Choose best strategy between provided ones\n\n        Parameters\n        ----------\n        labels : list\n            Strategy labels to compare.\n        parallel : bool, optional\n            Perform `n_best` strategies evaluation in parallel.\n            True by default.\n        use_cache : bool, optional\n            Use solver cache if available. True by default.\n\n        Returns\n        -------\n        dict\n            Results as a dictionary.\n        '
    n_best = self._learner.options['n_best']
    x = []
    time = []
    infeas = []
    cost = []
    strategies = [self.encoding[label] for label in labels]
    cache = ([None] * n_best)
    if (self._solver_cache and use_cache):
        cache = [self._solver_cache[label] for label in labels]
    n_jobs = (u.get_n_processes() if parallel else 1)
    results = Parallel(n_jobs=n_jobs, batch_size=batch_size)((delayed(self._problem.solve)(problem_data, strategy=strategies[j], cache=cache[j]) for j in range(n_best)))
    x = [r['x'] for r in results]
    time = [r['time'] for r in results]
    infeas = [r['infeasibility'] for r in results]
    cost = [r['cost'] for r in results]
    infeas = np.array(infeas)
    cost = np.array(cost)
    idx_filter = np.where((infeas <= stg.INFEAS_TOL))[0]
    if (len(idx_filter) > 0):
        if (self._problem.sense() == Minimize):
            idx_pick = idx_filter[np.argmin(cost[idx_filter])]
        elif (self._problem.sense() == Maximize):
            idx_pick = idx_filter[np.argmax(cost[idx_filter])]
        else:
            e.value_error('Objective type not understood')
    else:
        idx_pick = np.argmin(infeas)
    result = {}
    result['x'] = x[idx_pick]
    result['time'] = np.sum(time)
    result['strategy'] = strategies[idx_pick]
    result['cost'] = cost[idx_pick]
    result['infeasibility'] = infeas[idx_pick]
    return result
