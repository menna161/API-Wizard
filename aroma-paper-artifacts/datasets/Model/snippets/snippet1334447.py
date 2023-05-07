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


def test_custom_inverse_reset():
    "Test resetting a custom inverse to the model's default inverse."

    class TestModel(Model):
        n_inputs = 0
        outputs = ('y',)

        @property
        def inverse(self):
            return models.Shift()

        @staticmethod
        def evaluate():
            return 0
    m = TestModel()
    assert isinstance(m.inverse, models.Shift)
    m.inverse = models.Scale()
    assert isinstance(m.inverse, models.Scale)
    del m.inverse
    assert isinstance(m.inverse, models.Shift)
