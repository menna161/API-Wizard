import pytest
import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling.models import Polynomial1D, Polynomial2D
from astropy.modeling.fitting import LinearLSQFitter
from astropy.modeling.core import Model
from astropy.modeling.parameters import Parameter


def test_shapes():
    p2 = Polynomial1D(1, n_models=3, model_set_axis=2)
    assert (p2.c0.shape == (1, 1, 3))
    assert (p2.c1.shape == (1, 1, 3))
    p1 = Polynomial1D(1, n_models=2, model_set_axis=1)
    assert (p1.c0.shape == (1, 2))
    assert (p1.c1.shape == (1, 2))
    p1 = Polynomial1D(1, c0=[1, 2], c1=[3, 4], n_models=2, model_set_axis=(- 1))
    assert (p1.c0.shape == (2,))
    assert (p1.c1.shape == (2,))
    e1 = [1, 2]
    e2 = [3, 4]
    a1 = np.array([[10, 20], [30, 40]])
    a2 = np.array([[50, 60], [70, 80]])
    t = TParModel([a1, a2], [e1, e2], n_models=2, model_set_axis=(- 1))
    assert (t.coeff.shape == (2, 2, 2))
    assert (t.e.shape == (2, 2))
    t = TParModel([[a1, a2]], [[e1, e2]], n_models=2, model_set_axis=1)
    assert (t.coeff.shape == (1, 2, 2, 2))
    assert (t.e.shape == (1, 2, 2))
    t = TParModel([a1, a2], [e1, e2], n_models=2, model_set_axis=0)
    assert (t.coeff.shape == (2, 2, 2))
    assert (t.e.shape == (2, 2))
    t = TParModel([a1, a2], e=[1, 2], n_models=2, model_set_axis=0)
    assert (t.coeff.shape == (2, 2, 2))
    assert (t.e.shape == (2,))
