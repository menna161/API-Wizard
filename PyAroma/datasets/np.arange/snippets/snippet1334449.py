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


def test_render_model_1d():
    npix = 101
    image = np.zeros(npix)
    coords = np.arange(npix)
    model = models.Gaussian1D()
    test_pts = [0, 49.1, 49.5, 49.9, 100]
    test_stdv = np.arange(5.5, 6.7, 0.2)
    for (x0, stdv) in [(p, s) for p in test_pts for s in test_stdv]:
        model.mean = x0
        model.stddev = stdv
        expected = model(coords)
        for x in [coords, None]:
            for im in [image.copy(), None]:
                if ((im is None) & (x is None)):
                    continue
                actual = model.render(out=im, coords=x)
                assert_allclose(expected, actual, atol=3e-07)
                if ((x0, stdv) == (49.5, 5.5)):
                    boxed = model.render()
                    flux = np.sum(expected)
                    assert (((flux - np.sum(boxed)) / flux) < 1e-07)
