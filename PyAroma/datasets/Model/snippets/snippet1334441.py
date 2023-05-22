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


def test_inputless_model():
    '\n    Regression test for\n    https://github.com/astropy/astropy/pull/3772#issuecomment-101821641\n    '

    class TestModel(Model):
        n_outputs = 1
        a = Parameter()

        @staticmethod
        def evaluate(a):
            return a
    m = TestModel(1)
    assert (m.a == 1)
    assert (m() == 1)
    m = TestModel([1, 2, 3], model_set_axis=False)
    assert (len(m) == 1)
    assert np.all((m() == [1, 2, 3]))
    m = TestModel(a=[1, 2, 3], model_set_axis=0)
    assert (len(m) == 3)
    assert np.all((m() == [1, 2, 3]))
    m = TestModel(a=[[1, 2, 3], [4, 5, 6]], model_set_axis=0)
    assert (len(m) == 2)
    assert np.all((m() == [[1, 2, 3], [4, 5, 6]]))
