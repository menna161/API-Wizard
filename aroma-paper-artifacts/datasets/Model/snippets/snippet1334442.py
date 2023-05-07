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


def test_ParametericModel():
    with pytest.raises(TypeError):
        models.Gaussian1D(1, 2, 3, wrong=4)
