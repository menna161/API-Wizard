import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.stats import bayesian_blocks, RegularEvents
from astropy.utils.exceptions import AstropyUserWarning


def test_fitness_function_results():
    'Test results for several fitness functions'
    rng = np.random.RandomState(42)
    t = rng.randn(100)
    edges = bayesian_blocks(t, fitness='events')
    assert_allclose(edges, [(- 2.6197451), (- 0.71094865), 0.36866702, 1.85227818])
    t[80:] = t[:20]
    edges = bayesian_blocks(t, fitness='events', p0=0.01)
    assert_allclose(edges, [(- 2.6197451), (- 0.47432431), (- 0.46202823), 1.85227818])
    dt = 0.01
    t = (dt * np.arange(1000))
    x = np.zeros(len(t))
    N = (len(t) // 10)
    x[rng.randint(0, len(t), N)] = 1
    x[rng.randint(0, (len(t) // 2), N)] = 1
    edges = bayesian_blocks(t, x, fitness='regular_events', dt=dt)
    assert_allclose(edges, [0, 5.105, 9.99])
    t = (100 * rng.rand(20))
    x = np.exp(((- 0.5) * ((t - 50) ** 2)))
    sigma = 0.1
    x_obs = (x + (sigma * rng.randn(len(x))))
    edges = bayesian_blocks(t, x_obs, sigma, fitness='measures')
    expected = [4.360377, 48.456895, 52.597917, 99.455051]
    assert_allclose(edges, expected)
    p0_sel = 0.05
    edges = bayesian_blocks(t, x_obs, sigma, fitness='measures', p0=p0_sel)
    assert_allclose(edges, expected)
    ncp_prior_sel = (4 - np.log(((73.53 * p0_sel) * (len(t) ** (- 0.478)))))
    edges = bayesian_blocks(t, x_obs, sigma, fitness='measures', ncp_prior=ncp_prior_sel)
    assert_allclose(edges, expected)
    gamma_sel = np.exp((- ncp_prior_sel))
    edges = bayesian_blocks(t, x_obs, sigma, fitness='measures', gamma=gamma_sel)
    assert_allclose(edges, expected)
