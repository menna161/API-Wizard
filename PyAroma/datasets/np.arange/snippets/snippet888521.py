import copy
import dataclasses
import numpy as np
import pytest
import statsmodels
import whynot as wn
from whynot import parameter


def truns_scorer(treated_runs):
    start_vals = sorted([run.initial_state.val for run in treated_runs])
    assert np.allclose(np.arange(len(treated_runs)), start_vals)
    for run in treated_runs:
        assert np.allclose(np.array([s.val for s in run.states]), (run.initial_state.val + np.arange(10)))
    n = len(treated_runs)
    propensities = np.zeros((n,))
    propensities[:(n // 2)] = 1.0
    return propensities
