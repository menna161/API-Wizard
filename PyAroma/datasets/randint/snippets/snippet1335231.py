import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.stats import bayesian_blocks, RegularEvents
from astropy.utils.exceptions import AstropyUserWarning


def test_regular_events():
    rng = np.random.RandomState(0)
    dt = 0.01
    steps = np.concatenate([np.unique(rng.randint(0, 500, 100)), np.unique(rng.randint(500, 1000, 200))])
    t = (dt * steps)
    bins1 = bayesian_blocks(t, fitness='regular_events', dt=dt)
    assert (len(bins1) == 3)
    assert_allclose(bins1[1], 5, rtol=0.05)
    bins2 = bayesian_blocks(t, fitness=RegularEvents, dt=dt)
    assert_allclose(bins1, bins2)
    bins3 = bayesian_blocks(t, fitness=RegularEvents(dt=dt))
    assert_allclose(bins1, bins3)
