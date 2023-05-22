import copy
import dataclasses
import numpy as np
import pytest
import statsmodels
import whynot as wn
from whynot import parameter


def cruns_scorer(untreated_runs):
    start_vals = sorted([run.initial_state.val for run in untreated_runs])
    assert np.allclose(np.arange(len(untreated_runs)), start_vals)
    for run in untreated_runs:
        assert np.allclose(np.array([s.val for s in run.states]), run.initial_state.val)
    n = len(untreated_runs)
    propensities = np.zeros((n,))
    propensities[:(n // 2)] = 1.0
    return propensities
