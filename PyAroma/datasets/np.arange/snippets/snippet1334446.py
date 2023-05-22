import os
import sys
import subprocess
import pytest
import numpy as np
from inspect import signature
from numpy.testing import assert_allclose
import astropy
from astropy.modeling.core import Model, custom_model
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
import astropy.units as u
from astropy.tests.helper import assert_quantity_allclose
import scipy


def test_custom_inverse():
    'Test setting a custom inverse on a model.'
    p = models.Polynomial1D(1, c0=(- 2), c1=3)
    inv = models.Polynomial1D(1, c0=(2.0 / 3.0), c1=(1.0 / 3.0))
    with pytest.raises(NotImplementedError):
        p.inverse
    p.inverse = inv
    x = np.arange(100)
    assert_allclose(x, p(p.inverse(x)))
    assert_allclose(x, p.inverse(p(x)))
    p.inverse = None
    with pytest.raises(NotImplementedError):
        p.inverse
