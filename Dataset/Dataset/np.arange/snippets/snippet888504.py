import copy
import dataclasses
import numpy as np
import pytest
import statsmodels
import whynot as wn
from whynot import parameter


def test_propensity_scorer_observation():
    'Test propensity scorer in the observational setting.'

    def crun_scorer(untreated_run):
        start = untreated_run.initial_state.val
        assert np.allclose(np.array([s.val for s in untreated_run.states]), start)
        return 0.5
    exp = build_experiment(state_sampler=correlated_state_sampler, propensity_scorer=crun_scorer)
    dataset = exp.run(num_samples=100, seed=1234)
    check_rct_assigment(dataset.treatments, 0.5)

    def trun_scorer(treated_run):
        start = treated_run.initial_state.val
        run_vals = np.array([s.val for s in treated_run.states])
        assert np.allclose((start + np.arange(10)), run_vals)
        return 0.5
    exp = build_experiment(state_sampler=correlated_state_sampler, propensity_scorer=trun_scorer)
    dataset = exp.run(num_samples=100, seed=1234)
    check_rct_assigment(dataset.treatments, 0.5)

    def cruns_scorer(untreated_runs):
        start_vals = sorted([run.initial_state.val for run in untreated_runs])
        assert np.allclose(np.arange(len(untreated_runs)), start_vals)
        for run in untreated_runs:
            assert np.allclose(np.array([s.val for s in run.states]), run.initial_state.val)
        n = len(untreated_runs)
        propensities = np.zeros((n,))
        propensities[:(n // 2)] = 1.0
        return propensities
    n = 100
    exp = build_experiment(state_sampler=correlated_state_sampler, propensity_scorer=cruns_scorer)
    dataset = exp.run(num_samples=n, seed=1234)
    assert np.allclose(dataset.treatments[:(n // 2)], 1)
    assert np.allclose(dataset.treatments[(n // 2):], 0)

    def truns_scorer(treated_runs):
        start_vals = sorted([run.initial_state.val for run in treated_runs])
        assert np.allclose(np.arange(len(treated_runs)), start_vals)
        for run in treated_runs:
            assert np.allclose(np.array([s.val for s in run.states]), (run.initial_state.val + np.arange(10)))
        n = len(treated_runs)
        propensities = np.zeros((n,))
        propensities[:(n // 2)] = 1.0
        return propensities
    exp = build_experiment(state_sampler=correlated_state_sampler, propensity_scorer=truns_scorer)
    dataset = exp.run(num_samples=n, seed=1234)
    assert np.allclose(dataset.treatments[:(n // 2)], 1)
    assert np.allclose(dataset.treatments[(n // 2):], 0)
