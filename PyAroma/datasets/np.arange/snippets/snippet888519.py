import copy
import dataclasses
import numpy as np
import pytest
import statsmodels
import whynot as wn
from whynot import parameter


def trun_scorer(treated_run):
    start = treated_run.initial_state.val
    run_vals = np.array([s.val for s in treated_run.states])
    assert np.allclose((start + np.arange(10)), run_vals)
    return 0.5
