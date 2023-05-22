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


@pytest.mark.skipif('not HAS_SCIPY')
def test_units_with_bounding_box():
    points = np.arange(10, 20)
    table = (np.arange(10) * u.Angstrom)
    t = models.Tabular1D(points, lookup_table=table)
    assert isinstance(t(10), u.Quantity)
    assert isinstance(t(10, with_bounding_box=True), u.Quantity)
    assert_quantity_allclose(t(10), t(10, with_bounding_box=True))
