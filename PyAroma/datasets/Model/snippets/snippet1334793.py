import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.modeling.core import Model
from astropy.modeling.models import Gaussian1D, Shift, Scale, Pix2Sky_TAN
from astropy import units as u
from astropy.units import UnitsError
from astropy.tests.helper import assert_quantity_allclose


def test_compound_return_units():
    '\n    Test that return_units on the first model in the chain is respected for the\n    input to the second.\n    '

    class PassModel(Model):
        n_inputs = 2
        n_outputs = 2

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @property
        def input_units(self):
            ' Input units. '
            return {'x0': u.deg, 'x1': u.deg}

        @property
        def return_units(self):
            ' Output units. '
            return {'x0': u.deg, 'x1': u.deg}

        def evaluate(self, x, y):
            return (x.value, y.value)
    cs = (Pix2Sky_TAN() | PassModel())
    assert_quantity_allclose(cs((0 * u.deg), (0 * u.deg)), ((0, 90) * u.deg))
