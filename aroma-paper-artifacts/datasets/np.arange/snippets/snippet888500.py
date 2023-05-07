import copy
import dataclasses
import numpy as np
import pytest
import statsmodels
import whynot as wn
from whynot import parameter


def test_state_sampler():
    'Test the state sampler function.'

    def initial_state_covariates(run):
        'Outcome is the initial state of the run.'
        return run.initial_state.val

    def random_initial_state(rng):
        'Initial state is 0 for all rollouts.'
        if (rng.uniform() < 0.5):
            return ToyState(val=0)
        return ToyState(val=1)
    exp = build_experiment(state_sampler=random_initial_state, covariate_builder=initial_state_covariates)
    dataset0 = exp.run(num_samples=100, seed=1234)
    dataset1 = exp.run(num_samples=100, seed=1234)
    assert np.allclose(dataset0.covariates, dataset1.covariates)
    exp = build_experiment(state_sampler=correlated_state_sampler, covariate_builder=initial_state_covariates)
    dataset = exp.run(num_samples=100, seed=1234)
    assert np.allclose(np.expand_dims(np.arange(100), axis=1), dataset.covariates)

    @parameter(name='init_val', default=2)
    def parameterized_sampler(init_val):
        return ToyState(val=init_val)
    exp = build_experiment(state_sampler=parameterized_sampler, covariate_builder=initial_state_covariates)
    dataset = exp.run(num_samples=10)
    assert np.allclose(dataset.covariates, 2)
    dataset = exp.run(num_samples=10, init_val=3.14)
    assert np.allclose(dataset.covariates, 3.14)
    dataset = exp.run(num_samples=10, init_val=1234)
    assert np.allclose(dataset.covariates, 1234)
    with pytest.raises(ValueError):
        exp.run(num_samples=10, random_val=123)
